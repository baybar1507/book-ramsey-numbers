# New Results on Book Ramsey Numbers R(B_{n-1}, B_n)

## Summary

We prove that R(B_{n-1}, B_n) = 4n - 1 for all n up to 35, and for the additional values n = 53, 71, 77, 83, 95. This extends the results of Wesley (2024), who established R(B_{n-1}, B_n) = 4n - 1 for n <= 21 and for an infinite family of n where 2n - 1 is a prime power congruent to 1 mod 4.

## Background

The book graph B_n consists of n triangles sharing a common edge. The Ramsey number R(B_{n-1}, B_n) is the smallest N such that every red/blue coloring of the edges of K_N contains either a red B_{n-1} or a blue B_n.

It was conjectured that R(B_{n-1}, B_n) = 4n - 1 for all n >= 2. Wesley (2024) confirmed this for:
- All n <= 21 (computational)
- An infinite family where 2n - 1 is a prime power congruent to 1 mod 4

The witness graphs are 2-block circulant graphs on 2m vertices (m = 2n - 1), defined by three difference sets D11, D12, D22. A valid witness has:
- No B_{n-1} subgraph (max co-degree over edges <= n - 2)
- No B_n in the complement (max co-degree over non-edges <= n - 1)

## New Results

### Method 1: Simulated Annealing Search (n = 22-34)

For n = 22, 23, 24, 26, 28, 29, 30, 32, 33, 34, 35, we found witness graphs via a simulated annealing search over 2-block circulant graphs. (Values n = 25, 27, 31 are already covered by Wesley's infinite family since 2n-1 is a prime power congruent to 1 mod 4 in each case.)

The search algorithm:
- Operates on the difference sets (D11, D12) that define the circulant structure
- Uses a two-phase SA: smooth scoring for exploration, then integer scoring for refinement
- Parallelizes across multiple (k1_pairs, temperature, seed) combinations
- Verified independently by exhaustive co-degree checking

### Method 2: Algebraic Construction (n = 35, 53, 71, 77, 83, 95)

We give a new algebraic construction that applies when q = 4n - 1 is prime and q is congruent to 3 mod 8. Let:

- rho = a primitive root mod q
- Q = {quadratic residues mod q}
- m = 2n - 1 = (q - 1)/2

Then define:
- D11 = {a in {1, ..., m-1} : rho^(2a) + 1 is in Q}
- D12 = {a in {0, ..., m-1} : rho^(2a) - 1 is in Q}
- D22 = {1, ..., m-1} \ D11

This construction yields a valid witness graph for R(B_{n-1}, B_n) = 4n - 1.

**New infinite family.** The construction gives a valid witness whenever q = 4n - 1 is prime with q congruent to 3 mod 8. By Dirichlet's theorem on primes in arithmetic progressions, there are infinitely many such primes, yielding an infinite family of n for which R(B_{n-1}, B_n) = 4n - 1.

**Proof.** A complete proof that this construction satisfies all six codegree conditions is given in `proof.md`. The proof shows that the Legendre pair property (Delta(D11,D11,d) + Delta(D12,D12,d) = n-2 for all nonzero d) follows from character sum evaluations over the finite field F_q, using the key fact that chi(2) = -1 when q = 3 mod 8. The cross-block codegrees are handled by a purely combinatorial argument using the symmetry of D11.

This family is distinct from Wesley's infinite family (which requires 2n - 1 to be a prime power congruent to 1 mod 4). The two families overlap for some small values but are generally independent.

The new values contributed by this construction (not already found via SA or covered by Wesley) are n = 53, 71, 77, 83, 95.

### Complete List of New Results

| n | m = 2n-1 | q = 4n-1 | Method | Notes |
|---|----------|----------|--------|-------|
| 22 | 43 | 87 | SA | m = 43 prime |
| 23 | 45 | 91 | SA | m = 45 = 9 x 5 |
| 24 | 47 | 95 | SA | m = 47 prime |
| 26 | 51 | 103 | SA | m = 51 = 3 x 17 |
| 28 | 55 | 111 | SA | m = 55 = 5 x 11 |
| 29 | 57 | 115 | SA | m = 57 = 3 x 19 |
| 30 | 59 | 119 | SA | m = 59 prime |
| 32 | 63 | 127 | SA | m = 63 = 9 x 7 |
| 33 | 65 | 131 | SA | m = 65 = 5 x 13 |
| 34 | 67 | 135 | SA | m = 67 prime |
| 35 | 69 | 139 | SA + Algebraic | q = 139 prime, 139 = 3 mod 8 |
| 53 | 105 | 211 | Algebraic | q = 211 prime, 211 = 3 mod 8 |
| 71 | 141 | 283 | Algebraic | q = 283 prime, 283 = 3 mod 8 |
| 77 | 153 | 307 | Algebraic | q = 307 prime, 307 = 3 mod 8 |
| 83 | 165 | 331 | Algebraic | q = 331 prime, 331 = 3 mod 8 |
| 95 | 189 | 379 | Algebraic | q = 379 prime, 379 = 3 mod 8 |

All results have been independently verified by exhaustive computation of co-degrees.

## Files

- `proof.md` - Complete proof that the algebraic construction yields valid witnesses for all q = 4n-1 prime with q = 3 mod 8
- `construct.py` - Algebraic construction: computes D11, D12, D22 for eligible n and verifies the witness
- `search.py` - Simulated annealing search with parallelism for finding witnesses computationally
- `verify.py` - Independent verification by exhaustive co-degree computation
- `results.json` - All witness data (difference sets D11, D12, D22 for each n)
- `adjacency_strings.json` - Adjacency strings (upper triangle) for all witness graphs

## Verification

To verify a result:

```bash
python verify.py results.json --n 22
```

To verify all results:

```bash
python verify.py results.json
```

To generate a witness using the algebraic construction:

```bash
python construct.py --n 35
```

To run the SA search for a new value:

```bash
python search.py --n 30
```

## References

- Wesley, W. (2024). Lower Bounds for Book Ramsey Numbers. arXiv:2410.03625.
- Lidicky, B., McKinley, G., Pfender, F., Van Overberghe, C. (2024). Small Ramsey numbers for books, wheels, and generalizations. arXiv:2407.07285.
- Rousseau, C. C. and Sheehan, J. (1978). On Ramsey numbers for books. J. Graph Theory 2(1), 77-87.
- Szekeres, G. (1969). Tournaments and Hadamard matrices. L'Enseignement Math. 15, 269-278.
- Momihara, K. and Xiang, Q. (2018). Skew Hadamard difference families and skew Hadamard matrices. arXiv:1801.08776.
