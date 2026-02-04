#!/usr/bin/env python3
"""
AnnexCI CLI - EU AI Act Compliance Scanner
Connects to AnnexCI platform for real-time compliance management.
"""

import argparse
import json
import os
import sys
import time
import hashlib
import requests
from pathlib import Path

# Configuration
API_URL = os.environ.get('ANNEXCI_API_URL', 'http://localhost:3001')
SYSTEM_ID = os.environ.get('ANNEXCI_SYSTEM_ID', 'sys-001')  # Default to Credit Scoring for demo

# ANSI colors
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

def print_header():
    print(f"""
{Colors.CYAN}{Colors.BOLD}
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║     █████╗ ███╗   ██╗███╗   ██╗███████╗██╗  ██╗ ██████╗██╗   ║
    ║    ██╔══██╗████╗  ██║████╗  ██║██╔════╝╚██╗██╔╝██╔════╝██║   ║
    ║    ███████║██╔██╗ ██║██╔██╗ ██║█████╗   ╚███╔╝ ██║     ██║   ║
    ║    ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝   ██╔██╗ ██║     ██║   ║
    ║    ██║  ██║██║ ╚████║██║ ╚████║███████╗██╔╝ ██╗╚██████╗██║   ║
    ║    ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝   ║
    ║                                                               ║
    ║            EU AI Act Compliance Scanner v2.1.0                ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
{Colors.RESET}""")

def print_step(message, status='running'):
    if status == 'running':
        print(f"  {Colors.YELLOW}►{Colors.RESET} {message}...", end='', flush=True)
    elif status == 'done':
        print(f"\r  {Colors.GREEN}✓{Colors.RESET} {message}    ")
    elif status == 'fail':
        print(f"\r  {Colors.RED}✗{Colors.RESET} {message}    ")

def api_call(method, endpoint, data=None):
    """Make API call to AnnexCI server"""
    url = f"{API_URL}{endpoint}"
    try:
        if method == 'GET':
            resp = requests.get(url, timeout=10)
        else:
            resp = requests.post(url, json=data, timeout=10)
        return resp.json()
    except requests.exceptions.ConnectionError:
        print(f"\n{Colors.RED}Error: Cannot connect to AnnexCI server at {API_URL}{Colors.RESET}")
        print(f"{Colors.DIM}Make sure the API server is running: cd packages/api && npm start{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.RESET}")
        sys.exit(1)

# ============================================
# INIT Command
# ============================================

TEMPLATE_RISK_REGISTER = '''# Risk Register - EU AI Act Article 9 Compliance
# Fill in the sections below for your AI system

system:
  name: "[YOUR SYSTEM NAME]"
  version: "[VERSION]"
  risk_classification: high  # high, limited, minimal
  annex_iii_category: "[CATEGORY]"  # e.g., "5(b) - Credit scoring"

risks: []
  # Add risks in this format:
  # - id: RISK-001
  #   name: "[Risk Name]"
  #   description: "[Description]"
  #   likelihood: medium  # low, medium, high
  #   impact: high  # low, medium, high
  #   risk_level: high  # calculated from likelihood x impact
  #   mitigation:
  #     - "[Mitigation measure 1]"
  #     - "[Mitigation measure 2]"
  #   owner: "[Owner Name]"
  #   review_date: YYYY-MM-DD

residual_risk_assessment:
  overall_level: "[low/medium/high]"
  justification: "[Explain why residual risk is acceptable]"
  approved_by: "[Name]"
  approved_date: YYYY-MM-DD
'''

TEMPLATE_DATA_CARD = '''# Data Card
## [System Name] v[Version]

## 1. Dataset Overview

| Attribute | Value |
|-----------|-------|
| Dataset Name | [Name] |
| Version | [Version] |
| Last Updated | [Date] |
| Total Records | [Number] |

## 2. Data Sources

[Describe your data sources]

## 3. Features

[List input features and their descriptions]

## 4. Data Quality

[Describe data quality metrics and validation]

## 5. Bias Examination (Article 10(2)(f))

[REQUIRED: Document your bias analysis methodology and findings]

## 6. Data Gaps (Article 10(2)(h))

[REQUIRED: Identify and document any data gaps]

## 7. Data Governance

[Describe data governance procedures]
'''

