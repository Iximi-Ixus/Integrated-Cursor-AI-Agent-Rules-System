#!/bin/bash

# Black Box Challenge Evaluation Script
# This script tests your reimbursement calculation implementation against 1,000 historical cases

set -e

echo "🧾 Black Box Challenge - Reimbursement System Evaluation"
echo "======================================================="
echo

# Check if jq is available
if ! command -v jq &> /dev/null; then
    echo "❌ Error: jq is required but not installed!"
    echo "Please install jq to parse JSON files:"
    echo "  macOS: brew install jq"
    echo "  Ubuntu/Debian: sudo apt-get install jq"
    echo "  CentOS/RHEL: sudo yum install jq"
    exit 1
fi

# Check if bc is available for floating point arithmetic
if ! command -v bc &> /dev/null; then
    echo "❌ Error: bc (basic calculator) is required but not installed!"
    echo "Please install bc for floating point calculations:"
    echo "  macOS: brew install bc"
    echo "  Ubuntu/Debian: sudo apt-get install bc"
    echo "  CentOS/RHEL: sudo yum install bc"
    exit 1
fi

# Check if run.sh exists
if [ ! -f "run.sh" ]; then
    echo "❌ Error: run.sh not found!"
    echo "Please create a run.sh script that takes three parameters:"
    echo "  ./run.sh <trip_duration_days> <miles_traveled> <total_receipts_amount>"
    echo "  and outputs the reimbursement amount"
    exit 1
fi

# Make run.sh executable
chmod +x run.sh

# Check if public cases exist
if [ ! -f "public_cases.json" ]; then
    echo "❌ Error: public_cases.json not found!"
    echo "Please ensure the public cases file is in the current directory."
    exit 1
fi

echo "📊 Running evaluation against 1,000 test cases..."
echo

# Extract all test data upfront in a single jq call for better performance
echo "Extracting test data..."
test_data=$(jq -r '.[] | "\(.input.trip_duration_days):\(.input.miles_traveled):\(.input.total_receipts_amount):\(.expected_output)"' public_cases.json)

# Convert to arrays for faster access (compatible with bash 3.2+)
test_cases=()
while IFS= read -r line; do
    test_cases+=("$line")
