#!/usr/bin/env python3
"""
Bank Reconciliation Script
Matches bank statement transactions with accounting records.
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import hashlib

class BankReconciliation:
    """Performs bank reconciliation between statement and books."""
    
    def __init__(self, tolerance: float = 0.01):
        """
        Initialize reconciliation.
        
        Args:
            tolerance: Amount tolerance for matching (default $0.01)
        """
        self.tolerance = tolerance
        self.matches = []
        self.statement_only = []
        self.books_only = []
        self.duplicates = []
        
    def _generate_txn_hash(self, date: str, amount: float, payee: str) -> str:
        """Generate a hash for transaction matching."""
        key = f"{date}_{amount:.2f}_{payee}".lower()
        return hashlib.md5(key.encode()).hexdigest()
    
    def find_exact_matches(self, statement_df: pd.DataFrame, books_df: pd.DataFrame) -> Tuple[List, pd.DataFrame, pd.DataFrame]:
        """
        Find exact matches between statement and books.
        
        Args:
            statement_df: Bank statement transactions
            books_df: Accounting books transactions
            
        Returns:
            Tuple of (matches, unmatched_statement, unmatched_books)
        """
        # Add transaction hashes
        statement_df['txn_hash'] = statement_df.apply(
            lambda row: self._generate_txn_hash(row['date'], row['amount'], row['payee']),
            axis=1
        )
        books_df['txn_hash'] = books_df.apply(
            lambda row: self._generate_txn_hash(row['date'], row['amount'], row['payee']),
            axis=1
        )
        
        # Find matches
        matched_hashes = set(statement_df['txn_hash']) & set(books_df['txn_hash'])
        
        matches = []
        for txn_hash in matched_hashes:
            stmt_row = statement_df[statement_df['txn_hash'] == txn_hash].iloc[0]
            book_row = books_df[books_df['txn_hash'] == txn_hash].iloc[0]
            
            matches.append({
                'date': stmt_row['date'],
                'payee': stmt_row['payee'],
                'amount': stmt_row['amount'],
                'statement_id': stmt_row.get('id', ''),
                'books_id': book_row.get('id', ''),
                'status': 'Matched'
            })
        
        # Unmatched transactions
        unmatched_statement = statement_df[~statement_df['txn_hash'].isin(matched_hashes)]
        unmatched_books = books_df[~books_df['txn_hash'].isin(matched_hashes)]
        
        return matches, unmatched_statement, unmatched_books
    
    def find_fuzzy_matches(self, statement_df: pd.DataFrame, books_df: pd.DataFrame, days_window: int = 3) -> List[Dict]:
        """
        Find fuzzy matches (same amount, nearby dates, similar payee).
        
        Args:
            statement_df: Unmatched statement transactions
            books_df: Unmatched books transactions
            days_window: Days to look forward/backward for date matching
            
        Returns:
            List of potential matches for review
        """
        potential_matches = []
        
        for _, stmt_row in statement_df.iterrows():
            stmt_date = pd.to_datetime(stmt_row['date'])
            stmt_amount = float(stmt_row['amount'])
            
            # Find transactions with same amount within date window
            date_min = stmt_date - timedelta(days=days_window)
            date_max = stmt_date + timedelta(days=days_window)
            
            candidates = books_df[
                (pd.to_datetime(books_df['date']) >= date_min) &
                (pd.to_datetime(books_df['date']) <= date_max) &
                (abs(books_df['amount'] - stmt_amount) <= self.tolerance)
            ]
            
            for _, book_row in candidates.iterrows():
                similarity_score = self._calculate_similarity(
                    stmt_row['payee'], 
                    book_row['payee']
                )
                
                if similarity_score > 0.6:  # 60% similar
                    potential_matches.append({
                        'statement_date': stmt_row['date'],
                        'statement_payee': stmt_row['payee'],
                        'statement_amount': stmt_amount,
                        'books_date': book_row['date'],
                        'books_payee': book_row['payee'],
                        'books_amount': float(book_row['amount']),
                        'similarity': similarity_score,
                        'status': 'Potential Match - Review Needed'
                    })
        
        return potential_matches
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate string similarity (simple implementation)."""
        text1 = text1.lower()
        text2 = text2.lower()
        
        # Exact match
        if text1 == text2:
            return 1.0
        
        # Contains match
        if text1 in text2 or text2 in text1:
            return 0.8
        
        # Word overlap
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        overlap = len(words1 & words2)
        return overlap / max(len(words1), len(words2))
    
    def detect_duplicates(self, df: pd.DataFrame) -> List[Dict]:
        """Detect potential duplicate transactions."""
        duplicates = []
        
        # Group by date and amount
        grouped = df.groupby(['date', 'amount'])
        
        for (date, amount), group in grouped:
            if len(group) > 1:
                # Check if payees are similar
                payees = group['payee'].tolist()
                for i in range(len(payees)):
                    for j in range(i + 1, len(payees)):
                        if self._calculate_similarity(payees[i], payees[j]) > 0.7:
                            duplicates.append({
                                'date': date,
                                'amount': amount,
                                'payee_1': payees[i],
                                'payee_2': payees[j],
                                'flag': 'Potential Duplicate'
                            })
        
        return duplicates
    
    def generate_reconciliation_report(
        self, 
        statement_df: pd.DataFrame, 
        books_df: pd.DataFrame,
        statement_ending_balance: float
    ) -> str:
        """Generate a comprehensive reconciliation report."""
        
        # Perform reconciliation
        exact_matches, unmatched_stmt, unmatched_books = self.find_exact_matches(
            statement_df.copy(), 
            books_df.copy()
        )
        
        fuzzy_matches = self.find_fuzzy_matches(unmatched_stmt, unmatched_books)
        
        # Detect duplicates
        stmt_duplicates = self.detect_duplicates(statement_df)
        book_duplicates = self.detect_duplicates(books_df)
        
        # Build report
        report = []
        report.append("=" * 60)
        report.append("BANK RECONCILIATION REPORT")
        report.append("=" * 60)
        report.append(f"Statement Period: {statement_df['date'].min()} to {statement_df['date'].max()}")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Summary
        report.append("SUMMARY")
        report.append("-" * 60)
        report.append(f"Statement Transactions: {len(statement_df):>10}")
        report.append(f"Books Transactions:     {len(books_df):>10}")
        report.append(f"Exact Matches:          {len(exact_matches):>10}")
        report.append(f"Potential Matches:      {len(fuzzy_matches):>10}")
        report.append(f"Statement Only:         {len(unmatched_stmt):>10}")
        report.append(f"Books Only:             {len(unmatched_books):>10}")
        report.append("")
        
        # Balance reconciliation
        report.append("BALANCE RECONCILIATION")
        report.append("-" * 60)
        report.append(f"Statement Ending Balance:     ${statement_ending_balance:>12,.2f}")
        
        # Outstanding checks (in books but not statement)
        outstanding_checks = unmatched_books[unmatched_books['amount'] < 0]['amount'].sum()
        report.append(f"Less: Outstanding Checks:     ${outstanding_checks:>12,.2f}")
        
        # Deposits in transit (in books but not statement)  
        deposits_in_transit = unmatched_books[unmatched_books['amount'] > 0]['amount'].sum()
        report.append(f"Plus: Deposits in Transit:    ${deposits_in_transit:>12,.2f}")
        
        adjusted_balance = statement_ending_balance + outstanding_checks + deposits_in_transit
        report.append(f"Adjusted Balance:             ${adjusted_balance:>12,.2f}")
        report.append("")
        
        book_balance = books_df['amount'].sum()
        report.append(f"Book Balance:                 ${book_balance:>12,.2f}")
        
        variance = adjusted_balance - book_balance
        report.append(f"Variance:                     ${variance:>12,.2f}")
        
        if abs(variance) < 0.01:
            report.append("\n✅ Books are RECONCILED")
        else:
            report.append("\n⚠️  VARIANCE DETECTED - Investigation Needed")
        
        report.append("")
        
        # Items needing attention
        if len(unmatched_stmt) > 0:
            report.append("⚠️  TRANSACTIONS ON STATEMENT BUT NOT IN BOOKS")
            report.append("-" * 60)
            for _, row in unmatched_stmt.head(10).iterrows():
                report.append(f"  {row['date']} | {row['payee']:30} | ${row['amount']:>10,.2f}")
            if len(unmatched_stmt) > 10:
                report.append(f"  ... and {len(unmatched_stmt) - 10} more")
            report.append("")
        
        if len(unmatched_books) > 0:
            report.append("⚠️  TRANSACTIONS IN BOOKS BUT NOT ON STATEMENT")
            report.append("-" * 60)
            for _, row in unmatched_books.head(10).iterrows():
                report.append(f"  {row['date']} | {row['payee']:30} | ${row['amount']:>10,.2f}")
            if len(unmatched_books) > 10:
                report.append(f"  ... and {len(unmatched_books) - 10} more")
            report.append("")
        
        if len(fuzzy_matches) > 0:
            report.append("🔍 POTENTIAL MATCHES FOR REVIEW")
            report.append("-" * 60)
            for match in fuzzy_matches[:10]:
                report.append(f"  Statement: {match['statement_date']} | {match['statement_payee']}")
                report.append(f"  Books:     {match['books_date']} | {match['books_payee']}")
                report.append(f"  Amount: ${match['statement_amount']:.2f} | Similarity: {match['similarity']:.1%}")
                report.append("")
            if len(fuzzy_matches) > 10:
                report.append(f"  ... and {len(fuzzy_matches) - 10} more")
        
        if stmt_duplicates or book_duplicates:
            report.append("⚠️  POTENTIAL DUPLICATES DETECTED")
            report.append("-" * 60)
            for dup in (stmt_duplicates + book_duplicates)[:5]:
                report.append(f"  {dup['date']} | ${dup['amount']:.2f}")
                report.append(f"    {dup['payee_1']} vs {dup['payee_2']}")
            report.append("")
        
        return "\n".join(report)


def reconcile_from_csv(statement_file: str, books_file: str, ending_balance: float):
    """
    Reconcile bank statement and books from CSV files.
    
    Args:
        statement_file: Path to bank statement CSV
        books_file: Path to accounting books CSV  
        ending_balance: Ending balance from bank statement
    """
    # Read files
    statement_df = pd.read_csv(statement_file)
    books_df = pd.read_csv(books_file)
    
    # Perform reconciliation
    reconciler = BankReconciliation()
    report = reconciler.generate_reconciliation_report(
        statement_df, 
        books_df, 
        ending_balance
    )
    
    print(report)
    
    return reconciler


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python bank_reconciliation.py <statement.csv> <books.csv> <ending_balance>")
        print("\nBoth CSVs must have columns: date, payee, amount")
        sys.exit(1)
    
    statement_file = sys.argv[1]
    books_file = sys.argv[2]
    ending_balance = float(sys.argv[3])
    
    reconcile_from_csv(statement_file, books_file, ending_balance)
