# Prime Power Extension: R(B_{n-1}, B_n) = 4n-1 for q = p^k ≡ 3 (mod 8)

## Theorem

Let q = p^k be a prime power with q ≡ 3 (mod 8). Set n = (q+1)/4. Then R(B_{n-1}, B_n) = 4n - 1.

---

## Part I: Character Preservation

**Lemma (Forced Congruence).** If q = p^k ≡ 3 (mod 8) with p odd, then p ≡ 3 (mod 8) and k is odd.

*Proof.* p² ≡ 1 (mod 8) for odd p, so p^k ≡ p^{k mod 2} (mod 8). If k is even, p^k ≡ 1 (mod 8), contradiction. So k is odd and p ≡ q ≡ 3 (mod 8). ∎

**Lemma (Character Preservation).** Let q = p^k with p odd and k odd. For all a ∈ GF(p)*, χ_q(a) = χ_p(a).

*Proof.* For a ∈ GF(p)*, a^{p-1} = 1. So χ_q(a) = a^{(q-1)/2} = (a^{(p-1)/2})^S = χ_p(a)^S where S = (p^k-1)/(p-1) = 1 + p + ... + p^{k-1}. S is a sum of k odd terms, hence has parity k. Since k is odd, S is odd, so χ_p(a)^S = χ_p(a). ∎

**Corollary.** For q = p^k ≡ 3 (mod 8): χ_q(-1) = -1 and χ_q(2) = -1.

---

## Part II: Line-by-Line Verification of the Prime Proof

I now verify that every step of the proof (as written for q prime) goes through verbatim when q = p^k is a prime power with q ≡ 3 (mod 8).

### Translation of the setup

The prime proof uses:
- ρ a primitive root mod q (generator of (Z/qZ)*)
- g = ρ² (generator of Q, the quadratic residues)
- χ the Legendre symbol mod q
- Q the quadratic residues mod q

For the prime power case, replace with:
- ρ a generator of GF(q)* (cyclic of order q-1)
- g = ρ² (generator of the index-2 subgroup Q of squares in GF(q)*)
- χ the quadratic character of GF(q) (χ(x) = x^{(q-1)/2})
- Q = {x² : x ∈ GF(q)*} = ⟨g⟩

The map a ↦ g^a is a bijection from Z_m to Q, where m = (q-1)/2. This holds because g has order m in GF(q)*. The 2-block circulant graph lives on Z_m ⊔ Z_m. All of this is identical.

### Step 1a: D₁₁ is symmetric ✓

Uses only:
- g^m = 1 (since g has order m) → true over any GF(q)
- g^{m-a} = (g^a)^{-1} → true over any GF(q)
- χ(g^a) = 1 since g^a ∈ Q → true over any GF(q)

No prime-specific content.

### Step 1b: D₁₂ is antisymmetric ✓

Uses only:
- g^{m-a} = (g^a)^{-1} → true over any GF(q)
- χ(g^a) = 1 → true over any GF(q)
- **χ(-1) = -1** → true by Character Preservation Lemma

No prime-specific content.

### Step 1c: |D₁₁| = |D₁₂| = n-1 ✓

**For |D₁₁|:** The computation proceeds:

1. **χ(2) = -1** (used to show the x = 1 boundary term vanishes)
   → True by Character Preservation Lemma. ✓

