"""
Independent verification of book Ramsey witnesses.

Builds the full 2m-vertex graph and exhaustively checks all co-degrees.
This is slow (O(N^2 * degree)) but completely trustworthy.

Usage:
    python verify.py results.json          # verify all results in file
    python verify.py results.json --n 28   # verify single n
"""

import json
import argparse
import time


def verify_witness(n, D11, D12):
    """
    Build the full 2m-vertex graph and exhaustively verify:
    - max common neighbors over edges <= n-2  (no B_{n-1})
    - max common non-neighbors over non-edges <= n-1  (complement has no B_n)

    Returns (ok, max_edge_codeg, max_nonedge_codeg, edge_hist, nonedge_hist)
    """
    m = 2 * n - 1
    D11s = set(D11)
    D12s = set(D12)
    D22s = set(range(1, m)) - D11s

    # Structural checks
    assert D22s == set(range(1, m)) - D11s, "D22 complement check failed"
    assert all((m - d) % m in D11s for d in D11s), "D11 not symmetric"

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

    # Check no self-loops and symmetry
    for v in range(N):
        assert v not in neighbors[v], f"Self-loop at {v}"
    for u in range(N):
        for v in neighbors[u]:
            assert u in neighbors[v], f"Asymmetric edge {u}-{v}"

    all_verts = set(range(N))
    max_e = 0
    max_ne = 0
    max_e_pair = None
    max_ne_pair = None
    edge_hist = {}
    nonedge_hist = {}

    for u in range(N):
        for v in range(u + 1, N):
            if v in neighbors[u]:
                cn = len(neighbors[u] & neighbors[v])
                edge_hist[cn] = edge_hist.get(cn, 0) + 1
                if cn > max_e:
                    max_e = cn
                    max_e_pair = (u, v)
            else:
                non_u = all_verts - neighbors[u] - {u}
                non_v = all_verts - neighbors[v] - {v}
                cn_bar = len(non_u & non_v)
                nonedge_hist[cn_bar] = nonedge_hist.get(cn_bar, 0) + 1
                if cn_bar > max_ne:
                    max_ne = cn_bar
                    max_ne_pair = (u, v)

    ok = max_e <= n - 2 and max_ne <= n - 1
    num_edges = sum(len(nb) for nb in neighbors) // 2

    return {
        "ok": ok,
        "N": N,
        "num_edges": num_edges,
        "max_edge_codeg": max_e,
        "max_edge_pair": max_e_pair,
        "max_nonedge_codeg": max_ne,
        "max_nonedge_pair": max_ne_pair,
        "edge_target": n - 2,
        "nonedge_target": n - 1,
        "edge_hist": {str(k): v for k, v in sorted(edge_hist.items())},
        "nonedge_hist": {str(k): v for k, v in sorted(nonedge_hist.items())},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify book Ramsey witnesses")
    parser.add_argument("file", help="JSON results file")
    parser.add_argument("--n", type=int, help="Verify single n")
    args = parser.parse_args()

    with open(args.file) as f:
        results = json.load(f)

    targets = [args.n] if args.n else sorted(int(k) for k in results.keys())

    for n in targets:
        key = str(n)
        if key not in results:
            print(f"n={n}: not in results file")
            continue
        r = results[key]
        if not r.get("found"):
            print(f"n={n}: no witness found")
            continue

        m = 2 * n - 1
        D11 = r["D11"]
        D12 = r["D12"]

        print(f"n={n}, m={m}: verifying {2*m}-vertex graph ... ", end="", flush=True)
        t0 = time.time()
        v = verify_witness(n, D11, D12)
        elapsed = time.time() - t0

        status = "PASS" if v["ok"] else "FAIL"
        print(f"{status} ({elapsed:.1f}s)")
        print(f"  |D11|={len(D11)}, |D12|={len(D12)}, |D22|={m-1-len(D11)}")
        print(f"  Max edge codeg: {v['max_edge_codeg']} (limit {v['edge_target']})")
        print(f"  Max nonedge codeg: {v['max_nonedge_codeg']} (limit {v['nonedge_target']})")
        if v["ok"]:
            print(f"  R(B_{n-1}, B_{n}) = {4*n - 1} CONFIRMED")
        print(f"  Edge dist: {v['edge_hist']}")
        print(f"  Nonedge dist: {v['nonedge_hist']}")
        print()
