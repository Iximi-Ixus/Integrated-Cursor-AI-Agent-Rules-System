#!/usr/bin/env python3
"""
FRESH REVERSE ENGINEERING APPROACH - Final 1.5 Hours
8090 Black Box Reimbursement Challenge

CRITICAL PIVOT: Back to basics reverse engineering
- Abandon complex optimization (all attempts failed)
- Return to original strategy guide methodology  
- Focus: Discover ACTUAL business logic, not tune coefficients
- Time: 30 minutes for data analysis, 60 minutes for implementation

BASELINE: Score 17,372 (avg error $172.72) - NEEDS BREAKTHROUGH
GOAL: Discover the real business rules through systematic pattern analysis
"""

import json
import pandas as pd
import numpy as np
import sys
import os

def load_and_analyze_data():
    """Load public cases and perform systematic reverse engineering analysis"""
    print("🔍 FRESH REVERSE ENGINEERING - DATA ANALYSIS")
    print("=" * 50)
    
    # Load public cases
    with open('../Challenge Info/top-coder-challenge/public_cases.json', 'r') as f:
        cases = json.load(f)
    
    # Convert to DataFrame
    data = []
    for case in cases:
        data.append({
            'days': case['input']['trip_duration_days'],
            'miles': case['input']['miles_traveled'],
            'receipts': case['input']['total_receipts_amount'],
            'reimbursement': case['expected_output']
        })
    
    df = pd.DataFrame(data)
    print(f"📊 Loaded {len(df)} cases for analysis")
    return df

def analyze_per_diem_base(df):
    """STEP 1: Isolate per diem by finding minimal travel cases"""
    print("\n🎯 STEP 1: PER DIEM ANALYSIS")
    print("-" * 30)
    
    # Look for cases with minimal mileage and receipts
    minimal_travel = df[(df['miles'] <= 50) & (df['receipts'] <= 50)]
    print(f"📊 Minimal travel cases: {len(minimal_travel)}")
    
    if len(minimal_travel) > 0:
        print("💡 Per diem analysis on minimal travel cases:")
        per_day_rates = minimal_travel['reimbursement'] / minimal_travel['days']
        print(f"   Average per-day rate: ${per_day_rates.mean():.2f}")
        print(f"   Range: ${per_day_rates.min():.2f} - ${per_day_rates.max():.2f}")
        print(f"   Standard deviation: ${per_day_rates.std():.2f}")
        
        # Look for day-based patterns
        by_days = minimal_travel.groupby('days').agg({
            'reimbursement': ['mean', 'count']
        }).round(2)
        print("\n📈 Per diem by trip duration:")
        print(by_days)
    
    # Alternative: Look at zero receipt cases
    zero_receipts = df[df['receipts'] == 0]
    print(f"\n📊 Zero receipt cases: {len(zero_receipts)}")
    
    if len(zero_receipts) > 0:
        # Analyze reimbursement vs. miles for zero receipt cases
        print("💡 Zero receipt pattern analysis:")
        zero_receipts['reimbursement_per_mile'] = zero_receipts['reimbursement'] / zero_receipts['miles']
        print(f"   Average reimbursement per mile: ${zero_receipts['reimbursement_per_mile'].mean():.3f}")
        
    return minimal_travel, zero_receipts

