# Plan Mensual Comidas - File Organization & Cleanup Plan

## 🎯 **OBJECTIVE**
Systematically review, consolidate, and organize all files in the Plan Mensual Comidas project to eliminate duplicates, deprecated files, and improve maintainability.

## 🚨 **CRITICAL ISSUES IDENTIFIED**

### 1. **DUPLICATE DATA DIRECTORIES**
```
❌ PROBLEMS:
- data/                    (normal directory)
- data /                   (directory with trailing space)
- data / recipes / errores/ (contains: test_recipe.txt)
- data/recipes/errores/    (contains: multiple test files)

✅ SOLUTION:
- Remove the "data /" directory entirely
- Consolidate all content into "data/"
- Update any scripts that reference the spaced directory
```

### 2. **SCATTERED CONFIGURATION FILES**
```
❌ CURRENT STATE:
- mypy.ini (root level)
- config/testing/mypy.ini
- pytest.ini (root level)  
- config/testing/pytest.ini
- pyproject.toml (root level)
- setup.cfg (root level)

✅ CONSOLIDATION PLAN:
- Move ALL config to pyproject.toml (modern standard)
- Keep config/testing/ for environment-specific overrides only
- Remove duplicate root-level config files
```

### 3. **DOCUMENTATION STRUCTURE**
```
📁 CURRENT: docs/
├── automation-improvements.md
├── development.md
├── llm.md
├── notion.md
├── roadmap.md
├── user-guide.md
├── validation-report.md
├── features/
├── llm/
├── tools/
└── examples/

✅ ORGANIZATION:
- Consolidate scattered .md files into logical subdirectories
- Remove outdated documentation
- Create clear documentation hierarchy
```

### 4. **SCRIPTS ORGANIZATION**
```
📁 CURRENT: scripts/
├── development/
├── refactoring/
├── manage_scripts.py
├── performance.py
├── test_docs.py
├── cleanup_logs.sh
└── run_integration_tests.sh

✅ STATUS: Well organized, minimal cleanup needed
```

### 5. **TEST STRUCTURE ANALYSIS**
```
📊 STATISTICS:
- Total test files: 36
- Total Python files (non-test): 115
- Test coverage appears comprehensive

✅ STATUS: Good structure, check for deprecated tests only
```

## 🔧 **IMMEDIATE CLEANUP ACTIONS**

### **PRIORITY 1: Fix Directory Issues**
1. **Remove problematic spaced directory:**
   ```bash
   # Check contents first
   find "data /" -type f
   # Remove if confirmed duplicate
   rm -rf "data /"
   ```

2. **Verify data integrity:**
   ```bash
   # Ensure all recipe files are in data/recipes/
   find data/recipes/ -name "*.txt" | wc -l
   ```

### **PRIORITY 2: Consolidate Configuration**
1. **Move all config to pyproject.toml:**
   - Merge mypy.ini settings
   - Merge pytest.ini settings
   - Merge setup.cfg settings

2. **Remove redundant files:**
   ```bash
   rm mypy.ini pytest.ini setup.cfg
   ```

3. **Keep config/testing/ for environment-specific overrides only**

### **PRIORITY 3: Documentation Cleanup**
1. **Create logical structure:**
   ```
   docs/
   ├── README.md
   ├── user-guide/
   ├── development/
   ├── architecture/
   ├── api/
   └── tools/
   ```

2. **Move files to appropriate directories**

## 📋 **EXECUTION PLAN**

### **Phase 1: Safety Backup**
- [ ] Create git branch: `cleanup/file-organization`
- [ ] Verify all important files are tracked in git

### **Phase 2: Directory Cleanup**
- [ ] Remove `data /` directory after content verification
- [ ] Verify all recipe test files are properly located

### **Phase 3: Configuration Consolidation**
- [ ] Create comprehensive pyproject.toml
- [ ] Remove old config files

### **Phase 4: Final Verification**
- [ ] Run all tests to ensure nothing is broken
- [ ] Verify all scripts work correctly

## 🎯 **SUCCESS CRITERIA**
- [ ] No duplicate directories
- [ ] Single source of truth for configuration
- [ ] Logical documentation hierarchy
- [ ] All tests pass
- [ ] All scripts functional
- [ ] Clean git status

## ⚠️ **RISKS & MITIGATION**
- **Risk:** Breaking existing workflows
- **Mitigation:** Work in feature branch, test thoroughly
- **Risk:** Losing important configuration
- **Mitigation:** Careful migration, backup everything
- **Risk:** Breaking relative imports
- **Mitigation:** Update paths systematically, test imports 