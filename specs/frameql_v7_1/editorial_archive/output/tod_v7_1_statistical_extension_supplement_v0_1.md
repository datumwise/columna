---
title: "The Theory of Data — Statistical Extension Reference"
subtitle: "Companion supplement to Version 7.1 Full Manuscript Working Draft 0.4"
author: "Huayin Wang"
date: "Working Supplement 0.1 — 7 September 2026"
lang: en-US
---

**datumwise, an independent open-source research project**  
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)  
**Status:** Working reference supplement; no separate DOI or implementation authority.  
**Foundation:** [ToD v7.1 — Full Manuscript Working Draft 0.4](the_theory_of_data_v7_1_full_manuscript_working_draft_v0_4.md).

# Purpose and standing

This supplement preserves the eight statistical extension entries and extension-matrix rows previously included in Full Manuscript Working Draft 0.3, §§11.6.1–11.6.8 and Appendix A. Each entry body and each matrix row is retained unchanged; the entry headings are renumbered S.1–S.8. The relocation is editorial. It is neither a new admission nor a withdrawal of an inherited law.

These entries retain Version 7.0's conditional catalog standing: an entry identifies an intended canonical analytical-law kind, at its stated level of contract completion. Admission for realization requires the common family-law contract in the main manuscript, including its target specification, formation, participation, sufficient-state adequacy, and exceptional-case obligations. The four propositions in the foundation do not newly prove every formula or convention collected here. No TOP-k or rank-correlation admission is added. [2, §6.2]

The foundation is readable without this supplement. A review of a particular extension's formula or convention should use the corresponding entry here as well as the common contract. In the entries, \(I\) is a constitutive input anchor and \(A\) an admitted target with \(I\succeq A\). Operands and every role of a basis are interpreted under the participation stated by the law. Mathematical forms are not shipped Frame-QL syntax.

# Inherited entries

## S.1 Weighted mean

For `weighted_mean(x@I,w@I)`, one sufficient-state basis under governed joint participation and a valid weight domain is

\[
\left\{sum((xw)@I),\;sum(w@I)\right\}.
\]

Its constructor is

\[
weighted\_mean(x@I,w@I)@A
=\frac{sum((xw)@I)@A}{sum(w@I)@A}.
\]

The product must be formed while the paired values are available at \(I\). The denominator must use the same admitted joint participation. Missing, zero, negative, or otherwise inadmissible weights and a zero denominator require the law's explicit treatment; the label “weight” supplies none of these decisions.

## S.2 Raw moments

For integer \(k\ge1\), write

\[
moment(x@I,k).
\]

One sufficient basis is \(\{sum((x^k)@I),count(x@I)\}\), giving

\[
moment(x@I,k)@A
=\frac{sum((x^k)@I)@A}{count(x@I)@A}
\]

on the applicable nonempty domain. The first raw moment may canonicalize to MEAN where the analytical law and conventions agree. The pointwise power is part of formation at \(I\), not an operation applied after a different aggregation.

## S.3 Variance and standard deviation

A variance family carries its convention:

\[
variance(x@I;ddof=d).
\]

Let \(n=count(x@I)@A\), \(s_1=sum(x@I)@A\), and \(s_2=sum((x^2)@I)@A\), all under matching participation. One exact construction is

\[
variance(x@I;ddof=d)@A
=\frac{s_2-s_1^2/n}{n-d}
\]

on the convention's defined domain. Common \(d=0\) and \(d=1\) conventions distinguish population and sample denominators. The formula is an analytical equality, not a recommendation that every finite-precision engine use this numerically unqualified evaluation path.

Standard deviation has the same-anchor constructor

\[
stddev(x@I;ddof=d)@A
=\sqrt{variance(x@I;ddof=d)@A}.
\]

Variance is sufficient for that target at the same anchor without becoming self-sufficient from its finalized scalar for variance continuation.

## S.4 Root mean square

The family `rms(x@I)` has the constructor

\[
rms(x@I)@A=\sqrt{moment(x@I,2)@A}
\]

on the admitted domain. The second raw moment is therefore a sufficient-state family for RMS.

## S.5 Central moments, skewness, and kurtosis

The baseline admits central-moment constructions of the form

\[
central\_moment(x@I,k;convention=c).
\]

For population central moments, raw sums through order \(k\) and count form one exact sufficient basis. Skewness and kurtosis retain their explicit conventions because finite-sample corrections and excess-kurtosis choices differ.

For the population-moment conventions,

\[
skewness=\frac{\mu_3}{\mu_2^{3/2}},
\qquad
kurtosis=\frac{\mu_4}{\mu_2^2},
\]

where \(\mu_k\) is the corresponding central moment. The law must state its defined domain and convention rather than permitting an implementation to select one silently.

## S.6 Covariance and Pearson correlation

For

\[
covariance(x@I,y@I;ddof=d),
\]

let \(J\) denote the governed jointly participating points. One exact basis carries, over \(J\),

\[
n,\quad\sum x,\quad\sum y,\quad\sum xy.
\]

These may be represented through the appropriate self-sufficient sum/count families formed from the paired expression at \(I\). Every component must use the same co-participation contract. Marginal support of \(x\) and \(y\) does not establish paired support.