done <<< "$test_data"
num_cases=${#test_cases[@]}

# Initialize counters and arrays
successful_runs=0
exact_matches=0
close_matches=0
total_error="0"
max_error="0"
max_error_case=""
results_array=()
errors_array=()

# Process each test case
for ((i=0; i<num_cases; i++)); do
    if [ $((i % 100)) -eq 0 ]; then
        echo "Progress: $i/$num_cases cases processed..." >&2
    fi
    
    # Extract test case data from pre-loaded array
    IFS=':' read -r trip_duration miles_traveled receipts_amount expected <<< "${test_cases[i]}"
    
    # Run the user's implementation
    if script_output=$(./run.sh "$trip_duration" "$miles_traveled" "$receipts_amount" 2>/dev/null); then
        # Check if output is a valid number
        output=$(echo "$script_output" | tr -d '[:space:]')
        if [[ $output =~ ^-?[0-9]+\.?[0-9]*$ ]]; then
            actual="$output"
            
            # Calculate absolute error using bc
            error=$(echo "scale=10; if ($actual - $expected < 0) -1 * ($actual - $expected) else ($actual - $expected)" | bc)
            
            # Store result in memory array
            results_array+=("$((i+1)):$expected:$actual:$error:$trip_duration:$miles_traveled:$receipts_amount")
            
            successful_runs=$((successful_runs + 1))
            
            # Check for exact match (within $0.01)
            if (( $(echo "$error < 0.01" | bc -l) )); then
                exact_matches=$((exact_matches + 1))
            fi
            
            # Check for close match (within $1.00)
            if (( $(echo "$error < 1.0" | bc -l) )); then
                close_matches=$((close_matches + 1))
            fi
            
            # Update total error
            total_error=$(echo "scale=10; $total_error + $error" | bc)
            
            # Track maximum error
            if (( $(echo "$error > $max_error" | bc -l) )); then
                max_error="$error"
                max_error_case="Case $((i+1)): $trip_duration days, $miles_traveled miles, \$$receipts_amount receipts"
            fi
            
        else
            errors_array+=("Case $((i+1)): Invalid output format: $output")
        fi
    else
        # Capture stderr for error reporting
        error_msg=$(./run.sh "$trip_duration" "$miles_traveled" "$receipts_amount" 2>&1 >/dev/null | tr -d '\n')
        errors_array+=("Case $((i+1)): Script failed with error: $error_msg")
    fi
done

# Calculate and display results
if [ $successful_runs -eq 0 ]; then
    echo "❌ No successful test cases!"
    echo ""
    echo "Your script either:"
    echo "  - Failed to run properly"
    echo "  - Produced invalid output format"
    echo "  - Timed out on all cases"
    echo ""
    echo "Check the errors below for details."
else
    # Calculate average error
    avg_error=$(echo "scale=2; $total_error / $successful_runs" | bc)
    
    # Calculate percentages
    exact_pct=$(echo "scale=1; $exact_matches * 100 / $successful_runs" | bc)
    close_pct=$(echo "scale=1; $close_matches * 100 / $successful_runs" | bc)
    
    echo "✅ Evaluation Complete!"
    echo ""
    echo "📈 Results Summary:"
    echo "  Total test cases: $num_cases"
    echo "  Successful runs: $successful_runs"
    echo "  Exact matches (±\$0.01): $exact_matches (${exact_pct}%)"
    echo "  Close matches (±\$1.00): $close_matches (${close_pct}%)"
    echo "  Average error: \$${avg_error}"
    echo "  Maximum error: \$${max_error}"
    echo ""
    
    # Calculate score (lower is better)
    score=$(echo "scale=2; $avg_error * 100 + ($num_cases - $exact_matches) * 0.1" | bc)
    echo "🎯 Your Score: $score (lower is better)"
    echo ""
    
    # Provide feedback based on exact matches
    if [ $exact_matches -eq $num_cases ]; then
        echo "🏆 PERFECT SCORE! You have reverse-engineered the system completely!"
    elif [ $exact_matches -gt 950 ]; then
        echo "🥇 Excellent! You are very close to the perfect solution."
    elif [ $exact_matches -gt 800 ]; then
        echo "🥈 Great work! You have captured most of the system behavior."
    elif [ $exact_matches -gt 500 ]; then
        echo "🥉 Good progress! You understand some key patterns."
    else
        echo "📚 Keep analyzing the patterns in the interviews and test cases."
    fi
    
    echo ""
    echo "💡 Tips for improvement:"
    if [ $exact_matches -lt $num_cases ]; then
        echo "  Check these high-error cases:"
        
        # Sort results by error (descending) in memory and show top 5
        IFS=$'\n' high_error_cases=($(printf '%s\n' "${results_array[@]}" | sort -t: -k4 -nr | head -5))
        for result in "${high_error_cases[@]}"; do
            IFS=: read -r case_num expected actual error trip_duration miles_traveled receipts_amount <<< "$result"
            printf "    Case %s: %s days, %s miles, \$%s receipts\n" "$case_num" "$trip_duration" "$miles_traveled" "$receipts_amount"
            printf "      Expected: \$%.2f, Got: \$%.2f, Error: \$%.2f\n" "$expected" "$actual" "$error"
        done
    fi
fi

# Show errors if any
if [ ${#errors_array[@]} -gt 0 ]; then
    echo
    echo "⚠️  Errors encountered:"
    for ((j=0; j<${#errors_array[@]} && j<10; j++)); do
        echo "  ${errors_array[j]}"
    done
    if [ ${#errors_array[@]} -gt 10 ]; then
        echo "  ... and $((${#errors_array[@]} - 10)) more errors"
    fi
fi

echo
echo "📝 Next steps:"
echo "  1. Fix any script errors shown above"
echo "  2. Ensure your run.sh outputs only a number"
echo "  3. Analyze the patterns in the interviews and public cases"
echo "  4. Test edge cases around trip length and receipt amounts"
echo "  5. Submit your solution via the Google Form when ready!" 