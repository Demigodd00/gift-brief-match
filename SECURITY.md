# Security

## Scope

This repository is a bounded Intelligent Contract, its direct and five-validator tests, and an opt-in StudioNet smoke test. It has no frontend, backend, database, token, payout, upgrade proxy, or privileged secret.

## Trust model

The prompt forbids private-trait inference, output categories are closed, and final recipient choice remains an authenticated deterministic action.

The organizer freezes the public brief and controls the shortlist; each address proposes once; only the named recipient makes the final selection.

## Implemented controls

- Concrete immutable GenVM runner hash; no floating `latest` dependency.
- Address normalization, explicit role separation, one-time actions, collection caps, and lifecycle locks.
- Bounded text and strict model-response schemas with `[EXPECTED]` versus `[LLM_ERROR]` failure classes.
- Sorted, delimited untrusted evidence packets and independent validator replay.
- All storage is read before entering nondeterministic callbacks; the final static audit found zero `self`/storage reads inside consensus callbacks.
- No cross-contract calls, fund custody, transfer, automatic purchase, deletion, or off-chain webhook.
- `.env`, caches, artifacts, wallet files, and local deployment material are ignored. Live wallets are encrypted and stored outside the workspace.

## Contract-specific safety properties

- Only an assessed FIT proposal can enter the organizer's shortlist.
- A proposer can revise a flagged proposal once before shortlisting starts.
- The organizer cannot choose for the recipient and the contract cannot buy the item.

## Residual risks

- All proposal and preference text is public contract data.
- Declared attributes are not independently verified.
- The result is a planning aid, not a safety, suitability, or purchase guarantee.

This contract should not be used to make legal, medical, financial, employment, admission, or physical-safety decisions unless its own policy explicitly supports that domain and an independent professional review is added. This version does not.

## Reporting

Report a vulnerability privately to the repository owner with the contract name, affected method, reproduction, expected invariant, and impact. Do not include private keys or personal data. The owner should reproduce it in a fresh disposable deployment before publishing details.
