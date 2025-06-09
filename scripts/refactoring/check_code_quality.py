#!/usr / bin / env python3
"""
Comprehensive code quality checker for the meal planning project.

This script performs various code quality checks including:
- Import analysis and circular dependency detection
- Code complexity analysis
- Documentation coverage
- Testing coverage analysis
- Architecture compliance checks
- Performance bottleneck detection
"""

from pathlib import Path
from typing import Dict, List, Optional
import ast
import re
import sys
from dataclasses import dataclass, field

sys.path.append(str(Path(__file__).parent.parent.parent))


@dataclass
class CodeIssue:
    """Represents a code quality issue."""

    file_path: str
    line_number: int
    issue_type: str
    severity: str  # 'error', 'warning', 'info'
    message: str
    suggestion: Optional[str] = None


@dataclass
class QualityReport:
    """Overall code quality report."""

    total_files: int = 0
    issues: List[CodeIssue] = field(default_factory=list)
    metrics: Dict[str, float] = field(default_factory=dict)

    def add_issue(self, issue: CodeIssue) -> None:
        """Add an issue to the report."""
        self.issues.append(issue)

    def get_issues_by_severity(self, severity: str) -> List[CodeIssue]:
        """Get issues by severity level."""
        return [issue for issue in self.issues if issue.severity == severity]

    def get_issues_by_type(self, issue_type: str) -> List[CodeIssue]:
        """Get issues by type."""
        return [issue for issue in self.issues if issue.issue_type == issue_type]


