# 🛠️ Project Scripts Directory

This directory contains optimized and consolidated scripts for managing various aspects of the meal planning project. After a comprehensive review and cleanup, we've streamlined the scripts to focus on essential development, monitoring, and maintenance tasks.

## 📋 Script Inventory

### 🔧 Core Scripts

| Script | Category | Description | Status |
|--------|----------|-------------|--------|
| `performance.py` | Monitoring | Recipe processing performance metrics | ✅ Enhanced |
| `check_code_quality.py` | Quality | Comprehensive code quality analysis | ✅ New |
| `update_imports.py` | Development | Import optimization and management | ✅ Enhanced |
| `cleanup_logs.sh` | Maintenance | Log file and cache cleanup | ✅ Existing |
| `run_integration_tests.sh` | Testing | Integration test execution | ✅ Existing |
| `reorganize.py` | Development | Project structure reorganization | ✅ Existing |
| `manage_scripts.py` | Management | Script orchestration utility | ✅ New |

### 🗂️ Directory Structure

```
scripts/
├── README.md                           # This file
├── manage_scripts.py                   # Script management utility
├── performance.py                      # Enhanced performance monitoring
├── cleanup_logs.sh                     # Log cleanup utility
├── run_integration_tests.sh            # Integration testing
├── development/
│   ├── update_imports.py              # Enhanced import manager
│   └── reorganize.py                  # Project reorganization
└── refactoring/
    └── check_code_quality.py          # Comprehensive quality checker
```

## 🚀 Quick Start

### Using the Script Manager

The easiest way to work with scripts is through the management utility:

```bash
# List all available scripts
python scripts/manage_scripts.py

# Check script health
python scripts/manage_scripts.py health

# List scripts by category
python scripts/manage_scripts.py list quality

# Run a specific script
python scripts/manage_scripts.py run quality --root core --severity error
```

### Direct Script Usage

Each script can also be run directly:

```bash
# Performance monitoring
python scripts/performance.py --detailed --export performance_report.json

# Code quality analysis
python scripts/refactoring/check_code_quality.py --root core --export quality_report.json

# Import optimization
python scripts/development/update_imports.py --root core --check-only

# Log cleanup
bash scripts/cleanup_logs.sh

# Integration tests
bash scripts/run_integration_tests.sh
```

## 📊 Script Details

### 1. Performance Monitor (`performance.py`)

**Enhanced features:**
- Beautiful formatted output with emojis and tables
- Multiple export formats (JSON)
- Batch processing metrics
- Cache performance analysis
- LLM vs rule-based processing breakdown
- Clear/reset functionality

```bash
# Examples
python scripts/performance.py --detailed
python scripts/performance.py --batch --export metrics.json
python scripts/performance.py --clear
```

### 2. Code Quality Checker (`check_code_quality.py`)

**Comprehensive analysis:**
- Cyclomatic complexity analysis
- Documentation coverage
- Type hint coverage
- Naming convention compliance
- Architecture layer violations
- Import analysis
- Code smell detection

```bash
# Examples
python scripts/refactoring/check_code_quality.py --root core
python scripts/refactoring/check_code_quality.py --severity error
python scripts/refactoring/check_code_quality.py --export quality_report.json
```

### 3. Import Manager (`update_imports.py`)

**Advanced features:**
- Relative to absolute import conversion
- Unused import detection
- Import statement organization
- Circular dependency detection
- Safe import removal

```bash
# Examples
python scripts/development/update_imports.py --root core
python scripts/development/update_imports.py --check-only
python scripts/development/update_imports.py --dry-run
```

### 4. Script Manager (`manage_scripts.py`)

**Centralized control:**
- Script discovery and health checking
- Unified execution interface
- Category-based filtering
- Argument forwarding

```bash
# Examples
python scripts/manage_scripts.py health
python scripts/manage_scripts.py run performance --detailed
python scripts/manage_scripts.py list development
```

## 🧹 Cleanup Actions Taken

### ❌ Removed Duplicates and Obsolete Scripts

- `fix_long_lines.py` (duplicate of `fix_line_lengths.py`)
- `fix_line_lengths.py` (one-time fixes, no longer needed)
- `final_fix.py` (specific one-time fixes)
- `fix_whitespace.py` (one-time fixes)
- `scripts/refactoring/refactor-core-*.py` (specific one-time refactoring tasks)
- `scripts/refactoring/fix_issues.py` (replaced by comprehensive quality checker)
- `scripts/refactoring/fix_syntax.py` (no longer needed)

### 📁 Removed Empty Directories

