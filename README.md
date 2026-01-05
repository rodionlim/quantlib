# quantlib

[![PyPI version](https://badge.fury.io/py/quantlib-st.svg)](https://badge.fury.io/py/quantlib-st)
[![CI](https://github.com/rodionlim/quantlib-st/actions/workflows/ci.yml/badge.svg)](https://github.com/rodionlim/quantlib-st/actions/workflows/ci.yml)
[![GHCR](https://img.shields.io/badge/ghcr-quantlib--st-blue?logo=github)](https://github.com/rodionlim/quantlib-st/pkgs/container/quantlib-st)

Minimal, self-contained CLI tools and library for quantitative finance.

## Subcommands

- **[corr](src/correlation/README.md)**: Compute correlation matrices over time from returns.
- **[costs](src/src/costs/README.md)**: Calculate Sharpe Ratio (SR) costs for instruments based on spread and fees.

## Install (editable - for developers)

From the repo root:

- `cd quantlib`
- `python -m pip install -e .`

This installs the `quantlib` command.

## Build a single binary with PyInstaller

From `quantlib/`:

- `make build`

Binary will be at `dist/quantlib`.

## Docker

Pull a published image from GitHub Container Registry:

- `docker pull ghcr.io/rodionlim/quantlib-st:latest`

Run a quick correlation query by piping a CSV into the container (one-liner):

- `cat sample_data/returns_10x4.csv | docker run --rm -i ghcr.io/rodionlim/quantlib-st:latest corr --min-periods 3 --ew-lookback 10`

When publishing the image the Makefile also tags and pushes `:latest` in addition to the versioned tag.

## Package Sample Usage
