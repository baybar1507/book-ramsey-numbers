# Proof that the construction yields R(B_{n-1}, B_n) = 4n-1 for q = 4n-1 prime, q ≡ 3 (mod 8)

## Setup

Let q = 4n-1 be prime with q ≡ 3 (mod 8). Set m = (q-1)/2 = 2n-1. Let ρ be a primitive root mod q, g = ρ², and χ the Legendre symbol mod q. Let Q denote the quadratic residues mod q.

Define:
- D₁₁ = {a ∈ {1,...,m-1} : χ(gᵃ + 1) = 1}
- D₁₂ = {a ∈ {1,...,m-1} : χ(gᵃ - 1) = 1}
- D₂₂ = {1,...,m-1} \ D₁₁

Note: g has order m in (ℤ/qℤ)*, and a ↦ gᵃ is a bijection from ℤ_m to Q.

**Theorem.** The 2-block circulant graph on ℤ_m ⊔ ℤ_m with adjacency defined by (D₁₁, D₁₂, D₂₂) has no B_{n-1} subgraph and its complement has no B_n subgraph.

This is equivalent to showing six codegree bounds hold (cf. Wesley [arXiv:2410.03625], Lemma 9): for the graph G to avoid B_{n-1}, every edge must have codegree ≤ n-2; for the complement to avoid B_n, every non-edge must have complement codegree ≤ n-1. There are three pair types (within V₁, within V₂, cross V₁–V₂), each contributing an edge and a non-edge condition. By the circulant structure, codegrees depend only on the difference d.

## Step 1: Structural properties

### 1a. D₁₁ is symmetric

**Claim:** a ∈ D₁₁ iff m-a ∈ D₁₁.

Since g^m = ρ^{q-1} = 1, we have g^{m-a} = g^{-a} = (gᵃ)⁻¹. Then:

χ(g^{m-a} + 1) = χ(1/gᵃ + 1) = χ((1 + gᵃ)/gᵃ) = χ(1 + gᵃ) · χ(gᵃ)⁻¹ = χ(gᵃ + 1)

since gᵃ ∈ Q, so χ(gᵃ) = 1. ∎

### 1b. D₁₂ is antisymmetric

**Claim:** D₁₂ ∩ (-D₁₂) = ∅ and D₁₂ ∪ (-D₁₂) = {1,...,m-1}.

We have g^{m-a} = (gᵃ)⁻¹, so:

χ(g^{m-a} - 1) = χ(1/gᵃ - 1) = χ((1 - gᵃ)/gᵃ) = χ(-(gᵃ - 1)) · χ(gᵃ)⁻¹ = χ(-1) · χ(gᵃ - 1)

Since q ≡ 3 (mod 4), χ(-1) = -1. So χ(g^{m-a} - 1) = -χ(gᵃ - 1).

Hence a ∈ D₁₂ iff m-a ∉ D₁₂ (noting gᵃ - 1 ≠ 0 for a ≠ 0). ∎

### 1c. Sizes

**Claim:** |D₁₁| = |D₁₂| = n-1.

For |D₁₁|: count x ∈ Q with χ(x+1) = 1. Using the indicator (1+χ(·))/2:

|D₁₁| = Σ_{x ∈ Q, x≠1} (1 + χ(x+1))/2

Since q ≡ 3 (mod 8), χ(2) = -1 (by the second supplement to quadratic reciprocity). So the x = 1 term has χ(2) = -1, giving (1+(-1))/2 = 0. Thus we can include x = 1 without changing the count:

|D₁₁| = (1/2) Σ_{x ∈ Q} (1 + χ(x+1)) = m/2 + (1/2) Σ_{x ∈ Q} χ(x+1)

Now Σ_{x ∈ Q} χ(x+1) = (1/2) Σ_{x ∈ F_q*} (1+χ(x))χ(x+1) = (1/2)[Σ_{x≠0} χ(x+1) + Σ_{x≠0} χ(x)χ(x+1)].

The first sum: Σ_{x ∈ F_q*} χ(x+1) = Σ_{y ∈ F_q \setminus \{1\}} χ(y) = -χ(1) = -1.

The second sum: Σ_{x ∈ F_q*} χ(x)χ(x+1). The x = -1 term contributes χ(-1)χ(0) = 0, so this equals Σ_{x ≠ 0,-1} χ(x(x+1)). Substituting a = -x:

Σ_{x ≠ 0,-1} χ(x)χ(x+1) = χ(-1) · Σ_{a ≠ 0,1} χ(a)χ(1-a) = -J(χ,χ)

