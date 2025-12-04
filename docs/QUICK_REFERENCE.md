# FinGuard Quick Reference Card

## What FinGuard Does
AI Accounting & Finance Operations Agent that handles 80-90% of bookkeeping tasks for small-to-medium businesses.

## Activation Triggers
Say things like:
- "Categorize these transactions"
- "Reconcile my bank account"
- "Generate my P&L"
- "Project my cash flow"
- "Run monthly close"
- "Create an invoice"

## Core Capabilities

| Function | What to Say |
|----------|-------------|
| **Categorize Transactions** | "Categorize this CSV" |
| **Bank Reconciliation** | "Reconcile November, ending balance $X" |
| **P&L Report** | "Generate P&L for Q4" |
| **Cash Flow** | "Project cash flow next 8 weeks" |
| **Monthly Close** | "Run monthly close for [Month]" |
| **Invoice Creation** | "Create invoice for [Client] - $[Amount]" |
| **AR Aging** | "Show me AR aging report" |
| **AP Review** | "What bills are due this week?" |

## Output Format
FinGuard always provides:
1. One-Sentence Summary
2. Key Findings
3. Items Needing Attention
4. Insights & Recommendations
5. Accountant Review Needed (if triggered)
6. Questions for You

## Auto-Categorization Rules

| Payee Pattern | Category |
|---------------|----------|
| Stripe, PayPal, Square | Sales / Service |
| Upwork, Fiverr, Toptal | Subcontractors |
| AWS, Vercel, OpenAI | Software & Tools |
| Gusto, ADP, Payroll | Payroll & Benefits |
| Google Ads, Facebook Ads | Marketing & Advertising |
| Amazon, Office Depot | Office Expenses |
| Hotel, Uber, Airline | Travel & Meals |

## Escalation Triggers
FinGuard automatically flags:
- ⚠️ Transactions ≥$10,000 to new payees
- ⚠️ Negative cash projected in 30 days
- ⚠️ Fraud indicators (duplicates, weekend wires, round amounts)
- ⚠️ 1099 contractors ≥$600 YTD
- ⚠️ Sales tax nexus concerns

## File Formats Supported
- CSV (bank statements, transactions)
- PDF (invoices, receipts, statements)
- Excel/XLSX (financial data)
- Payroll reports (Gusto, ADP, etc.)

## Chart of Accounts
**Revenue:** Sales/Service, Refunds, Other Income  
**COGS:** Materials, Subcontractors, Processing Fees  
**OpEx:** Payroll, Marketing, Software, Office, Travel, Rent, Professional Fees

## Python Scripts Included

```bash
# Auto-categorize transactions
python categorize_transactions.py input.csv output.csv

# Reconcile bank account
python bank_reconciliation.py statement.csv books.csv ending_balance

# Generate financial reports
python generate_financial_reports.py transactions.csv "Period Name"
```

## Monthly Close Checklist
FinGuard handles:
- ✓ Bank & card reconciliation
- ✓ Payroll reconciliation
- ✓ AR aging summary
- ✓ AP summary
- ✓ Transaction review
- ✓ Net profit calculation
- ✓ Insights & recommendations

## Key Behaviors

**Uncertainty = Pause**  
FinGuard never guesses. If data is unclear, it asks.

**Self-Audit Mode**  
Every output is checked for:
- Totals = Subtotals?
- Debits = Credits?
- Consistency across periods?

**Industry Adaptive**  
Auto-adjusts for E-commerce, SaaS, Retail, Restaurants, Services

**Memory Enabled**  
Remembers preferences, never re-asks known information

## What FinGuard Is NOT
- ❌ Not a CPA
- ❌ Not tax advice
- ❌ Not legal advice
- ❌ Not a replacement for human judgment

## Tips for Success
1. Be specific with requests
2. Provide complete data files
3. Tell FinGuard your industry
4. Review recommendations before acting
5. Use consistently for best learning

## Contact Style
- Professional but warm
- Plain English (technical terms explained)
- Light, dry humor when appropriate
- Never panics

---

**Need Help?** Just ask: "FinGuard, how do I [task]?"
