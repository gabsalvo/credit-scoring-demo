# Instructions for Use
## Credit Scoring Model v2.1.0

### Article 13 Compliance - Transparency Documentation

---

## 1. System Overview

The Credit Scoring Model v2.1.0 is an AI-powered system designed to assess credit risk for consumer loan applications. This document provides instructions for deployers and users as required by Article 13 of the EU AI Act.

---

## 2. Intended Purpose

### 2.1 What This System Does
- Analyzes loan applications to predict repayment probability
- Provides risk scores from 0-1000 (higher = lower risk)
- Generates approval/decline recommendations
- Produces explainable decision factors

### 2.2 What This System Does NOT Do
- Make final lending decisions (human oversight required for amounts > €10,000)
- Process business loan applications
- Assess mortgage applications
- Operate outside EU jurisdiction

---

## 3. Technical Specifications

| Specification | Value |
|---------------|-------|
| Input Format | JSON via REST API |
| Response Time | < 200ms (p99) |
| Availability | 99.9% SLA |
| Supported Languages | EN, DE, FR, ES, IT |

### 3.1 API Endpoint
```
POST https://api.acme-credit.com/v2/score
Authorization: Bearer <token>
Content-Type: application/json
```

### 3.2 Required Inputs
```json
{
  "applicant_id": "string",
  "income_annual": "number",
  "employment_length_months": "number",
  "credit_history_length_months": "number",
  "existing_debt": "number",
  "requested_amount": "number"
}
```

---

## 4. Accuracy and Limitations

### 4.1 Performance Characteristics
- Overall accuracy: 84.7% (AUC-ROC)
- False positive rate: 12.3%
- False negative rate: 8.9%

### 4.2 Known Limitations
1. **Limited history applicants**: Accuracy drops to 71% for applicants with < 6 months credit history
2. **Income verification**: Self-reported income not independently verified
3. **Economic conditions**: Model trained on 2020-2025 data; recession performance unknown

### 4.3 Conditions Affecting Performance
- Data quality issues may increase error rates
- High-volume periods may increase response times
- Model performance degrades over time without retraining

---

## 5. Human Oversight Requirements

### 5.1 Mandatory Review Cases
Human review is REQUIRED for:
- All applications > €25,000
- Model confidence < 70%
- Any applicant dispute
- Applications from new customer segments

### 5.2 Oversight Interface
Access the oversight dashboard at:
`https://oversight.acme-credit.com`

Credentials provided separately to authorized personnel.

---

## 6. Logging and Audit

### 6.1 Automatic Logging
The system automatically logs:
- All input data (encrypted)
- Model version used
- Score and recommendation
- Response time
- Any errors or exceptions

### 6.2 Log Retention
Logs retained for 7 years per regulatory requirement.

### 6.3 Audit Access
Auditors can request log exports via:
`audit-requests@acme-credit.com`

---

## 7. Incident Reporting

### 7.1 How to Report Issues
Report any system issues or concerns to:
- Email: ai-incidents@acme-credit.com
- Phone: +31 20 123 4567 (24/7)
- Portal: https://support.acme-credit.com

### 7.2 Response Times
- Critical (system down): 15 minutes
- High (accuracy issues): 4 hours
- Medium (feature requests): 5 business days

---

## 8. Contact Information

| Role | Contact |
|------|---------|
| Technical Support | support@acme-credit.com |
| Compliance Questions | compliance@acme-credit.com |
| Data Protection Officer | dpo@acme-credit.com |

---

**Document Version:** 2.1.0  
**Effective Date:** 2026-01-29  
**Review Date:** 2026-07-29