where J(χ,χ) = Σ_{a ∈ F_q} χ(a)χ(1-a) is the Jacobi sum. Since χ is a quadratic character (so χ² = ε₀, the principal character), the standard evaluation gives J(χ,χ) = -χ(-1) (see Ireland–Rosen, *A Classical Introduction to Modern Number Theory*, Proposition 8.3.2, or Berndt–Evans–Williams, *Gauss and Jacobi Sums*, §2.1). Since q ≡ 3 (mod 4), χ(-1) = -1, so J(χ,χ) = 1.

So the second sum is -1.

Therefore Σ_{x ∈ Q} χ(x+1) = (1/2)(-1 + (-1)) = -1.

|D₁₁| = (2n-1)/2 + (1/2)(-1) = n - 1. ∎

For |D₁₂|: by Step 1b, D₁₂ and -D₁₂ partition {1,...,m-1} into two equal halves, so |D₁₂| = (m-1)/2 = (2n-2)/2 = n-1. ∎

## Step 2: The Legendre pair property

**Claim:** For all d ∈ {1,...,m-1}:

Δ(D₁₁, D₁₁, d) + Δ(D₁₂, D₁₂, d) = n - 2

where Δ(A, B, d) = |{a ∈ A : (a+d) mod m ∈ B}|. (All arithmetic on indices is mod m throughout.)

### Proof

Let c = g^d ∈ Q, c ≠ 1. Define the true indicator e(y) = 1_{y ∈ Q} and the algebraic proxy ẽ(y) = (1+χ(y))/2. These agree for y ≠ 0; for y = 0, e(0) = 0 but ẽ(0) = 1/2. So we must track where product arguments hit zero.

For the D₁₁ autocorrelation: strictly speaking, Δ(D₁₁, D₁₁, d) = Σ_{x ∈ Q \ {1, c⁻¹}} e(x+1)e(xc+1), since a = 0 and a = m-d (corresponding to x = g⁰ = 1 and x = g^{m-d} = c⁻¹) are excluded from D₁₁ ⊂ {1,...,m-1}. However, since q ≡ 3 (mod 8), χ(2) = -1 by the second supplement to quadratic reciprocity, so e(2) = 0. The x = 1 term contributes e(1+1)e(c+1) = e(2)·e(c+1) = 0, and the x = c⁻¹ term contributes e(c⁻¹+1)e(c⁻¹·c+1) = e(c⁻¹+1)·e(2) = 0. So both omitted terms vanish and the sum extends to all x ∈ Q. Furthermore, the arguments x+1 and xc+1 never hit zero on Q: x+1 = 0 requires x = -1 ∉ Q (since q ≡ 3 mod 4), and xc+1 = 0 requires x = -c⁻¹ ∉ Q for the same reason. So we can freely replace e with ẽ:

Σ_{x ∈ Q} e(x+1)e(xc+1) = Σ_{x ∈ Q} ẽ(x+1)ẽ(xc+1).

For the D₁₂ autocorrelation Σ_{x ∈ Q} e(x-1)e(xc-1): the argument x-1 = 0 at x = 1, and xc-1 = 0 at x = c⁻¹. At both points e = 0 but ẽ = 1/2. The mismatches are:

- x = 1: ẽ(0)·ẽ(c-1) = (1/2)ẽ(c-1), but e(0)·e(c-1) = 0.
- x = c⁻¹: ẽ(c⁻¹-1)·ẽ(0) = (1/2)ẽ(c⁻¹-1), but e(c⁻¹-1)·e(0) = 0.

Therefore:

S := Δ(D₁₁,D₁₁,d) + Δ(D₁₂,D₁₂,d) = Σ_{x ∈ Q}[ẽ(x+1)ẽ(xc+1) + ẽ(x-1)ẽ(xc-1)] - (1/2)ẽ(c-1) - (1/2)ẽ(c⁻¹-1)

**Computing the main sum.** Expand:

ẽ(x+1)ẽ(xc+1) + ẽ(x-1)ẽ(xc-1) = (1/4)[(1+χ(x+1))(1+χ(xc+1)) + (1+χ(x-1))(1+χ(xc-1))]

Summing over x ∈ Q gives (1/4)[2m + T₂ + T₃ + T₄ + T₅ + T₆ + T₇] where:

- T₂ = Σ_{x ∈ Q} χ(x+1) = -1 (computed above)
- T₃ = Σ_{x ∈ Q} χ(x-1). Expanding via (1+χ(x))/2: T₃ = (1/2)[Σ_{x ∈ F_q*} χ(x-1) + Σ_{x ∈ F_q*} χ(x)χ(x-1)]. The first inner sum is Σ_{y ≠ -1} χ(y) = -χ(-1) = 1. For the second, substitute x → 1-x: Σ χ(x)χ(x-1) = Σ χ(1-x)χ(-x) = χ(-1) Σ χ(x)χ(1-x) = -J(χ,χ) = -1. So T₃ = (1/2)(1 + (-1)) = 0.
- T₄ = Σ_{x ∈ Q} χ(xc+1) = -1 (since xc ranges over Q as x does, this equals T₂)
- T₅ = Σ_{x ∈ Q} χ(xc-1) = 0 (since xc ranges over Q as x does, this equals T₃)
- T₆ + T₇ = Σ_{x ∈ Q}[χ((x+1)(xc+1)) + χ((x-1)(xc-1))]

**The key cancellation: T₆ + T₇ = -2.**

Write T₆ = (1/2)[A₊ + B₊] and T₇ = (1/2)[A₋ + B₋] where:

- A₊ = Σ_{x ∈ F_q*} χ((x+1)(xc+1))
- B₊ = Σ_{x ∈ F_q*} χ(x(x+1)(xc+1)) = Σ_{x ∈ F_q*} χ(cx³ + (c+1)x² + x)
- A₋ = Σ_{x ∈ F_q*} χ((x-1)(xc-1))
- B₋ = Σ_{x ∈ F_q*} χ(x(x-1)(xc-1)) = Σ_{x ∈ F_q*} χ(cx³ - (c+1)x² + x)

For A₊: (x+1)(xc+1) = cx² + (c+1)x + 1. This is a non-degenerate quadratic in x (discriminant (c+1)² - 4c = (c-1)² ≠ 0 since c ≠ 1). By the standard evaluation of quadratic character sums (see e.g. Berndt–Evans–Williams, *Gauss and Jacobi Sums*, Theorem 1.1.5, or Ireland–Rosen, *A Classical Introduction to Modern Number Theory*, Proposition 8.1.4): for a non-degenerate quadratic f(x) = αx² + βx + γ with α ∈ Q, Σ_{x ∈ F_q} χ(f(x)) = -χ(α) = -1 (since χ(c) = 1).

Subtracting the x = 0 term (χ(1) = 1): A₊ = -1 - 1 = -2.

By an identical calculation (the quadratic (x-1)(xc-1) = cx² - (c+1)x + 1 has the same leading coefficient and discriminant), A₋ = -2.

For B₋: substitute x → -x in cx³ - (c+1)x² + x to get -(cx³ + (c+1)x² + x). Since the sum ranges over all of F_q*:

B₋ = Σ_{x ∈ F_q*} χ(-(cx³ + (c+1)x² + x)) = χ(-1) · B₊ = -B₊

Therefore:

T₆ + T₇ = (1/2)[(A₊ + B₊) + (A₋ + B₋)] = (1/2)[(-2 + B₊) + (-2 - B₊)] = -2 ∎

So the main sum = (1/4)[2(2n-1) - 1 + 0 - 1 + 0 - 2] = (4n - 6)/4 = n - 3/2.

**Computing the correction term.**

(1/2)ẽ(c-1) + (1/2)ẽ(c⁻¹-1) = (1/4)[1 + χ(c-1)] + (1/4)[1 + χ(c⁻¹-1)]

= (1/4)[2 + χ(c-1) + χ(c⁻¹-1)]

Now χ(c⁻¹-1) = χ((1-c)/c) = χ(1-c) (since c ∈ Q) = χ(-(c-1)) = χ(-1)χ(c-1) = -χ(c-1).

So the correction = (1/4)[2 + χ(c-1) - χ(c-1)] = 1/2.

**Conclusion:** S = (n - 3/2) - 1/2 = n - 2. ∎

### Why q ≡ 3 (mod 8) is needed

The argument uses χ(2) = -1 to ensure e(2) = 0, which makes the D₁₁ boundary terms at x = 1 and x = c⁻¹ vanish cleanly. When q ≡ 7 (mod 8), χ(2) = 1 and additional d-dependent correction terms arise in the D₁₁ autocorrelation, breaking the Legendre pair property.

## Step 3: Within-block codegrees

We first establish a key identity relating the autocorrelations of D₁₁ and D₂₂.

**Lemma.** For all d ∈ {1,...,m-1}: Δ(D₂₂, D₂₂, d) = Δ(D₁₁, D₁₁, d) - 1 + 2·1_{D₁₁}(d).

*Proof.* Since D₁₁ and D₂₂ partition {1,...,m-1}, for any d ≠ 0:

