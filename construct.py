"""
Algebraic construction for book Ramsey witnesses.

For primes q = 4n-1 with q ≡ 3 mod 8, constructs a 2-block circulant graph
on 2m vertices (m = 2n-1) that witnesses R(B_{n-1}, B_n) = 4n-1.

Construction:
    Let ρ be a primitive root mod q, Q = quadratic residues mod q.
    D11 = {a ∈ {1,...,m-1} : ρ^(2a) + 1 ∈ Q}
    D12 = {a ∈ {0,...,m-1} : ρ^(2a) - 1 ∈ Q}
    D22 = {1,...,m-1} \ D11

Usage:
    python construct.py --n 35           # construct and verify single n
    python construct.py --list 100       # list all eligible n up to 100
    python construct.py --all 100        # construct all eligible n up to 100
"""

import json
import argparse
import time


def is_prime(n):
    """Check if n is prime."""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def primitive_root(q):
    """Find the smallest primitive root mod q (q must be prime)."""
    if q == 2:
        return 1
    # Factor q-1
    phi = q - 1
    factors = set()
    n = phi
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.add(d)
            n //= d
        d += 1
    if n > 1:
        factors.add(n)

    for g in range(2, q):
        ok = True
        for p in factors:
            if pow(g, phi // p, q) == 1:
                ok = False
                break
        if ok:
            return g
    return None


def quadratic_residues(q):
    """Return the set of quadratic residues mod q (excluding 0)."""
    QR = set()
    for x in range(1, q):
        QR.add(pow(x, 2, q))
    return QR


def is_eligible(n):
    """Check if n is eligible for the algebraic construction.
    Requires q = 4n-1 to be prime and q ≡ 3 mod 8.
    """
    q = 4 * n - 1
    return is_prime(q) and q % 8 == 3


def construct(n):
    """
    Construct the difference sets D11, D12, D22 for the witness graph.

    Returns (D11, D12, D22) or None if n is not eligible.
    """
    q = 4 * n - 1
    if not is_prime(q) or q % 8 != 3:
        return None

    m = 2 * n - 1  # = (q-1)/2
    rho = primitive_root(q)
    Q = quadratic_residues(q)

    # Precompute powers of rho mod q
    # rho^(2a) for a in range(m)
    pow_table = [1] * m
    rho2 = pow(rho, 2, q)
    for a in range(1, m):
        pow_table[a] = (pow_table[a - 1] * rho2) % q

    # D11 = {a in {1,...,m-1} : rho^(2a) + 1 in Q}
    D11 = []
    for a in range(1, m):
        val = (pow_table[a] + 1) % q
        if val in Q:
            D11.append(a)

    # D12 = {a in {0,...,m-1} : rho^(2a) - 1 in Q}
    D12 = []
    for a in range(0, m):
        val = (pow_table[a] - 1) % q
        if val != 0 and val in Q:
            D12.append(a)

    # D22 = {1,...,m-1} \ D11
    D11_set = set(D11)
    D22 = sorted([a for a in range(1, m) if a not in D11_set])

    return D11, D12, D22


def verify_witness(n, D11, D12):
    """
    Build the full 2m-vertex graph and exhaustively verify:
    - max common neighbors over edges <= n-2  (no B_{n-1})
    - max common non-neighbors over non-edges <= n-1  (complement has no B_n)
    """
    m = 2 * n - 1
    D11s = set(D11)
    D12s = set(D12)
    D22s = set(range(1, m)) - D11s

    # Check D11 symmetry
    for d in D11s:
        assert (m - d) % m in D11s, f"D11 not symmetric: {d} in D11 but {(m-d)%m} not"

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


def build_adjacency_string(n, D11, D12):
    """Build the adjacency string (upper triangle) for the 2m-vertex graph."""
    m = 2 * n - 1
    D11s = set(D11)
    D12s = set(D12)
    D22s = set(range(1, m)) - D11s
    N = 2 * m

    # Build adjacency as a function
    def is_edge(u, v):
        if u >= v:
            u, v = v, u
        if u < m and v < m:
            # Both in V1: edge iff (v - u) % m in D11
            return ((v - u) % m) in D11s
        elif u < m and v >= m:
            # u in V1, v in V2: edge iff (v-m - u) % m in D12
            return ((v - m - u) % m) in D12s
        else:
            # Both in V2: edge iff (v - u) % m in D22
            return ((v - u) % m) in D22s

    bits = []
    for i in range(N):
        for j in range(i + 1, N):
            bits.append('1' if is_edge(i, j) else '0')
    return ''.join(bits)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Algebraic book Ramsey construction")
    parser.add_argument("--n", type=int, help="Construct witness for specific n")
    parser.add_argument("--list", type=int, metavar="MAX_N",
                        help="List all eligible n up to MAX_N")
    parser.add_argument("--all", type=int, metavar="MAX_N",
                        help="Construct and verify all eligible n up to MAX_N")
    parser.add_argument("--verify", action="store_true",
                        help="Verify the constructed witness (slow for large n)")
    parser.add_argument("--adjacency", action="store_true",
                        help="Output the adjacency string")
    parser.add_argument("--output", type=str, help="Save results to JSON file")
    args = parser.parse_args()

    if args.list:
        print(f"Eligible n <= {args.list} for algebraic construction (q=4n-1 prime, q=3 mod 8):")
        for n in range(2, args.list + 1):
            if is_eligible(n):
                q = 4 * n - 1
                m = 2 * n - 1
                print(f"  n={n}: q={q}, m={m}")
        exit(0)

    targets = []
    if args.n:
        targets = [args.n]
    elif args.all:
        targets = [n for n in range(2, args.all + 1) if is_eligible(n)]
    else:
        parser.print_help()
        exit(1)

    results = {}
    for n in targets:
        q = 4 * n - 1
        m = 2 * n - 1

        if not is_eligible(n):
            print(f"n={n}: NOT ELIGIBLE (q={q}, prime={is_prime(q)}, q mod 8 = {q % 8})")
            continue

        print(f"n={n}: q={q}, m={m}, primitive root = {primitive_root(q)}")
        result = construct(n)
        if result is None:
            print(f"  Construction failed.")
            continue

        D11, D12, D22 = result
        print(f"  |D11| = {len(D11)}, |D12| = {len(D12)}, |D22| = {len(D22)}")
        print(f"  D11 = {D11}")
        print(f"  D12 = {D12}")
        print(f"  D22 = {D22}")

        results[str(n)] = {
            "n": n,
            "q": q,
            "m": m,
            "D11": D11,
            "D12": D12,
            "D22": D22,
            "primitive_root": primitive_root(q),
        }

        if args.verify:
            print(f"  Verifying {2*m}-vertex graph ... ", end="", flush=True)
            t0 = time.time()
            ok, max_e, max_ne = verify_witness(n, D11, D12)
            elapsed = time.time() - t0
            status = "PASS" if ok else "FAIL"
            print(f"{status} ({elapsed:.1f}s)")
            print(f"  Max edge codeg: {max_e} (limit {n-2})")
            print(f"  Max nonedge codeg: {max_ne} (limit {n-1})")
            results[str(n)]["verified"] = ok

        if args.adjacency:
            adj = build_adjacency_string(n, D11, D12)
            print(f"  Adjacency string length: {len(adj)}")
            results[str(n)]["adjacency_string"] = adj

        print()

    if args.output and results:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {args.output}")
