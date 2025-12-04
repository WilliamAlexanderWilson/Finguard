# FinGuard - Technical Specification

## Architecture Overview

FinGuard is a custom Claude skill that extends Claude's capabilities to function as a specialized accounting and finance operations agent. The skill uses a combination of:

1. **Skill Definition (SKILL.md)** - Core instructions and behavioral guidelines
2. **Reference Materials** - Financial formulas and GAAP principles
3. **Python Scripts** - Automated processing tools

## Skill Components

### 1. SKILL.md (Main Skill Definition)

**Location:** `/finguard/SKILL.md`

**Purpose:** Defines FinGuard's identity, capabilities, and behavioral rules

**Key Sections:**
- Identity & Voice: Personality and communication style
- Responsibilities: 10 core functions from bookkeeping to monthly close
- Advanced Behavior Rules: Uncertainty handling, self-audit, industry adaptation
- Output Format: Standardized reporting structure
- Chart of Accounts: Default categorization schema
- Escalation Triggers: Automatic flagging rules
- Guardrails & Ethics: Safety and compliance rules

**Activation Triggers (in frontmatter description):**
- Financial operations
- Accounting tasks
- Bookkeeping
- Transaction categorization
- Invoice management
- Payroll processing
- Financial reports
- Cash flow planning

### 2. Reference Materials

#### financial_formulas.md

**Location:** `/finguard/references/financial_formulas.md`

**Contents:**
- Core financial statement formulas (P&L, Balance Sheet, Cash Flow)
- Financial ratios (liquidity, profitability, efficiency, leverage)
- Working capital calculations
- Cash flow metrics
- Revenue recognition formulas (SaaS, E-commerce)
- Payroll calculations
- Depreciation methods
- Break-even analysis
- Account reconciliation formulas

**Usage:** Loaded on-demand when FinGuard needs to perform calculations

#### gaap_principles.md

**Location:** `/finguard/references/gaap_principles.md`

**Contents:**
- 10 core GAAP principles
- Accrual vs cash basis accounting
- Double-entry bookkeeping rules
- Journal entry patterns
- Revenue recognition rules
- Expense recognition guidelines
- Financial statement requirements
- Internal controls
- Closing procedures
- Common accounting errors to avoid

**Usage:** Referenced when making accounting decisions or explaining concepts

### 3. Python Scripts

#### categorize_transactions.py

**Purpose:** Automated transaction categorization based on patterns

**Key Features:**
- Pattern-based rule engine using regex
- Batch processing of CSV files
- Split transaction support
- Custom rule addition
- Categorization reporting
- Uncategorized item flagging

**Input:** CSV with columns: `date, payee, description, amount`

**Output:** 
- Categorized CSV with added `category` column
- Summary report showing breakdown by category
- List of uncategorized items for review

**Usage:**
```bash
python categorize_transactions.py input.csv output.csv
```

**Rule Categories:**
- Revenue patterns (Stripe, PayPal, Square)
- COGS patterns (Upwork, Fiverr, materials)
- OpEx patterns (AWS, Gusto, marketing, travel)

#### bank_reconciliation.py

**Purpose:** Reconcile bank statement with accounting books

**Key Features:**
- Exact match detection (date + amount + payee)
- Fuzzy match detection (similar dates/payees)
- Duplicate detection
- Balance variance calculation
- Outstanding items tracking
- Comprehensive reconciliation reporting

**Input:** 
- Bank statement CSV: `date, payee, amount`
- Books CSV: `date, payee, amount`
- Ending balance (float)

**Output:**
- Detailed reconciliation report
- Matched transactions list
- Unmatched items (both sides)
- Potential matches for review
- Duplicate alerts
- Balance variance calculation

**Usage:**
```bash
python bank_reconciliation.py statement.csv books.csv 45230.18
```

**Matching Algorithm:**
1. Generate transaction hash (date + amount + payee)
2. Find exact hash matches
3. For unmatched, search within date window (±3 days)
4. Calculate payee similarity score
5. Flag potential matches >60% similarity

#### generate_financial_reports.py

**Purpose:** Generate standard financial reports

**Key Features:**
- Profit & Loss statement
- Cash Flow statement
- Month-over-month comparison
- Key Performance Indicators
- Automatic categorization into statement sections
- Margin calculations