Δ(D₁₁, D₁₁, d) + Δ(D₁₁, D₂₂, d) = |D₁₁| - 1_{D₁₁}(m-d) = (n-1) - 1_{D₁₁}(d)    ... (*)

where the subtracted term accounts for the unique a = m-d ∈ D₁₁ (if it exists) with (a+d) mod m = 0 ∉ D₁₁ ∪ D₂₂. Here we use the symmetry of D₁₁: 1_{D₁₁}(m-d) = 1_{D₁₁}(d).

Similarly: Δ(D₂₂, D₁₁, d) + Δ(D₂₂, D₂₂, d) = (n-1) - 1_{D₂₂}(d)    ... (**)

By the symmetry of D₁₁, Δ(D₁₁, D₂₂, d) = Δ(D₂₂, D₁₁, d). (Substitute a → m-a-d and use 1_{D₁₁}(m-a) = 1_{D₁₁}(a). Note that D₂₂ = {1,...,m-1} \ D₁₁ is also symmetric, since D₁₁ is symmetric and {1,...,m-1} is closed under a ↦ m-a.) Substituting (*) into (**):

Δ(D₂₂, D₂₂, d) = (n-1) - 1_{D₂₂}(d) - [(n-1) - 1_{D₁₁}(d) - Δ(D₁₁, D₁₁, d)] = Δ(D₁₁, D₁₁, d) + 1_{D₁₁}(d) - 1_{D₂₂}(d).

Since exactly one of 1_{D₁₁}(d), 1_{D₂₂}(d) equals 1, this gives Δ(D₂₂, D₂₂, d) = Δ(D₁₁, D₁₁, d) - 1 + 2·1_{D₁₁}(d). ∎

With this identity and the Legendre pair property from Step 2 (LP), the six within-block codegree bounds follow. In each case, vertices i and j in the same block differ by d (mod m), and the codegree (for edges) or complement codegree (for non-edges) decomposes into same-block and cross-block contributions.

### Edges within V₁ (d ∈ D₁₁)

- Common neighbors in V₁: Δ(D₁₁, D₁₁, d).
- Common neighbors in V₂: Δ(D₁₂, D₁₂, d).
- Total = n - 2 by (LP). Bound: ≤ n - 2. ✓

### Non-edges within V₁ (d ∈ D₂₂)

- Common non-neighbors in V₁: Δ(D₂₂, D₂₂, d) = Δ(D₁₁, D₁₁, d) - 1 (since d ∈ D₂₂, so 1_{D₁₁}(d) = 0).
- Common non-neighbors in V₂: m - 2|D₁₂| + Δ(D₁₂, D₁₂, d) = 1 + Δ(D₁₂, D₁₂, d). (Inclusion-exclusion: the m offsets from V₂ minus those adjacent to i, minus those adjacent to j, plus those adjacent to both. No self-exclusion since V₂ ≠ V₁.)
- Total = Δ(D₁₁, D₁₁, d) + Δ(D₁₂, D₁₂, d) = n - 2 by (LP). Bound: ≤ n - 1. ✓

### Edges within V₂ (d ∈ D₂₂)

- Common neighbors in V₂: Δ(D₂₂, D₂₂, d) = Δ(D₁₁, D₁₁, d) - 1 (since d ∈ D₂₂).
- Common neighbors in V₁: Δ(D₁₂, D₁₂, d). (A vertex w ∈ V₁ is a common neighbor iff (u-w) mod m ∈ D₁₂ and (v-w) mod m ∈ D₁₂, giving the D₁₂ autocorrelation.)
- Total = Δ(D₁₁, D₁₁, d) - 1 + Δ(D₁₂, D₁₂, d) = (n-2) - 1 = n - 3. Bound: ≤ n - 2. ✓

### Non-edges within V₂ (d ∈ D₁₁)

- Common non-neighbors in V₂: Δ(D₁₁, D₁₁, d). A vertex w+m ∈ V₂ is a common non-neighbor iff (w-u) mod m ∉ D₂₂ and (w-v) mod m ∉ D₂₂, i.e. both differences lie in D₁₁ ∪ {0}. The zero cases correspond to w = u or w = v, which are excluded from codegree counts (a vertex is not its own non-neighbor). So the count is exactly Δ(D₁₁, D₁₁, d).
- Common non-neighbors in V₁: m - 2|D₁₂| + Δ(D₁₂, D₁₂, d) = 1 + Δ(D₁₂, D₁₂, d).
- Total = Δ(D₁₁, D₁₁, d) + 1 + Δ(D₁₂, D₁₂, d) = (n-2) + 1 = n - 1. Bound: ≤ n - 1. ✓

