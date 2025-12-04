#!/usr/bin/env python3
"""
Financial Report Generation Script
Generates P&L, Balance Sheet, and Cash Flow reports.
"""

import pandas as pd
from datetime import datetime
from typing import Dict, Tuple
from collections import defaultdict

class FinancialReporter:
    """Generates standard financial reports."""
    
    def __init__(self):
        self.chart_of_accounts = self._initialize_coa()
        
    def _initialize_coa(self) -> Dict[str, str]:
        """Initialize chart of accounts mapping."""
        return {
            # Revenue
            'Sales / Service': 'Revenue',
            'Refunds & Discounts': 'Revenue',
            'Other Income': 'Revenue',
            
            # COGS
            'Materials & Supplies': 'COGS',
            'Subcontractors': 'COGS',
            'Payment Processing Fees': 'COGS',
            
            # Operating Expenses
            'Payroll & Benefits': 'Operating Expenses',
            'Marketing & Advertising': 'Operating Expenses',
            'Software & Tools': 'Operating Expenses',
            'Office Expenses': 'Operating Expenses',
            'Travel & Meals': 'Operating Expenses',
            'Rent & Utilities': 'Operating Expenses',
            'Professional Fees': 'Operating Expenses',
            'Other OpEx': 'Operating Expenses',
        }
    
    def generate_profit_loss(self, transactions_df: pd.DataFrame, period_name: str = "") -> str:
        """
        Generate Profit & Loss (Income Statement).
        
        Args:
            transactions_df: DataFrame with columns: date, category, amount
            period_name: Name of the period (e.g., "November 2024")
            
        Returns:
            Formatted P&L report
        """
        # Group by category
        by_category = transactions_df.groupby('category')['amount'].sum()
        
        # Categorize into statement sections
        revenue = 0
        cogs = 0
        opex = defaultdict(float)
        
        for category, amount in by_category.items():
            section = self.chart_of_accounts.get(category, 'Other OpEx')
            
            if section == 'Revenue':
                revenue += amount
            elif section == 'COGS':
                cogs += abs(amount)  # COGS is typically negative
            elif section == 'Operating Expenses':
                opex[category] = abs(amount)
        
        # Calculate totals
        gross_profit = revenue - cogs
        total_opex = sum(opex.values())
        net_income = gross_profit - total_opex
        
        # Build report
        report = []
        report.append("=" * 60)
        report.append(f"PROFIT & LOSS STATEMENT")
        if period_name:
            report.append(f"Period: {period_name}")
        report.append("=" * 60)
        report.append("")
        
        # Revenue section
        report.append("REVENUE")
        report.append("-" * 60)
        for category, amount in by_category.items():
            if self.chart_of_accounts.get(category) == 'Revenue':
                report.append(f"  {category:45} ${amount:>12,.2f}")
        report.append(f"{'Total Revenue':45} ${revenue:>12,.2f}")
        report.append("")
        
        # COGS section
        report.append("COST OF GOODS SOLD")
        report.append("-" * 60)
        for category, amount in by_category.items():
            if self.chart_of_accounts.get(category) == 'COGS':
                report.append(f"  {category:45} ${abs(amount):>12,.2f}")
        report.append(f"{'Total COGS':45} ${cogs:>12,.2f}")
        report.append("")
        
        # Gross Profit
        report.append(f"{'GROSS PROFIT':45} ${gross_profit:>12,.2f}")
        gross_margin = (gross_profit / revenue * 100) if revenue > 0 else 0
        report.append(f"{'Gross Margin':45} {gross_margin:>12.1f}%")
        report.append("")
        
        # Operating Expenses
        report.append("OPERATING EXPENSES")
        report.append("-" * 60)
        for category, amount in sorted(opex.items(), key=lambda x: x[1], reverse=True):
            report.append(f"  {category:45} ${amount:>12,.2f}")
        report.append(f"{'Total Operating Expenses':45} ${total_opex:>12,.2f}")
        report.append("")
        
        # Net Income
        report.append("=" * 60)
        report.append(f"{'NET INCOME':45} ${net_income:>12,.2f}")
        net_margin = (net_income / revenue * 100) if revenue > 0 else 0
        report.append(f"{'Net Margin':45} {net_margin:>12.1f}%")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def generate_cash_flow(self, transactions_df: pd.DataFrame, period_name: str = "") -> str:
        """
        Generate Cash Flow Statement.
        
        Args:
            transactions_df: DataFrame with columns: date, category, amount
            period_name: Name of the period
            
        Returns:
            Formatted cash flow report
        """
        # Sort by date
        df_sorted = transactions_df.sort_values('date')
        
        # Calculate running balance
        df_sorted['running_balance'] = df_sorted['amount'].cumsum()
        
        starting_balance = 0  # Assume starting at 0 or get from previous period
        ending_balance = df_sorted['running_balance'].iloc[-1]
        
        # Categorize cash flows
        operating = 0
        investing = 0
        financing = 0
        
        for _, row in df_sorted.iterrows():
            category = row['category']
            amount = row['amount']
            
            # Simple categorization (can be enhanced)
            if 'Equipment' in category or 'Asset' in category:
                investing += amount
            elif 'Loan' in category or 'Equity' in category:
                financing += amount
            else:
                operating += amount
        
        # Build report
        report = []
        report.append("=" * 60)
        report.append(f"CASH FLOW STATEMENT")
        if period_name:
            report.append(f"Period: {period_name}")
        report.append("=" * 60)
        report.append("")
        
        report.append(f"Beginning Cash Balance:     ${starting_balance:>12,.2f}")
        report.append("")
        
        report.append("OPERATING ACTIVITIES")
        report.append("-" * 60)
        report.append(f"  Net cash from operations   ${operating:>12,.2f}")
        report.append("")
        
        report.append("INVESTING ACTIVITIES")
        report.append("-" * 60)
        report.append(f"  Net cash from investing    ${investing:>12,.2f}")
        report.append("")
        
        report.append("FINANCING ACTIVITIES")
        report.append("-" * 60)
        report.append(f"  Net cash from financing    ${financing:>12,.2f}")
        report.append("")
        
        net_change = operating + investing + financing
        report.append("=" * 60)
        report.append(f"Net Change in Cash:         ${net_change:>12,.2f}")
        report.append(f"Ending Cash Balance:        ${ending_balance:>12,.2f}")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def generate_monthly_comparison(
        self, 
        current_df: pd.DataFrame, 
        previous_df: pd.DataFrame,
        current_month: str,
        previous_month: str
    ) -> str:
        """
        Generate month-over-month comparison.
        
        Args:
            current_df: Current month transactions
            previous_df: Previous month transactions
            current_month: Name of current month
            previous_month: Name of previous month
            
        Returns:
            Formatted comparison report
        """
        # Calculate totals for each month
        current_by_cat = current_df.groupby('category')['amount'].sum()
        previous_by_cat = previous_df.groupby('category')['amount'].sum()
        
        # Get all categories
        all_categories = set(current_by_cat.index) | set(previous_by_cat.index)
        
        # Build comparison
        report = []
        report.append("=" * 80)
        report.append(f"MONTH-OVER-MONTH COMPARISON")
        report.append(f"{previous_month} vs {current_month}")
        report.append("=" * 80)
        report.append("")
        report.append(f"{'Category':35} {previous_month:>15} {current_month:>15} {'Change':>12}")
        report.append("-" * 80)
        
        for category in sorted(all_categories):
            prev_amount = previous_by_cat.get(category, 0)
            curr_amount = current_by_cat.get(category, 0)
            change = curr_amount - prev_amount
            change_pct = (change / prev_amount * 100) if prev_amount != 0 else 0
            
            report.append(
                f"{category:35} ${prev_amount:>13,.2f} ${curr_amount:>13,.2f} "
                f"${change:>10,.2f} ({change_pct:>5.1f}%)"
            )
        
        # Totals
        prev_total = previous_df['amount'].sum()
        curr_total = current_df['amount'].sum()
        total_change = curr_total - prev_total
        total_change_pct = (total_change / prev_total * 100) if prev_total != 0 else 0
        
        report.append("=" * 80)
        report.append(
            f"{'TOTAL':35} ${prev_total:>13,.2f} ${curr_total:>13,.2f} "
            f"${total_change:>10,.2f} ({total_change_pct:>5.1f}%)"
        )
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def generate_kpis(self, transactions_df: pd.DataFrame) -> str:
        """Generate key performance indicators."""
        # Calculate KPIs
        revenue = transactions_df[
            transactions_df['category'].str.contains('Sales|Service|Income', na=False)
        ]['amount'].sum()
        
        expenses = abs(transactions_df[transactions_df['amount'] < 0]['amount'].sum())
        net_income = revenue - expenses
        
        avg_daily_revenue = revenue / 30 if len(transactions_df) > 0 else 0
        avg_transaction = transactions_df['amount'].mean()
        
        # Build report
        report = []
        report.append("KEY PERFORMANCE INDICATORS")
        report.append("-" * 60)
        report.append(f"Total Revenue:              ${revenue:>12,.2f}")
        report.append(f"Total Expenses:             ${expenses:>12,.2f}")
        report.append(f"Net Income:                 ${net_income:>12,.2f}")
        report.append(f"Average Daily Revenue:      ${avg_daily_revenue:>12,.2f}")
        report.append(f"Average Transaction:        ${avg_transaction:>12,.2f}")
        report.append(f"Number of Transactions:     {len(transactions_df):>12}")
        
        if revenue > 0:
            report.append(f"Net Margin:                 {(net_income/revenue*100):>11.1f}%")
        
        return "\n".join(report)


def generate_reports_from_csv(transactions_file: str, period_name: str = ""):
    """Generate all reports from a transactions CSV."""
    # Read transactions
    df = pd.read_csv(transactions_file)
    
    # Initialize reporter
    reporter = FinancialReporter()
    
    # Generate reports
    print("\n")
    print(reporter.generate_profit_loss(df, period_name))
    print("\n\n")
    print(reporter.generate_cash_flow(df, period_name))
    print("\n\n")
    print(reporter.generate_kpis(df))
    print("\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python generate_financial_reports.py <transactions.csv> [period_name]")
        print("\nTransactions CSV must have columns: date, category, amount")
        sys.exit(1)
    
    transactions_file = sys.argv[1]
    period_name = sys.argv[2] if len(sys.argv) > 2 else ""
    
    generate_reports_from_csv(transactions_file, period_name)