2. **Σ_{x ∈ Q} χ(x+1) = -1.** The proof expands via the (1+χ)/2 indicator:
   Σ_{x ∈ Q} χ(x+1) = (1/2)[Σ_{x ∈ GF(q)*} χ(x+1) + Σ_{x ∈ GF(q)*} χ(x)χ(x+1)]

   First inner sum: Σ_{x ∈ GF(q)*} χ(x+1) = Σ_{y ≠ 1} χ(y) = -χ(1) = -1.
   This is a complete sum over GF(q)*. Uses only that χ is nontrivial, so Σ_{x ∈ GF(q)*} χ(x) = 0.
   → True over any GF(q). ✓

   Second inner sum: Σ_{x ∈ GF(q)*} χ(x)χ(x+1) = -J(χ,χ) where J(χ,χ) = Σ_{a+b=1} χ(a)χ(b).
   The standard evaluation J(χ,χ) = -χ(-1) holds for ANY quadratic character over ANY finite field
   (see Ireland–Rosen Prop 8.3.2 or Berndt–Evans–Williams §2.1 — the proofs use only the Gauss
   sum identity g(χ)² = χ(-1)q, which holds over all GF(q)).
   Since χ(-1) = -1: J(χ,χ) = 1, so the second inner sum = -1.
   → True over any GF(q). ✓

   Result: Σ_{x ∈ Q} χ(x+1) = (1/2)(-1-1) = -1. Then |D₁₁| = (2n-1)/2 + (-1)/2 = n-1. ✓

**For |D₁₂|:** Uses only the antisymmetry from Step 1b. Purely combinatorial. ✓

### Step 2: Legendre pair property Δ(D₁₁,D₁₁,d) + Δ(D₁₂,D₁₂,d) = n-2 ✓

This is the heart of the proof. Every character sum that appears:

**Boundary terms vanish because χ(2) = -1:**
The terms at x = 1 and x = c⁻¹ contribute factors of e(2) = 1_{Q}(2) = 0.
→ Uses χ(2) = -1. True by Character Preservation. ✓

**-1 ∉ Q** (needed to ensure x+1 ≠ 0 and xc+1 ≠ 0 on Q):
→ Uses χ(-1) = -1. True by Character Preservation. ✓

**T₂ = Σ_{x ∈ Q} χ(x+1) = -1:**
→ Already verified in Step 1c. ✓

**T₃ = Σ_{x ∈ Q} χ(x-1) = 0:**
Uses Σ_{x ∈ GF(q)*} χ(x-1) = Σ_{y≠-1} χ(y) = -χ(-1) = 1, a complete sum over GF(q)*.
And Σ_{x ∈ GF(q)*} χ(x)χ(x-1): the proof substitutes x → 1-x and gets
χ(-1)·Σ χ(x)χ(1-x) = -J(χ,χ) = -1.
→ Complete sums + Jacobi evaluation. True over any GF(q). ✓

**T₄ = Σ_{x ∈ Q} χ(xc+1) = -1** and **T₅ = Σ_{x ∈ Q} χ(xc-1) = 0:**
Uses the fact that x ↦ xc is a bijection Q → Q (since c ∈ Q and Q is a subgroup).
So T₄ = T₂ = -1 and T₅ = T₃ = 0.
→ Uses Q is a subgroup of GF(q)*. True over any GF(q). ✓

**A₊ = Σ_{x ∈ GF(q)*} χ((x+1)(xc+1)) = -2:**
The polynomial f(x) = (x+1)(xc+1) = cx² + (c+1)x + 1 is a nondegenerate quadratic
(discriminant (c-1)² ≠ 0 since c ≠ 1) with leading coefficient c ∈ Q.
The standard result: for f(x) = αx² + βx + γ with α ≠ 0, disc ≠ 0,
  Σ_{x ∈ GF(q)} χ(f(x)) = -χ(α).
This is proved by completing the square (valid since char ≠ 2, which holds because
q is an odd prime power) and using Σ_{x ∈ GF(q)} χ(x²-a) = -1 for a ≠ 0.
**This holds over any finite field of odd characteristic.**
(See Ireland–Rosen Prop 8.1.4, or Lidl–Niederreiter Theorem 5.48.)
So Σ_{x ∈ GF(q)} χ(f(x)) = -χ(c) = -1.
Subtracting the x = 0 term: χ(1) = 1. Hence A₊ = -1 - 1 = -2.
→ True over any GF(q). ✓

