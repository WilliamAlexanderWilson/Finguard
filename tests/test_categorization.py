#!/usr/bin/env python3
"""
Basic tests for FinGuard transaction categorization
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'skill', 'scripts'))

import pandas as pd
from categorize_transactions import TransactionCategorizer

def test_categorization_rules():
    """Test that basic categorization rules work"""
    categorizer = TransactionCategorizer()
    
    # Test Stripe revenue
    assert categorizer.categorize_transaction('Stripe', 'Payment', 100.0) == 'Sales / Service'
    
    # Test Upwork contractor
    assert categorizer.categorize_transaction('Upwork', 'Freelancer payment', -500.0) == 'Subcontractors'
    
    # Test AWS software
    assert categorizer.categorize_transaction('AWS', 'Cloud hosting', -200.0) == 'Software & Tools'
    
    # Test Gusto payroll
    assert categorizer.categorize_transaction('Gusto', 'Payroll run', -5000.0) == 'Payroll & Benefits'
    
    print("✅ All categorization tests passed!")

def test_batch_processing():
    """Test batch processing of transactions"""
    categorizer = TransactionCategorizer()
    
    # Create sample data
    data = {
        'date': ['2024-11-01', '2024-11-02', '2024-11-03'],
        'payee': ['Stripe', 'AWS', 'Upwork'],
        'description': ['Payment', 'Hosting', 'Design work'],
        'amount': [1000.0, -100.0, -500.0]
    }
    df = pd.DataFrame(data)
    
    # Categorize
    result = categorizer.categorize_batch(df)
    
    # Verify
    assert 'category' in result.columns
    assert len(result) == 3
    assert result.iloc[0]['category'] == 'Sales / Service'
    assert result.iloc[1]['category'] == 'Software & Tools'
    assert result.iloc[2]['category'] == 'Subcontractors'
    
    print("✅ Batch processing test passed!")

def test_custom_rules():
    """Test adding custom categorization rules"""
    categorizer = TransactionCategorizer()
    
    # Add custom rule
    categorizer.add_custom_rule(
        pattern=r'custom-vendor',
        category='Custom Category',
        category_type='opex'
    )
    
    # Test it works
    result = categorizer.categorize_transaction('Custom-Vendor Inc', 'Service', -100.0)
    assert result == 'Custom Category'
    
    print("✅ Custom rules test passed!")

if __name__ == '__main__':
    print("Running FinGuard Tests...\n")
    
    try:
        test_categorization_rules()
        test_batch_processing()
        test_custom_rules()
        
        print("\n✅ All tests passed successfully!")
        sys.exit(0)
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        sys.exit(1)
