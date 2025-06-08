#!/usr/bin/env python3
"""
8090 Black Box Challenge - ML Model Validation
Verify the 98.89% Random Forest accuracy claim against actual public_cases.json data

This script will:
1. Load the real public_cases.json data
2. Implement the Random Forest model from Phase 1 
3. Test the actual accuracy against real expected outputs
4. Identify where our 98.89% claim went wrong
"""

import json
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

def load_actual_data():
    """Load the real public_cases.json data"""
    print("🔍 LOADING ACTUAL PUBLIC CASES DATA")
    print("=" * 50)
    
    with open('Challenge Info/top-coder-challenge/public_cases.json', 'r') as f:
        data = json.load(f)
    
    # Convert to DataFrame
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
    
    print(f"Loaded {len(df)} cases")
    print(f"Columns: {list(df.columns)}")
    print(f"Data shape: {df.shape}")
    print()
    print("Sample data:")
    print(df.head())
    print()
    print("Data statistics:")
    print(df.describe())
    
    return df

def create_features(df):
    """Create features as described in Phase 1 findings"""
    print("\n🔧 CREATING FEATURES FROM PHASE 1")
    print("=" * 50)
    
    # Calculate derived features
    df['miles_per_day'] = df['miles_traveled'] / df['trip_duration_days']
    df['receipts_per_day'] = df['total_receipts_amount'] / df['trip_duration_days']
    df['inverse_duration'] = 1.0 / df['trip_duration_days']
    
    # Non-linear features (from Phase 1 findings)
    df['receipts_squared'] = df['total_receipts_amount'] ** 2
    df['miles_squared'] = df['miles_traveled'] ** 2
    df['duration_squared'] = df['trip_duration_days'] ** 2
    
    # Efficiency features (Kevin's theory)
    df['kevin_efficiency'] = ((df['miles_per_day'] >= 180) & (df['miles_per_day'] <= 220)).astype(int)
    df['extreme_efficiency'] = (df['miles_per_day'] > 400).astype(int)
    df['low_efficiency'] = (df['miles_per_day'] < 25).astype(int)
    
    # Duration categories (death spiral)
    df['short_trip'] = (df['trip_duration_days'] <= 3).astype(int)
    df['medium_trip'] = ((df['trip_duration_days'] >= 4) & (df['trip_duration_days'] <= 6)).astype(int)
    df['long_trip'] = (df['trip_duration_days'] >= 7).astype(int)
    
    # Spending categories (spend-to-win)
    df['high_spending'] = (df['receipts_per_day'] > 100).astype(int)
    df['extreme_spending'] = (df['receipts_per_day'] > 200).astype(int)
    
    print(f"Created features. New shape: {df.shape}")
    print("New columns:", [col for col in df.columns if col not in ['trip_duration_days', 'miles_traveled', 'total_receipts_amount', 'reimbursement']])
    
    return df

def test_random_forest_model(df):
    """Test Random Forest model against actual data"""
    print("\n🌲 TESTING RANDOM FOREST MODEL")
    print("=" * 50)
    
    # Prepare features (exclude target)
    feature_cols = [col for col in df.columns if col != 'reimbursement']
    X = df[feature_cols].values
    y = df['reimbursement'].values
    
    print(f"Features: {len(feature_cols)}")
    print(f"Feature names: {feature_cols}")
    
    # Train Random Forest (same parameters as Phase 1 claims)
    rf = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42
    )
    
    rf.fit(X, y)
    y_pred = rf.predict(X)
    
    # Calculate actual performance
    r2 = r2_score(y, y_pred)
    mae = mean_absolute_error(y, y_pred)
    
    print(f"\n📊 ACTUAL RANDOM FOREST PERFORMANCE:")
    print(f"  R² Score: {r2:.4f} ({r2*100:.2f}%)")
    print(f"  MAE: ${mae:.2f}")
    print(f"  RMSE: ${np.sqrt(((y - y_pred) ** 2).mean()):.2f}")
    
    # Feature importance
    print(f"\n🔍 FEATURE IMPORTANCE:")
    importance_pairs = list(zip(feature_cols, rf.feature_importances_))
    importance_pairs.sort(key=lambda x: x[1], reverse=True)
    
    for i, (feature, importance) in enumerate(importance_pairs[:10]):
        print(f"  {i+1:2d}. {feature:20s}: {importance:.4f} ({importance*100:.1f}%)")
    
    # Error analysis
    errors = np.abs(y - y_pred)
    print(f"\n📈 ERROR ANALYSIS:")
    print(f"  Mean error: ${errors.mean():.2f}")
    print(f"  Max error: ${errors.max():.2f}")
    print(f"  Cases within $1: {(errors <= 1.0).sum()} ({(errors <= 1.0).mean()*100:.1f}%)")
    print(f"  Cases within $5: {(errors <= 5.0).sum()} ({(errors <= 5.0).mean()*100:.1f}%)")
    print(f"  Cases within $10: {(errors <= 10.0).sum()} ({(errors <= 10.0).mean()*100:.1f}%)")
    
    # Worst predictions
    worst_indices = np.argsort(errors)[-10:]
    print(f"\n❌ WORST 10 PREDICTIONS:")
    for i, idx in enumerate(worst_indices):
        actual = y[idx]
        predicted = y_pred[idx]
        error = errors[idx]
        days = df.iloc[idx]['trip_duration_days']
        miles = df.iloc[idx]['miles_traveled']
        receipts = df.iloc[idx]['total_receipts_amount']
        print(f"  {i+1:2d}. {days}d, {miles}mi, ${receipts:.2f} → Pred: ${predicted:.2f}, Actual: ${actual:.2f}, Error: ${error:.2f}")
    
    return rf, y_pred, r2, mae

