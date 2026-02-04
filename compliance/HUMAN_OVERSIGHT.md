# Human Oversight Procedures
## Credit Scoring Model v2.1.0

### Article 14 Compliance Documentation

---

## 1. Oversight Structure

### 1.1 Designated Oversight Personnel

| Role | Name | Responsibility |
|------|------|----------------|
| Primary Oversight | M. Silva (CRO) | Final authority on model decisions |
| Technical Oversight | J. Chen (ML Lead) | Model performance monitoring |
| Compliance Oversight | A. Park (Legal) | Regulatory alignment |

### 1.2 Oversight Authority
The CRO has authority to:
- Override any automated decision
- Halt model operations immediately
- Mandate retraining or recalibration
- Escalate to executive leadership

---

## 2. Human Review Triggers

### 2.1 Mandatory Human Review
The following cases ALWAYS require human review:

| Trigger | Threshold | Reviewer |
|---------|-----------|----------|
| Loan amount | > €25,000 | Senior Analyst |
| Model confidence | < 70% | Credit Analyst |
| Applicant dispute | Any | CRO Team |
| Edge cases | Flagged by model | Credit Analyst |

### 2.2 Sampling Review
- 5% random sample of all decisions reviewed weekly
- 100% of declined applications reviewed within 48 hours

---

## 3. Override Procedures

### 3.1 Decision Override Process

```
1. Analyst identifies case requiring override
2. Document reason in Override Request Form
3. Submit to supervisor for approval
4. If approved, override applied with audit trail
5. Monthly review of all overrides by CRO
```

### 3.2 Override Documentation
Each override must include:
- Original model decision and confidence
- Reason for override (structured categories)
- Supporting evidence
- Approver signature
- Timestamp

---

## 4. Stop Mechanism (Article 14(4)(e))

### 4.1 Emergency Stop Procedure

**Trigger Conditions:**
- Model accuracy drops below 75% AUC
- Bias disparity exceeds 15% for any group
- Security incident affecting model integrity
- Regulatory directive

**Stop Process:**
1. Any oversight personnel can initiate stop
2. Automated decisions immediately halted
3. All pending applications queued for human review
4. CRO notified within 15 minutes
5. Root cause analysis initiated

### 4.2 Stop Authority
The following personnel can execute emergency stop:
- CRO (M. Silva)
- ML Lead (J. Chen)
- On-call engineer (24/7 rotation)
- Any executive leadership member

### 4.3 Restart Procedure
Model can only restart after:
1. Root cause identified and documented
2. Remediation implemented
3. CRO sign-off obtained
4. Test batch validated (n=100 manual review)

---

## 5. Training Requirements

### 5.1 Required Training for Oversight Personnel

| Training | Frequency | Duration |
|----------|-----------|----------|
| EU AI Act Overview | Annual | 4 hours |
| Model Interpretation | Quarterly | 2 hours |
| Bias Detection | Quarterly | 2 hours |
| Override Procedures | Annual | 1 hour |

### 5.2 Training Records
All training completion recorded in HR system with:
- Date completed
- Assessment score (minimum 80% required)
- Certification expiry

---

## 6. Transaction History Oversight (New in v2.1)

### 6.1 Additional Oversight for New Feature
The transaction_history feature added in v2.1 requires:
- Enhanced privacy review for all decisions using this feature
- Quarterly audit of transaction data access logs
- Customer consent verification before feature activation

### 6.2 Feature-Specific Review
- First 1000 decisions using transaction_history: 100% human review
- Ongoing: 10% sample review of transaction_history-influenced decisions

---

## 7. Audit Trail

All oversight activities logged with:
- User ID and role
- Action taken
- Timestamp
- IP address
- Affected records

Logs retained for 7 years per regulatory requirement.

---

**Document Owner:** M. Silva (CRO)  
**Last Updated:** 2026-01-29  
**Next Review:** 2026-04-29
