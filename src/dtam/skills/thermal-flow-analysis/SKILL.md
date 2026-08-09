---
name: thermal-flow-analysis
description: Analyze thermal gradients and forecast simple thermal mixing dynamics.
---

# Thermal flow analysis

## Steps
1. Gather channel values (`read_temperature_channels` or prior state).
2. Call `analyze_thermal_gradient`.
3. Call `simulate_thermal_flow` for short-horizon advisory forecasts.
4. Relate thermal drift to possible B0/frequency impact qualitatively.
