import pandas as pd

from scripts.build_xente_features import build_features
from scripts.xente_online_features import (
    XenteOnlineFeatureBuilder,
)


def sample_raw():
    return pd.DataFrame(
        [
            {
                "TransactionId": "T1",
                "CustomerId": "C1",
                "Amount": 100.0,
                "Value": 100.0,
                "TransactionStartTime": "2026-01-01T00:00:00Z",
                "ProductCategory": "A",
                "ChannelId": "C",
                "ProviderId": "P",
                "ProductId": "X",
                "PricingStrategy": 1,
                "FraudResult": 0,
            },
            {
                "TransactionId": "T2",
                "CustomerId": "C1",
                "Amount": 200.0,
                "Value": 200.0,
                "TransactionStartTime": "2026-01-01T00:30:00Z",
                "ProductCategory": "A",
                "ChannelId": "C",
                "ProviderId": "P",
                "ProductId": "X",
                "PricingStrategy": 1,
                "FraudResult": 1,
            },
        ]
    )


def test_online_features_match_batch_features():
    raw = sample_raw()
    batch = build_features(raw)

    builder = XenteOnlineFeatureBuilder()
    online = pd.DataFrame(
        [
            builder.transform_and_update(
                row
            )
            for row in raw.assign(
                TransactionStartTime=pd.to_datetime(
                    raw["TransactionStartTime"],
                    utc=True,
                )
            )
            .sort_values(
                [
                    "TransactionStartTime",
                    "TransactionId",
                ]
            )
            .to_dict("records")
        ]
    )

    columns = [
        "prior_tx_count",
        "prior_value_mean",
        "prior_value_std",
        "gap_minutes",
        "tx_count_1h",
        "tx_count_24h",
        "tx_count_7d",
        "value_ratio_prior_mean",
        "prior_product_share",
        "prior_channel_share",
        "log_value",
        "is_credit",
        "hour",
        "weekday",
        "log_prior_tx_count",
        "log_prior_value_mean",
        "log_prior_value_std",
        "log_gap_minutes",
        "log_tx_count_1h",
        "log_tx_count_24h",
        "log_tx_count_7d",
        "value_ratio_clip",
    ]

    pd.testing.assert_frame_equal(
        batch[columns].reset_index(drop=True),
        online[columns].reset_index(drop=True),
        check_dtype=False,
    )
