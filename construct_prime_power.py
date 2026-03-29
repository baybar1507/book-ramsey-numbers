"""
Algebraic construction for R(B_{n-1}, B_n) = 4n-1 when q = 4n-1 is a prime power with q = 3 mod 8.

Extends the prime case (construct.py) to prime powers using GF(q) arithmetic.
Requires the 'galois' package: pip install galois

Usage:
    python construct_prime_power.py --q 1331       # q = 11^3
    python construct_prime_power.py --n 333        # n = 333 -> q = 1331
    python construct_prime_power.py --verify-all   # verify all new prime power cases up to n=500
"""

import argparse
import json
import time
import sys
import os
import numpy as np

try:
    import galois
except ImportError:
    print("Error: 'galois' package required. Install with: pip install galois")
    sys.exit(1)


def is_prime_power_3mod8(q):
    """Check if q is a prime power congruent to 3 mod 8."""
    if q < 2 or q % 8 != 3:
        return False, 0, 0
    for p in range(2, int(q**0.5) + 1):
        if q % p == 0:
            k = 0
            tmp = q
            while tmp % p == 0:
                tmp //= p
                k += 1
            if tmp == 1:
                return True, p, k
            return False, 0, 0
    # q is prime
    return True, q, 1


def construct_witness_prime_power(q):
    """Construct D11, D12, D22 for prime power q = 3 mod 8."""
    ok, p, k = is_prime_power_3mod8(q)
    if not ok:
        raise ValueError(f"q={q} is not a prime power congruent to 3 mod 8")

    n = (q + 1) // 4
    m = 2 * n - 1

    GF = galois.GF(q)
    g = GF.primitive_element
    g2 = g * g  # g2 has order m = (q-1)/2

    # Build g2 powers
    g2_powers = [GF(1)]
    for i in range(1, m):
        g2_powers.append(g2_powers[-1] * g2)

    # Quadratic character
    half = (q - 1) // 2

    def is_qr(x):
        if x == GF(0):
            return False
        return x ** half == GF(1)

    # D11 = {a in {1,...,m-1} : chi(g2^a + 1) = 1}
    D11 = [a for a in range(1, m) if is_qr(g2_powers[a] + GF(1))]
    # D12 = {a in {0,...,m-1} : chi(g2^a - 1) = 1}
    D12 = [a for a in range(m) if is_qr(g2_powers[a] - GF(1))]
    D22 = sorted(set(range(1, m)) - set(D11))

    return n, m, D11, D12, D22


def verify_witness(n, D11, D12):
    """Verify the witness by exhaustive codegree checking."""
    m = 2 * n - 1
    D11s = set(D11)
    D12s = set(D12)
    D22s = set(range(1, m)) - D11s

    N = 2 * m
    neighbors = [set() for _ in range(N)]

    for i in range(m):
        for d in D11s:
            j = (i + d) % m
            neighbors[i].add(j)
            neighbors[j].add(i)
        for d in D12s:
            j_b = (i + d) % m + m
            neighbors[i].add(j_b)
            neighbors[j_b].add(i)
        for d in D22s:
            j_b = (i + d) % m + m
            neighbors[i + m].add(j_b)
            neighbors[j_b].add(i + m)

    all_verts = set(range(N))
    max_e = 0
    max_ne = 0

    for u in range(N):
        for v in range(u + 1, N):
            if v in neighbors[u]:
                cn = len(neighbors[u] & neighbors[v])
                if cn > max_e:
                    max_e = cn
            else:
                non_u = all_verts - neighbors[u] - {u}
                non_v = all_verts - neighbors[v] - {v}
                cn_bar = len(non_u & non_v)
                if cn_bar > max_ne:
                    max_ne = cn_bar

    ok = max_e <= n - 2 and max_ne <= n - 1
    return ok, max_e, max_ne


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prime power book Ramsey construction")
    parser.add_argument("--q", type=int, help="Prime power q (must be 3 mod 8)")
    parser.add_argument("--n", type=int, help="Ramsey parameter n (q = 4n-1)")
    parser.add_argument("--verify-all", action="store_true", help="Verify all new prime power cases")
    parser.add_argument("--no-verify", action="store_true", help="Skip verification")
    args = parser.parse_args()

    if args.verify_all:
        from sympy import isprime
        print("Searching for new prime power cases (not prime, not Wesley)...")
        for p in range(3, 200):
            if not isprime(p):
                continue
            if p % 8 != 3:
                continue
            for k in [3, 5, 7]:
                q = p ** k
                n = (q + 1) // 4
                m = 2 * n - 1

                # Check if Wesley covers it
                from sympy import factorint
                f = factorint(m)
                is_pp = len(f) == 1
                wesley = is_pp and m % 4 == 1

                if wesley:
                    print(f"  q={q} (p={p} k={k}) n={n}: Wesley covers, skipping")
                    continue

                print(f"  q={q} (p={p} k={k}) n={n}: constructing...", end="", flush=True)
                t0 = time.time()
                n_r, m_r, D11, D12, D22 = construct_witness_prime_power(q)
                print(f" |D11|={len(D11)}", end="", flush=True)

                if not args.no_verify:
                    ok, max_e, max_ne = verify_witness(n_r, D11, D12)
                    elapsed = time.time() - t0
                    print(f" edge={max_e}/{n_r-2} ne={max_ne}/{n_r-1} {'PASS' if ok else 'FAIL'} ({elapsed:.1f}s)")
                else:
                    print(f" (not verified)")
                if q > 100000:
                    break
        sys.exit(0)

    if args.n:
        q = 4 * args.n - 1
    elif args.q:
        q = args.q
    else:
        print("Specify --q or --n")
        sys.exit(1)

    ok_pp, p, k = is_prime_power_3mod8(q)
    if not ok_pp:
        print(f"q={q} is not a prime power congruent to 3 mod 8")
        sys.exit(1)

    print(f"q = {q} = {p}^{k}")
    t0 = time.time()
    n, m, D11, D12, D22 = construct_witness_prime_power(q)
    print(f"n = {n}, m = {m}")
    print(f"|D11| = {len(D11)}, |D12| = {len(D12)}, |D22| = {len(D22)}")

    if not args.no_verify:
        print("Verifying...", flush=True)
        ok, max_e, max_ne = verify_witness(n, D11, D12)
        elapsed = time.time() - t0
        print(f"Max edge codeg: {max_e} (limit {n-2})")
        print(f"Max nonedge codeg: {max_ne} (limit {n-1})")
        print(f"{'PASS' if ok else 'FAIL'} ({elapsed:.1f}s)")
        if ok:
            print(f"\nR(B_{n-1}, B_{n}) = {4*n-1} CONFIRMED")
    else:
        print(f"D11 = {D11}")
        print(f"D12 = {D12}")