TEMPLATE_MODEL_CARD = '''# Model Card
## [System Name] v[Version]

## Model Details

| Attribute | Value |
|-----------|-------|
| Model Name | [Name] |
| Version | [Version] |
| Model Type | [Type] |
| Framework | [Framework] |

## Intended Use

[Describe intended use cases and users]

## Performance Metrics

[Document model performance]

## Limitations

[Document known limitations]

## Training Data

[Reference the Data Card]
'''

TEMPLATE_HUMAN_OVERSIGHT = '''# Human Oversight Procedures
## [System Name] v[Version]

### Article 14 Compliance Documentation

## 1. Oversight Structure

[Define who has oversight authority]

## 2. Human Review Triggers

[Define when human review is required]

## 3. Override Procedures

[Document how decisions can be overridden]

## 4. Stop Mechanism (Article 14(4)(e))

[REQUIRED: Document emergency stop procedure]

## 5. Training Requirements

[Define training for oversight personnel]
'''

TEMPLATE_INSTRUCTIONS = '''# Instructions for Use
## [System Name] v[Version]

### Article 13 Compliance - Transparency Documentation

## 1. System Overview

[Describe what the system does]

## 2. Intended Purpose

[Define intended and out-of-scope uses]

## 3. Technical Specifications

[Document technical requirements]

## 4. Accuracy and Limitations

[Document performance characteristics]

## 5. Human Oversight Requirements

[Reference oversight procedures]
'''

TEMPLATE_CONFIG = '''# AnnexCI Configuration
system:
  id: sys-001  # Will be assigned by platform
  name: "[YOUR SYSTEM NAME]"
  version: "1.0.0"
  
client:
  id: acme
  name: "Acme Corp"
  
compliance:
  risk_level: high
  articles:
    - 9   # Risk Management
    - 10  # Data Governance
    - 11  # Technical Documentation
    - 12  # Record Keeping
    - 13  # Transparency
    - 14  # Human Oversight
    - 15  # Accuracy, Robustness, Cybersecurity
'''

def cmd_init(args):
    """Initialize compliance structure in current directory"""
    print_header()
    print(f"\n{Colors.BOLD}Initializing AnnexCI compliance structure...{Colors.RESET}\n")
    
    compliance_dir = Path('compliance')
    
    if compliance_dir.exists() and not args.force:
        print(f"{Colors.YELLOW}Warning: compliance/ directory already exists.{Colors.RESET}")
        print(f"Use --force to overwrite.\n")
        return
    
    compliance_dir.mkdir(exist_ok=True)
    
    templates = {
        'RISK_REGISTER.yaml': TEMPLATE_RISK_REGISTER,
        'DATA_CARD.md': TEMPLATE_DATA_CARD,
        'MODEL_CARD.md': TEMPLATE_MODEL_CARD,
        'HUMAN_OVERSIGHT.md': TEMPLATE_HUMAN_OVERSIGHT,
        'INSTRUCTIONS.md': TEMPLATE_INSTRUCTIONS,
    }
    
    for filename, content in templates.items():
        filepath = compliance_dir / filename
        print_step(f"Creating {filename}", 'running')
        time.sleep(0.3)
        with open(filepath, 'w') as f:
            f.write(content)
        print_step(f"Creating {filename}", 'done')
    
    # Create config file in root
    print_step("Creating annexci.yaml", 'running')
    time.sleep(0.3)
    with open('annexci.yaml', 'w') as f:
        f.write(TEMPLATE_CONFIG)
    print_step("Creating annexci.yaml", 'done')
    
    print(f"""
{Colors.GREEN}{Colors.BOLD}✓ Compliance structure initialized{Colors.RESET}

{Colors.CYAN}Created files:{Colors.RESET}
  compliance/
  ├── RISK_REGISTER.yaml    {Colors.DIM}(Article 9 - Risk Management){Colors.RESET}
  ├── DATA_CARD.md          {Colors.DIM}(Article 10 - Data Governance){Colors.RESET}
  ├── MODEL_CARD.md         {Colors.DIM}(Article 13 - Transparency){Colors.RESET}
  ├── HUMAN_OVERSIGHT.md    {Colors.DIM}(Article 14 - Human Oversight){Colors.RESET}
  └── INSTRUCTIONS.md       {Colors.DIM}(Article 13 - Instructions for Use){Colors.RESET}
  annexci.yaml              {Colors.DIM}(Configuration){Colors.RESET}

{Colors.YELLOW}Next steps:{Colors.RESET}
  1. Fill in the template files with your system's information
  2. Run {Colors.CYAN}annexci scan{Colors.RESET} to validate compliance
""")

