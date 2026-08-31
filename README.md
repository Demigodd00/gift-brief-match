# Gift Brief Match

Matches public gift proposals to a recipient's explicit preference brief and constraints, then leaves the shortlist and final choice with humans.

## Why it is an Intelligent Contract

Validators independently bind a four-dimension fit mask covering occasion, preferences, hard constraints, and maintenance. The contract stores that intermediate record and deterministically derives FIT, RISKY, or NO_FIT; a failed hard constraint always yields NO_FIT. The derived result controls revision and shortlist eligibility while the recipient retains the final choice.

## Reusable deployment model

Deploy once per recipient and occasion. Up to ten proposers can participate, and the contract source can be redeployed for any new brief.

One completed deployment is an auditable record and is not reset or silently repurposed. Reuse means deploying the same reviewed source with new constructor data.

## Roles and workflow

The organizer freezes the public brief and controls the shortlist; each address proposes once; only the named recipient makes the final selection.

State path: `COLLECTING → MATCHING ↔ SHORTLISTING → COMPLETE`

## Evidence boundary

Occasion, public preferences, public constraints, gift name, description, declared attributes, and an optional proposer revision.

The source packet is deliberately limited to public preference text and proposer-declared gift details. No shopping site, private profile, or inferred characteristic is consulted.

## Core invariants

- Only an assessed FIT proposal can enter the organizer's shortlist.
- Every assessment stores the four-dimension mask; the model never supplies the final fit category.
- A proposer can revise a flagged proposal once before shortlisting starts.
- The organizer cannot choose for the recipient and the contract cannot buy the item.

## Public interface

Write methods: `assess_gift, choose_gift, lock_proposals, propose_gift, revise_gift, shortlist_gift`

View methods: `get_policy, get_proposal, get_state`

`get_policy` exposes the machine-readable operating boundary and confirms that this contract never custodies funds.

## Verification

Pinned GenVM runner: `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`

```powershell
python -m pip install -r requirements.txt
genvm-lint check contracts/gift_brief_match.py
genvm-lint typecheck contracts/gift_brief_match.py
pytest tests/direct -q
python tests/run_glsim.py --port 4000 --validators 5 --no-browser
gltest tests/integration/test_glsim_consensus.py --network localnet -q
```

The StudioNet smoke test is opt-in and requires three disposable owner-specific test accounts. It reads state using `LATEST_FINAL` and asserts successful finalized execution.

## Previous StudioNet deployment (superseded)

These links and the recorded source hash refer to the earlier category-only implementation. Redeploy the structured-mask version and replace this section before submission.

- Contract: https://explorer-studio.genlayer.com/address/0xeC3Ec1C92B98e3f6231b5298EBF58A758584a2A5
- Studio import: https://studio.genlayer.com/?import-contract=0xeC3Ec1C92B98e3f6231b5298EBF58A758584a2A5
- Deployment transaction: https://explorer-studio.genlayer.com/tx/0x70151c27ca0f8703a7307cee66c7adbdafdfed564bdba8d866583bae07b607cd
- Intelligent transaction: https://explorer-studio.genlayer.com/tx/0xf29aa8c730e9d402ae6d4bdb6102920b70674f1f979edf91c3479fa77c44fa42
- Observed legacy final-state sample: `"FIT"`
- Audited source SHA-256: `32cc5cc101ead8db46de540baeada5ec1fa1503e2e1d881953b4e22078dcd400`

## Limitations

- All proposal and preference text is public contract data.
- Declared attributes are not independently verified.
- The result is a planning aid, not a safety, suitability, or purchase guarantee.

## Repository map

- `contracts/gift_brief_match.py` — Intelligent Contract source
- `tests/direct` — fast leader/validator and lifecycle tests
- `tests/integration/test_glsim_consensus.py` — five-validator simulator flow
- `tests/integration/test_studionet_smoke.py` — live opt-in proof
- `deployments/studionet.json` — source-bound public deployment evidence
- `ARCHITECTURE.md`, `SOURCE_POLICY.md`, `SECURITY.md`, `AUDIT.md` — review material

License: MIT.
