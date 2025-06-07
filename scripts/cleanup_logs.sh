#!/bin/bash

# Exit on error
set -e

# Configuration
TEST_RESULTS_DIR="var/test-results"
APP_LOGS_DIR="var/logs"
MAX_TEST_RESULTS_AGE=30  # days
MAX_APP_LOGS_AGE=7       # days
MAX_TEST_RESULTS_SIZE=100  # MB
MAX_APP_LOGS_SIZE=50      # MB

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Function to get directory size in MB
get_dir_size() {
    local dir=$1
    du -sm "$dir" | cut -f1
}

# Function to clean old files
clean_old_files() {
    local dir=$1
    local max_age=$2
    local pattern=$3
    
    log "Cleaning files older than $max_age days in $dir"
    find "$dir" -name "$pattern" -type f -mtime +$max_age -delete
}

# Function to archive old files
archive_old_files() {
    local dir=$1
    local max_age=$2
    local pattern=$3
    local archive_dir="$dir/archive"
    
    # Create archive directory if it doesn't exist
    mkdir -p "$archive_dir"
    
    # Move old files to archive
    log "Archiving files older than $max_age days in $dir"
    find "$dir" -name "$pattern" -type f -mtime +$max_age -exec mv {} "$archive_dir/" \;
    
    # Compress archive if it exists and is not empty
    if [ -d "$archive_dir" ] && [ "$(ls -A "$archive_dir")" ]; then
        local archive_name="archive_$(date '+%Y%m%d').tar.gz"
        tar -czf "$archive_dir/$archive_name" -C "$archive_dir" .
        rm -f "$archive_dir"/*.log "$archive_dir"/*.txt
    fi
}

# Function to check and clean if directory size exceeds limit
check_dir_size() {
    local dir=$1
    local max_size=$2
    
    local current_size=$(get_dir_size "$dir")
    if [ "$current_size" -gt "$max_size" ]; then
        log "Directory $dir size ($current_size MB) exceeds limit ($max_size MB)"
        # Archive oldest files first
        archive_old_files "$dir" 1 "*"
    fi
}

# Main cleanup process
log "Starting log cleanup process"

# Clean test results
if [ -d "$TEST_RESULTS_DIR" ]; then
    log "Processing test results directory"
    check_dir_size "$TEST_RESULTS_DIR" "$MAX_TEST_RESULTS_SIZE"
    clean_old_files "$TEST_RESULTS_DIR" "$MAX_TEST_RESULTS_AGE" "*.log"
fi

# Clean application logs
if [ -d "$APP_LOGS_DIR" ]; then
    log "Processing application logs directory"
    check_dir_size "$APP_LOGS_DIR" "$MAX_APP_LOGS_SIZE"
    clean_old_files "$APP_LOGS_DIR" "$MAX_APP_LOGS_AGE" "*.log"
    clean_old_files "$APP_LOGS_DIR" "$MAX_APP_LOGS_AGE" "*.txt"
fi

log "Log cleanup completed" 