- `scripts/deployment/` (empty)
- `scripts/maintenance/` (empty)

### 🔄 Enhanced Existing Scripts

- **performance.py**: Added better formatting, export capabilities, and comprehensive metrics
- **update_imports.py**: Complete rewrite with advanced import analysis and optimization
- **check_code_quality.py**: New comprehensive replacement for multiple small checking scripts

## 🎯 Best Practices

### Script Development

1. **Use the script manager** for consistent execution
2. **Add new scripts** to the manager's registry
3. **Include comprehensive docstrings** and help text
4. **Support export formats** for automation
5. **Use appropriate exit codes** for CI/CD integration

### Code Quality Workflow

```bash
# 1. Check for critical errors
python scripts/manage_scripts.py run quality --severity error

# 2. Optimize imports
python scripts/manage_scripts.py run imports --root core

# 3. Run tests
python scripts/manage_scripts.py run test

# 4. Monitor performance
python scripts/manage_scripts.py run performance --detailed
```

### Maintenance Workflow

```bash
# 1. Clean up logs
python scripts/manage_scripts.py run cleanup

# 2. Reset performance metrics
python scripts/manage_scripts.py run performance --clear

# 3. Health check
python scripts/manage_scripts.py health
```

## 📈 Integration with CI/CD

All scripts support automation and can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions step
- name: Code Quality Check
  run: |
    python scripts/refactoring/check_code_quality.py --root core --export quality-report.json
    if [ $? -ne 0 ]; then
      echo "Code quality issues found"
      exit 1
    fi
```

## 🔧 Script Categories

### 📊 Monitoring
- Performance tracking
- Metrics collection
- Health monitoring

### 🛡️ Quality
- Code standards compliance
- Architecture validation
- Documentation coverage

### 🔨 Development
- Import management
- Code organization
- Structure optimization

### 🧹 Maintenance
- Log cleanup
- Cache management
- System maintenance

### 🧪 Testing
- Integration tests
- Test automation
- Quality gates

## 🚀 Future Enhancements

- **Workflow automation**: Predefined script sequences
- **Configuration management**: Centralized script settings
- **Reporting dashboard**: Web-based metrics visualization
- **Integration hooks**: Git hooks and IDE integration
- **Performance benchmarking**: Historical trend analysis

## 📞 Usage Support

For questions about specific scripts:

1. Check the script's `--help` output
2. Review the docstrings in the source code
3. Use the script manager's health check
4. Refer to this README for workflows

**Example:**
```bash
python scripts/performance.py --help
python scripts/manage_scripts.py health
```

### Quality Scripts

Scripts for maintaining code quality and standards compliance.

#### check_code_quality.py (Quality Checker)
- **Purpose**: Comprehensive code quality analysis tool
- **Status**: ✅ New - Professional grade analysis
- **Features**: 
  - Cyclomatic complexity analysis
  - Documentation coverage checking  
  - Type hint coverage analysis
  - Naming convention compliance
  - Architecture layer violation detection
  - Import analysis and circular dependency detection
  - Code smell detection
  - Line length compliance checking
- **Usage**: 
  ```bash
  python scripts/manage_scripts.py run quality --root core
  python scripts/refactoring/check_code_quality.py --export results.json
  ```

#### code_formatter.py (Code Formatter & Linter Fixer)
- **Purpose**: Automatically fix linter issues, whitespace, and flake8 violations
- **Status**: ✅ New - Comprehensive formatter
- **Features**:
  - Flake8 violations fixing (E, W, F codes)
  - Whitespace issues (trailing spaces, blank lines)
  - Line length violations
  - Import organization and cleanup
  - PEP 8 compliance issues
  - Code formatting consistency
  - Integration with black, isort, autopep8
- **Usage**:
  ```bash
  # Check what would be fixed
  python scripts/manage_scripts.py run format --check-only --root core
  
  # Apply fixes with built-in formatter
  python scripts/refactoring/code_formatter.py --root core --no-external
  
  # Apply fixes with external formatters (recommended)
  python scripts/refactoring/code_formatter.py --root core
  
  # Aggressive mode for more fixes
  python scripts/refactoring/code_formatter.py --root core --aggressive
  ```

### Development Scripts

```bash
# 1. Check for critical errors
python scripts/manage_scripts.py run quality --severity error

# 2. Optimize imports
python scripts/manage_scripts.py run imports --root core

# 3. Run tests
python scripts/manage_scripts.py run test

# 4. Monitor performance
python scripts/manage_scripts.py run performance --detailed
```

---

✨ **The scripts directory is now optimized, consolidated, and ready for efficient development workflows!** 