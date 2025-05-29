# Scripts Directory

This directory contains utility scripts to help you set up, validate, and maintain your Cursor AI Agent Rules System.

## Available Scripts

### 📋 validate_setup.py
**Purpose**: Comprehensive validation of your Cursor Rules installation and configuration

**Usage:**
```bash
# Basic validation
python scripts/validate_setup.py

# Detailed validation with customization scores
python scripts/validate_setup.py --detailed

# Check specific project directory
python scripts/validate_setup.py --project-root /path/to/your/project
```

**What it checks:**
- ✅ Directory structure and file presence
- ✅ Placeholder replacement and customization level  
- ✅ Cross-rule references and integration points
- ✅ Auto-trigger keyword configuration
- ✅ Common setup issues and file format problems

**Example output:**
```
🚀 Cursor AI Agent Rules System - Setup Validation
✓ Rules directory exists: .cursor/rules
✓ Found 010-cursor_general_rules.mdc (Central coordination hub)
⚠ 011-cursor_project_rules.mdc: Contains unreplaced placeholders: [PROJECT_NAME]
✓ Cross-reference @010-cursor_general_rules → 010-cursor_general_rules.mdc ✓

=== VALIDATION SUMMARY ===
Passed: 8
Warnings: 3  
Errors: 0
Overall Status: GOOD
```

## Requirements

### Python Scripts
- Python 3.7+
- No additional dependencies required (uses only standard library)

## Usage Tips

### For New Installations
```bash
# After copying .mdc files to .cursor/rules/
python scripts/validate_setup.py

# If you see warnings about placeholders:
# 1. Use design doc integration (see README.md)
# 2. Or manually replace placeholders in key files
```

### For Existing Installations
```bash
# Regular health check
python scripts/validate_setup.py --detailed

# Check after making customizations
python scripts/validate_setup.py
```

### Troubleshooting Common Issues

#### "Rules directory not found"
```bash
mkdir -p .cursor/rules
cp *.mdc .cursor/rules/
```

#### "Missing files"
```bash
# Download missing files from the repository
# Copy them to .cursor/rules/
```

#### "Contains unreplaced placeholders"
```bash
# Option 1: Use design doc integration (recommended)
# Open Cursor Chat and use the customization prompt from README.md

# Option 2: Manual replacement
# Edit files in .cursor/rules/ and replace [PROJECT_NAME] etc.
```

#### "Cross-reference errors"
```bash
# Usually means missing .mdc files
# Ensure all 13 files are present in .cursor/rules/
```

## Contributing Scripts

If you create useful scripts for the community:

1. **Follow naming convention**: `action_description.py`
2. **Include docstring**: Explain purpose and usage
3. **Add to this README**: Document the new script
4. **Test with multiple projects**: Ensure broad compatibility
5. **Submit pull request**: Help the community!

## Script Development Guidelines

### Python Scripts
- Use Python 3.7+ compatible code
- Include comprehensive error handling
- Provide colored output for better UX
- Support command-line arguments for flexibility
- Include detailed help text and examples

### Cross-Platform Compatibility
- Use `pathlib.Path` for file operations
- Handle different line endings appropriately
- Test on Windows, macOS, and Linux
- Avoid shell-specific commands in Python scripts 