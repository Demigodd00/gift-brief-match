# Source Policy

## Authoritative source collection

The source packet is deliberately limited to public preference text and proposer-declared gift details. No shopping site, private profile, or inferred characteristic is consulted.

Concretely, the validator evidence consists of: occasion, public preferences, public constraints, gift name, description, declared attributes, and an optional proposer revision.

## No autonomous retrieval

This contract performs no HTTP request, web search, URL rendering, oracle lookup, or hidden enrichment. A URL or source label inside user text remains untrusted text; validators are not asked to open it. This prevents mutable pages, blocked domains, and different search results from changing consensus.

## Collection responsibility

The deployer and participants must provide complete, lawfully usable, non-secret material. On-chain storage proves which bytes were considered after normalization; it does not prove authorship, completeness, ownership, or real-world truth.

## Normalization and limits

Text inputs normalize CRLF/CR to LF, trim surrounding whitespace, and enforce field-specific minimum and maximum lengths. Collection sizes are capped. Structured model output uses closed categories or fixed-order binary masks and fails closed on extra, missing, malformed, or out-of-range values.

## Prompt-injection boundary

Every evidence packet is serialized as sorted JSON and surrounded by named START/END delimiters. The prompt states that the packet is data, never instructions. A validator independently replays the assessment before any result is stored.

## Interpretation boundary

All proposal and preference text is public contract data. Declared attributes are not independently verified. Applications must show these limits next to results and use a fresh deployment when the underlying source set or policy changes.