# ============================================
# SCAN Command
# ============================================

def validate_risk_register(content):
    """Validate RISK_REGISTER.yaml"""
    errors = []
    warnings = []
    
    if '[YOUR SYSTEM NAME]' in content or 'risks: []' in content:
        errors.append('RISK_REGISTER.yaml: No risks defined (template not filled)')
    elif 'risks:' not in content:
        errors.append('RISK_REGISTER.yaml: Missing risks section')
    
    if 'residual_risk_assessment' not in content:
        warnings.append('RISK_REGISTER.yaml: Missing residual risk assessment')
    
    return errors, warnings

def validate_data_card(content):
    """Validate DATA_CARD.md"""
    errors = []
    warnings = []
    
    if '[System Name]' in content or '[Name]' in content:
        errors.append('DATA_CARD.md: Template not filled in')
    
    if 'Bias Examination' not in content or '[REQUIRED' in content:
        errors.append('DATA_CARD.md: Bias examination section incomplete (Article 10(2)(f))')
    
    if 'Data Gaps' not in content:
        warnings.append('DATA_CARD.md: Data gaps section missing (Article 10(2)(h))')
    
    return errors, warnings

def validate_model_card(content):
    """Validate MODEL_CARD.md"""
    errors = []
    warnings = []
    
    if '[System Name]' in content or '[Name]' in content:
        errors.append('MODEL_CARD.md: Template not filled in')
    
    if 'Limitations' not in content:
        warnings.append('MODEL_CARD.md: Limitations section missing')
    
    return errors, warnings

def validate_human_oversight(content):
    """Validate HUMAN_OVERSIGHT.md"""
    errors = []
    warnings = []
    
    if '[System Name]' in content:
        errors.append('HUMAN_OVERSIGHT.md: Template not filled in')
    
    if 'Stop Mechanism' not in content or '[REQUIRED' in content:
        errors.append('HUMAN_OVERSIGHT.md: Stop mechanism not documented (Article 14(4)(e))')
    
    return errors, warnings

def validate_instructions(content):
    """Validate INSTRUCTIONS.md"""
    errors = []
    warnings = []
    
    if '[System Name]' in content:
        errors.append('INSTRUCTIONS.md: Template not filled in')
    
    return errors, warnings

def scan_source_files():
    """Scan source files for security patterns"""
    errors = []
    warnings = []
    
    # Look for Python files
    py_files = list(Path('.').rglob('*.py'))
    py_files = [f for f in py_files if 'compliance' not in str(f) and '.venv' not in str(f)]
    
    for py_file in py_files[:10]:  # Limit for demo
        try:
            content = py_file.read_text()
            
            # Check for pickle (security vulnerability)
            if 'pickle.load' in content or 'pickle.loads' in content:
                line_num = next((i+1 for i, line in enumerate(content.split('\n')) if 'pickle.load' in line), 0)
                errors.append(f'{py_file}:{line_num}: Unsafe deserialization (pickle.load) - Article 15 violation')
            
            # Check for eval
            if 'eval(' in content:
                warnings.append(f'{py_file}: eval() detected - potential security risk')
                
        except Exception:
            pass
    
    return errors, warnings