**A₋ = Σ_{x ∈ GF(q)*} χ((x-1)(xc-1)) = -2:**
Same calculation (same leading coefficient c, same discriminant (c-1)²).
→ True over any GF(q). ✓

**B₋ = -B₊** (the cubic cancellation):
B₊ = Σ_{x ∈ GF(q)*} χ(cx³ + (c+1)x² + x).
B₋ = Σ_{x ∈ GF(q)*} χ(cx³ - (c+1)x² + x).
Substituting x → -x in B₋: the argument becomes -cx³ - (c+1)x² - x = -(cx³ + (c+1)x² + x).
Since x ↦ -x is a bijection GF(q)* → GF(q)*:
  B₋ = Σ χ(-(cx³+(c+1)x²+x)) = χ(-1)·B₊ = -B₊.
→ **Uses χ(-1) = -1.** True by Character Preservation. ✓

**T₆ + T₇ = (1/2)[(-2+B₊) + (-2-B₊)] = -2.** The B₊ terms cancel. ✓

**Main sum = (1/4)[2(2n-1) - 1 + 0 - 1 + 0 - 2] = n - 3/2.** Arithmetic. ✓

**Correction term:**
χ(c⁻¹-1) = χ((1-c)/c) = χ(1-c)·χ(c)⁻¹ = χ(1-c) since c ∈ Q.
Then χ(1-c) = χ(-(c-1)) = χ(-1)·χ(c-1) = -χ(c-1).
So correction = (1/4)[2 + χ(c-1) - χ(c-1)] = 1/2.
→ Uses c ∈ Q and χ(-1) = -1. Both true over any GF(q). ✓

**S = n - 3/2 - 1/2 = n - 2.** ✓

### Step 3: Within-block codegrees ✓

**Entirely combinatorial.** Uses only:
- D₁₁ symmetric (Step 1a)
- D₂₂ = {1,...,m-1} \ D₁₁ (definition)
- |D₁₁| = |D₁₂| = n-1 (Step 1c)
- Δ(D₁₁,D₁₁,d) + Δ(D₁₂,D₁₂,d) = n-2 (Step 2)

No character sums. No field-specific content. ✓

### Step 4: Cross-block codegrees ✓

**Entirely combinatorial.** The key identity

  Σ_s 1_{D₁₁}(s)·1_{D₁₂}(d-s) = Σ_s 1_{D₁₁}(s)·1_{D₁₂}(s+d)

uses only the symmetry of D₁₁ (substitute s → m-s). The cross-edge codegree calculation uses this identity plus |D₁₂| = n-1. The cross non-edge calculation uses this identity plus |D₂₂| = n-1 and |D₁₂| = n-1.

No character sums. No field-specific content. ✓

---

## Part III: Conclusion

Every computation in the prime proof uses only the following inputs:

| Input | Where used | Prime proof source | Prime power proof source |
|-------|------------|--------------------|--------------------------|
| GF(q)* cyclic of order q-1 | Setup | Z/qZ structure | Standard finite field theory |
| g = ρ² generates Q, order m | Setup | Primitive root | Generator of GF(q)* |
| χ(-1) = -1 | Steps 1b, 2 | q ≡ 3 mod 4 | Character Preservation |
| χ(2) = -1 | Steps 1c, 2 | q ≡ 3 mod 8, QR | Character Preservation |
| Σ_{GF(q)*} χ(x) = 0 | Step 1c | Nontrivial character | Nontrivial character |
| J(χ,χ) = -χ(-1) | Steps 1c, 2 | Ireland–Rosen 8.3.2 | Same (field-agnostic) |
| Σ_{GF(q)} χ(αx²+βx+γ) = -χ(α) | Step 2 | Ireland–Rosen 8.1.4 | Same (field-agnostic) |
| Q is a subgroup of GF(q)* | Step 2 | Obvious | Obvious |
| Steps 3–4 are combinatorial | Steps 3–4 | — | — |

