#!/usr/bin/env python3
"""
Quick evaluation script - no unicode characters
"""

import json
import subprocess
import statistics

def quick_eval():
    print("Quick Evaluation")
    print("=" * 20)
    
    # Load public cases
    with open('Challenge Info/top-coder-challenge/public_cases.json', 'r') as f:
        cases = json.load(f)
    
    # Sample first 100 cases for quick evaluation
    sample_cases = cases[:100]
    
    errors = []
    for i, case in enumerate(sample_cases):
        try:
            result = subprocess.run([
                'python', 'calculate_reimbursement.py',
                str(case['input']['trip_duration_days']),
                str(case['input']['miles_traveled']),
                str(case['input']['total_receipts_amount'])
            ], capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                predicted = float(result.stdout.strip())
                actual = case['expected_output']
                error = abs(predicted - actual)
                errors.append(error)
            else:
                print(f"Error in case {i}: {result.stderr}")
        except Exception as e:
            print(f"Exception in case {i}: {e}")
    
    if errors:
        avg_error = statistics.mean(errors)
        max_error = max(errors)
        score = sum(errors)
        
        print(f"Sample of {len(errors)} cases:")
        print(f"Average error: ${avg_error:.2f}")
        print(f"Maximum error: ${max_error:.2f}")
        print(f"Sample score: {score:.2f}")
        print(f"Projected full score: {score * 10:.0f}")
    else:
        print("No successful cases!")

if __name__ == "__main__":
    quick_eval() 