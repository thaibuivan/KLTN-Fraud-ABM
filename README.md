# KLTN — Fraud Policy Simulation / ABM

Research workspace for an undergraduate thesis on **transaction-fraud policy experimentation under limited review capacity and uncertainty**.

The project develops an earlier pilot, `FinRisk-ABM-Policy-Simulation`, into a more defensible empirical simulation using:
- Xente Fraud Detection as the primary transaction stream;
- leakage-safe customer-history features;
- an interpretable fraud-risk baseline;
- a persistent event-driven alert queue;
- FIFO vs risk-priority review rules;
- capacity/load stress tests;
- temporal, model-structure and stochastic robustness checks.

## Research focus

The thesis is not a classifier leaderboard study.

Core question:

> How do alert thresholds, review capacity and queue-priority rules interact to change fraud capture, backlog and waiting-time trade-offs?

The current methodological label is intentionally conservative:
**dynamic fraud-policy simulation with agent-based/stateful components**.

Whether the final thesis uses the stricter “ABM” label will depend on supervisor feedback and the final frozen mechanism set.

## Current architecture

```text
Xente transaction stream
        ↓
past-only customer state/features
        ↓
risk engine
        ↓
alert policy / threshold
        ↓
persistent alert queue
        ↓
pooled review capacity
        ↓
FIFO or risk-priority service
        ↓
fraud capture / FP / backlog / waiting
```

## Primary data

Primary dataset:
**Xente Fraud Detection Challenge**.

Raw competition files are intentionally **not committed**.

Local layout:

```text
data/
└── raw/
    └── xente/
        └── training.csv
```

`data/raw/` and row-level derived files are gitignored.

## Setup

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
```

## Reproduce the current baseline

### 1. Profile Xente

```bash
python scripts/profile_xente.py \
  --input data/raw/xente/training.csv
```

### 2. Build past-only features

```bash
python scripts/build_xente_features.py \
  --input data/raw/xente/training.csv \
  --output data/interim/xente_features.csv
```

### 3. Train chronological logistic baseline

```bash
python scripts/train_xente_baseline.py \
  --input data/interim/xente_features.csv \
  --output-dir outputs/local/xente_baseline
```

### 4. Run persistent queue baseline

```bash
python scripts/simulate_alert_queue.py \
  --validation-scores outputs/local/xente_baseline/validation_scores.csv \
  --test-scores outputs/local/xente_baseline/test_scores.csv \
  --target-alert-rate 0.01 \
  --capacity-ratios 0.75,1.0,1.25
```

### 5. Run model-structure robustness

```bash
python scripts/run_xente_model_robustness.py \
  --input data/interim/xente_features.csv
```

### 6. Run temporal robustness

```bash
python scripts/run_xente_temporal_robustness.py \
  --input data/interim/xente_features.csv
```

### 7. Run fixed-staffing threshold sensitivity

```bash
python scripts/run_alert_rate_sensitivity.py \
  --validation-scores outputs/local/xente_baseline/validation_scores.csv \
  --test-scores outputs/local/xente_baseline/test_scores.csv \
  --alert-rates 0.005,0.01,0.02,0.05 \
  --reference-alert-rate 0.01 \
  --capacity-ratios 0.75,1.0,1.25
```

### 8. Run variable team-capacity sensitivity

```bash
python scripts/run_variable_capacity_sensitivity.py \
  --validation-scores outputs/local/xente_baseline/validation_scores.csv \
  --test-scores outputs/local/xente_baseline/test_scores.csv \
  --target-alert-rate 0.01 \
  --reference-alert-rate 0.01 \
  --requested-capacity-ratio 1.0 \
  --team-capacity-cvs 0,0.3,0.6 \
  --seeds 100
```

### 9. Verification

```bash
pytest -q
```

## Current design notes

Start here:
- `00 Dashboard/KLTN Dashboard.md`
- `03 Model design/Candidate Core Specification v0.3.md`
- `03 Model design/Core Experiment Grid v0.1.md`
- `03 Model design/Validation Plan v0.1.md`
- `03 Model design/Evidence Parameter Matrix.md`

Current experiment notes:
- `05 Experiments/Xente Queue Pilot v0.1.md`
- `05 Experiments/Xente Robustness Pack v0.1.md`
- `05 Experiments/Xente Alert-rate and Starvation Sensitivity v0.1.md`
- `05 Experiments/Xente Variable Team Capacity Sensitivity v0.1.md`

## Current claim boundary

The repository may support conditional statements such as:

> Under the evaluated Xente event streams and capacity/model structures, alert thresholds and queue disciplines change the allocation of scarce review capacity and create trade-offs among fraud capture, backlog and waiting-time distribution.

It does **not** establish:
- a production threshold for a bank;
- a staffing level for a Vietnamese bank;
- a universal best fraud policy;
- realistic bank SLA waiting times;
- exact analyst accuracy or fraud-recovery rates.

## Legacy project

The earlier `FinRisk-ABM-Policy-Simulation` repository is kept as a pilot/archive.

Useful logic is migrated selectively; legacy assumptions are not treated as thesis evidence unless re-grounded.

## Git workflow

- `main`: accepted version.
- `chatgpt-draft`: working changes prepared for review.

Recommended:
1. review the draft PR;
2. merge only after methodology/scope decisions are accepted;
3. pull to the local Obsidian vault.

## Data and security

Do not commit:
- Xente raw competition files;
- row-level restricted datasets;
- API keys/tokens;
- employer/confidential data;
- proprietary bank information.
