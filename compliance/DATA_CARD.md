# Data Card: Credit Scoring Model v2.1.0

## 1. Dataset Overview

| Attribute | Value |
|-----------|-------|
| Dataset Name | Credit Application Dataset |
| Version | 3.2.1 |
| Last Updated | 2026-01-15 |
| Total Records | 2,847,392 |
| Time Period | 2020-01-01 to 2025-12-31 |

## 2. Data Sources

### Primary Sources
- **Internal Applications**: 78% of records
  - Source: Acme Corp loan application system
  - Collection: Direct customer input + automated enrichment
  
- **Credit Bureau Data**: 22% of records
  - Source: Experian, Equifax (anonymized)
  - Collection: API integration, monthly refresh

## 3. Features

### Input Features (Article 10 Compliance)

| Feature | Type | Description | Source |
|---------|------|-------------|--------|
| income_annual | numeric | Declared annual income | Application |
| employment_length | numeric | Years at current employer | Application |
| debt_to_income | numeric | Calculated DTI ratio | Derived |
| credit_history_length | numeric | Months of credit history | Bureau |
| transaction_history | object | Aggregated transaction patterns | Bank API |

### Excluded Features (Fairness)
- race, ethnicity (never collected)
- gender (not used in model)
- zip_code (proxy for protected class)

## 4. Data Quality

### Completeness
- Overall: 97.3% complete
- Critical fields: 99.8% complete
- Missing value handling: Median imputation for numeric, mode for categorical

### Accuracy
- Validation against external sources: 94.2% match rate
- Manual audit sample (n=1000): 98.1% accurate

## 5. Bias Examination (Article 10(2)(f))

### Methodology
We conducted comprehensive bias analysis using:
1. Demographic parity testing across age groups
2. Equalized odds analysis for gender (inferred from names for audit only)
3. Geographic distribution analysis

### Findings

| Group | Approval Rate | Population % | Disparity |
|-------|---------------|--------------|-----------|
| Urban | 68.2% | 78% | Baseline |
| Suburban | 71.4% | 18% | +3.2% |
| Rural | 62.1% | 4% | -6.1% |

### Rural Population Gap
- **Issue Identified**: Rural applicants show 6.1% lower approval rate
- **Root Cause**: Lower representation in training data (4% vs 18% population)
- **Remediation**: 
  - Augmented training data with synthetic rural profiles
  - Implemented calibration layer for rural zip codes
  - Ongoing monitoring with quarterly review

## 6. Data Gaps (Article 10(2)(h))

### Identified Gaps
1. **Rural Representation**: 4% in dataset vs 18% population
   - Status: REMEDIATED (see Section 5)
   
2. **Recent Immigrants**: Limited credit history data
   - Status: Alternative data sources being evaluated
   
3. **Gig Economy Workers**: Income verification challenges
   - Status: Bank transaction analysis added in v2.1

## 7. Data Governance

- **Data Controller**: Acme Corp
- **Retention Period**: 7 years (regulatory requirement)
- **Access Controls**: Role-based, audit logged
- **Encryption**: AES-256 at rest, TLS 1.3 in transit

## 8. Version History

| Version | Date | Changes |
|---------|------|---------|
| 3.2.1 | 2026-01-15 | Added transaction_history feature |
| 3.2.0 | 2025-10-01 | Rural data augmentation |
| 3.1.0 | 2025-07-01 | Initial bias remediation |
