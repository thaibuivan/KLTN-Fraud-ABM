"""Interpretable adaptive-fraudster prototype.

This module is deliberately small and scenario-agnostic. It is not an empirical
claim about real fraudster cognition. Parameters such as learning rate,
exploration and dormancy are uncertain behavioral assumptions that must be
sensitivity-tested before thesis conclusions are drawn.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import math
import random
from typing import Dict, Iterable, Optional

RESPONSES = {"APPROVE", "CHALLENGE", "REVIEW", "BLOCK"}


@dataclass
class StrategyState:
    value: float = 0.0
    attempts: int = 0
    successes: int = 0

    @property
    def success_rate(self) -> float:
        return self.successes / self.attempts if self.attempts else 0.0


@dataclass
class AdaptiveFraudster:
    strategies: Iterable[str]
    learning_rate: float = 0.2
    epsilon: float = 0.1
    challenge_penalty: float = 0.30
    review_penalty: float = 0.15
    block_penalty: float = 1.0
    consecutive_block_limit: int = 3
    dormancy_steps: int = 2
    seed: Optional[int] = None

    states: Dict[str, StrategyState] = field(init=False)
    current_strategy: str = field(init=False)
    consecutive_blocks: int = field(default=0, init=False)
    dormant_until: int = field(default=0, init=False)

    def __post_init__(self) -> None:
        strategies = list(self.strategies)
        if not strategies:
            raise ValueError("At least one strategy is required.")
        if not 0 < self.learning_rate <= 1:
            raise ValueError("learning_rate must be in (0, 1].")
        if not 0 <= self.epsilon <= 1:
            raise ValueError("epsilon must be in [0, 1].")

        self._rng = random.Random(self.seed)
        self.states = {name: StrategyState() for name in strategies}
        self.current_strategy = strategies[0]

    def is_dormant(self, step: int) -> bool:
        return step < self.dormant_until

    def choose_strategy(self, step: int) -> Optional[str]:
        """Choose a strategy with epsilon-greedy exploration."""
        if self.is_dormant(step):
            return None

        if self._rng.random() < self.epsilon:
            self.current_strategy = self._rng.choice(list(self.states))
            return self.current_strategy

        best_value = max(state.value for state in self.states.values())
        candidates = [
            name
            for name, state in self.states.items()
            if math.isclose(state.value, best_value)
        ]
        self.current_strategy = self._rng.choice(candidates)
        return self.current_strategy

    def observe(self, response: str, amount: float, step: int) -> float:
        """Update the selected strategy value after observing system feedback."""
        if response not in RESPONSES:
            raise ValueError(f"Unknown response: {response}")
        if amount < 0:
            raise ValueError("amount must be non-negative")

        state = self.states[self.current_strategy]
        state.attempts += 1

        if response == "APPROVE":
            reward = float(amount)
            state.successes += 1
            self.consecutive_blocks = 0
        elif response == "CHALLENGE":
            reward = -self.challenge_penalty * float(amount)
            self.consecutive_blocks = 0
        elif response == "REVIEW":
            reward = -self.review_penalty * float(amount)
            self.consecutive_blocks = 0
        else:
            reward = -self.block_penalty * float(amount)
            self.consecutive_blocks += 1
            if self.consecutive_blocks >= self.consecutive_block_limit:
                self.dormant_until = step + 1 + self.dormancy_steps
                self.consecutive_blocks = 0

        state.value += self.learning_rate * (reward - state.value)
        return reward


@dataclass
class StaticFraudster(AdaptiveFraudster):
    """Comparator that always uses one fixed strategy."""

    fixed_strategy: Optional[str] = None

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.fixed_strategy is not None:
            if self.fixed_strategy not in self.states:
                raise ValueError("fixed_strategy must be one of strategies")
            self.current_strategy = self.fixed_strategy

    def choose_strategy(self, step: int) -> Optional[str]:
        if self.is_dormant(step):
            return None
        return self.current_strategy
