#!/usr/bin/env python3
"""
Transaction Categorization Script
Automatically categorizes financial transactions based on payee, amount, and patterns.
"""

import pandas as pd
import re
from typing import Dict, List, Tuple
from datetime import datetime

class TransactionCategorizer:
    """Categorizes financial transactions based on rules and patterns."""
    
    def __init__(self):
        self.rules = self._initialize_rules()
        self.uncategorized = []
        
    def _initialize_rules(self) -> Dict[str, List[Tuple[str, str]]]:
        """Initialize categorization rules."""
        return {
            # Revenue patterns
            'revenue': [
                (r'stripe|paypal|square|venmo|shopify', 'Sales / Service'),
                (r'refund|return', 'Refunds & Discounts'),
                (r'interest|dividend', 'Other Income'),
            ],
            
            # COGS patterns
            'cogs': [
                (r'upwork|fiverr|toptal|freelancer', 'Subcontractors'),
                (r'stripe fee|paypal fee|processing fee', 'Payment Processing Fees'),
                (r'inventory|materials|supplies|raw', 'Materials & Supplies'),
            ],
            
            # Operating Expenses patterns
            'opex': [
                (r'gusto|adp|payroll|paychex|rippling', 'Payroll & Benefits'),
                (r'google ads|facebook ads|linkedin ads|marketing', 'Marketing & Advertising'),
                (r'aws|azure|openai|vercel|github|software|saas', 'Software & Tools'),
                (r'amazon|office depot|staples|supplies', 'Office Expenses'),
                (r'hotel|airbnb|uber|lyft|airline|restaurant', 'Travel & Meals'),
                (r'rent|lease|utilities|electric|gas|water|internet', 'Rent & Utilities'),
                (r'lawyer|attorney|accountant|cpa|consultant', 'Professional Fees'),
            ],
        }
    
    def categorize_transaction(self, payee: str, description: str, amount: float) -> str:
        """
        Categorize a single transaction.
        
        Args:
            payee: The payee/merchant name
            description: Transaction description
            amount: Transaction amount (positive for income, negative for expense)
            
        Returns:
            Category name
        """
        text = f"{payee} {description}".lower()
        
        # Check all rule categories
        for category_type, patterns in self.rules.items():
            for pattern, category in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    return category
        
        # Flag for manual review
        return 'Uncategorized - Review Needed'
    
    def categorize_batch(self, transactions_df: pd.DataFrame) -> pd.DataFrame:
        """
        Categorize a batch of transactions from a DataFrame.
        
        Args:
            transactions_df: DataFrame with columns: date, payee, description, amount
            
        Returns:
            DataFrame with added 'category' column
        """
        transactions_df['category'] = transactions_df.apply(
            lambda row: self.categorize_transaction(
                row['payee'], 
                row.get('description', ''), 
                row['amount']
            ),
            axis=1
        )
        
        # Track uncategorized for reporting
        self.uncategorized = transactions_df[
            transactions_df['category'] == 'Uncategorized - Review Needed'
        ].to_dict('records')
        
        return transactions_df
    
    def split_transaction(self, payee: str, amount: float, splits: Dict[str, float]) -> List[Dict]:
        """
        Split a transaction into multiple categories.
        
        Args:
            payee: The payee name
            amount: Total transaction amount
            splits: Dictionary of {category: amount}
            
        Returns:
            List of split transactions
        """
        if abs(sum(splits.values()) - amount) > 0.01:
            raise ValueError(f"Split amounts {sum(splits.values())} don't match total {amount}")
        
        split_transactions = []
        for category, split_amount in splits.items():
            split_transactions.append({
                'payee': payee,
                'amount': split_amount,
                'category': category,
                'split_from': amount
            })
        
        return split_transactions
    
    def add_custom_rule(self, pattern: str, category: str, category_type: str = 'opex'):
        """Add a custom categorization rule."""
        if category_type not in self.rules:
            self.rules[category_type] = []
        self.rules[category_type].append((pattern, category))
    
    def generate_categorization_report(self, transactions_df: pd.DataFrame) -> str:
        """Generate a summary report of categorized transactions."""
        report = []
        report.append("Transaction Categorization Summary")
        report.append("=" * 50)
        report.append(f"\nTotal Transactions: {len(transactions_df)}")
        report.append(f"Date Range: {transactions_df['date'].min()} to {transactions_df['date'].max()}")
        report.append("\nCategories Breakdown:")
        report.append("-" * 50)
        
        category_summary = transactions_df.groupby('category').agg({
            'amount': ['sum', 'count']
        }).round(2)
        
        for category, row in category_summary.iterrows():
            report.append(f"{category:40} ${row['amount']['sum']:12,.2f} ({int(row['amount']['count'])} txns)")
        
        if self.uncategorized:
            report.append("\n⚠️  Uncategorized Transactions Needing Review:")
            report.append("-" * 50)
            for txn in self.uncategorized[:10]:  # Show first 10
                report.append(f"  {txn['date']} | {txn['payee']:30} | ${txn['amount']:10,.2f}")
            if len(self.uncategorized) > 10:
                report.append(f"\n  ... and {len(self.uncategorized) - 10} more")
        
        return "\n".join(report)


def categorize_from_csv(input_file: str, output_file: str = None) -> pd.DataFrame:
    """
    Categorize transactions from a CSV file.
    
    Args:
        input_file: Path to input CSV (must have: date, payee, description, amount)
        output_file: Path to output CSV (optional)
        
    Returns:
        Categorized DataFrame
    """
    # Read transactions
    df = pd.read_csv(input_file)
    required_columns = ['date', 'payee', 'amount']
    
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"CSV must contain columns: {required_columns}")
    
    # Ensure description column exists
    if 'description' not in df.columns:
        df['description'] = ''
    
    # Categorize
    categorizer = TransactionCategorizer()
    categorized_df = categorizer.categorize_batch(df)
    
    # Print report
    print(categorizer.generate_categorization_report(categorized_df))
    
    # Save if output file specified
    if output_file:
        categorized_df.to_csv(output_file, index=False)
        print(f"\n✅ Categorized transactions saved to: {output_file}")
    
    return categorized_df


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python categorize_transactions.py <input.csv> [output.csv]")
        print("\nInput CSV must have columns: date, payee, amount")
        print("Optional columns: description")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    categorize_from_csv(input_file, output_file)
