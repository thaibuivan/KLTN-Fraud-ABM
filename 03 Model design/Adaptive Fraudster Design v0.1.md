# Adaptive Fraudster Design v0.1

## Purpose

The adaptive fraudster is a **stress mechanism for policy testing**, not the final research objective.

The fraudster observes system feedback and updates strategy preferences over time.

## State

Possible state variables:

- current strategy;
- strategy value estimates;
- recent success rate;
- number of consecutive blocks;
- recent system responses;
- optional dormancy counter.

## Actions

Abstract strategy set for the first prototype:

- low-amount / threshold-avoidance behavior;
- high-amount behavior;
- timing-shift behavior;
- identity/card switching behavior.

Scenario-specific strategies should only be added when supported by public evidence or clearly labelled as assumptions.

## Observations

System response:

- APPROVE;
- CHALLENGE / STEP-UP;
- REVIEW;
- BLOCK.

## Reward

A simple interpretable form:

```text
APPROVE fraud  -> positive reward proportional to successful amount
CHALLENGE      -> negative reward
REVIEW         -> small/moderate negative reward
BLOCK          -> larger negative reward
```

## Learning rule

First implementation should remain interpretable:

```math
V_s^{new} = V_s^{old} + \alpha(r_t - V_s^{old})
```

where:
- `V_s` is the estimated value of strategy `s`;
- `r_t` is observed reward;
- `alpha` is the learning rate.

Strategy selection can use epsilon-greedy exploration.

Deep RL is not required for the minimum viable thesis model.

## Dormancy mechanism

If the fraudster is blocked repeatedly, it may become dormant for a small number of simulation steps before returning.

This is a behavioral assumption unless independently grounded.

## Parameter status

Parameters such as learning rate, exploration rate, block tolerance and dormancy duration are **not automatically identifiable from IEEE-CIS or Xente**.

They should be:
- documented as behavioral assumptions;
- varied over plausible ranges;
- included in sensitivity analysis.

## Static comparator

The static-fraudster baseline uses a fixed strategy and does not update strategy values.

Experiment 1 compares static and adaptive behavior under otherwise identical conditions.