Pearson correlation additionally needs \(\sum x^2\) and \(\sum y^2\) under that same joint participation. A canonical form is

\[
correlation(x@I,y@I;method=pearson).
\]

The applicable denominator and exceptional cases remain part of the law. Rank-based correlation is not admitted here merely by analogy to Pearson or by the fact that ranking is executable.

## S.7 Quantile, percentile, and median

Exact quantiles can use the multiset family as one sufficient basis:

\[
quantile(x@I,p;convention=q)@A
=Q_{p,q}(multiset(x@I)@A).
\]

The convention \(q\) determines the applicable finite-sample interpolation rule and domain. Exact state may retain all participating values with multiplicity; analytical materializability does not imply cheap or compact storage.

Under the same convention, percentile and median may canonicalize as

\[
percentile(x@I,p)\equiv quantile(x@I,p/100),
\]

\[
median(x@I)\equiv quantile(x@I,0.5).
\]

The required ordering is over the value domain. These quantile constructions do not depend on an order of analytical input points.

## S.8 Geometric and harmonic mean

For the declared positive domain of \(x\),

\[
geometric\_mean(x@I)@A
=\exp\!\left(\frac{sum((\log x)@I)@A}{count(x@I)@A}\right).
\]

The logarithm is formed pointwise at the constitutive anchor. Nothing here claims that taking a logarithm preserves the operand family identity.

For a domain on which the reciprocals and constructor are defined,

\[
harmonic\_mean(x@I)@A
=\frac{count(x@I)@A}{sum((1/x)@I)@A}.
\]

Both constructions require matching participation and explicit exceptional cases. Their analytical statements do not assert that any particular profile realizes them.

# S.9 Inherited extension matrix

These rows are retained verbatim from Full Manuscript Working Draft 0.3, Appendix A. The central-moment row already collected an inherited construction; its relocation adds no admission.

| Standing | Analytical family or construction | Sufficient-state basis / continuation | Required semantic distinctions |
|---|---|---|---|
| Inherited extension | Weighted mean: `weighted_mean(x@I,w@I)` | Sum of paired products and sum of participating weights | Joint participation, weight domain, denominator |
| Inherited extension | Raw moment: `moment(x@I,k)` | Sum of powers and count | Power formed at constitutive anchor; order-one equivalence where admitted |
| Inherited extension | Variance: `variance(x@I;ddof=d)` | Count, sum, sum of squares | Denominator convention and defined domain |
| Inherited extension | Standard deviation: `stddev(x@I;ddof=d)` | Same-anchor variance family | Square root; does not confer variance self-continuation |
| Inherited extension | RMS: `rms(x@I)` | Second raw moment | Square root and applicable domain |
| Inherited extension | Central moments: `central_moment(x@I,k;convention=c)` | Raw sums through order \(k\) and count for the population convention | Convention, matched participation, definedness |
| Inherited extension | Skewness | Moments through order 3 or equivalent admitted basis | Finite-sample convention, nondegenerate domain |
| Inherited extension | Kurtosis | Moments through order 4 or equivalent admitted basis | Excess / finite-sample convention, nondegenerate domain |
| Inherited extension | Covariance: `covariance(x@I,y@I;ddof=d)` | Joint count, sums, cross-product sum | Same governed pair domain in every role |
| Inherited extension | Pearson correlation: `correlation(x@I,y@I;method=pearson)` | Joint co-moments through second order | Same pair domain; denominator and exceptional cases |
| Inherited extension | Quantile: `quantile(x@I,p;convention=q)` | Exact multiset or admitted exact-equivalent basis | Value order, probability level, interpolation convention |
| Inherited extension | Median | Alias of quantile at \(0.5\) under the same convention | No duplicate identity by mere spelling |
| Inherited extension | Percentile | Alias of quantile at \(p/100\) under the same convention | Parameter conversion preserves convention |
| Inherited extension | Geometric mean | Sum of logarithms and count | Positive domain; logarithm formed before reduction |
| Inherited extension | Harmonic mean | Reciprocal sum and count | Reciprocal and final-constructor domains |

# Source and section map

| Former location in Full Manuscript 0.3 | Location here |
|---|---|
| §11.6.1 | §S.1 |
| §11.6.2 | §S.2 |
| §11.6.3 | §S.3 |
| §11.6.4 | §S.4 |
| §11.6.5 | §S.5 |
| §11.6.6 | §S.6 |
| §11.6.7 | §S.7 |
| §11.6.8 | §S.8 |
| Appendix A, inherited-extension rows | §S.9 |

**[1]** Wang, Huayin. *The Theory of Data: A Foundation for Analytical Identity, Derivability, and Consistency*. Version 7.1, Full Manuscript Working Draft 0.3. Immediate textual source. Working Draft 0.4 remains the current foundation review target for this packet.

**[2]** Wang, Huayin. *The Theory of Data: A Foundation for Analytical Identity, Derivability, and Consistency*. Version 7.0, 3 September 2026. DOI: 10.5281/zenodo.22289091. The published predecessor identified by the supplied source. Its §6.2 is the inherited catalog; metadata is carried from that source, not newly verified here.
