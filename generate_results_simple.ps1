# Black Box Challenge - Results Generation Script (PowerShell)
# This script runs your implementation against test cases and outputs results to private_results.txt

Write-Host "Black Box Challenge - Generating Private Results" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Check if private_cases.json exists
if (-not (Test-Path "private_cases.json")) {
    Write-Host "Error: private_cases.json not found!" -ForegroundColor Red
    Write-Host "Please ensure the private cases file is in the current directory."
    exit 1
}

# Check if calculate_reimbursement.py exists
if (-not (Test-Path "calculate_reimbursement.py")) {
    Write-Host "Error: calculate_reimbursement.py not found!" -ForegroundColor Red
    Write-Host "Please ensure your implementation is in the current directory."
    exit 1
}

Write-Host "Processing test cases and generating results..." -ForegroundColor Yellow
Write-Host "Output will be saved to private_results.txt" -ForegroundColor Yellow
Write-Host ""

# Load and parse JSON
Write-Host "Loading private_cases.json..." -ForegroundColor Green
try {
    $jsonContent = Get-Content "private_cases.json" -Raw | ConvertFrom-Json
    $totalCases = $jsonContent.Count
    Write-Host "Found $totalCases test cases to process" -ForegroundColor Green
} catch {
    Write-Host "Error loading private_cases.json: $_" -ForegroundColor Red
    exit 1
}

# Remove existing results file if it exists
if (Test-Path "private_results.txt") {
    Remove-Item "private_results.txt"
}

Write-Host "Processing $totalCases test cases..." -ForegroundColor Yellow
$results = @()
$errorCount = 0

# Process each test case
for ($i = 0; $i -lt $totalCases; $i++) {
    if (($i % 1000) -eq 0 -and $i -gt 0) {
        Write-Host "Progress: $i/$totalCases cases processed..." -ForegroundColor Cyan
    }
    
    $testCase = $jsonContent[$i]
    $days = $testCase.trip_duration_days
    $miles = $testCase.miles_traveled  
    $receipts = $testCase.total_receipts_amount
    
    try {
        # Run the Python implementation
        $output = python calculate_reimbursement.py $days $miles $receipts 2>$null
        
        if ($output -match "^-?\d*\.?\d+$") {
            # Valid numeric output
            $results += $output.Trim()
        } else {
            # Invalid output
            Write-Host "Error on case $($i+1): Invalid output format: $output" -ForegroundColor Red
            $results += "ERROR"
            $errorCount++
        }
    } catch {
        # Script execution failed
        Write-Host "Error on case $($i+1): Script failed: $_" -ForegroundColor Red
        $results += "ERROR"
        $errorCount++
    }
}

# Write all results to file
$results | Out-File -FilePath "private_results.txt" -Encoding ASCII

Write-Host ""
Write-Host "Results generated successfully!" -ForegroundColor Green
Write-Host "Output saved to private_results.txt" -ForegroundColor Green
Write-Host "Processed $totalCases cases with $errorCount errors" -ForegroundColor Green

if ($errorCount -gt 0) {
    Write-Host "Warning: $errorCount cases had errors" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Check private_results.txt - it should contain one result per line"
Write-Host "  2. Each line corresponds to the same-numbered test case in private_cases.json"
Write-Host "  3. Lines with 'ERROR' indicate cases where your script failed"
Write-Host "  4. Submit your private_results.txt file when ready!" 