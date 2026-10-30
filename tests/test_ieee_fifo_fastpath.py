import pandas as pd

from scripts.policy_queue_engine import PolicyQueueEngine
from scripts.fraud_policies import Action


class AlwaysReview:
    def decide(self, context):
        return Action.REVIEW


def event(i, hour):
    return {
        "TransactionId": i,
        "TransactionStartTime": pd.Timestamp("2025-01-01T00:00Z") + pd.Timedelta(hours=hour),
        "Value": 1.0,
        "FraudResult": 0,
        "risk_probability": 0.5,
    }


def test_monotonic_fifo_fastpath_and_busy_server_shortcut():
    x = PolicyQueueEngine(AlwaysReview(), pooled_service_rate_per_hour=0.1)
    for i, hour in enumerate([0.0, 0.1, 0.2, 0.3]):
        x.process_event(event(i, hour))
    assert x._fifo_monotonic
    assert x._choose_queue_index() == 0
    old = x.queue.copy()
    x.drain_until(pd.Timestamp("2025-01-01T00:12Z"))
    assert x.queue == old


def test_out_of_order_arrivals_use_exact_sorted_fifo_fallback():
    x = PolicyQueueEngine(AlwaysReview(), pooled_service_rate_per_hour=0.1)
    for i, hour in enumerate([0.0, 3.0, 2.0]):
        x.process_event(event(i, hour))
    assert not x._fifo_monotonic
    assert x.queue[x._choose_queue_index()]["TransactionId"] == 2
