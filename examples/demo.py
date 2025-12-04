#!/usr/bin/env python3
"""
FinGuard Demo Script
Demonstrates the key features of FinGuard's transaction categorization
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'skill', 'scripts'))

import pandas as pd
from categorize_transactions import TransactionCategorizer

def run_demo():
    """Run a demonstration of FinGuard's capabilities"""
    
    print("=" * 60)
    print("FinGuard Demo - Transaction Categorization")
    print("=" * 60)
    print()
    
    # Load sample data
    sample_file = os.path.join(os.path.dirname(__file__), 'sample_transactions.csv')
    
    if not os.path.exists(sample_file):
        print(f"❌ Sample file not found: {sample_file}")
        print("Please ensure sample_transactions.csv exists in the examples/ directory")
        return
    
    print(f"📁 Loading sample data from: {sample_file}")
    df = pd.read_csv(sample_file)
    print(f"✅ Loaded {len(df)} transactions")
    print()
    
    # Display first few transactions
    print("📋 First 5 transactions:")
    print("-" * 60)
    print(df.head().to_string(index=False))
    print()
    
    # Initialize categorizer
    print("🤖 Initializing FinGuard categorization engine...")
    categorizer = TransactionCategorizer()
    print(f"✅ Loaded {len(categorizer.rules)} rule categories")
    print()
    
    # Categorize
    print("⚙️  Categorizing transactions...")
    categorized_df = categorizer.categorize_batch(df)
    print("✅ Categorization complete!")
    print()
    
    # Show results
    print("📊 CATEGORIZATION RESULTS")
    print("=" * 60)
    print()
    
    # Summary by category
    summary = categorized_df.groupby('category').agg({
        'amount': 'sum',
        'payee': 'count'
    }).round(2)
    summary.columns = ['Total Amount', 'Transaction Count']
    summary = summary.sort_values('Total Amount', ascending=False)
    
    print("By Category:")
    print("-" * 60)
    for category, row in summary.iterrows():
        print(f"  {category:40} ${row['Total Amount']:>12,.2f} ({int(row['Transaction Count'])} txns)")
    
    print()
    print("-" * 60)
    
    # Overall metrics
    revenue = categorized_df[categorized_df['amount'] > 0]['amount'].sum()
    expenses = abs(categorized_df[categorized_df['amount'] < 0]['amount'].sum())
    net = revenue - expenses
    
    print(f"  {'Total Revenue':40} ${revenue:>12,.2f}")
    print(f"  {'Total Expenses':40} ${expenses:>12,.2f}")
    print(f"  {'Net Income':40} ${net:>12,.2f}")
    print("=" * 60)
    print()
    
    # Show any uncategorized
    uncategorized = categorized_df[categorized_df['category'] == 'Uncategorized - Review Needed']
    if len(uncategorized) > 0:
        print("⚠️  UNCATEGORIZED TRANSACTIONS (need review):")
        print("-" * 60)
        for _, row in uncategorized.iterrows():
            print(f"  {row['date']} | {row['payee']:30} | ${row['amount']:>10,.2f}")
        print()
    else:
        print("✅ All transactions successfully categorized!")
        print()
    
    # Generate full report
    print("📄 Generating detailed report...")
    report = categorizer.generate_categorization_report(categorized_df)
    print()
    print(report)
    print()
    
    # Save output
    output_file = os.path.join(os.path.dirname(__file__), 'demo_output.csv')
    categorized_df.to_csv(output_file, index=False)
    print(f"💾 Categorized data saved to: {output_file}")
    print()
    
    print("=" * 60)
    print("Demo complete! ✨")
    print()
    print("Next steps:")
    print("  1. Review the categorization results")
    print("  2. Try with your own transaction data")
    print("  3. Customize rules for your specific vendors")
    print("  4. Install the full Claude skill for AI-powered insights")
    print("=" * 60)

if __name__ == '__main__':
    try:
        run_demo()
    except Exception as e:
        print(f"❌ Error running demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