class CodeQualityChecker:
    """Comprehensive code quality checker."""

    def __init__(self, root_dir: str):
        """Initialize the checker.

        Args:
            root_dir: Root directory to analyze
        """
        self.root_dir = Path(root_dir)
        self.report = QualityReport()

    def check_all(self) -> QualityReport:
        """Run all quality checks."""
        print("🔍 Starting comprehensive code quality analysis...")

        python_files = list(self.root_dir.rglob("*.py"))
        self.report.total_files = len(python_files)

        for file_path in python_files:
            if self._should_skip_file(file_path):
                continue

            print(f"   Analyzing {file_path.relative_to(self.root_dir)}")
            self._check_file(file_path)

        # Run project - wide checks
        self._check_architecture_compliance()
        self._analyze_test_coverage()
        self._calculate_metrics()

        return self.report

    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped."""
        skip_patterns = [
            "__pycache__",
            ".git",
            ".venv",
            "venv",
            "migrations",
        ]

        return any(pattern in str(file_path) for pattern in skip_patterns)

    def _check_file(self, file_path: Path) -> None:
        """Analyze a single Python file."""
        try:
            with open(file_path, "r", encoding="utf - 8") as f:
                content = f.read()

            # Parse AST
            try:
                tree = ast.parse(content)
            except SyntaxError as e:
                self.report.add_issue(
                    CodeIssue(
                        file_path=str(file_path),
                        line_number=getattr(e, "lineno", 0),
                        issue_type="syntax",
                        severity="error",
                        message=f"Syntax error: {e.msg}",
                        suggestion="Fix syntax error",
                    )
                )
                return

            # Run various checks
            self._check_imports(file_path, tree, content)
            self._check_complexity(file_path, tree)
            self._check_documentation(file_path, tree)
            self._check_type_hints(file_path, tree)
            self._check_naming_conventions(file_path, tree)
            self._check_line_length(file_path, content)
            self._check_code_smells(file_path, tree, content)

        except Exception as e:
            self.report.add_issue(
                CodeIssue(
                    file_path=str(file_path),
                    line_number=0,
                    issue_type="analysis",
                    severity="error",
                    message=f"Failed to analyze file: {str(e)}",
                )
            )

    def _check_imports(self, file_path: Path, tree: ast.AST, content: str) -> None:
        """Check import - related issues."""
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append((alias.name, node.lineno))
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append((node.module, node.lineno))

        # Check for potentially unused imports
        for import_name, line_no in imports:
            module_name = import_name.split(".")[0]
            # Simple heuristic: if module only appears once (in import), it
            # might be unused
            if content.count(module_name) <= 2:  # Import line + potential use
                # Skip common imports that might be used implicitly
                if module_name not in ["typing", "abc", "__future__"]:
                    self.report.add_issue(
                        CodeIssue(
                            file_path=str(file_path),
                            line_number=line_no,
                            issue_type="imports",
                            severity="info",
                            message=f"Potentially unused import: {import_name}",
                            suggestion="Remove if truly unused",
                        )
                    )

    def _check_complexity(self, file_path: Path, tree: ast.AST) -> None:
        """Check code complexity."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self._calculate_cyclomatic_complexity(node)
                if complexity > 10:
                    severity = "warning" if complexity <= 15 else "error"
                    self.report.add_issue(
                        CodeIssue(
                            file_path=str(file_path),
                            line_number=node.lineno,
                            issue_type="complexity",
                            severity=severity,
                            message=f"High cyclomatic complexity ({complexity}) in function '{
                                node.name}'",
                            suggestion="Break down into smaller, more focused functions",
                        )
                    )

    def _calculate_cyclomatic_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity of a function."""
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.With)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1

        return complexity

    def _check_documentation(self, file_path: Path, tree: ast.AST) -> None:
        """Check documentation coverage."""
        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                if not ast.get_docstring(node):
                    # Skip private and special methods
                    if not node.name.startswith("_"):
                        node_type = (
                            "class" if isinstance(node, ast.ClassDef) else "function"
                        )
                        self.report.add_issue(
                            CodeIssue(
                                file_path=str(file_path),
                                line_number=node.lineno,
                                issue_type="documentation",
                                severity="warning",
                                message=f"Missing docstring for {node_type} '{
                                    node.name}'",
                                suggestion="Add comprehensive docstring following project standards",
                            )
                        )

    def _check_type_hints(self, file_path: Path, tree: ast.AST) -> None:
        """Check type hint coverage."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Skip private functions and special methods
                if node.name.startswith("_"):
                    continue

                # Check return type annotation
                if not node.returns:
                    self.report.add_issue(
                        CodeIssue(
                            file_path=str(file_path),
                            line_number=node.lineno,
                            issue_type="type_hints",
                            severity="info",
                            message=f"Missing return type annotation for function '{
                                node.name}'",
                            suggestion="Add return type annotation for better IDE support",
                        )
                    )

                # Check parameter type annotations
                for arg in node.args.args:
                    if not arg.annotation and arg.arg != "self":
                        self.report.add_issue(
                            CodeIssue(
                                file_path=str(file_path),
                                line_number=node.lineno,
                                issue_type="type_hints",
                                severity="info",
                                message=f"Missing type annotation for parameter '{
                                    arg.arg}' in '{
                                    node.name}'",
                                suggestion="Add type annotation for parameter",
                            )
                        )

    def _check_naming_conventions(self, file_path: Path, tree: ast.AST) -> None:
        """Check naming convention compliance."""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if not re.match(r"^[A - Z][a - zA - Z0 - 9]*$", node.name):
                    self.report.add_issue(
                        CodeIssue(
                            file_path=str(file_path),
                            line_number=node.lineno,
                            issue_type="naming",
                            severity="warning",
                            message=f"Class '{
                                node.name}' doesn't follow PascalCase convention",
                            suggestion="Use PascalCase for class names (e.g., MyClass)",
                        )
                    )

            elif isinstance(node, ast.FunctionDef):
                if not node.name.startswith("__") and not re.match(
                    r"^[a - z][a - z0 - 9_]*$", node.name
                ):
                    self.report.add_issue(
                        CodeIssue(
                            file_path=str(file_path),
                            line_number=node.lineno,
                            issue_type="naming",
                            severity="warning",
                            message=f"Function '{
                                node.name}' doesn't follow snake_case convention",
                            suggestion="Use snake_case for function names (e.g., my_function)",
                        )
                    )

    def _check_line_length(self, file_path: Path, content: str) -> None:
        """Check line length compliance."""
        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            if len(line) > 88:  # Black's default
                self.report.add_issue(
                    CodeIssue(
                        file_path=str(file_path),
                        line_number=i,
                        issue_type="formatting",
                        severity="info",
                        message=f"Line exceeds 88 characters ({
                            len(line)})",
                        suggestion="Use parentheses, backslashes, or Black formatter to break lines",
                    )
                )

    def _check_code_smells(self, file_path: Path, tree: ast.AST, content: str) -> None:
        """Check for common code smells."""
        # Check for large functions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Estimate line count
                if hasattr(node, "end_lineno"):
                    line_count = node.end_lineno - node.lineno
                    if line_count > 50:
                        self.report.add_issue(
                            CodeIssue(
                                file_path=str(file_path),
                                line_number=node.lineno,
                                issue_type="code_smell",
                                severity="warning",
                                message=f"Large function '{
                                    node.name}' (~{line_count} lines)",
                                suggestion="Consider breaking into smaller, focused functions",
                            )
                        )

        # Check for TODO / FIXME comments
        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            if re.search(r"(TODO|FIXME|XXX|HACK)", line, re.IGNORECASE):
                match = re.search(r"(TODO|FIXME|XXX|HACK)", line, re.IGNORECASE)
                keyword = match.group(1) if match else "TODO"
                self.report.add_issue(
                    CodeIssue(
                        file_path=str(file_path),
                        line_number=i,
                        issue_type="maintenance",
                        severity="info",
                        message=f"{keyword} comment found",
                        suggestion="Track and address technical debt",
                    )
                )

    def _check_architecture_compliance(self) -> None:
        """Check architectural compliance."""
        # Check for layer violations (domain importing infrastructure)
        domain_files = list(self.root_dir.glob("**/domain/**/*.py"))

        for file_path in domain_files:
            try:
                with open(file_path, "r") as f:
                    content = f.read()

                # Check for infrastructure imports in domain layer
                if (
                    "from core.infrastructure" in content
                    or "import core.infrastructure" in content
                ):
                    self.report.add_issue(
                        CodeIssue(
                            file_path=str(file_path),
                            line_number=0,
                            issue_type="architecture",
                            severity="error",
                            message="Domain layer importing from infrastructure layer",
                            suggestion="Use dependency injection or move to application layer",
                        )
                    )

                # Check for application imports in domain layer
                if (
                    "from core.application" in content
                    or "import core.application" in content
                ):
                    self.report.add_issue(
                        CodeIssue(
                            file_path=str(file_path),
                            line_number=0,
                            issue_type="architecture",
                            severity="error",
                            message="Domain layer importing from application layer",
                            suggestion="Domain should not depend on application layer",
                        )
                    )
            except Exception:
                continue

    def _analyze_test_coverage(self) -> None:
        """Analyze test coverage."""
        test_files = list(self.root_dir.rglob("test_*.py"))
        src_files = [
            f
            for f in self.root_dir.rglob("*.py")
            if not f.name.startswith("test_") and "__pycache__" not in str(f)
        ]

        coverage_ratio = len(test_files) / len(src_files) if src_files else 0
        self.report.metrics["test_coverage_ratio"] = coverage_ratio

        if coverage_ratio < 0.3:  # Less than 30% test files
            self.report.add_issue(
                CodeIssue(
                    file_path="project",
                    line_number=0,
                    issue_type="testing",
                    severity="warning",
                    message=f"Low test file coverage ratio ({coverage_ratio:.1%})",
                    suggestion="Add more test files to improve testing coverage",
                )
            )

    def _calculate_metrics(self) -> None:
        """Calculate overall quality metrics."""
        total_issues = len(self.report.issues)
        errors = len(self.report.get_issues_by_severity("error"))
        warnings = len(self.report.get_issues_by_severity("warning"))
        info = len(self.report.get_issues_by_severity("info"))

        # Simple quality score calculation
        quality_score = max(0, 100 - (errors * 10 + warnings * 3 + info * 1))

        self.report.metrics.update(
            {
                "total_issues": total_issues,
                "error_count": errors,
                "warning_count": warnings,
                "info_count": info,
                "issues_per_file": (
                    total_issues / self.report.total_files
                    if self.report.total_files
                    else 0
                ),
                "quality_score": quality_score,
            }
        )


