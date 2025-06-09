#!/bin/bash

# Exit on error
set -e

# Initialize test results
TEST_RESULTS_DIR=".test_results"
mkdir -p "$TEST_RESULTS_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
TEST_LOG="$TEST_RESULTS_DIR/test_run_$TIMESTAMP.log"
SUMMARY_LOG="$TEST_RESULTS_DIR/summary_$TIMESTAMP.log"
PERFORMANCE_LOG="$TEST_RESULTS_DIR/performance_$TIMESTAMP.log"
COVERAGE_LOG="$TEST_RESULTS_DIR/coverage_$TIMESTAMP.log"

# Maximum number of retries for flaky tests
MAX_RETRIES=3

# Function to log messages
log() {
    echo "$1" | tee -a "$TEST_LOG"
}

# Function to log test results
log_test_result() {
    local test_name=$1
    local status=$2
    local duration=$3
    local details=$4
    local retry_count=$5
    
    echo "Test: $test_name" >> "$SUMMARY_LOG"
    echo "Status: $status" >> "$SUMMARY_LOG"
    echo "Duration: ${duration}s" >> "$SUMMARY_LOG"
    if [ -n "$retry_count" ]; then
        echo "Retries: $retry_count" >> "$SUMMARY_LOG"
    fi
    if [ -n "$details" ]; then
        echo "Details: $details" >> "$SUMMARY_LOG"
    fi
    echo "----------------------------------------" >> "$SUMMARY_LOG"
}

# Function to log performance metrics
log_performance() {
    local test_name=$1
    local metrics=$2
    
    echo "Test: $test_name" >> "$PERFORMANCE_LOG"
    echo "$metrics" >> "$PERFORMANCE_LOG"
    echo "----------------------------------------" >> "$PERFORMANCE_LOG"
}

# Function to log coverage
log_coverage() {
    local test_name=$1
    local coverage=$2
    
    echo "Test: $test_name" >> "$COVERAGE_LOG"
    echo "$coverage" >> "$COVERAGE_LOG"
    echo "----------------------------------------" >> "$COVERAGE_LOG"
}

# Function to run tests and capture results
run_tests() {
    local test_command=$1
    local test_name=$2
    local test_file=$(echo "$test_command" | grep -o "tests/.*\.py")
    local retry_count=0
    local success=false
    
    # Check if test file exists
    if [ ! -f "$test_file" ]; then
        log "Error: Test file $test_file not found"
        log_test_result "$test_name" "FAILED" "0" "Test file not found"
        return 1
    fi
    
    while [ $retry_count -lt $MAX_RETRIES ] && [ "$success" = false ]; do
        local start_time=$(date +%s.%N)
        
        if [ $retry_count -gt 0 ]; then
            log "Retry $retry_count for $test_name..."
        else
            log "Running $test_name..."
        fi
        log "Command: $test_command"
        
        if $test_command 2>&1 | tee -a "$TEST_LOG"; then
            local end_time=$(date +%s.%N)
            local duration=$(echo "$end_time - $start_time" | bc)
            log_test_result "$test_name" "PASSED" "$duration" "" "$retry_count"
            success=true
            
            # Extract performance metrics if available
            if grep -q "performance metrics" "$TEST_LOG"; then
                local metrics=$(grep -A 10 "performance metrics" "$TEST_LOG")
                log_performance "$test_name" "$metrics"
            fi
            
            # Extract coverage if available
            if grep -q "coverage:" "$TEST_LOG"; then
                local coverage=$(grep -A 20 "coverage:" "$TEST_LOG")
                log_coverage "$test_name" "$coverage"
            fi
        else
            local end_time=$(date +%s.%N)
            local duration=$(echo "$end_time - $start_time" | bc)
            local error_details=$(tail -n 20 "$TEST_LOG")
            
            if [ $retry_count -eq $((MAX_RETRIES-1)) ]; then
                log_test_result "$test_name" "FAILED" "$duration" "$error_details" "$retry_count"
                return 1
            else
                log "Test failed, retrying..."
                retry_count=$((retry_count + 1))
                sleep 2  # Wait before retry
            fi
        fi
    done
    
    return 0
}

# Function to print test summary
print_summary() {
    log "\nTest Summary:"
    log "----------------------------------------"
    log "Total Tests: $(grep -c "Test:" "$SUMMARY_LOG")"
    log "Passed: $(grep -c "Status: PASSED" "$SUMMARY_LOG")"
    log "Failed: $(grep -c "Status: FAILED" "$SUMMARY_LOG")"
    log "----------------------------------------"
    
    if grep -q "Status: FAILED" "$SUMMARY_LOG"; then
        log "\nFailed Tests:"
        log "----------------------------------------"
        grep -A 3 "Status: FAILED" "$SUMMARY_LOG"
    fi
    
    if [ -f "$PERFORMANCE_LOG" ]; then
        log "\nPerformance Summary:"
        log "----------------------------------------"
        cat "$PERFORMANCE_LOG"
    fi
    
    if [ -f "$COVERAGE_LOG" ]; then
        log "\nCoverage Summary:"
        log "----------------------------------------"
        cat "$COVERAGE_LOG"
        
        # Print modules with 0% coverage
        log "\nModules with 0% Coverage:"
        log "----------------------------------------"
        grep -B 1 "0%" "$COVERAGE_LOG" | grep -v "0%" | grep -v "--" | sort | uniq
    fi
    
    log "\nDetailed logs available at:"
    log "Test Log: $TEST_LOG"
    log "Summary Log: $SUMMARY_LOG"
    if [ -f "$PERFORMANCE_LOG" ]; then
        log "Performance Log: $PERFORMANCE_LOG"
    fi
    if [ -f "$COVERAGE_LOG" ]; then
        log "Coverage Log: $COVERAGE_LOG"
    fi
}

# Create and setup virtual environment
log "Setting up virtual environment..."
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
.venv/bin/pip install -e .

# Run integration tests with real LLM
log "Running integration tests with real LLM..."
run_tests ".venv/bin/python -m pytest tests/recipe/test_real_integration.py -v --cov=core" "Integration Tests"

# Run end-to-end tests
log "Running end-to-end tests..."
run_tests ".venv/bin/python -m pytest tests/recipe/test_e2e.py -v --cov=core" "End-to-End Tests"

# Run phi model test
log "Running phi model test..."
run_tests ".venv/bin/python -m pytest tests/recipe/test_phi.py -v --cov=core" "Phi Model Test"

# Show performance metrics
log "Showing performance metrics..."
.venv/bin/python -c "from core.utils.performance import print_performance_metrics; print_performance_metrics()"

# Print final summary
print_summary

# Exit with appropriate status
if grep -q "Status: FAILED" "$SUMMARY_LOG"; then
    exit 1
else
    exit 0
fi 