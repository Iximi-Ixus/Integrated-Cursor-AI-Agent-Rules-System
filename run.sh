#!/bin/bash

# Black Box Challenge - Our Implementation
# This script calls our Python implementation with the three required parameters
# Usage: ./run.sh <trip_duration_days> <miles_traveled> <total_receipts_amount>

# Our implementation: Python with simple linear model
python calculate_reimbursement.py "$1" "$2" "$3" 