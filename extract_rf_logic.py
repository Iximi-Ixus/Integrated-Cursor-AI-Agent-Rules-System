#!/usr/bin/env python3
"""
Extract Random Forest Logic for Standard Library Implementation
Goal: Convert the 97.14% accurate Random Forest into standard library Python code
"""

import json
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import export_text
import warnings
warnings.filterwarnings('ignore')

def load_and_prepare_data():
    """Load and prepare data with all features"""
    with open('Challenge Info/top-coder-challenge/public_cases.json', 'r') as f:
        data = json.load(f)
    
    rows = []
    for case in data:
        input_data = case['input']
        expected = case['expected_output']
        
        rows.append({
            'trip_duration_days': input_data['trip_duration_days'],
            'miles_traveled': input_data['miles_traveled'],
            'total_receipts_amount': input_data['total_receipts_amount'],
            'reimbursement': expected
        })
    
    df = pd.DataFrame(rows)
    
    # Create all features
    df['miles_per_day'] = df['miles_traveled'] / df['trip_duration_days']
    df['receipts_per_day'] = df['total_receipts_amount'] / df['trip_duration_days']
    df['inverse_duration'] = 1.0 / df['trip_duration_days']
    df['receipts_squared'] = df['total_receipts_amount'] ** 2
    df['miles_squared'] = df['miles_traveled'] ** 2
    df['duration_squared'] = df['trip_duration_days'] ** 2
    
    return df

def train_simplified_model(df):
    """Train a simplified Random Forest focused on top features"""
    print("🌲 TRAINING SIMPLIFIED RANDOM FOREST")
    print("=" * 50)
    
    # Use only the most important features from our analysis
    top_features = [
        'total_receipts_amount',
        'receipts_squared', 
        'miles_traveled',
        'inverse_duration',
        'trip_duration_days'
    ]
    
    X = df[top_features].values
    y = df['reimbursement'].values
    
    # Train a simpler model with fewer trees for interpretability
    rf = RandomForestRegressor(
        n_estimators=5,  # Fewer trees for simpler extraction
        max_depth=6,     # Shallower trees
        min_samples_split=10,
        min_samples_leaf=5,
        random_state=42
    )
    
    rf.fit(X, y)
    
    # Check performance
    y_pred = rf.predict(X)
    r2 = np.corrcoef(y, y_pred)[0, 1] ** 2
    mae = np.mean(np.abs(y - y_pred))
    
    print(f"Simplified model performance:")
    print(f"  R² Score: {r2:.4f} ({r2*100:.2f}%)")
    print(f"  MAE: ${mae:.2f}")
    
    return rf, top_features

def extract_tree_rules(rf, feature_names):
    """Extract simple rules from the first tree"""
    print("\n🔍 EXTRACTING TREE RULES")
    print("=" * 50)
    
    # Get the first tree (most important)
    first_tree = rf.estimators_[0]
    
    # Export as text
    tree_rules = export_text(first_tree, 
                           feature_names=feature_names,
                           max_depth=4)  # Limit depth for readability
    
    print("First tree rules (simplified):")
    print(tree_rules)
    
    return tree_rules

def analyze_receipt_relationship(df):
    """Analyze the quadratic receipt relationship discovered"""
    print("\n💡 ANALYZING QUADRATIC RECEIPT RELATIONSHIP")
    print("=" * 50)
    
    # Group by receipt ranges and analyze patterns
    df['receipt_range'] = pd.cut(df['total_receipts_amount'], 
                                bins=[0, 10, 50, 100, 200, 500, 1000, float('inf')],
                                labels=['0-10', '10-50', '50-100', '100-200', '200-500', '500-1000', '1000+'])
    
    receipt_analysis = df.groupby('receipt_range').agg({
        'reimbursement': ['mean', 'count'],
        'total_receipts_amount': 'mean',
        'trip_duration_days': 'mean',
        'miles_traveled': 'mean'
    }).round(2)
    
    print("Receipt range analysis:")
    print(receipt_analysis)
    
    # Analyze receipt coefficient by range
    print("\n📊 RECEIPT COEFFICIENT ANALYSIS:")
    for range_name, group in df.groupby('receipt_range'):
        if len(group) > 5:  # Only ranges with enough data
            # Calculate effective receipt coefficient
            # Remove base per diem and mileage to isolate receipt effect
            base_cost = group['trip_duration_days'] * 50 + group['miles_traveled'] * 0.5
            receipt_contribution = group['reimbursement'] - base_cost
            avg_receipt_ratio = (receipt_contribution / group['total_receipts_amount']).mean()
            
            print(f"  {range_name:10s}: {avg_receipt_ratio:.3f} (avg ratio)")

def create_optimized_implementation():
    """Create an optimized implementation based on Random Forest insights"""
    print("\n🚀 CREATING OPTIMIZED IMPLEMENTATION")
    print("=" * 50)
    
    implementation_code = '''
def calculate_reimbursement_optimized(trip_duration_days, miles_traveled, total_receipts_amount):
    """
    Random Forest-inspired implementation
    Based on 97.14% accurate model insights:
    - Quadratic receipt relationship (receipts_squared = 34.2% importance)
    - Inverse duration relationship (death spiral effect)
    - Linear mileage component
    """
    import math
    
    # Feature engineering (key insights from Random Forest)
    inverse_duration = 1.0 / trip_duration_days
    receipts_squared = total_receipts_amount ** 2
    
    # Base components (traditional approach)
    per_diem_base = trip_duration_days * 55  # Base per diem
    mileage_base = miles_traveled * 0.58     # Base mileage
    
    # QUADRATIC RECEIPT COMPONENT (most important feature!)
    # Random Forest showed receipts_squared is 34.2% of importance
    receipt_linear = total_receipts_amount * 0.8  # Linear component
    receipt_quadratic = receipts_squared * 0.00001  # Quadratic enhancement
    
    # INVERSE DURATION EFFECT (death spiral - 6.9% importance)
    duration_adjustment = inverse_duration * 50  # 1-day trips get bonus
    
    # Combine all components
    total = per_diem_base + mileage_base + receipt_linear + receipt_quadratic + duration_adjustment
    
    return round(total, 2)
'''
    
    print("Generated optimized implementation code:")
    print(implementation_code)
    
    return implementation_code

def main():
    """Main analysis"""
    print("🔍 RANDOM FOREST LOGIC EXTRACTION")
    print("=" * 60)
    
    # Load data
    df = load_and_prepare_data()
    
    # Train simplified model
    rf, feature_names = train_simplified_model(df)
    
    # Extract tree rules
    tree_rules = extract_tree_rules(rf, feature_names)
    
    # Analyze receipt relationship
    analyze_receipt_relationship(df)
    
    # Create optimized implementation
    optimized_code = create_optimized_implementation()
    
    return df, rf, optimized_code

if __name__ == "__main__":
    df, rf, code = main() 