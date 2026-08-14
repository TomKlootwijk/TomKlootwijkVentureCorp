# Equimolarity: molecular-weight programming, not a cipher

## Why the wording is central

The phrase "substantially equimolar" is not decorative patent language. In a linear step-growth reaction between a difunctional dihydroxy compound and a difunctional diepoxide, high chain length is possible only when:

- the two complementary functional groups are very close to equivalent;
- conversion is very high;
- water, alcohols and monofunctional impurities do not consume functions; and
- the growing polymer remains mobile enough for end groups to find each other.

The patent defines a dihydroxy:diepoxy molar ratio of about 1.04 to 0.98, preferably 1.02 to 0.99. Because each ideal molecule has two relevant functions, molecular ratio and functional-group equivalent ratio coincide.

## Carothers-Flory relation

Let `r` be the ratio of the smaller initial number of functional groups to the larger, so `0 < r <= 1`, and let `p` be the conversion of the limiting functions. The ideal number-average degree of polymerization is:

`Xn = (1 + r) / (1 + r - 2 r p)`

At complete conversion of the limiting group:

`Xn,max = (1 + r) / (1 - r)`

The result is nonlinear. A seemingly small analytical or weighing error can impose a hard ceiling on chain length.

| Dihydroxy:diepoxy feed | r used in equation | Ideal Xn ceiling at p = 1 |
|---:|---:|---:|
| 1.040:1 | 0.9615 | 51 |
| 1.020:1 | 0.9804 | 101 |
| 1.010:1 | 0.9901 | 201 |
| 1.000:1 | 1.0000 | unbounded in the ideal model |
| 0.990:1 | 0.9900 | 199 |
| 0.980:1 | 0.9800 | 99 |
| 0.970:1 | 0.9700 | 65.7 |

Even exact stoichiometry is not enough. At `r = 1`, `Xn = 1/(1-p)`, so 99% conversion gives Xn about 100, 99.5% gives 200, and 99.9% gives 1,000. This is why the solvent and solubility claims are inseparable from the equimolar claim: the reaction must remain homogeneous long enough to drive the final fractions of a percent of conversion.

## Re-reading Example 1

The easy but incomplete reading is 0.97 mol BPS versus 1.00 mol DGE-BPS. The patent expressly says to include BPS present as salt. Adding 0.05 mol monosodium BPS gives an effective BPS-derived total of 1.02 mol. That is exactly the upper edge of the preferred range.

Under the ideal model, a 1.02:1 feed gives an Xn ceiling of about 101 monomer molecules. In a symmetric BPS/DGE-BPS system, that is on the order of 50 alternating feed pairs. A rough mass estimate based on the two-monomer pair is in the tens of kilodaltons, consistent with the later industry's description of these materials as high-molecular-weight epoxy or phenoxy resins. This estimate is illustrative only: the patent reports intrinsic viscosity, not absolute molar mass, and branching, cyclic material and end-group chemistry alter the mapping.

## Why a slight deliberate imbalance can be useful

A perfectly balanced polymer can retain two different reactive end groups and continue changing during hot processing. A controlled small excess can:

- cap both chain ends predominantly with the excess function;
- set a reproducible molecular-weight ceiling;
- reduce residual epoxide when phenol is in excess;
- stabilize the product against uncontrolled post-polymerization; and
- provide defined hydroxyl-rich end chemistry.

Example 4 makes this strategy explicit. After rapid polymerization at 150 C, about 2.5 g BPS (approximately 0.010 mol) is added to stop further growth. It is an end-group intervention, not merely a quench by cooling.

## Why purity and dryness are stoichiometry controls

Every reactive impurity perturbs effective `r` or prevents `p` from approaching unity. Water and alcohol are especially damaging because they can be monofunctional chain terminators. A few mole percent of functionality loss is enough to cut the ideal degree of polymerization by an order of magnitude.

This is why the patent specifies:

- very low water content;
- anhydrous catalyst introduction;
- high-melting, purified p,p'-BPS;
- low o,p'-isomer content;
- low chloride in DGE-BPS; and
- a solvent that neither reacts with phenol nor epoxide.

A later high-molecular-weight BPS epoxy patent repeats the same design logic using an epoxy:phenolic-OH equivalent ratio of 1:0.94-1.06, high 4,4'-BPS purity and low hydrolyzable chlorine. A conventional polysulfone patent likewise states that a deviation as small as 5% from equal molar amounts seriously reduces molecular weight. These later documents independently confirm that the original ratio language describes ordinary but critical polymer physics, not coded chemistry.