def analyze_mileage_patterns(df):
    """STEP 2: Discover mileage reimbursement structure"""
    print("\n🎯 STEP 2: MILEAGE ANALYSIS")
    print("-" * 30)
    
    # Look for short trips with minimal receipts to isolate mileage effect
    short_minimal_receipts = df[(df['days'] <= 2) & (df['receipts'] <= 100)]
    print(f"📊 Short trips, minimal receipts: {len(short_minimal_receipts)}")
    
    if len(short_minimal_receipts) > 10:
        # Calculate per-mile reimbursement
        short_minimal_receipts = short_minimal_receipts.copy()
        short_minimal_receipts['per_mile'] = short_minimal_receipts['reimbursement'] / short_minimal_receipts['miles']
        
        print("💡 Mileage rate analysis:")
        print(f"   Average per-mile rate: ${short_minimal_receipts['per_mile'].mean():.3f}")
        print(f"   Range: ${short_minimal_receipts['per_mile'].min():.3f} - ${short_minimal_receipts['per_mile'].max():.3f}")
        
        # Look for mileage tiers
        mileage_bins = [0, 100, 200, 500, 1000, float('inf')]
        short_minimal_receipts['mileage_tier'] = pd.cut(short_minimal_receipts['miles'], bins=mileage_bins)
        
        by_mileage = short_minimal_receipts.groupby('mileage_tier').agg({
            'per_mile': ['mean', 'count']
        }).round(3)
        print("\n📈 Per-mile rates by mileage tier:")
        print(by_mileage)
    
    return short_minimal_receipts

def analyze_receipt_patterns(df):
    """STEP 3: Discover receipt reimbursement logic"""
    print("\n🎯 STEP 3: RECEIPT ANALYSIS")
    print("-" * 30)
    
    # Look for cases with minimal travel to isolate receipt effect
    minimal_travel_high_receipts = df[(df['days'] <= 3) & (df['miles'] <= 100) & (df['receipts'] > 200)]
    print(f"📊 Minimal travel, high receipts: {len(minimal_travel_high_receipts)}")
    
    if len(minimal_travel_high_receipts) > 10:
        minimal_travel_high_receipts = minimal_travel_high_receipts.copy()
        minimal_travel_high_receipts['receipt_ratio'] = minimal_travel_high_receipts['reimbursement'] / minimal_travel_high_receipts['receipts']
        
        print("💡 Receipt ratio analysis:")
        print(f"   Average receipt ratio: {minimal_travel_high_receipts['receipt_ratio'].mean():.3f}")
        print(f"   Range: {minimal_travel_high_receipts['receipt_ratio'].min():.3f} - {minimal_travel_high_receipts['receipt_ratio'].max():.3f}")
        
        # Look for receipt amount tiers
        receipt_bins = [0, 200, 500, 1000, 1500, 2000, float('inf')]
        minimal_travel_high_receipts['receipt_tier'] = pd.cut(minimal_travel_high_receipts['receipts'], bins=receipt_bins)
        
        by_receipt = minimal_travel_high_receipts.groupby('receipt_tier').agg({
            'receipt_ratio': ['mean', 'count']
        }).round(3)
        print("\n📈 Receipt ratios by amount tier:")
        print(by_receipt)
    
    # Alternative: All cases receipt analysis
    df_copy = df.copy()
    df_copy['receipt_ratio'] = df_copy['reimbursement'] / df_copy['receipts']
    
    # Filter out extreme ratios (outliers)
    reasonable_ratios = df_copy[(df_copy['receipt_ratio'] > 0.1) & (df_copy['receipt_ratio'] < 10)]
    print(f"\n📊 All cases receipt ratio analysis ({len(reasonable_ratios)} reasonable cases):")
    print(f"   Average receipt ratio: {reasonable_ratios['receipt_ratio'].mean():.3f}")
    print(f"   Median receipt ratio: {reasonable_ratios['receipt_ratio'].median():.3f}")
    
    return minimal_travel_high_receipts, reasonable_ratios

