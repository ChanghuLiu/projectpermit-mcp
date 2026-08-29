# Address-Premium Sampling Boundary — 2026-08-29

## Purpose

`docs/ADDRESS_AWARE_VALUE_AUDIT.md` shows that current adapter-derived property context can change permit routing only in a subset of jurisdictions/rules, especially Ottawa/Gatineau heritage/PIIA-sensitive exemption paths.

A 2026-08-29 research attempt tested whether Ottawa's public issued-permit dataset could estimate the real-world incidence of address/property-context value.

The route was closed because the sampling frame is structurally biased for that question.

## Why issued permits are the wrong denominator

Ottawa's current heritage overlay affects ProjectPermit primarily when the scope would otherwise be:

- `LIKELY_NOT_REQUIRED`; or
- `MUNICIPAL_CONFIRMATION_REQUIRED`.

For example, same-size window replacement can move from `LIKELY_NOT_REQUIRED` to `ADDITIONAL_REVIEW_REQUIRED` when the property is heritage-designated / inside the relevant heritage overlay.

By contrast, a structural addition, structural alteration or non-exempt plumbing change is already permit-positive before heritage context is considered. Heritage may add another review requirement without changing the overall permit routing.

An **issued building permit dataset** is conditioned on projects that entered the permit process. It therefore systematically omits many ordinary permit-exempt scopes — exactly the population in which address/heritage context may create the most important routing flip.

Consequently:

> `heritage/address flips among issued permits` is **not** a defensible estimate of `address/property context changes among all candidate preflights`.

The former can materially understate the latter.

## Closed research attempt

PR #72 created a read-only source probe for Ottawa's official 2026 permit item. The probe itself emitted only public item metadata/resources and no permit rows.

The PR was intentionally closed without merge after the sampling-bias review. The problem was not lack of public data; it was the wrong denominator for the commercial question.

Do not reopen this route merely because a cleaner FeatureServer, monthly file or easier download becomes available.

## What would be valid

The address-premium incidence metric still requires a representative **upstream** sample where projects are observed before knowing whether a permit will be required.

A useful sample should include, for chronological/current-family cases:

1. original scope facts available at intake/quote time;
2. municipality/address when naturally available;
3. scope-only ProjectPermit routing;
4. derived property context when resolvable;
5. address-aware routing;
6. whether the property context materially changed the safe next step;
7. actual workflow/permit outcome when available.

The commercial metric remains:

`cases where derived property/address context materially changes safe routing / all representative candidate preflights`

not:

`heritage properties / issued permits`.

## Decision impact

**No score change.** Canonical remains **48/100 — PAUSE / RE-SCOPE**.

This closes another tempting but invalid public-data shortcut. The address-aware premium remains unproven and still needs representative upstream E3/operator evidence. Do not add new GIS/property rules merely to increase the synthetic flip rate.