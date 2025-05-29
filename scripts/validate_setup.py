#!/usr/bin/env python3
"""
Cursor AI Agent Rules System - Setup Validation Script

This script validates that the Cursor AI Agent Rules System is properly installed
and configured for your project. It checks file presence, placeholder replacement,
and cross-rule integration points.

Usage:
    python scripts/validate_setup.py
    python scripts/validate_setup.py --fix-common-issues
    python scripts/validate_setup.py --detailed-report
"""

import os
import sys
import re
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Set
import json

class Colors:
    """Terminal color codes for better output formatting"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class ValidationResult:
    """Container for validation results"""
    def __init__(self):
        self.passed = 0
        self.warnings = 0
        self.errors = 0
        self.messages = []
        
    def add_pass(self, message: str):
        self.passed += 1
        self.messages.append((f"{Colors.GREEN}✓{Colors.END}", message))
        
    def add_warning(self, message: str):
        self.warnings += 1
        self.messages.append((f"{Colors.YELLOW}⚠{Colors.END}", message))
        
    def add_error(self, message: str):
        self.errors += 1
        self.messages.append((f"{Colors.RED}✗{Colors.END}", message))
        
    def print_summary(self):
        print(f"\n{Colors.BOLD}=== VALIDATION SUMMARY ==={Colors.END}")
        print(f"{Colors.GREEN}Passed: {self.passed}{Colors.END}")
        print(f"{Colors.YELLOW}Warnings: {self.warnings}{Colors.END}")
        print(f"{Colors.RED}Errors: {self.errors}{Colors.END}")
        
        overall_status = "GOOD" if self.errors == 0 else "NEEDS ATTENTION"
        status_color = Colors.GREEN if self.errors == 0 else Colors.RED
        print(f"\n{Colors.BOLD}Overall Status: {status_color}{overall_status}{Colors.END}")

class CursorRulesValidator:
    """Main validator for Cursor AI Agent Rules System"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.rules_dir = self.project_root / ".cursor" / "rules"
        self.result = ValidationResult()
        
        # Expected rule files
        self.required_files = {
            "010-cursor_general_rules.mdc": "Central coordination hub",
            "011-cursor_project_rules.mdc": "Technology stack templates",
            "012-learned_memories.mdc": "Project knowledge storage", 
            "013-cursor_riper_rules.mdc": "RIPER methodology framework",
            "020-task_list.mdc": "Active task management",
            "021-cursor_environment_rules.mdc": "Environment detection",
            "022-cursor_git_rules.mdc": "Git workflow integration",
            "030-cursor_task_rules.mdc": "Task workflow rules",
            "031-cursor_memory_rules.mdc": "Memory management framework",
            "032-cursor_quality_rules.mdc": "Quality assurance gates",
            "040-cursor_organization_rules.mdc": "File organization standards",
            "090-completed_tasks.mdc": "Task completion archive",
            "091-learned_memories_archive.mdc": "Historical knowledge archive"
        }
        
        # Common placeholders that should be replaced
        self.placeholders = [
            "[PROJECT_NAME]",
            "[PROJECT_COMMAND_QUALITY]", 
            "[MAIN_LANGUAGE]",
            "[TECH_STACK]",
            "[FRAMEWORK]",
            "[MIN_VERSION]",
            "[PACKAGE_MANAGER]"
        ]
        
        # Cross-rule references
        self.cross_references = {
            "@010-cursor_general_rules": "010-cursor_general_rules.mdc",
            "@011-cursor_project_rules": "011-cursor_project_rules.mdc",
            "@012-learned_memories": "012-learned_memories.mdc",
            "@013-cursor_riper_rules": "013-cursor_riper_rules.mdc",
            "@020-task_list": "020-task_list.mdc",
            "@021-cursor_environment_rules": "021-cursor_environment_rules.mdc",
            "@022-cursor_git_rules": "022-cursor_git_rules.mdc",
            "@030-cursor_task_rules": "030-cursor_task_rules.mdc",
            "@031-cursor_memory_rules": "031-cursor_memory_rules.mdc",
            "@032-cursor_quality_rules": "032-cursor_quality_rules.mdc",
            "@040-cursor_organization_rules": "040-cursor_organization_rules.mdc",
            "@090-completed_tasks": "090-completed_tasks.mdc",
            "@091-learned_memories_archive": "091-learned_memories_archive.mdc"
        }

    def validate_directory_structure(self):
        """Check if required directories and files exist"""
        print(f"{Colors.BOLD}Checking Directory Structure...{Colors.END}")
        
        if not self.rules_dir.exists():
            self.result.add_error(f"Rules directory not found: {self.rules_dir}")
            return
            
        self.result.add_pass(f"Rules directory exists: {self.rules_dir}")
        
        # Check for required files
        for filename, description in self.required_files.items():
            file_path = self.rules_dir / filename
            if file_path.exists():
                self.result.add_pass(f"Found {filename} ({description})")
            else:
                self.result.add_error(f"Missing {filename} ({description})")
                
        # Check for legacy .cursorrules file
        legacy_file = self.project_root / ".cursorrules"
        if legacy_file.exists():
            self.result.add_warning("Found legacy .cursorrules file - consider removing to avoid conflicts")

    def validate_file_content(self):
        """Check file content for common issues"""
        print(f"\n{Colors.BOLD}Checking File Content...{Colors.END}")
        
        for filename in self.required_files.keys():
            file_path = self.rules_dir / filename
            if not file_path.exists():
                continue
                
            try:
                content = file_path.read_text(encoding='utf-8')
                self._check_file_content(filename, content)
            except Exception as e:
                self.result.add_error(f"Could not read {filename}: {e}")

    def _check_file_content(self, filename: str, content: str):
        """Check individual file content"""
        # Check for placeholders that might need replacement
        unreplaced_placeholders = []
        for placeholder in self.placeholders:
            if placeholder in content:
                unreplaced_placeholders.append(placeholder)
                
        if unreplaced_placeholders:
            self.result.add_warning(
                f"{filename}: Contains unreplaced placeholders: {', '.join(unreplaced_placeholders)}"
            )
        else:
            self.result.add_pass(f"{filename}: Placeholders appear to be customized")
            
        # Check for proper MDC format
        if not content.startswith('---') and 'description:' in content[:500]:
            self.result.add_pass(f"{filename}: Proper MDC format with metadata")
        elif content.startswith('#'):
            self.result.add_pass(f"{filename}: Valid Markdown format")
        else:
            self.result.add_warning(f"{filename}: Unusual file format detected")
            
        # Check for cross-rule references
        found_refs = []
        for ref_pattern, target_file in self.cross_references.items():
            if ref_pattern in content:
                found_refs.append(ref_pattern)
                
        if found_refs:
            self.result.add_pass(f"{filename}: Contains {len(found_refs)} cross-rule references")

    def validate_cross_references(self):
        """Validate that cross-rule references point to existing files"""
        print(f"\n{Colors.BOLD}Checking Cross-Rule References...{Colors.END}")
        
        all_references = set()
        reference_sources = {}
        
        for filename in self.required_files.keys():
            file_path = self.rules_dir / filename
            if not file_path.exists():
                continue
                
            try:
                content = file_path.read_text(encoding='utf-8')
                for ref_pattern in self.cross_references.keys():
                    if ref_pattern in content:
                        all_references.add(ref_pattern)
                        if ref_pattern not in reference_sources:
                            reference_sources[ref_pattern] = []
                        reference_sources[ref_pattern].append(filename)
            except Exception:
                continue
                
        # Check if referenced files exist
        for ref_pattern, target_file in self.cross_references.items():
            if ref_pattern in all_references:
                target_path = self.rules_dir / target_file
                if target_path.exists():
                    self.result.add_pass(f"Cross-reference {ref_pattern} → {target_file} ✓")
                else:
                    self.result.add_error(f"Cross-reference {ref_pattern} → MISSING {target_file}")
                    
        if all_references:
            self.result.add_pass(f"Found {len(all_references)} total cross-rule references")
        else:
            self.result.add_warning("No cross-rule references found - integration may not work properly")

    def validate_customization_level(self):
        """Check how well the system has been customized"""
        print(f"\n{Colors.BOLD}Checking Customization Level...{Colors.END}")
        
        customization_scores = {}
        
        for filename in self.required_files.keys():
            file_path = self.rules_dir / filename
            if not file_path.exists():
                continue
                
            try:
                content = file_path.read_text(encoding='utf-8')
                score = self._calculate_customization_score(content)
                customization_scores[filename] = score
            except Exception:
                continue
                
        if customization_scores:
            avg_score = sum(customization_scores.values()) / len(customization_scores)
            
            if avg_score >= 80:
                self.result.add_pass(f"High customization level: {avg_score:.1f}%")
            elif avg_score >= 50:
                self.result.add_warning(f"Moderate customization level: {avg_score:.1f}%")
            else:
                self.result.add_warning(f"Low customization level: {avg_score:.1f}% - consider using design doc integration")
                
            # Show individual file scores if detailed
            if hasattr(self, 'detailed') and self.detailed:
                for filename, score in sorted(customization_scores.items()):
                    status = "✓" if score >= 70 else "⚠" if score >= 40 else "✗"
                    print(f"  {status} {filename}: {score:.1f}%")

    def _calculate_customization_score(self, content: str) -> float:
        """Calculate customization score based on placeholder replacement and content"""
        total_checks = 0
        passed_checks = 0
        
        # Check placeholder replacement
        for placeholder in self.placeholders:
            total_checks += 1
            if placeholder not in content:
                passed_checks += 1
                
        # Check for project-specific content (heuristics)
        project_indicators = [
            r'[A-Za-z]+Service',  # Service names
            r'api\.',  # API references
            r'npm|pip|cargo|go',  # Package managers
            r'React|Django|Flask|Express',  # Frameworks
            r'\.env|\.json|\.yaml',  # Config files
        ]
        
        for pattern in project_indicators:
            total_checks += 1
            if re.search(pattern, content, re.IGNORECASE):
                passed_checks += 1
                
        return (passed_checks / total_checks * 100) if total_checks > 0 else 0

    def validate_integration_keywords(self):
        """Check if auto-trigger keywords are properly configured"""
        print(f"\n{Colors.BOLD}Checking Auto-Trigger Keywords...{Colors.END}")
        
        keyword_files = {
            "010-cursor_general_rules.mdc": ["task", "quality", "project"],
            "011-cursor_project_rules.mdc": ["code", "implementation", "standard"],
            "013-cursor_riper_rules.mdc": ["research", "plan", "execute", "review"],
            "020-task_list.mdc": ["task", "priority", "feature"],
            "021-cursor_environment_rules.mdc": ["environment", "deploy", "config"],
            "032-cursor_quality_rules.mdc": ["quality", "test", "validation"]
        }
        
        for filename, expected_keywords in keyword_files.items():
            file_path = self.rules_dir / filename
            if not file_path.exists():
                continue
                
            try:
                content = file_path.read_text(encoding='utf-8').lower()
                found_keywords = [kw for kw in expected_keywords if kw in content]
                
                if len(found_keywords) >= len(expected_keywords) * 0.7:  # 70% threshold
                    self.result.add_pass(f"{filename}: Auto-trigger keywords configured")
                else:
                    self.result.add_warning(f"{filename}: Missing some auto-trigger keywords")
            except Exception:
                continue

    def check_common_issues(self):
        """Check for common setup issues"""
        print(f"\n{Colors.BOLD}Checking Common Issues...{Colors.END}")
        
        # Check for common file extension mistakes
        cursor_dir = self.project_root / ".cursor"
        if cursor_dir.exists():
            md_files = list(cursor_dir.rglob("*.md"))
            if md_files:
                self.result.add_warning(f"Found .md files in .cursor/ - should be .mdc: {[f.name for f in md_files]}")
                
        # Check for empty files
        for filename in self.required_files.keys():
            file_path = self.rules_dir / filename
            if file_path.exists() and file_path.stat().st_size < 100:
                self.result.add_warning(f"{filename}: File is very small (< 100 bytes)")
                
        # Check for potential encoding issues
        for filename in self.required_files.keys():
            file_path = self.rules_dir / filename
            if file_path.exists():
                try:
                    content = file_path.read_text(encoding='utf-8')
                    if '\ufffd' in content:  # Unicode replacement character
                        self.result.add_error(f"{filename}: Contains encoding errors")
                except UnicodeDecodeError:
                    self.result.add_error(f"{filename}: UTF-8 encoding error")

    def generate_suggestions(self):
        """Generate specific suggestions based on validation results"""
        print(f"\n{Colors.BOLD}Recommendations...{Colors.END}")
        
        if self.result.errors > 0:
            print(f"{Colors.RED}🔧 Required Actions:{Colors.END}")
            if not self.rules_dir.exists():
                print("  • Create .cursor/rules directory and copy .mdc files")
            
            missing_files = []
            for filename in self.required_files.keys():
                if not (self.rules_dir / filename).exists():
                    missing_files.append(filename)
                    
            if missing_files:
                print(f"  • Copy missing files: {', '.join(missing_files)}")
                
        if self.result.warnings > 0:
            print(f"{Colors.YELLOW}💡 Suggested Improvements:{Colors.END}")
            print("  • Use design doc integration for better customization")
            print("  • Replace placeholder values with project specifics")
            print("  • Test with: 'Following our project rules, help me plan a feature'")
            
        if self.result.errors == 0 and self.result.warnings <= 2:
            print(f"{Colors.GREEN}🎉 Great job! Your setup looks good.{Colors.END}")
            print("  • Try: 'Load our task list and show priorities'")
            print("  • Try: 'Use RIPER methodology for this implementation'")

    def run_full_validation(self, detailed: bool = False):
        """Run complete validation suite"""
        self.detailed = detailed
        
        print(f"{Colors.BOLD}{Colors.CYAN}🚀 Cursor AI Agent Rules System - Setup Validation{Colors.END}")
        print(f"Project: {self.project_root.absolute()}")
        print(f"Rules Directory: {self.rules_dir}")
        
        self.validate_directory_structure()
        self.validate_file_content()
        self.validate_cross_references()
        self.validate_customization_level()
        self.validate_integration_keywords()
        self.check_common_issues()
        
        # Print all messages
        print(f"\n{Colors.BOLD}Detailed Results:{Colors.END}")
        for symbol, message in self.result.messages:
            print(f"  {symbol} {message}")
            
        self.result.print_summary()
        self.generate_suggestions()
        
        return self.result.errors == 0

def main():
    parser = argparse.ArgumentParser(description="Validate Cursor AI Agent Rules System setup")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--detailed", action="store_true", help="Show detailed validation report")
    parser.add_argument("--fix-common-issues", action="store_true", help="Attempt to fix common issues")
    
    args = parser.parse_args()
    
    validator = CursorRulesValidator(args.project_root)
    
    if args.fix_common_issues:
        print(f"{Colors.YELLOW}Auto-fix not implemented yet. Please fix issues manually.{Colors.END}")
        
    success = validator.run_full_validation(detailed=args.detailed)
    
    exit_code = 0 if success else 1
    sys.exit(exit_code)

if __name__ == "__main__":
    main() 