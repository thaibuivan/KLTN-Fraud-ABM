# Parameter Registry v0.2

The main methodological task is not to find one "true" number for every parameter. It is to separate parameters by evidential status and test robustness where exact identification is impossible.

| Parameter | Meaning | Initial source class | Role | Sensitivity priority |
|---|---|---|---|---|
| fraud prevalence | share of fraud transactions | empirical dataset | calibration/input | low-medium |
| amount distribution | transaction-value distribution | empirical dataset | calibration/input | low |
| temporal distribution | transaction timing pattern | empirical dataset | calibration/input | medium |
| customer transaction frequency | activity rate/history | empirical if identifiable | state/input | medium |
| risk threshold | action threshold | experiment | policy variable | high |
| queue discipline | FIFO / risk-priority / other | experiment | policy variable | high |
| analyst capacity | cases processed per period | literature/scenario | operational uncertainty | high |
| review time | time per case | literature/scenario | operational uncertainty | high |
| analyst accuracy | review correctness | literature/scenario | operational uncertainty | medium-high |
| fraudster learning rate alpha | adaptation speed | explicit behavioral assumption | behavioral uncertainty | high |
| exploration epsilon | probability of trying alternatives | explicit behavioral assumption | behavioral uncertainty | high |
| strategy-switch mechanism | adaptation rule | model design | structural uncertainty | high |
| block tolerance | repeated blocks before dormancy | explicit assumption | behavioral uncertainty | high |
| dormancy duration | inactive period after repeated blocks | explicit assumption | behavioral uncertainty | medium |
| review cost | analyst handling cost | literature/scenario | economic uncertainty | medium |
| false-positive cost | cost of unnecessary intervention | literature/scenario | economic uncertainty | high |
| friction cost | customer inconvenience/abandonment proxy | literature/scenario | economic uncertainty | high |

## Four parameter classes

### 1. Empirical parameters
Estimated directly where the dataset supports identification.

Examples: fraud prevalence, amount distribution, observable timing patterns.

### 2. Literature-informed operational parameters
Public evidence or plausible ranges.

Examples: analyst capacity, review time, analyst accuracy.

### 3. Policy parameters
Not estimated because they are intentionally manipulated.

Examples: risk thresholds, queue-priority rule, capacity-aware decision rule.

### 4. Uncertain behavioral assumptions
Not directly identified by transaction datasets.

Examples: fraudster learning rate, exploration rate, switching threshold and dormancy.

These must be reported transparently and stress-tested.

## Key methodological principle

Do not calibrate an unobservable behavioral mechanism as if it were directly observed. If the data do not identify a parameter, treat it as uncertain rather than inventing false precision.