## Step 4: Cross-block codegrees

The proof is purely combinatorial, requiring only the symmetry of D₁₁.

### Key identity

**Claim:** Σ_s 1_{D₁₁}(s) · 1_{D₁₂}(d-s) = Σ_s 1_{D₁₁}(s) · 1_{D₁₂}(s+d).

*Proof.* Substitute s → m-s. Since D₁₁ is symmetric (1_{D₁₁}(m-s) = 1_{D₁₁}(s)) and d-(m-s) ≡ d+s (mod m):

Σ_s 1_{D₁₁}(s) · 1_{D₁₂}(d-s) = Σ_s 1_{D₁₁}(m-s) · 1_{D₁₂}(d-m+s) = Σ_s 1_{D₁₁}(s) · 1_{D₁₂}(s+d). ∎

### Cross-edges (d ∈ D₁₂)

The codegree of a cross-edge (i ∈ V₁, j+m ∈ V₂) with d = j-i ∈ D₁₂ is:

C(d) = [common neighbors in V₁] + [common neighbors in V₂]

Common neighbors in V₁:
= |{s ∈ D₁₁ : d-s ∈ D₁₂}| =: A

Common neighbors in V₂:
= |{s ∈ D₁₂ : s-d ∈ D₂₂}|
= |{s ∈ D₁₂ : s ≠ d}| - |{s ∈ D₁₂ : s ≠ d, s-d ∈ D₁₁}|
= (|D₁₂| - 1) - |{r ∈ D₁₁ : r+d ∈ D₁₂}|   (setting r = s-d)
= (n - 2) - Σ_r 1_{D₁₁}(r) · 1_{D₁₂}(r+d)
= (n - 2) - A   (by the key identity)

Total: C(d) = A + (n-2) - A = **n - 2** ≤ n - 2. ✓

### Cross non-edges (d ∉ D₁₂, including d = 0)

The complement codegree (common non-neighbors) is:

In V₁:
= |{s ∈ D₂₂ : d-s ∉ D₁₂}|
= |D₂₂| - |{s ∈ D₂₂ : d-s ∈ D₁₂}|
= (n-1) - [|{s ∈ ℤ_m* : d-s ∈ D₁₂}| - |{s ∈ D₁₁ : d-s ∈ D₁₂}|]
= (n-1) - [|D₁₂| - A]

(Here |{s ∈ ℤ_m* : d-s ∈ D₁₂}| = |D₁₂|: since d ∉ D₁₂ and 0 ∉ D₁₂, the map t ↦ s = d-t is a bijection from D₁₂ to {s ∈ ℤ_m* : d-s ∈ D₁₂}.)
= (n-1) - (n-1) + A = A

In V₂:
= |{s ∈ D₁₁ : s+d ∉ D₁₂}|
= |D₁₁| - Σ_s 1_{D₁₁}(s) · 1_{D₁₂}(s+d)
= (n-1) - A   (by the key identity)

Total: A + (n-1) - A = **n - 1** ≤ n - 1. ✓

## Summary

All six codegree conditions are satisfied:

| Pair type | Condition | Value | Bound | Status |
|-----------|-----------|-------|-------|--------|
| Edge in V₁ (d ∈ D₁₁) | codeg ≤ n-2 | n-2 | n-2 | ✓ |
| Non-edge in V₁ (d ∈ D₂₂) | complement codeg ≤ n-1 | n-2 | n-1 | ✓ |
| Edge in V₂ (d ∈ D₂₂) | codeg ≤ n-2 | n-3 | n-2 | ✓ |
| Non-edge in V₂ (d ∈ D₁₁) | complement codeg ≤ n-1 | n-1 | n-1 | ✓ |
| Cross-edge (d ∈ D₁₂) | codeg ≤ n-2 | n-2 | n-2 | ✓ |
| Cross non-edge (d ∉ D₁₂) | complement codeg ≤ n-1 | n-1 | n-1 | ✓ |

By Dirichlet's theorem on primes in arithmetic progressions, there are infinitely many primes q ≡ 3 (mod 8), and hence infinitely many n for which q = 4n-1 is such a prime. For each such n, the construction gives a graph on 4n-2 vertices avoiding B_{n-1} whose complement avoids B_n, establishing R(B_{n-1}, B_n) ≥ 4n-1. Combined with the upper bound R(B_{n-1}, B_n) ≤ 4n-1 proved by Rousseau and Sheehan (1978, Theorem 1 in Wesley's notation), this gives R(B_{n-1}, B_n) = 4n-1 for all such n. ∎
