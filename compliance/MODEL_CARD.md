# Model Card: Credit Scoring Model v2.1.0

## Model Details

| Attribute | Value |
|-----------|-------|
| Model Name | Credit Scoring Model |
| Version | 2.1.0 |
| Model Type | Gradient Boosting Classifier (XGBoost) |
| Framework | XGBoost 2.0.3, Python 3.11 |
| Last Trained | 2026-01-20 |

## Intended Use

### Primary Use Case
Automated credit risk assessment for consumer loan applications up to €50,000.

### Intended Users
- Acme Corp credit analysts
- Automated decisioning system (for applications < €10,000)

### Out-of-Scope Uses
- Business lending decisions
- Applications > €50,000 (requires human review)
- Mortgage underwriting
- Any use outside EU jurisdiction

## Performance Metrics

### Overall Performance

| Metric | Value | Threshold |
|--------|-------|-----------|
| AUC-ROC | 0.847 | > 0.80 |
| Precision | 0.823 | > 0.75 |
| Recall | 0.791 | > 0.70 |
| F1 Score | 0.807 | > 0.75 |

### Performance by Segment

| Segment | AUC-ROC | Sample Size |
|---------|---------|-------------|
| Prime (700+) | 0.891 | 1,423,891 |
| Near-Prime (650-699) | 0.834 | 847,291 |
| Subprime (<650) | 0.812 | 576,210 |

## Limitations

### Known Limitations
1. **Cold Start**: Limited accuracy for applicants with < 6 months credit history
2. **Income Verification**: Self-reported income not independently verified for all applications
3. **Economic Sensitivity**: Model trained on stable economic period; may underperform in recession

### Failure Modes
- High-income, low-credit-history applicants may be incorrectly declined
- Recent address changes may trigger false positives for fraud

## Training Data

- **Dataset**: Credit Application Dataset v3.2.1
- **Records**: 2,847,392
- **Time Period**: 2020-2025
- **Train/Test Split**: 80/20, stratified by outcome

## Ethical Considerations

### Fairness
- Model does not use protected characteristics as direct inputs
- Proxy variables (zip code) explicitly excluded
- Regular bias audits conducted quarterly

### Transparency
- SHAP values available for all decisions
- Customer-facing explanations generated for declines

## Updates and Monitoring

- **Retraining Frequency**: Quarterly or when AUC drops below 0.80
- **Monitoring**: Daily performance dashboards, weekly bias reports
- **Human Review**: All declines for applications > €25,000