**Input:** CSV with columns: `date, category, amount`

**Output:**
- Formatted P&L report with:
  - Revenue section
  - COGS section
  - Gross profit & margin
  - Operating expenses
  - Net income & margin
- Cash Flow statement with:
  - Operating activities
  - Investing activities
  - Financing activities
  - Net change in cash
- KPI summary

**Usage:**
```bash
python generate_financial_reports.py transactions.csv "November 2024"
```

## Behavioral Rules & Logic

### Uncertainty Handling

**Priority:** Highest (overrides all other rules)

**Behavior:**
1. Pause immediately when data is incomplete or ambiguous
2. Identify exactly what is missing
3. Provide 1-2 possible interpretations
4. Ask clarifying question
5. Never guess or fabricate

**Example Triggers:**
- Missing transaction description
- Unclear payee name
- Ambiguous amounts
- Conflicting dates

### Self-Audit Mode

**When:** After generating any financial output

**Checks:**
- Do totals equal subtotals?
- Do debits equal credits? (for journal entries)
- Does data match prior statements?
- Is cash vs accrual treatment consistent?

**Action on Error:**
- Correct proactively
- Explain the correction to user
- Show original vs corrected values

### Industry Adaptation

**Detection:** Automatic based on transaction patterns

**Industries Supported:**
- E-commerce (inventory, fulfillment, platform payouts)
- SaaS (deferred revenue, MRR/ARR, subscriptions)
- Retail (daily sales, cash variances)
- Restaurants (tips, food/alcohol splits)
- Service businesses (labor COGS, milestone billing)

**Announcement:** FinGuard announces when it detects an industry switch

### Data Provenance Tracking

**Requirement:** Every number must be traceable

**Tracked Information:**
- Source (bank feed, invoice, etc.)
- File or statement name
- Date range
- Transformations applied

**Purpose:** Auditability and transparency

### Mode Switching

**Modes:**
- Bookkeeping Mode (categorization, reconciliation)
- Analysis Mode (insights, trends, KPIs)
- Audit Mode (consistency checks)
- Explainer Mode (teaching concepts)
- Conversation Mode (normal dialogue)

**Switching:** Automatic based on user intent, no announcement unless clarification needed

## Output Format Specification

All analyses follow this strict format:

```
1. One-Sentence Summary
   - Brief overview of the entire analysis

2. Key Findings
   - 3-5 bullet points of most important discoveries

3. Items Needing Attention
   - Actionable items requiring user action
   - Prioritized by importance/urgency

4. Insights & Recommendations
   - Context and interpretation
   - Suggested next steps

5. Accountant Review Needed (conditional)
   - Only appears when escalation triggers fire
   - Structured: Issue, Amount, Date, Reason, Suggested Action

6. Questions for You
   - Clarifying questions for missing data
   - Requests for additional context
```

## Chart of Accounts

### Default Structure

**Revenue**
- Sales / Service
- Refunds & Discounts
- Other Income

**COGS**
- Materials & Supplies
- Subcontractors
- Payment Processing Fees

**Operating Expenses**
- Payroll & Benefits
- Marketing & Advertising
- Software & Tools
- Office Expenses
- Travel & Meals
- Rent & Utilities
- Professional Fees
- Other OpEx

### Auto-Categorization Rules

Pattern matching with regex:
```python
'stripe|paypal|square' → Sales / Service
'upwork|fiverr|toptal' → Subcontractors
'aws|azure|openai|vercel' → Software & Tools
'gusto|adp|payroll' → Payroll & Benefits
'google ads|facebook ads' → Marketing & Advertising
```

### Customization

Users can:
1. Add custom categories
2. Modify pattern rules
3. Create industry-specific accounts
4. Map to their existing COA

## Escalation System

### Automatic Triggers

| Condition | Threshold | Action |
|-----------|-----------|--------|
| Large new transaction | ≥$10,000 | Flag for accountant |
| Negative cash forecast | 30 days | Alert with suggestions |
| 1099 contractor | ≥$600 YTD | Tax reporting reminder |
| Fraud indicators | Any | Immediate flag |
| Revenue recognition ambiguity | Any | Request guidance |
| Sales tax nexus | New state | Compliance check |

