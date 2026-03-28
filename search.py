"""
Book Ramsey number search via simulated annealing on 2-block circulant graphs.

Searches for witnesses proving R(B_{n-1}, B_n) = 4n - 1 by finding a graph
on 2m = 2(2n-1) vertices with no B_{n-1} and whose complement has no B_n.

The graph is a 2-block circulant over Z_m ⊔ Z_m defined by difference sets
D11 (within V1), D12 (across V1-V2), and D22 = {1,...,m-1} \ D11 (within V2).

Usage:
    python search.py --n 30              # search single case
    python search.py --range 22 50       # search all new cases in range
    python search.py --n 30 --steps 500000 --seeds 100  # custom params
"""

import numba as nb
import numpy as np
import math
import time
import json
import argparse
import os
from concurrent.futures import ProcessPoolExecutor, as_completed


# ============================================================
# Core numba-jitted functions
# ============================================================

@nb.njit
def compute_A_nb(arr):
    m = arr.shape[0]
    out = np.zeros(m, dtype=np.int16)
    for d in range(m):
        s = 0
        for t in range(m):
            s += arr[t] * arr[(t + d) % m]
        out[d] = s
    return out


@nb.njit
def score_smooth(n, x, Ax, Ay):
    """Continuous score for SA phase 1. Adds smooth gradient near boundary."""
    k1 = 0
    m = x.shape[0]
    for i in range(m):
        k1 += x[i]
    T1 = n - 2
    T0 = 2 * k1 - n + 1
    score = 0.0
    for d in range(1, m):
        f = int(Ax[d]) + int(Ay[d])
        target = T1 if x[d] == 1 else T0
        ex = f - target
        if ex > 0:
            score += float(ex * ex)
        if ex >= 0:
            score += 0.01 * (float(ex) + 1.0)
    return score


@nb.njit
def score_integer(n, x, Ax, Ay):
    """Original integer score for SA phase 2 (final push to 0)."""
    k1 = 0
    m = x.shape[0]
    for i in range(m):
        k1 += x[i]
    T1 = n - 2
    T0 = 2 * k1 - n + 1
    score = 0
    for d in range(1, m):
        f = int(Ax[d]) + int(Ay[d])
        ex = f - T1 if x[d] == 1 else f - T0
        if ex > 0:
            score += ex * ex
    return score


@nb.njit
def x_flip_inplace_nb(a, x, Ax):
    m = x.shape[0]
    s = 1 - 2 * int(x[a])
    for d in range(m):
        val = 2 * s * (int(x[(d - a) % m]) + int(x[(d + a) % m]))
        if d == 0:
            val += 2
        if d == (2 * a) % m:
            val += 1
        if d == (m - 2 * a) % m:
            val += 1
        Ax[d] += val
    x[a] ^= 1
    x[m - a] ^= 1


@nb.njit
def y_flip_inplace_nb(b, y, Ay):
    m = y.shape[0]
    s = 1 - 2 * int(y[b])
    for d in range(m):
        val = s * (int(y[(b + d) % m]) + int(y[(b - d) % m]))
        if d == 0:
            val += 1
        Ay[d] += val
    y[b] ^= 1


@nb.njit
def init_state_nb(n, k1_pairs):
    m = 2 * n - 1
    h = (m - 1) // 2
    x = np.zeros(m, dtype=np.int8)
    count = 0
    while count < k1_pairs:
        a = np.random.randint(1, h + 1)
        if x[a] == 0:
            x[a] = 1
            x[m - a] = 1
            count += 1
    y = np.zeros(m, dtype=np.int8)
    count = 0
    while count < n - 1:
        b = np.random.randint(0, m)
        if y[b] == 0:
            y[b] = 1
            count += 1
    Ax = compute_A_nb(x)
    Ay = compute_A_nb(y)
    return x, y, Ax, Ay, score_smooth(n, x, Ax, Ay)


@nb.njit
def random_x_swap_candidate(n, x, Ax, Ay):
    m = x.shape[0]
    h = (m - 1) // 2
    while True:
        a = np.random.randint(1, h + 1)
        if x[a] == 1:
            break
    while True:
        b = np.random.randint(1, h + 1)
        if x[b] == 0:
            break
    x2 = x.copy()
    Ax2 = Ax.copy()
    x_flip_inplace_nb(a, x2, Ax2)
    x_flip_inplace_nb(b, x2, Ax2)
    return a, b, x2, Ax2, score_smooth(n, x2, Ax2, Ay)