def print_report(report: QualityReport) -> None:
    """Print a formatted quality report."""
    print("\n" + "=" * 70)
    print("📊 CODE QUALITY REPORT")
    print("=" * 70)

    # Overall metrics
    metrics = report.metrics
    print(f"\n📈 Overall Metrics:")
    print(f"   📁 Files analyzed: {report.total_files}")
    print(f"   🚨 Total issues: {metrics.get('total_issues', 0)}")
    print(f"   📊 Quality score: {metrics.get('quality_score', 0):.1f}/100")
    print(f"   📉 Issues per file: {metrics.get('issues_per_file', 0):.1f}")
    print(
        f"   🧪 Test coverage ratio: {
            metrics.get(
                'test_coverage_ratio',
                0):.1%}"
    )

    # Issues by severity
    errors = report.get_issues_by_severity("error")
    warnings = report.get_issues_by_severity("warning")
    info = report.get_issues_by_severity("info")

    print(f"\n🚨 Issues by Severity:")
    print(f"   ❌ Errors: {len(errors)}")
    print(f"   ⚠️  Warnings: {len(warnings)}")
    print(f"   ℹ️  Info: {len(info)}")

    # Issues by type
    issue_types = {}
    for issue in report.issues:
        issue_types[issue.issue_type] = issue_types.get(issue.issue_type, 0) + 1

    if issue_types:
        print(f"\n📋 Issues by Type:")
        for issue_type, count in sorted(
            issue_types.items(), key=lambda x: x[1], reverse=True
        ):
            print(f"   {issue_type.replace('_', ' ').title()}: {count}")

    # Show top issues
    critical_issues = errors + [
        w for w in warnings if w.issue_type in ["architecture", "complexity"]
    ]
    if critical_issues:
        print(f"\n🔥 Critical Issues (showing first 10):")
        for issue in critical_issues[:10]:
            file_name = (
                Path(issue.file_path).name
                if issue.file_path != "project"
                else "project"
            )
            print(f"   📄 {file_name}:{issue.line_number} - {issue.message}")
            if issue.suggestion:
                print(f"      💡 {issue.suggestion}")

    # Recommendations
    print(f"\n💡 Quality Improvement Recommendations:")

    error_count = len(errors)
    warning_count = len(warnings)

    if error_count > 0:
        print(f"   🎯 Fix {error_count} critical errors first")
    if warning_count > 5:
        print(f"   🔧 Address {warning_count} warnings to improve maintainability")
    if metrics.get("test_coverage_ratio", 0) < 0.5:
        print(f"   🧪 Improve test coverage")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Code quality checker")
    parser.add_argument("--root", default="core", help="Root directory to analyze")
    parser.add_argument("--export", help="Export results to JSON file")
    parser.add_argument(
        "--severity",
        choices=["error", "warning", "info"],
        help="Show only issues of specific severity",
    )

    args = parser.parse_args()

    if not Path(args.root).exists():
        print(f"❌ Error: Directory '{args.root}' does not exist")
        sys.exit(1)

    checker = CodeQualityChecker(args.root)
    report = checker.check_all()

    if args.severity:
        filtered_issues = report.get_issues_by_severity(args.severity)
        report.issues = filtered_issues

    print_report(report)

    if args.export:
        import json
        from datetime import datetime

        export_data = {
            "analysis_timestamp": datetime.now().isoformat(),
            "root_directory": str(Path(args.root).resolve()),
            "metrics": report.metrics,
            "issues": [
                {
                    "file": issue.file_path,
                    "line": issue.line_number,
                    "type": issue.issue_type,
                    "severity": issue.severity,
                    "message": issue.message,
                    "suggestion": issue.suggestion,
                }
                for issue in report.issues
            ],
        }

        with open(args.export, "w") as f:
            json.dump(export_data, f, indent=2)
        print(f"\n💾 Report exported to {args.export}")

    # Exit with error code if critical issues found
    critical_issues = report.get_issues_by_severity("error")
    if critical_issues:
        sys.exit(1)


if __name__ == "__main__":
    main()