def discover_complex_patterns(df):
    """STEP 4: Look for complex interactions and edge cases"""
    print("\n🎯 STEP 4: COMPLEX PATTERN DISCOVERY")
    print("-" * 30)
    
    # Calculate efficiency metrics
    df_copy = df.copy()
    df_copy['miles_per_day'] = df_copy['miles'] / df_copy['days']
    df_copy['receipts_per_day'] = df_copy['receipts'] / df_copy['days']
    df_copy['reimbursement_per_day'] = df_copy['reimbursement'] / df_copy['days']
    
    # Look for day-based patterns
    print("💡 Trip duration analysis:")
    by_days = df_copy.groupby('days').agg({
        'reimbursement_per_day': ['mean', 'std', 'count']
    }).round(2)
    print(by_days.head(10))
    
    # Look for efficiency sweet spots
    print("\n💡 Efficiency analysis (Kevin's theory):")
    efficiency_bins = [0, 50, 100, 150, 200, 250, 300, float('inf')]
    df_copy['efficiency_tier'] = pd.cut(df_copy['miles_per_day'], bins=efficiency_bins)
    
    by_efficiency = df_copy.groupby('efficiency_tier').agg({
        'reimbursement_per_day': ['mean', 'count']
    }).round(2)
    print(by_efficiency)
    
    # Look for outliers and edge cases
    print("\n🚨 OUTLIER ANALYSIS:")
    # High reimbursement cases
    high_reimbursement = df_copy.nlargest(10, 'reimbursement')[['days', 'miles', 'receipts', 'reimbursement']]
    print("Top 10 highest reimbursements:")
    print(high_reimbursement)
    
    # Low reimbursement cases  
    low_reimbursement = df_copy.nsmallest(10, 'reimbursement')[['days', 'miles', 'receipts', 'reimbursement']]
    print("\nTop 10 lowest reimbursements:")
    print(low_reimbursement)
    
    return df_copy

def test_simple_formulas(df):
    """STEP 5: Test simple business logic formulas"""
    print("\n🎯 STEP 5: FORMULA TESTING")
    print("-" * 30)
    
    # Test various simple formulas and see which gets closest
    formulas = [
        ("Base + Days*50 + Miles*0.5 + Receipts*0.8", lambda d, m, r: 50 + d*50 + m*0.5 + r*0.8),
        ("Days*60 + Miles*0.58 + Receipts*0.7", lambda d, m, r: d*60 + m*0.58 + r*0.7),
        ("Days*80 + Miles*0.4 + Receipts*0.6", lambda d, m, r: d*80 + m*0.4 + r*0.6),
        ("Days*100 + Miles*0.3 + Receipts*0.5", lambda d, m, r: d*100 + m*0.3 + r*0.5),
        ("Base100 + Days*40 + Miles*0.6 + Receipts*0.9", lambda d, m, r: 100 + d*40 + m*0.6 + r*0.9),
    ]
    
    best_formula = None
    best_error = float('inf')
    
    for name, formula in formulas:
        errors = []
        for _, row in df.iterrows():
            predicted = formula(row['days'], row['miles'], row['receipts'])
            error = abs(predicted - row['reimbursement'])
            errors.append(error)
        
        avg_error = np.mean(errors)
        print(f"📊 {name}: Avg error ${avg_error:.2f}")
        
        if avg_error < best_error:
            best_error = avg_error
            best_formula = (name, formula)
    
    print(f"\n🏆 Best simple formula: {best_formula[0]}")
    print(f"   Average error: ${best_error:.2f}")
    
    return best_formula

def main():
    """Run complete fresh reverse engineering analysis"""
    print("🚀 FRESH REVERSE ENGINEERING - 8090 CHALLENGE")
    print("=" * 55)
    print("⏰ Time allocation: 30 minutes for data analysis")
    print("🎯 Goal: Discover ACTUAL business logic, not optimize coefficients")
    print()
    
    # Load data
    df = load_and_analyze_data()
    
    # Step 1: Per diem analysis
    minimal_travel, zero_receipts = analyze_per_diem_base(df)
    
    # Step 2: Mileage analysis  
    mileage_cases = analyze_mileage_patterns(df)
    
    # Step 3: Receipt analysis
    receipt_cases, all_receipt_analysis = analyze_receipt_patterns(df)
    
    # Step 4: Complex patterns
    enhanced_df = discover_complex_patterns(df)
    
    # Step 5: Test simple formulas
    best_formula = test_simple_formulas(df)
    
    print("\n" + "=" * 55)
    print("🎯 REVERSE ENGINEERING SUMMARY")
    print("=" * 55)
    print("💡 Key findings and next steps for implementation...")
    print(f"🏆 Best simple formula identified: {best_formula[0]}")
    print("📋 Use these patterns to build new implementation in next 60 minutes")

if __name__ == "__main__":
    main() 