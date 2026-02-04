# Credit Scoring Model

Acme Corp's AI-powered credit risk assessment system.

## Overview

This system evaluates consumer loan applications (up to €50,000) using machine learning to predict repayment probability.

**EU AI Act Classification:** High Risk (Annex III, Category 5(b))

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run prediction
python src/model.py
```

## Compliance

This system requires EU AI Act compliance documentation. Initialize with:

```bash
annexci init
annexci scan
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.1.0 | 2026-01 | Added transaction_history feature |
| 2.0.0 | 2025-10 | Migrated to safetensors format |
| 1.0.0 | 2025-01 | Initial release |
