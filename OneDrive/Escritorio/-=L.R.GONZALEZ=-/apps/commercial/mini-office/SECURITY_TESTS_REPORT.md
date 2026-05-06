# Security And Test Report

Status: local review.

## Current Evidence

- Functional tests: `python -m pytest -q`
- Runtime smoke: `python mini_office.py --status`
- Secret scan: workspace release scanner against `apps/commercial/mini-office`

## Current Boundary

The local smoke path does not require external services. Public sale and public
repository release remain blocked by legal, packaging, support, privacy, refund,
and clean-machine QA gates.
