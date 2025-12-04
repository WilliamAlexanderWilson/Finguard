# Setup Instructions

## Quick Start

### Option 1: Use with Claude AI (Recommended)

1. **Install the Claude Skill:**
   - Download the latest release
   - Open Claude (web, desktop, or mobile)
   - Go to Settings → Skills
   - Click "Add Skill" and upload the `.skill` file
   - Start a new conversation and say "Hey FinGuard"

2. **Upload your financial data:**
   - Export transactions from your bank as CSV
   - Upload to Claude
   - Say: "Categorize these transactions"

### Option 2: Use Python Scripts Standalone

1. **Install Python 3.8+:**
   ```bash
   python --version  # Should be 3.8 or higher
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the scripts:**
   ```bash
   # Categorize transactions
   python skill/scripts/categorize_transactions.py input.csv output.csv
   
   # Reconcile bank account
   python skill/scripts/bank_reconciliation.py statement.csv books.csv 45230.18
   
   # Generate financial reports
   python skill/scripts/generate_financial_reports.py transactions.csv "November 2024"
   ```

## CSV File Format

Your transaction CSV must have these columns:
- `date` - Transaction date (YYYY-MM-DD format)
- `payee` - Merchant/vendor name
- `amount` - Transaction amount (positive for income, negative for expenses)
- `description` - (Optional) Transaction details

Example:
```csv
date,payee,description,amount
2024-11-01,Stripe,Payment processing,2450.00
2024-11-02,AWS,Cloud hosting,-189.23
2024-11-03,Client Corp,Invoice payment,5000.00
```

## Testing

Test with the included sample data:
```bash
python skill/scripts/categorize_transactions.py examples/sample_transactions.csv output.csv
```

## Configuration

### Custom Categorization Rules

Edit `skill/scripts/categorize_transactions.py` and add to the `_initialize_rules()` method:

```python
'opex': [
    # Add your custom patterns here
    (r'your-vendor-name', 'Your Custom Category'),
]
```

### Chart of Accounts

The default chart of accounts is defined in `skill/SKILL.md`. You can customize it by:
1. Modifying the categorization rules in the Python scripts
2. Teaching FinGuard your preferences through conversation

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### CSV parsing errors
- Ensure your CSV has the required columns
- Check date format is YYYY-MM-DD
- Verify amounts are numeric (no currency symbols)

### Categorization seems wrong
- Review the patterns in `categorize_transactions.py`
- Add custom rules for your specific vendors
- The system learns from corrections over time

## Getting Help

- Check the [User Guide](docs/USER_GUIDE.md)
- See [Quick Reference](docs/QUICK_REFERENCE.md) for commands
- Review [Technical Spec](docs/TECHNICAL_SPEC.md) for API details
- Open an issue for bugs or questions

## Next Steps

Once set up:
1. Read the [Implementation Guide](docs/IMPLEMENTATION_GUIDE.md) for a 4-week roadmap
2. Try the examples in [User Guide](docs/USER_GUIDE.md)
3. Customize for your specific business needs