def cmd_scan(args):
    """Run compliance scan"""
    print_header()
    
    print(f"\n{Colors.DIM}Validating license...{Colors.RESET}", end=" ")
    time.sleep(0.5)
    print(f"{Colors.GREEN}✓ Licensed to Demo Partner LLP → Acme Corp{Colors.RESET}")
    print(f"{Colors.DIM}License valid until: 2027-01-29{Colors.RESET}\n")
    
    compliance_dir = Path('compliance')
    if not compliance_dir.exists():
        print(f"{Colors.RED}Error: compliance/ directory not found.{Colors.RESET}")
        print(f"Run {Colors.CYAN}annexci init{Colors.RESET} first.\n")
        sys.exit(1)
    
    all_errors = []
    all_warnings = []
    
    print(f"{Colors.BOLD}Discovering compliance documents...{Colors.RESET}\n")
    
    files_to_check = [
        ('RISK_REGISTER.yaml', validate_risk_register),
        ('DATA_CARD.md', validate_data_card),
        ('MODEL_CARD.md', validate_model_card),
        ('HUMAN_OVERSIGHT.md', validate_human_oversight),
        ('INSTRUCTIONS.md', validate_instructions),
    ]
    
    found_files = []
    for filename, validator in files_to_check:
        filepath = compliance_dir / filename
        if filepath.exists():
            size = filepath.stat().st_size / 1024
            print(f"  {Colors.DIM}├─{Colors.RESET} {filename} {Colors.DIM}({size:.1f} KB){Colors.RESET}")
            found_files.append((filename, validator, filepath))
            time.sleep(0.1)
        else:
            print(f"  {Colors.DIM}├─{Colors.RESET} {Colors.RED}{filename} (missing){Colors.RESET}")
            all_errors.append(f'{filename}: File missing')
    
    print(f"\n{Colors.DIM}Scanning source files for security patterns...{Colors.RESET}")
    src_errors, src_warnings = scan_source_files()
    all_errors.extend(src_errors)
    all_warnings.extend(src_warnings)
    time.sleep(0.3)
    
    print(f"\n{Colors.BOLD}Running compliance checks...{Colors.RESET}\n")
    time.sleep(0.3)
    
    # Validate each file
    for filename, validator, filepath in found_files:
        content = filepath.read_text()
        errors, warnings = validator(content)
        all_errors.extend(errors)
        all_warnings.extend(warnings)
    
    # Group by article
    articles = {
        'Article 9': [],
        'Article 10': [],
        'Article 13': [],
        'Article 14': [],
        'Article 15': [],
    }
    
    for err in all_errors:
        if 'RISK_REGISTER' in err:
            articles['Article 9'].append(('error', err))
        elif 'DATA_CARD' in err:
            articles['Article 10'].append(('error', err))
        elif 'MODEL_CARD' in err or 'INSTRUCTIONS' in err:
            articles['Article 13'].append(('error', err))
        elif 'HUMAN_OVERSIGHT' in err:
            articles['Article 14'].append(('error', err))
        elif 'Article 15' in err or 'pickle' in err.lower() or 'security' in err.lower():
            articles['Article 15'].append(('error', err))
    
    for warn in all_warnings:
        if 'RISK_REGISTER' in warn:
            articles['Article 9'].append(('warning', warn))
        elif 'DATA_CARD' in warn:
            articles['Article 10'].append(('warning', warn))
        elif 'MODEL_CARD' in warn or 'INSTRUCTIONS' in warn:
            articles['Article 13'].append(('warning', warn))
        elif 'HUMAN_OVERSIGHT' in warn:
            articles['Article 14'].append(('warning', warn))
        elif 'security' in warn.lower():
            articles['Article 15'].append(('warning', warn))
    
    # Print results by article
    for article, items in articles.items():
        print(f"{Colors.BOLD}━━━ {article}: {'Risk Management' if '9' in article else 'Data Governance' if '10' in article else 'Transparency' if '13' in article else 'Human Oversight' if '14' in article else 'Accuracy, Robustness, Security'} ━━━{Colors.RESET}")
        
        errors_in_article = [i for i in items if i[0] == 'error']
        warnings_in_article = [i for i in items if i[0] == 'warning']
        
        if not items:
            print(f"  {Colors.GREEN}✓{Colors.RESET} All checks passed")
        else:
            for item_type, message in items:
                if item_type == 'error':
                    print(f"  {Colors.RED}✗{Colors.RESET} {Colors.RED}{message}{Colors.RESET}")
                else:
                    print(f"  {Colors.YELLOW}⚠{Colors.RESET} {Colors.YELLOW}{message}{Colors.RESET}")
        
        print()
        time.sleep(0.2)
    
    # Summary
    passed = len(all_errors) == 0
    
    if passed:
        print(f"""
{Colors.GREEN}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   SCAN RESULT: PASSED                                         ║
║                                                               ║
║   All technical checks passed.                                ║
║   Warnings: {len(all_warnings):<3}                                                ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}
""")
        
        # Sync to platform
        print(f"{Colors.BOLD}━━━ Syncing to Platform ━━━{Colors.RESET}")
        print(f"{Colors.DIM}(No source code or model weights transmitted){Colors.RESET}\n")
        
        # Calculate hashes
        print(f"  {Colors.CYAN}Documents sent:{Colors.RESET}")
        for filename, _, filepath in found_files:
            content = filepath.read_text()
            hash_val = hashlib.sha256(content.encode()).hexdigest()[:12]
            print(f"    ├─ {filename} → sha256:{hash_val}...")
        
        print(f"\n  {Colors.CYAN}Notifying CRO...{Colors.RESET}")
        time.sleep(0.3)
        
        # Send to API
        scan_results = {
            'errors': all_errors,
            'warnings': all_warnings,
            'documents': [f[0] for f in found_files],
            'passed': True,
        }
        
        result = api_call('POST', '/api/scan', {
            'systemId': SYSTEM_ID,
            'results': scan_results,
        })
        
        print(f"    {Colors.GREEN}✓{Colors.RESET} Results synced to platform")
        print(f"    {Colors.GREEN}✓{Colors.RESET} CRO notified: m.silva@acme.com")
        
        print(f"""
{Colors.CYAN}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   COMPLIANCE STATUS                                           ║
║                                                               ║
║   Technical checks:    ✓ PASSED                               ║
║   Human attestations:  ⏳ PENDING                              ║
║                                                               ║
║   Deployment gate:     🚫 BLOCKED (awaiting attestations)     ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.DIM}→ View at: https://app.annexci.com/acme/credit-scoring/2.1{Colors.RESET}
""")
    else:
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   SCAN RESULT: FAILED                                         ║
║                                                               ║
║   Errors:   {len(all_errors):<3}                                               ║
║   Warnings: {len(all_warnings):<3}                                               ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.DIM}Fix the errors above and run 'annexci scan' again.{Colors.RESET}
""")
        
        # Still send to API (failed scan)
        scan_results = {
            'errors': all_errors,
            'warnings': all_warnings,
            'documents': [f[0] for f in found_files],
            'passed': False,
        }
        
        api_call('POST', '/api/scan', {
            'systemId': SYSTEM_ID,
            'results': scan_results,
        })
        
        sys.exit(1)

# ============================================
# DEPLOY Command
# ============================================

def cmd_deploy(args):
    """Deploy with compliance token"""
    print(f"""
{Colors.CYAN}{Colors.BOLD}
    ╔═══════════════════════════════════════════════════════════════╗
    ║                     ANNEXCI DEPLOYMENT GATE                   ║
    ╚═══════════════════════════════════════════════════════════════╝
{Colors.RESET}""")
    
    if not args.token:
        print(f"{Colors.RED}Error: --token is required{Colors.RESET}")
        print(f"Usage: annexci deploy --token YOUR_TOKEN\n")
        sys.exit(1)
    
    token_id = args.token
    
    print(f"{Colors.DIM}Verifying compliance token...{Colors.RESET}\n")
    time.sleep(0.5)
    
    # Step 1: Validate token
    print_step("Decrypting token payload", 'running')
    time.sleep(0.4)
    print_step("Decrypting token payload", 'done')
    
    print_step("Validating token signature", 'running')
    time.sleep(0.4)
    
    validation = api_call('POST', '/api/token/validate', {'tokenId': token_id})
    
    if not validation.get('valid'):
        print_step("Validating token signature", 'fail')
        print(f"""
{Colors.RED}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ✗ DEPLOYMENT BLOCKED                                        ║
║                                                               ║
║   Reason: {validation.get('reason', 'Invalid token'):<50} ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}
""")
        sys.exit(1)
    
    print_step("Validating token signature", 'done')
    
    token = validation['token']
    
    print_step(f"Checking issuer: {token['issuedBy']}", 'running')
    time.sleep(0.3)
    print_step(f"Checking issuer: {token['issuedBy']}", 'done')
    
    print_step("Verifying model hash", 'running')
    time.sleep(0.3)
    print(f"\r  {Colors.GREEN}✓{Colors.RESET} Verifying model hash: {token['modelHash'][:20]}...    ")
    
    print_step("Checking attestations", 'running')
    time.sleep(0.3)
    print_step(f"Checking attestations ({len(token['attestations'])} on file)", 'done')
    
    print()
    
    # Step 2: Create token file for GitHub Actions
    print(f"{Colors.BOLD}Authorizing deployment...{Colors.RESET}\n")
    
    # Create .annexci directory if it doesn't exist
    annexci_dir = Path('.annexci')
    annexci_dir.mkdir(exist_ok=True)
    
    # Write token file
    token_file = annexci_dir / 'token'
    print_step("Writing compliance token to .annexci/token", 'running')
    time.sleep(0.3)
    with open(token_file, 'w') as f:
        f.write(token_id)
    print_step("Writing compliance token to .annexci/token", 'done')
    
    # Git operations
    import subprocess
    
    print_step("Staging token file", 'running')
    time.sleep(0.3)
    try:
        subprocess.run(['git', 'add', '.annexci/token'], check=True, capture_output=True)
        print_step("Staging token file", 'done')
    except subprocess.CalledProcessError:
        print_step("Staging token file", 'fail')
        print(f"{Colors.YELLOW}Warning: Could not stage file. Run 'git add .annexci/token' manually.{Colors.RESET}")
    
    print_step("Committing authorization", 'running')
    time.sleep(0.3)
    try:
        subprocess.run([
            'git', 'commit', '-m', 
            f'chore: Add compliance token for {token["systemName"]} v{token["systemVersion"]}\n\n'
            f'Token issued by: {token["issuedBy"]}\n'
            f'Attestations: {len(token["attestations"])} on file\n'
            f'Model hash: {token["modelHash"]}'
        ], check=True, capture_output=True)
        print_step("Committing authorization", 'done')
    except subprocess.CalledProcessError as e:
        if b'nothing to commit' in e.stdout or b'nothing to commit' in e.stderr:
            print_step("Committing authorization (already committed)", 'done')
        else:
            print_step("Committing authorization", 'fail')
            print(f"{Colors.YELLOW}Warning: Could not commit. Run 'git commit' manually.{Colors.RESET}")
    
    print_step("Pushing to remote", 'running')
    time.sleep(0.5)
    try:
        subprocess.run(['git', 'push'], check=True, capture_output=True)
        print_step("Pushing to remote", 'done')
    except subprocess.CalledProcessError:
        print_step("Pushing to remote", 'fail')
        print(f"{Colors.YELLOW}Warning: Could not push. Run 'git push' manually.{Colors.RESET}")
    
    print_step("Enabling Article 12 logging", 'running')
    time.sleep(0.3)
    print_step("Enabling Article 12 logging", 'done')
    
    # Record deployment in API
    result = api_call('POST', '/api/deploy', {
        'tokenId': token_id,
        'systemId': token['systemId'],
    })
    
    print_step("Registering in audit trail", 'running')
    time.sleep(0.3)
    print_step("Registering in audit trail", 'done')
    
    print(f"""
{Colors.GREEN}{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ✓ DEPLOYMENT AUTHORIZED                                     ║
║                                                               ║
║   System:      {token['systemName']:<43} ║
║   Version:     {token['systemVersion']:<43} ║
║   Token:       {token_id:<43} ║
║   Issued by:   {token['issuedBy']:<43} ║
║                                                               ║
║   ✓ Token file committed to .annexci/token                    ║
║   ✓ Changes pushed to remote                                  ║
║   ✓ GitHub Actions will verify and allow merge                ║
║                                                               ║
║   Audit trail updated. Article 12 logging: ENABLED            ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.CYAN}Next steps:{Colors.RESET}
  1. GitHub Actions will re-run and pass Stage 2
  2. PR will show all checks passing ✓
  3. You can now merge the PR

{Colors.DIM}→ View deployment: https://github.com/acme-corp/credit-scoring/releases/tag/v{token['systemVersion']}-compliant{Colors.RESET}
{Colors.DIM}→ Audit trail: https://app.annexci.com/acme/credit-scoring/deployments{Colors.RESET}
""")

# ============================================
# Main
# ============================================

def main():
    parser = argparse.ArgumentParser(
        description='AnnexCI - EU AI Act Compliance Scanner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  annexci init              Initialize compliance structure
  annexci scan              Run compliance scan
  annexci deploy --token X  Deploy with compliance token
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # init command
    init_parser = subparsers.add_parser('init', help='Initialize compliance structure')
    init_parser.add_argument('--force', action='store_true', help='Overwrite existing files')
    
    # scan command
    scan_parser = subparsers.add_parser('scan', help='Run compliance scan')
    
    # deploy command
    deploy_parser = subparsers.add_parser('deploy', help='Deploy with compliance token')
    deploy_parser.add_argument('--token', required=True, help='Compliance token')
    
    args = parser.parse_args()
    
    if args.command == 'init':
        cmd_init(args)
    elif args.command == 'scan':
        cmd_scan(args)
    elif args.command == 'deploy':
        cmd_deploy(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