@nb.njit
def random_y_swap_candidate(n, y, x, Ax, Ay):
    m = y.shape[0]
    while True:
        c = np.random.randint(0, m)
        if y[c] == 1:
            break
    while True:
        d = np.random.randint(0, m)
        if y[d] == 0:
            break
    y2 = y.copy()
    Ay2 = Ay.copy()
    y_flip_inplace_nb(c, y2, Ay2)
    y_flip_inplace_nb(d, y2, Ay2)
    return c, d, y2, Ay2, score_smooth(n, x, Ax, Ay2)


@nb.njit
def sa_nb_seeded(n, k1_pairs, steps, temp0, seed):
    np.random.seed(seed)
    x, y, Ax, Ay, _ = init_state_nb(n, k1_pairs)
    phase2_start = int(steps * 0.7)
    # Start with smooth score
    score = score_smooth(n, x, Ax, Ay)
    best_score = score
    best_x = x.copy()
    best_y = y.copy()
    for step in range(1, steps + 1):
        # Switch scoring at phase boundary
        if step == phase2_start:
            score = float(score_integer(n, x, Ax, Ay))
            best_score = score
            best_x = x.copy()
            best_y = y.copy()
        use_smooth = step < phase2_start
        # Check for valid witness
        if score_integer(n, x, Ax, Ay) == 0:
            return 0.0, x, y
        T = max(temp0 * (1.0 - step / steps), 1e-3)
        if np.random.random() < 0.5:
            a, b, x2, Ax2, _ = random_x_swap_candidate(n, x, Ax, Ay)
            if use_smooth:
                ns = score_smooth(n, x2, Ax2, Ay)
            else:
                ns = float(score_integer(n, x2, Ax2, Ay))
            if ns - score <= 0 or np.random.random() < math.exp(-(ns - score) / T):
                x = x2
                Ax = Ax2
                score = ns
        else:
            c, d, y2, Ay2, _ = random_y_swap_candidate(n, y, x, Ax, Ay)
            if use_smooth:
                ns = score_smooth(n, x, Ax, Ay2)
            else:
                ns = float(score_integer(n, x, Ax, Ay2))
            if ns - score <= 0 or np.random.random() < math.exp(-(ns - score) / T):
                y = y2
                Ay = Ay2
                score = ns
        if score < best_score:
            best_score = score
            best_x = x.copy()
            best_y = y.copy()
    return best_score, best_x, best_y


# ============================================================
# Search driver
# ============================================================

def _run_one_seed(args):
    """Worker function for parallel search. Must be top-level for pickling."""
    n, k1p, steps, temp, seed = args
    r = sa_nb_seeded(n, k1p, steps, temp, seed)
    s = r[0]
    if s == 0.0:
        m = 2 * n - 1
        x, y = r[1], r[2]
        D11 = sorted([i for i in range(m) if x[i] == 1])
        D12 = sorted([i for i in range(m) if y[i] == 1])
        return (0, k1p, temp, seed, D11, D12)
    return (round(float(s), 1), k1p, temp, seed, None, None)