**No computation in the proof requires q to be prime.** Every character sum is either:
(a) a complete sum over GF(q) or GF(q)*, evaluated by standard results that hold over all finite fields, or
(b) reduced to such a sum via the (1+χ)/2 indicator for Q.

The proof never computes a "half-sum" Σ_{a=0}^{m-1} f(g^a) that cannot be reduced to a complete sum. The (1+χ)/2 trick converts sums over Q into sums over GF(q)*, and every resulting complete sum is evaluated by field-agnostic identities.

Therefore, the prime proof carries over to q = p^k ≡ 3 (mod 8) after replacing the prime-field facts by their finite-field analogues:
- Replace "Legendre symbol mod q" with "quadratic character of GF(q)"
- Replace "q ≡ 3 mod 4 implies χ(-1) = -1" with "Character Preservation Lemma"
- Replace "q ≡ 3 mod 8 and second supplement to QR implies χ(2) = -1" with "Character Preservation Lemma"

The six codegree bounds hold with identical values:

| Pair type | Value | Bound | Status |
|-----------|-------|-------|--------|
| Edge in V₁ (d ∈ D₁₁) | n-2 | ≤ n-2 | ✓ |
| Non-edge in V₁ (d ∈ D₂₂) | n-2 | ≤ n-1 | ✓ |
| Edge in V₂ (d ∈ D₂₂) | n-3 | ≤ n-2 | ✓ |
| Non-edge in V₂ (d ∈ D₁₁) | n-1 | ≤ n-1 | ✓ |
| Cross-edge (d ∈ D₁₂) | n-2 | ≤ n-2 | ✓ |
| Cross non-edge (d ∉ D₁₂) | n-1 | ≤ n-1 | ✓ |

Combined with R(B_{n-1}, B_n) ≤ 4n-1 (Rousseau–Sheehan 1978), this gives R(B_{n-1}, B_n) = 4n-1. ∎

---

## Genuinely New Cases

| p | k | q = p^k | n = (q+1)/4 | 2n-1 | Wesley? | New? |
|---|---|---------|-------------|------|---------|------|
| 3 | 3 | 27 | 7 | 13 (prime, ≡1 mod 4) | Yes | No |
| 11 | 3 | 1331 | 333 | 665 = 5·7·19 | No | **Yes** |
| 19 | 3 | 6859 | 1715 | 3429 = 3·1143 | No | **Yes** |
| 3 | 5 | 243 | 61 | 121 = 11² (≡1 mod 4) | Yes | No |
| 43 | 3 | 79507 | 19877 | 39753 | No | **Yes** |
| 67 | 3 | 300763 | 75191 | 150381 | No | **Yes** |
| 3 | 7 | 2187 | 547 | 1093 (prime, ≡1 mod 4) | Yes | No |

New cases come primarily from p ≡ 3 (mod 8) with p ≥ 11 and k = 3.

---

## Computational Verification (SageMath)