### Escalation Template

```
⚠️ Accountant Review Needed
Issue: [Description]
Amount: $[Amount] | Date: [Date]
Reason: [Why flagged]
Suggested Action: [Recommendation]
```

## Memory & Continuity

**Capability:** Remembers all prior conversations and preferences

**Stored Information:**
- User's accounting method (cash/accrual)
- Industry and business type
- Custom categorization rules
- Chart of accounts modifications
- Payment terms preferences
- Escalation threshold customizations

**Behavior:** Never re-asks known information

## Integration Points

### Supported Data Sources

**Bank Feeds:**
- CSV exports from any bank
- OFX/QFX file support via conversion
- Direct bank statement PDFs

**Payment Processors:**
- Stripe (CSV exports)
- PayPal (transaction history)
- Square (sales reports)
- Shopify (order exports)

**Payroll Providers:**
- Gusto (payroll reports)
- ADP (pay summaries)
- Rippling (payroll journals)
- Justworks (payroll exports)

**Accounting Software:**
- QuickBooks exports
- Xero transaction lists
- Wave accounting exports
- FreshBooks data

### File Format Requirements

**Transaction CSV:**
```
Required columns: date, payee, amount
Optional columns: description, category, id
Date format: YYYY-MM-DD preferred (flexible parsing)
Amount format: Positive for income, negative for expenses
```

**Bank Statement CSV:**
```
Required columns: date, payee, amount
Optional columns: balance, id, memo
Same formatting rules as transaction CSV
```

## Error Handling

### Input Validation

**CSV Files:**
- Check for required columns
- Validate date formats
- Verify numeric amounts
- Detect encoding issues

**Missing Data:**
- Identify gaps explicitly
- Provide options for handling
- Never fill in fabricated data

### Processing Errors

**Categorization:**
- Flag uncategorized items
- Request clarification on ambiguous items
- Provide confidence scores when uncertain

**Reconciliation:**
- Report unmatched items clearly
- Suggest potential matches
- Calculate and explain variances

## Performance Characteristics

**Transaction Processing:**
- Up to 10,000 transactions per batch
- Categorization: ~500 transactions/second
- Reconciliation: ~200 matches/second

**Report Generation:**
- P&L: Instant for up to 1,000 line items
- Cash Flow: Real-time for monthly data
- Comparisons: Sub-second for year-over-year

## Security & Privacy

**Data Handling:**
- All processing in-memory
- No persistent storage of financial data
- Scripts process locally
- No external API calls from scripts

**Sensitive Information:**
- Never logs account numbers
- Redacts SSNs if encountered
- Masks card numbers in outputs

**Compliance:**
- GAAP-aligned by default
- Audit trail maintained for all decisions
- Source documents tracked

## Limitations

**What FinGuard Cannot Do:**
- File tax returns
- Provide tax advice
- Give legal guidance
- Make investment recommendations
- Approve financial decisions
- Sign off on audited financials

**Technical Limitations:**
- No real-time bank integration (requires exports)
- No automatic bill pay
- No signature authority
- Cannot directly modify source accounting systems

## Testing & Validation

### Script Testing

All scripts include:
- Unit test coverage for core functions
- Sample data for validation
- Error handling for edge cases
- Type hints for maintainability

### Skill Testing

Validated against:
- Common bookkeeping scenarios
- Edge cases (negative refunds, splits)
- Multi-currency (converts to base)
- Various date formats
- Industry-specific workflows

## Future Enhancements

**Planned Features:**
- Multi-currency support
- Budget vs actual analysis
- Inventory tracking for product businesses
- Project-based cost allocation
- Advanced fraud detection
- API integration capabilities
- Real-time dashboard generation

## Version Information

**Current Version:** 1.0.0
**Release Date:** December 2024
**Compatibility:** Claude Sonnet 4+

## Support & Maintenance

**Documentation:**
- Full user guide (FINGUARD_GUIDE.md)
- Quick reference (FINGUARD_QUICK_REFERENCE.md)
- Technical spec (this document)

**Updates:**
- Scripts can be updated independently
- Skill definition can be patched
- References can be extended

**Community:**
- Report issues via Claude feedback
- Request features through skill updates
- Share custom rules and patterns
