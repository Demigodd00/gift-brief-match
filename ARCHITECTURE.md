# Architecture

## Deployment boundary

Deploy once per recipient and occasion. Up to ten proposers can participate, and the contract source can be redeployed for any new brief.

The constructor establishes the deployment's subject and policy. Later calls add only the bounded records allowed by the state machine; a completed instance cannot be reopened.

## Participants

The organizer freezes the public brief and controls the shortlist; each address proposes once; only the named recipient makes the final selection.

Addresses are normalized before authorization comparisons. Role checks and phase gates execute before any semantic assessment.

## State machine

`COLLECTING → MATCHING ↔ SHORTLISTING → COMPLETE`

The phase value is the primary lifecycle lock. Every write either advances that path, performs a documented single-use loop, or fails with an `[EXPECTED]` user error.

## Evidence assembly

Occasion, public preferences, public constraints, gift name, description, declared attributes, and an optional proposer revision.

Before consensus, the contract normalizes bounded text, reads all required storage, constructs a sorted JSON packet, and places it between explicit data delimiters. The nested nondeterministic callbacks use captured plain values and do not read contract storage.

## Consensus boundary

Return FIT, RISKY, or NO_FIT from declared proposal details and a bounded concern note. Validator consensus binds only the stable fit category.

The leader callback validates JSON shape, field types, closed categories, masks, and length bounds. A validator reruns the same semantic operation and rejects disagreement. Where an explanatory label can vary harmlessly, consensus binds the stable decision field while still checking that the leader's advisory text is well formed.

## Deterministic boundary

Identity gates, single proposal/revision limits, shortlist membership, and recipient selection are deterministic and cannot be delegated to the model.

Important invariants:

- Only an assessed FIT proposal can enter the organizer's shortlist.
- A proposer can revise a flagged proposal once before shortlisting starts.
- The organizer cannot choose for the recipient and the contract cannot buy the item.

No method sends value, pays rewards, escrows assets, deletes external data, or calls another contract.

## Failure model

- Invalid caller input or lifecycle use raises `[EXPECTED]` and leaves state unchanged.
- Malformed or out-of-policy model output raises `[LLM_ERROR]` and leaves the record assessable.
- Validator disagreement cannot commit an assessment.
- StudioNet proof reads explicitly target `LATEST_FINAL`, avoiding stale pre-final state.
