# FinGuard - AI Accounting & Finance Operations Agent
## Installation & Usage Guide

## What is FinGuard?

FinGuard is a custom AI skill that transforms Claude into a specialized accounting and finance operations agent for small-to-medium businesses. It handles 80-90% of day-to-day bookkeeping tasks, allowing one human accountant to oversee everything instead of an entire team.

## Features

✅ **Bookkeeping & Transaction Processing**
- Automatic categorization of bank feeds, credit cards, payment processors
- Strict consistent rules based on standard Chart of Accounts
- Never leaves transactions uncategorized

✅ **Bank & Credit Card Reconciliation**
- Matches transactions to invoices, bills, and payroll
- Flags duplicates and unexplained variances
- Produces plain-English reconciliation summaries

✅ **Accounts Receivable (AR)**
- Creates and drafts invoices
- Tracks aging and sends reminders
- Suggests payment plans

✅ **Accounts Payable (AP)**
- Extracts data from vendor invoices
- Schedules payments by due date
- Flags suspicious bills

✅ **Payroll Coordination**
- Ingests reports from Gusto, ADP, Rippling, Justworks
- Maps wages, taxes, benefits to correct accounts
- Warns about anomalies

✅ **Financial Reporting**
- Monthly P&L, Balance Sheet, Cash Flow
- Month-over-month and year-over-year comparisons
- Plain English explanations with KPIs

✅ **Cash Flow Forecasting**
- 4-12 week projections
- Highlights negative cash weeks
- Suggests concrete actions

✅ **Anomaly & Risk Detection**
- Unusual spending spikes
- New large vendors
- Potential fraud indicators

## How to Install

### Step 1: Download the Skill
You've already generated the skill file: `finguard.skill`

### Step 2: Install in Claude
1. Open Claude (web, desktop, or mobile)
2. Go to Settings → Skills
3. Click "Add Skill" or "Upload Skill"
4. Select the `finguard.skill` file
5. Confirm installation

### Step 3: Verify Installation
After installation, you should see "finguard" listed in your Skills. The skill will automatically activate when you ask Claude accounting or finance-related questions.

## How to Use FinGuard

### First Time Setup

When you first interact with FinGuard, it will ask you for:
- Bank and credit card connection details
- Payment processors (Stripe, PayPal, etc.)
- Payroll provider
- Key preferences (cash vs accrual, sales tax, contractors)

### Common Use Cases

#### 1. Categorize Transactions
```
"Here's my bank statement CSV. Please categorize all transactions."
```

FinGuard will:
- Auto-categorize based on smart rules
- Flag uncertain items for your review
- Provide a summary report

#### 2. Reconcile Bank Account
```
"Reconcile my November bank statement. Ending balance was $45,230.18"
```

FinGuard will:
- Match statement to your books
- Find discrepancies
- Identify potential duplicates
- Generate reconciliation report

#### 3. Generate Financial Reports
```
"Generate my P&L for Q4 2024"
```

FinGuard will:
- Create Profit & Loss statement
- Show revenue, COGS, expenses
- Calculate margins and KPIs
- Provide 2-3 sentence insights

#### 4. Cash Flow Forecasting
```
"Project my cash flow for the next 8 weeks"
```

FinGuard will:
- Forecast based on current cash, AR, AP
- Highlight weeks with negative cash
- Suggest actions (chase invoices, delay payments)

#### 5. Monthly Close
```
"Run the monthly close for November"
```

FinGuard will:
- Reconcile all accounts
- Review AR and AP aging
- Check for uncategorized transactions
- Calculate net profit
- Provide summary and insights

#### 6. Invoice Management
```
"Create an invoice for Acme Corp - $5,000 for consulting services"
```

FinGuard will:
- Draft the invoice
- Track in AR aging
- Set up payment reminders

### Working with Files

FinGuard can process:
- CSV exports from banks and accounting software
- PDF invoices and receipts
- Excel spreadsheets
- Payroll reports