def search_n(n, steps=300000, seeds=80, max_time=600, verbose=True, workers=None):
    """Search for a witness for R(B_{n-1}, B_n) = 4n-1 using parallel workers."""
    if workers is None:
        workers = min(os.cpu_count() or 4, 8)
    m = 2 * n - 1
    h = (m - 1) // 2
    # Prioritize likely k1p values first, then fallback
    k1_range = [h // 2, h // 2 + 1, h // 2 - 1]
    # Prioritize lower temps (2.0, 5.0 have historically won)
    temps = [2.0, 5.0, 10.0, 20.0]
    t0 = time.time()

    # Submit ALL jobs at once across all (k1p, temp) combos
    all_jobs = []
    for k1p in k1_range:
        for temp in temps:
            for seed in range(seeds):
                all_jobs.append((n, k1p, steps, temp, seed))

    if verbose:
        print(f"  Launching {len(all_jobs)} jobs across {workers} workers...", flush=True)

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(_run_one_seed, job): job for job in all_jobs}
        best = 9999
        best_info = ""

        for future in as_completed(futures):
            if time.time() - t0 > max_time:
                for f in futures:
                    f.cancel()
                if verbose:
                    print(f"  TIMEOUT n={n} best={best} ({time.time()-t0:.0f}s)")
                return None, time.time() - t0

            s, rk1p, rtemp, rseed, D11, D12 = future.result()
            if s < best:
                best = s
                best_info = f"k1p={rk1p} temp={rtemp} seed={rseed}"
                if verbose and s > 0:
                    print(f"  n={n} new best={best} ({best_info}) ({time.time()-t0:.0f}s)", flush=True)
            if s == 0:
                for f in futures:
                    f.cancel()
                elapsed = time.time() - t0
                if verbose:
                    print(f"  FOUND n={n} k1p={rk1p} temp={rtemp} seed={rseed} ({elapsed:.1f}s)")
                return {"D11": D11, "D12": D12}, elapsed

    if verbose:
        print(f"  NOT FOUND n={n} best={best} ({best_info}) ({time.time()-t0:.0f}s)")
    return None, time.time() - t0


# ============================================================
# Helpers
# ============================================================

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def is_pp_1mod4(m):
    """Check if m is a prime power congruent to 1 mod 4."""
    if m % 4 != 1:
        return False
    for p in range(2, m + 1):
        if m % p == 0:
            k = m
            while k % p == 0:
                k //= p
            return k == 1 and is_prime(p)
    return False


def factorize(n):
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


def is_new_case(n):
    """Check if n is NOT already covered by Wesley's results (n<=21 or infinite family)."""
    if n <= 21:
        return False
    m = 2 * n - 1
    return not is_pp_1mod4(m)


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Book Ramsey witness search")
    parser.add_argument("--n", type=int, help="Search single n")
    parser.add_argument("--range", nargs=2, type=int, metavar=("LO", "HI"), help="Search range of n")
    parser.add_argument("--steps", type=int, default=300000, help="SA steps per run (default 300000)")
    parser.add_argument("--seeds", type=int, default=80, help="Seeds per (k1p, temp) combo (default 80)")
    parser.add_argument("--max-time", type=int, default=600, help="Max seconds per n (default 600)")
    parser.add_argument("--output", type=str, default="results.json", help="Output file (default results.json)")
    parser.add_argument("--workers", type=int, default=None, help="Parallel workers (default: cpu_count)")
    parser.add_argument("--all-cases", action="store_true", help="Include already-known cases too")
    args = parser.parse_args()

    # Numba warmup
    print("Compiling numba functions...", flush=True)
    sa_nb_seeded(22, 11, 100, 5.0, 0)
    print("Done.\n", flush=True)

    # Load existing results if any
    results_file = args.output
    if os.path.exists(results_file):
        with open(results_file) as f:
            all_results = json.load(f)
    else:
        all_results = {}

    # Determine which n values to search
    if args.n:
        targets = [args.n]
    elif args.range:
        lo, hi = args.range
        targets = list(range(lo, hi + 1))
    else:
        print("Specify --n or --range")
        exit(1)

    if not args.all_cases:
        targets = [n for n in targets if is_new_case(n)]

    print(f"Targets: {targets}\n")

    for n in targets:
        m = 2 * n - 1
        f = "x".join(str(x) for x in factorize(m))
        key = str(n)

        if key in all_results and all_results[key].get("found"):
            print(f"n={n} (m={m}={f}): already found, skipping")
            continue

        print(f"n={n} (m={m}={f}):", flush=True)
        result, elapsed = search_n(n, steps=args.steps, seeds=args.seeds, max_time=args.max_time, workers=args.workers)

        if result is not None:
            all_results[key] = {
                "found": True,
                "time": round(elapsed, 1),
                "m": m,
                "D11": result["D11"],
                "D12": result["D12"],
                "D22": sorted(list(set(range(1, m)) - set(result["D11"]))),
            }
            print(f"  -> Saved. D11 has {len(result['D11'])} elements, D12 has {len(result['D12'])} elements.\n")
        else:
            all_results[key] = {"found": False, "time": round(elapsed, 1), "m": m}
            print()

        # Save after each n in case of interruption
        with open(results_file, "w") as f:
            json.dump(all_results, f, indent=2)

    print(f"\nResults saved to {results_file}")