```python
def verify_prime_power_extension(p, k):
    """Verify the construction for q = p^k ≡ 3 (mod 8)."""
    q = p**k
    assert q % 8 == 3, f"q = {q} is not 3 mod 8"

    F = GF(q, 'a')
    n = (q + 1) // 4
    m = (q - 1) // 2

    # Verify character preservation
    assert not F(-1).is_square(), "chi(-1) should be -1"
    assert not F(2).is_square(), "chi(2) should be -1"

    # Find generator of Q
    rho = F.multiplicative_generator()
    g = rho**2
    assert g.multiplicative_order() == m

    def chi(x):
        if x == 0: return 0
        return 1 if x.is_square() else -1

    # Build sets
    g_powers = [g**a for a in range(m)]
    D11 = set(a for a in range(1, m) if chi(g_powers[a] + 1) == 1)
    D12 = set(a for a in range(1, m) if chi(g_powers[a] - 1) == 1)
    D22 = set(range(1, m)) - D11

    # Check sizes
    assert len(D11) == n - 1, f"|D11| = {len(D11)}, expected {n-1}"
    assert len(D12) == n - 1, f"|D12| = {len(D12)}, expected {n-1}"

    # Check symmetry
    for a in D11:
        assert (m - a) % m in D11 or (m - a) == 0, f"D11 not symmetric at {a}"

    # Check Legendre pair property
    def Delta(A, B, d):
        return sum(1 for a in A if (a + d) % m in B)

    for d in range(1, m):
        val = Delta(D11, D11, d) + Delta(D12, D12, d)
        assert val == n - 2, f"LP failed at d={d}: got {val}, expected {n-2}"

    # Check all six codegree bounds
    def Sigma_set(A, B, d):
        """Σ(A, B, d) = |{a ∈ A : (d - a) mod m ∈ B}|"""
        return sum(1 for a in A if (d - a) % m in B)

    # 1. Within V1, edge (d ∈ D11): codeg ≤ n-2
    for d in D11:
        val = Delta(D11, D11, d) + Delta(D12, D12, d)
        assert val == n - 2, f"V1 edge at d={d}: {val}, expected {n-2}"

    # 2. Within V1, non-edge (d ∈ D22): complement codeg ≤ n-1
    for d in D22:
        val = Delta(D22, D22, d) + (m - 2*len(D12) + Delta(D12, D12, d))
        assert val <= n - 1, f"V1 non-edge at d={d}: {val}, expected ≤ {n-1}"

    # 3. Within V2, edge (d ∈ D22): codeg ≤ n-2
    for d in D22:
        val = Delta(D22, D22, d) + Delta(D12, D12, d)
        assert val == n - 3, f"V2 edge at d={d}: {val}, expected {n-3}"

    # 4. Within V2, non-edge (d ∈ D11): complement codeg ≤ n-1
    for d in D11:
        val = Delta(D11, D11, d) + 1 + Delta(D12, D12, d)
        assert val == n - 1, f"V2 non-edge at d={d}: {val}, expected {n-1}"

    # 5. Cross-edge (d ∈ D12): codeg ≤ n-2
    #    Common nbrs in V1: Sigma(D11, D12, d) = |{s ∈ D11 : (d-s) mod m ∈ D12}|
    #    Common nbrs in V2: Delta(D12, D22, d) = |{s ∈ D12 : (s+d) mod m ∈ D22}|
    #    By the proof's key identity, these sum to n-2.
    for d in D12:
        A = Sigma_set(D11, D12, d)
        B = Delta(D12, D22, d)
        val = A + B
        assert val == n - 2, f"Cross-edge at d={d}: {val}, expected {n-2}"

    # 6. Cross non-edge (d ∉ D12, d ∈ {0,...,m-1}):
    #    complement codeg ≤ n-1
    #    Common non-nbrs in V1: Sigma(D22, complement of D12 in Z_m, d)
    #    Common non-nbrs in V2: |{s ∈ D11 : (s+d) mod m ∉ D12}|
    #    By the proof's key identity, these sum to n-1.
    non_D12 = set(range(m)) - D12
    for d in non_D12:
        # V1 contribution: |{s ∈ D22 : (d-s) mod m ∉ D12}|
        A = sum(1 for s in D22 if (d - s) % m not in D12)
        # V2 contribution: |{s ∈ D11 : (s+d) mod m ∉ D12}|
        B = sum(1 for s in D11 if (s + d) % m not in D12)
        val = A + B
        assert val == n - 1, f"Cross non-edge at d={d}: {val}, expected {n-1}"

    print(f"q = {p}^{k} = {q}, n = {n}: ALL 6 CONDITIONS VERIFIED")

# Test cases
verify_prime_power_extension(3, 3)    # q = 27, n = 7
verify_prime_power_extension(11, 3)   # q = 1331, n = 333 (genuinely new)
```