Just upload the files and tell FinGuard what you need.

## Automated Scripts

FinGuard includes three powerful Python scripts:

### 1. Transaction Categorization
```bash
python categorize_transactions.py transactions.csv output.csv
```
- Auto-categorizes based on payee/description
- Generates summary report
- Flags uncategorized items

### 2. Bank Reconciliation
```bash
python bank_reconciliation.py statement.csv books.csv 45230.18
```
- Matches statement to books
- Finds exact and fuzzy matches
- Detects duplicates
- Calculates variance

### 3. Financial Reports
```bash
python generate_financial_reports.py transactions.csv "November 2024"
```
- Generates P&L
- Generates Cash Flow Statement
- Calculates KPIs

## FinGuard's Personality

FinGuard speaks like a trusted senior bookkeeper:
- Professional yet warm
- Uses contractions and plain English
- Explains technical terms in parentheses
- Never panics, even when finding mistakes
- Light dry humor when appropriate

## Advanced Features

### Industry Adaptation
FinGuard automatically adjusts for:
- E-commerce (inventory, fulfillment fees)
- SaaS (deferred revenue, MRR/ARR)
- Retail (daily sales, cash variances)
- Restaurants (tips, food/alcohol splits)
- Service businesses (labor COGS, milestone billing)

### Self-Audit Mode
FinGuard checks its own work:
- Verifies totals match subtotals
- Ensures debits equal credits
- Confirms consistency across periods
- Proactively corrects errors

### Automatic Escalation
FinGuard flags for human review:
- Transactions ≥$10,000 to new payees
- Projected negative cash in 30 days
- Fraud indicators
- Revenue recognition ambiguity
- 1099 contractors over $600
- Sales tax nexus concerns

## Chart of Accounts

FinGuard uses this default structure:

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

You can customize this to match your business.

## Data Security & Ethics

FinGuard follows strict guidelines:
- Never fabricates numbers
- Always identifies missing data
- Labels estimates clearly
- Defaults to GAAP-like treatment
- Does not provide tax or legal advice
- Flags high-impact items for human review
- Maintains conservative, truthful approach

## Tips for Best Results

1. **Be Specific**: "Reconcile my Chase business checking for November" is better than "reconcile my account"

2. **Provide Context**: Tell FinGuard your industry, accounting method (cash/accrual), and any special situations

3. **Upload Complete Data**: Provide full bank statements, not partial exports

4. **Review Recommendations**: FinGuard is designed to assist, not replace, human judgment

5. **Use Consistently**: FinGuard remembers preferences and gets better over time

## Troubleshooting

**FinGuard isn't activating:**
- Make sure the skill is installed and enabled
- Use keywords like "bookkeeping," "reconcile," "P&L," "finances"

**Categorizations seem off:**
- Tell FinGuard your specific business type
- Provide examples of correct categorizations
- Ask to add custom rules

**Reports don't match expectations:**
- Verify your data files have the required columns
- Check date ranges are correct
- Confirm your accounting method (cash vs accrual)

## Support & Feedback

FinGuard is designed to learn and improve. If you encounter issues or have suggestions:
- Use the thumbs down button in Claude to provide feedback
- Describe what you expected vs. what you got
- Share examples of edge cases

## What FinGuard Can't Do

FinGuard is not a CPA and cannot:
- File tax returns
- Provide tax advice
- Give legal advice
- Make financial predictions without data
- Replace human judgment on complex matters

Always consult with a licensed professional for tax and legal matters.

---

## Quick Start Checklist

- [ ] Install finguard.skill in Claude
- [ ] Verify skill is active in Settings
- [ ] Upload your first bank statement or transaction file
- [ ] Tell FinGuard your business type and preferences
- [ ] Review the initial categorization
- [ ] Set up monthly close routine
- [ ] Integrate with your accounting workflow

**You're ready to go! FinGuard is now your AI accounting co-pilot.**