def compare_with_our_implementation(df):
    """Compare Random Forest with our current implementation"""
    print("\n🔄 COMPARING WITH OUR CURRENT IMPLEMENTATION")
    print("=" * 50)
    
    # Import our current function
    from calculate_reimbursement import calculate_reimbursement
    
    # Test our implementation
    our_predictions = []
    our_errors = []
    
    for _, row in df.iterrows():
        days = int(row['trip_duration_days'])
        miles = float(row['miles_traveled'])
        receipts = float(row['total_receipts_amount'])
        actual = row['reimbursement']
        
        try:
            predicted = calculate_reimbursement(days, miles, receipts)
            error = abs(predicted - actual)
            our_predictions.append(predicted)
            our_errors.append(error)
        except Exception as e:
            print(f"Error on case {days}d, {miles}mi, ${receipts}: {e}")
            our_predictions.append(0)
            our_errors.append(actual)
    
    # Calculate our performance metrics
    our_predictions = np.array(our_predictions)
    our_errors = np.array(our_errors)
    actual_values = df['reimbursement'].values
    
    # Calculate score (sum of absolute errors)
    our_score = our_errors.sum()
    our_mae = our_errors.mean()
    our_r2 = r2_score(actual_values, our_predictions) if len(our_predictions) > 0 else -999
    
    print(f"📊 OUR CURRENT IMPLEMENTATION PERFORMANCE:")
    print(f"  Score (sum of errors): {our_score:.2f}")
    print(f"  MAE: ${our_mae:.2f}")
    print(f"  R² Score: {our_r2:.4f} ({our_r2*100:.2f}%)")
    print(f"  Max error: ${our_errors.max():.2f}")
    print(f"  Cases within $1: {(our_errors <= 1.0).sum()} ({(our_errors <= 1.0).mean()*100:.1f}%)")
    print(f"  Cases within $10: {(our_errors <= 10.0).sum()} ({(our_errors <= 10.0).mean()*100:.1f}%)")
    
    return our_predictions, our_score

def main():
    """Main validation analysis"""
    print("🔍 8090 CHALLENGE - ML MODEL VALIDATION")
    print("=" * 60)
    print("Investigating the 98.89% Random Forest accuracy claim...")
    print()
    
    # Load actual data
    df = load_actual_data()
    
    # Create features
    df = create_features(df)
    
    # Test Random Forest model
    rf, rf_predictions, rf_r2, rf_mae = test_random_forest_model(df)
    
    # Compare with our implementation
    our_predictions, our_score = compare_with_our_implementation(df)
    
    # Final comparison
    print(f"\n" + "=" * 60)
    print("🏆 FINAL COMPARISON")
    print("=" * 60)
    print(f"CLAIMED Random Forest:  98.89% R² (from Phase 1)")
    print(f"ACTUAL Random Forest:   {rf_r2*100:.2f}% R² (tested on real data)")
    print(f"Our Implementation:     {r2_score(df['reimbursement'].values, our_predictions)*100:.2f}% R² (current solution)")
    print()
    print(f"ACTUAL Random Forest MAE: ${rf_mae:.2f}")
    print(f"Our Implementation MAE:   ${np.mean(np.abs(df['reimbursement'].values - our_predictions)):.2f}")
    print()
    print("🎯 CONCLUSION:")
    if rf_r2 > 0.95:
        print("✅ Random Forest model IS highly accurate!")
        print("❓ Problem may be in our implementation/feature engineering")
    elif rf_r2 > 0.8:
        print("⚠️  Random Forest model is good but not 98.89%")
        print("❓ Phase 1 accuracy measurement may have been wrong")
    else:
        print("❌ Random Forest model is NOT highly accurate")
        print("❓ Phase 1 claims were likely incorrect")
    
    return df, rf, our_predictions

if __name__ == "__main__":
    df, rf, our_predictions = main() 