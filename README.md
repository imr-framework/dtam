<div align="center">

# DTAM

![Python](https://img.shields.io/badge/python-v3.10+-blue.svg)
![Google ADK](https://img.shields.io/badge/Google%20ADK-Latest-green.svg)
![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-blue.svg)
![Development Status](https://img.shields.io/badge/status-Alpha-yellow.svg)

</div>

**Digital Twin Architecture for MRI** — physics-informed, agentic infrastructure for MRI digital twins.

Full documentation lives in [`docs/`](docs/) (preview with `make docs-serve`). This README covers how to run the project locally.

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)

## Install

```bash
uv sync --all-groups
```

For agent / Gemini calls, set a Google API key in the repo-root `.env` (see `src/dtam/agents/.env.example`):

```bash
GOOGLE_API_KEY=your-key-here
```

## Smoke test

```bash
uv run dtam
```

Example output:

```text
DTAM ready scanner=simulated_scanner mode=simulation sensors=3 measurements=3 ...
```

Or from Python:

```python
from dtam import bootstrap

app = bootstrap(scanner_id="simulated_scanner", environment="testing")
batch = app.adapter.read_measurements()
print(app.adapter.scanner_id, len(batch.measurements), batch.correlation_id)
```

## Servers

```bash
make twin-api     # Twin REST API → http://127.0.0.1:8080
make agents-api   # ADK agent API (GUI chat) → :8001
make web          # ADK web UI → :8001
make api          # ADK api_server (default port)
```

Details: [Twin HTTP API](docs/platform/twin-api.md), [Getting started](docs/start/index.md).

## Tests and checks

```bash
uv run pytest tests/unit tests/integration/test_foundation_bootstrap.py -q
make test         # full pytest suite
make lint
make typecheck
make check        # lint + typecheck + test
```

## Docs site

```bash
make docs-serve   # local preview
make docs         # strict build → site/
```

## Optional extras

```bash
# Thermal PINN training (see docs/digital_twin/thermal-pinn.md)
uv sync --extra pinn
uv run --extra pinn python -m dtam.digital_twin.models.thermal.pinn.train \
  --epochs 200 --out data/models/pinn

# Vendor HalbachMRIDesigner for magnet design CLI (see THIRD_PARTY.md)
make vendor-halbach
```

## Links

- Docs: [`docs/`](docs/) · Site config: `zensical.toml`
- Repository: https://github.com/LeoMcBills/dtam
- License: [`LICENSE`](LICENSE) · Third-party: [`THIRD_PARTY.md`](THIRD_PARTY.md)
