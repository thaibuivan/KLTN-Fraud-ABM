# Candidate Core Specification v0.3

## Status
**Candidate freeze — pending GVHD + practitioner validation.**

## Research purpose
Evaluate how fraud alert thresholds, limited review capacity and queue-priority rules interact to produce system-level trade-offs that are not visible from classifier metrics alone.

## Main research question
> How do alternative transaction-fraud alert and review policies perform under limited and uncertain operational capacity when evaluated on a dynamic empirical transaction stream?

## Sub-questions
1. How does analyst/review capacity affect fraud capture, backlog and waiting time?
2. How does changing the alert threshold alter workload and overload under fixed staffing?
3. Does risk-based queue prioritization improve fraud review under congestion, and what waiting-time/starvation cost does it create?
4. Are these conclusions robust to weaker score models, temporal variation and operational stochasticity?

## Empirical environment
Primary dataset:
- Xente Fraud Detection.

Stateful entity:
- CustomerId.

Data mode:
- chronological observed-event replay.

## Risk engine
Primary:
- regularized logistic regression with past-only customer history + transaction context.

Structural robustness:
- logistic specification without current Value signal.

The risk engine is an input to the policy simulator, not the thesis contribution.

## Operational model
Event-driven persistent alert queue.

Core state:
- alert arrival;
- score;
- queue position/priority;
- service start/end;
- waiting time;
- backlog.

Core queue rules:
- FIFO;
- risk-priority.

## Capacity
No claim of bank-specific analysts/day.

Two experiment modes:
1. relative capacity stress for one fixed alert policy;
2. fixed absolute pooled capacity when comparing thresholds.

Uncertainty:
- per-case service-time variation;
- day-level pooled-team capacity variation.

## Core outcomes
- fraud capture;
- false-positive reviews;
- alert volume;
- backlog;
- mean/P95/P99 waiting;
- >24/48/72h wait shares;
- low/high-priority tail waiting;
- cold-start subgroup outcomes.

## Explicit non-core items
- exact adaptive fraudster cognition;
- LLM analyst;
- bank-specific digital twin;
- individual analyst accuracy unless evidence improves;
- monetary net benefit as a primary conclusion.

## Current contribution candidate
> The thesis embeds an empirical fraud-risk score stream within a persistent operational review queue and demonstrates how threshold choice, capacity scarcity/variability and queue prioritization jointly change fraud-capture, backlog and service-delay trade-offs.

## Claim boundary
The thesis may conclude:
> a mechanism/policy performs differently across the evaluated Xente-based scenarios.

It may not conclude:
> a named bank should deploy a specific threshold or staffing level.

## Methodological identity
Preferred wording until GVHD decides:
**dynamic fraud-policy simulation with agent-based/stateful components**.

If GVHD accepts the ABM framing, justify it through:
- persistent customer state;
- persistent queue state;
- heterogeneous/uncertain service capacity;
- interaction between policy, arrival load, backlog and future service outcome.

If the committee prefers a stricter ABM definition, use:
**dynamic/discrete-event policy simulation**.

The scientific result does not depend on forcing the ABM label.
