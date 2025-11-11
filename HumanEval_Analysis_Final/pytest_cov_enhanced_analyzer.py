#!/usr/bin/env python3
"""
Enhanced Pytest-Cov Coverage Analyzer
Combines smart function handling with pytest-cov for accurate coverage measurement
"""

import json
import os
import subprocess
import tempfile
import shutil
import re
import ast
import importlib.util
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import pandas as pd


@dataclass
class CoverageResult:
    """Coverage result for a single solution"""
    problem_id: str
    llm_implementation: str
    tests_passed: int
    tests_failed: int
    total_tests: int
    line_coverage: float
    branch_coverage: Optional[float]
    interpretation: str
    error_details: List[str]


class PytestCovAnalyzer:
    """Enhanced analyzer using pytest-cov with smart function handling"""
    
    def __init__(self, test_cases_file: str = "selected_problems_testcases.json", 
                 html_output_dir: str = "coverage_html_reports"):
        self.test_cases_file = test_cases_file
        self.test_cases = {}
        self.html_output_dir = html_output_dir
        self.load_test_cases()
        
        # Create main HTML output directory
        if os.path.exists(self.html_output_dir):
            shutil.rmtree(self.html_output_dir)
        os.makedirs(self.html_output_dir, exist_ok=True)
    
    def load_test_cases(self):
        """Load test cases from JSON"""
        with open(self.test_cases_file, 'r') as f:
            self.test_cases = json.load(f)
        print(f"Loaded {len(self.test_cases)} problems with test cases")
    
    def get_function_name(self, solution_path: str, problem_id: str) -> str:
        """Extract the actual function name from solution file"""
        try:
            with open(solution_path, 'r') as f:
                content = f.read()
            
            # Special case for HumanEval/94
            if problem_id == "HumanEval/94":
                if 'def skjkasdkd' in content:
                    return 'skjkasdkd'
            
            # Parse AST to find function names
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Return first non-helper function
                    if not node.name.startswith('_'):
                        return node.name
        except Exception as e:
            print(f"    Warning: Could not parse {solution_path}: {e}")
        
        return "candidate"  # Fallback
    
    def create_pytest_test_file(self, solution_path: str, test_cases: List[str], 
                                problem_id: str, temp_dir: str) -> str:
        """Create a pytest test file for the solution"""
        problem_num = problem_id.split('/')[-1]
        test_file_path = os.path.join(temp_dir, f"test_humaneval_{problem_num}.py")
        
        # Get actual function name
        func_name = self.get_function_name(solution_path, problem_id)
        
        # Get solution details
        solution_module = Path(solution_path).stem
        solution_dir = str(Path(solution_path).parent.absolute())
        
        # Create test file content
        test_content = f"""# Auto-generated pytest test for {problem_id}
import sys
sys.path.insert(0, r'{solution_dir}')

try:
    from {solution_module} import {func_name}
except ImportError as e:
    print(f"Import error: {{e}}")
    {func_name} = None

# Create aliases for test compatibility
candidate = {func_name}
skjkasdkd = {func_name}  # For HumanEval/94

"""
        
        # Add test functions
        for i, test_case in enumerate(test_cases):
            # Clean up the test case
            test_code = test_case.strip()
            if not test_code.startswith('assert'):
                test_code = f"assert {test_code}"
            
            test_content += f"""
def test_case_{i}():
    \"\"\"Test case {i+1}\"\"\"
    {test_code}
"""
        
        # Write test file
        with open(test_file_path, 'w') as f:
            f.write(test_content)
        
        return test_file_path
    
    def run_pytest_with_coverage(self, solution_path: str, test_cases: List[str], 
                                 problem_id: str, llm_implementation: str = "") -> CoverageResult:
        """Run pytest with coverage for a solution"""
        temp_dir = tempfile.mkdtemp(prefix='pytest_cov_')
        
        try:
            # Create test file
            test_file = self.create_pytest_test_file(
                solution_path, test_cases, problem_id, temp_dir
            )
            
            # Prepare coverage command
            solution_module = Path(solution_path).stem
            coverage_json = os.path.join(temp_dir, 'coverage.json')
            html_temp_dir = os.path.join(temp_dir, 'htmlcov')
            
            cmd = [
                'pytest',
                test_file,
                f'--cov={solution_module}',
                '--cov-branch',
                '--cov-report=term-missing',
                f'--cov-report=json:{coverage_json}',
                f'--cov-report=html:{html_temp_dir}',
                '-v',
                '--tb=line',
                '-p', 'no:warnings'
            ]
            
            # Run pytest
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=temp_dir,
                timeout=30
            )
            
            # Parse results
            tests_passed, tests_failed = self._parse_test_counts(result.stdout + result.stderr, len(test_cases))
            line_cov, branch_cov = self._parse_coverage(coverage_json, solution_path)
            interpretation = self._generate_interpretation(tests_passed, tests_failed, line_cov, branch_cov)
            error_details = self._extract_errors(result.stdout + result.stderr)
            
            # Save HTML report to organized structure
            if llm_implementation and os.path.exists(html_temp_dir):
                self._save_html_report(html_temp_dir, llm_implementation, problem_id)
            
            return CoverageResult(
                problem_id=problem_id,
                llm_implementation="",  # Will be set by caller
                tests_passed=tests_passed,
                tests_failed=tests_failed,
                total_tests=len(test_cases),
                line_coverage=line_cov,
                branch_coverage=branch_cov,
                interpretation=interpretation,
                error_details=error_details
            )
            
        except subprocess.TimeoutExpired:
            return CoverageResult(
                problem_id=problem_id,
                llm_implementation="",
                tests_passed=0,
                tests_failed=len(test_cases),
                total_tests=len(test_cases),
                line_coverage=0.0,
                branch_coverage=None,
                interpretation="Timeout - execution exceeded 30 seconds",
                error_details=["Timeout"]
            )
        except Exception as e:
            return CoverageResult(
                problem_id=problem_id,
                llm_implementation="",
                tests_passed=0,
                tests_failed=len(test_cases),
                total_tests=len(test_cases),
                line_coverage=0.0,
                branch_coverage=None,
                interpretation=f"Error: {str(e)}",
                error_details=[str(e)]
            )
        finally:
            # Cleanup
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
    
    def _parse_test_counts(self, output: str, total_tests: int) -> Tuple[int, int]:
        """Parse test pass/fail counts from pytest output"""
        passed_match = re.search(r'(\d+) passed', output)
        failed_match = re.search(r'(\d+) failed', output)
        
        passed = int(passed_match.group(1)) if passed_match else 0
        failed = int(failed_match.group(1)) if failed_match else 0
        
        # If no explicit counts and return code indicates success
        if passed == 0 and failed == 0:
            if 'passed' in output.lower():
                passed = total_tests
            else:
                failed = total_tests
        
        return passed, failed
    
    def _parse_coverage(self, coverage_json_path: str, solution_path: str) -> Tuple[float, Optional[float]]:
        """Parse coverage data from JSON file"""
        try:
            if not os.path.exists(coverage_json_path):
                return 0.0, None
            
            with open(coverage_json_path, 'r') as f:
                cov_data = json.load(f)
            
            # Find the solution file in coverage data
            solution_file = Path(solution_path).name
            solution_abs = str(Path(solution_path).resolve())
            
            file_data = None
            for file_path, data in cov_data.get('files', {}).items():
                if solution_file in file_path or file_path == solution_abs:
                    file_data = data
                    break
            
            if file_data:
                summary = file_data.get('summary', {})
                line_cov = summary.get('percent_covered', 0.0)
                
                # Branch coverage
                branch_cov = None
                if 'num_branches' in summary and summary['num_branches'] > 0:
                    covered_branches = summary.get('covered_branches', 0)
                    total_branches = summary.get('num_branches', 0)
                    if total_branches > 0:
                        branch_cov = (covered_branches / total_branches) * 100
                
                return line_cov, branch_cov
        except Exception as e:
            print(f"      Warning: Could not parse coverage: {e}")
        
        return 0.0, None
    
    def _generate_interpretation(self, passed: int, failed: int, line_cov: float, 
                                 branch_cov: Optional[float]) -> str:
        """Generate one-line interpretation"""
        if failed > 0:
            return f"{failed} test(s) failed - fix failing tests first"
        
        if line_cov < 50:
            return "Low line coverage - significant untested code paths"
        elif line_cov < 80:
            return "Moderate line coverage - some untested code paths"
        
        if branch_cov is not None:
            if branch_cov < 50:
                return "Low branch coverage - untested conditional logic and error paths"
            elif branch_cov < 80:
                return "Moderate branch coverage - some conditional branches untested"
        
        if line_cov >= 90:
            if branch_cov and branch_cov >= 90:
                return "Excellent coverage - well-tested code"
            elif branch_cov:
                return "Good line coverage but some branches untested"
            else:
                return "Good line coverage achieved"
        
        return "Adequate coverage"
    
    def _extract_errors(self, output: str) -> List[str]:
        """Extract error messages from pytest output"""
        errors = []
        for line in output.split('\n'):
            if 'FAILED' in line or 'ERROR' in line or 'AssertionError' in line:
                errors.append(line.strip())
                if len(errors) >= 3:
                    break
        return errors
    
    def _save_html_report(self, html_temp_dir: str, llm_implementation: str, problem_id: str):
        """Save HTML coverage report to organized directory structure"""
        try:
            # Create directory structure: coverage_html_reports/llm_name/problem_id/
            problem_num = problem_id.split('/')[-1]
            target_dir = os.path.join(self.html_output_dir, llm_implementation, f"HumanEval_{problem_num}")
            
            # Copy HTML report
            if os.path.exists(target_dir):
                shutil.rmtree(target_dir)
            shutil.copytree(html_temp_dir, target_dir)
            
        except Exception as e:
            print(f"      Warning: Could not save HTML report: {e}")
    
    def analyze_all_solutions(self, base_path: str = "codes") -> List[CoverageResult]:
        """Analyze all solutions across all LLM implementations"""
        llm_implementations = [
            "gemma_Self_Planning",
            "gemma_self_edit",
            "llama_self_edit",
            "llama_self_planning"
        ]
        
        all_results = []
        
        print("\n" + "="*80)
        print("Running Pytest-Cov Analysis")
        print("="*80)
        
        for llm_impl in llm_implementations:
            print(f"\n{llm_impl}:")
            impl_path = os.path.join(base_path, llm_impl)
            
            if not os.path.exists(impl_path):
                continue
            
            for problem_id, test_cases in sorted(self.test_cases.items()):
                problem_num = problem_id.split('/')[-1]
                solution_file = f"HumanEval_{problem_num}.py"
                solution_path = os.path.join(impl_path, solution_file)
                
                if not os.path.exists(solution_path):
                    print(f"  {problem_id}: File not found")
                    continue
                
                print(f"  {problem_id}...", end=" ", flush=True)
                
                result = self.run_pytest_with_coverage(solution_path, test_cases, problem_id, llm_impl)
                result.llm_implementation = llm_impl
                all_results.append(result)
                
                # Status indicator
                status = "✓" if result.tests_failed == 0 else "✗"
                print(f"{status} {result.tests_passed}/{result.total_tests} tests, "
                      f"Line: {result.line_coverage:.1f}%, "
                      f"Branch: {result.branch_coverage:.1f}%" if result.branch_coverage else "N/A")
        
        return all_results
    
    def generate_reports(self, results: List[CoverageResult]):
        """Generate summary table and Excel reports"""
        if not results:
            print("No results to report")
            return
        
        # Console summary table
        print("\n" + "="*120)
        print("COVERAGE SUMMARY TABLE")
        print("="*120)
        print(f"{'Problem':<15} {'LLM':<25} {'Tests':<12} {'Line %':<10} {'Branch %':<12} {'Interpretation':<40}")
        print("-"*120)
        
        # Sort by LLM implementation and then by problem number
        def get_problem_num(problem_id):
            try:
                return int(problem_id.split('/')[-1])
            except:
                return 999
        
        for result in sorted(results, key=lambda x: (x.llm_implementation, get_problem_num(x.problem_id))):
            branch_str = f"{result.branch_coverage:.1f}" if result.branch_coverage else "N/A"
            print(f"{result.problem_id:<15} {result.llm_implementation:<25} "
                  f"{result.tests_passed}/{result.total_tests:<9} "
                  f"{result.line_coverage:<10.1f} {branch_str:<12} "
                  f"{result.interpretation:<40}")
        
        print("="*120)
        
        # Export to Excel
        self._export_to_excel(results)
        
        # Export to CSV
        self._export_to_csv(results)
        
        # Generate HTML index
        self._generate_html_index(results)
    
    def _export_to_excel(self, results: List[CoverageResult]):
        """Export results to Excel"""
        # Sort by LLM and problem number
        def get_problem_num(problem_id):
            try:
                return int(problem_id.split('/')[-1])
            except:
                return 999
        
        sorted_results = sorted(results, key=lambda x: (x.llm_implementation, get_problem_num(x.problem_id)))
        
        data = []
        for result in sorted_results:
            data.append({
                'Problem': result.problem_id,
                'LLM': result.llm_implementation,
                'Tests_Passed': result.tests_passed,
                'Tests_Failed': result.tests_failed,
                'Total_Tests': result.total_tests,
                'Line_Coverage_%': round(result.line_coverage, 1),
                'Branch_Coverage_%': round(result.branch_coverage, 1) if result.branch_coverage else "N/A",
                'Interpretation': result.interpretation,
                'Errors': '; '.join(result.error_details[:2]) if result.error_details else ""
            })
        
        df = pd.DataFrame(data)
        
        output_file = "pytest_cov_coverage_report.xlsx"
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Coverage_Results', index=False)
            
            # Adjust column widths
            worksheet = writer.sheets['Coverage_Results']
            worksheet.column_dimensions['A'].width = 15
            worksheet.column_dimensions['B'].width = 25
            worksheet.column_dimensions['C'].width = 12
            worksheet.column_dimensions['D'].width = 12
            worksheet.column_dimensions['E'].width = 12
            worksheet.column_dimensions['F'].width = 15
            worksheet.column_dimensions['G'].width = 15
            worksheet.column_dimensions['H'].width = 50
            worksheet.column_dimensions['I'].width = 50
        
        print(f"\nExcel report exported to: {output_file}")
    
    def _export_to_csv(self, results: List[CoverageResult]):
        """Export results to CSV"""
        import csv
        
        # Sort by LLM and problem number
        def get_problem_num(problem_id):
            try:
                return int(problem_id.split('/')[-1])
            except:
                return 999
        
        sorted_results = sorted(results, key=lambda x: (x.llm_implementation, get_problem_num(x.problem_id)))
        
        output_file = "pytest_cov_coverage_report.csv"
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Problem', 'LLM', 'Tests_Passed', 'Tests_Failed', 'Total_Tests',
                           'Line_Coverage_%', 'Branch_Coverage_%', 'Interpretation'])
            
            for result in sorted_results:
                branch_str = f"{result.branch_coverage:.1f}" if result.branch_coverage else "N/A"
                writer.writerow([
                    result.problem_id,
                    result.llm_implementation,
                    result.tests_passed,
                    result.tests_failed,
                    result.total_tests,
                    f"{result.line_coverage:.1f}",
                    branch_str,
                    result.interpretation
                ])
        
        print(f"CSV report exported to: {output_file}")
    
    def _generate_html_index(self, results: List[CoverageResult]):
        """Generate an HTML index page for easy navigation of coverage reports"""
        # Sort by LLM and problem number
        def get_problem_num(problem_id):
            try:
                return int(problem_id.split('/')[-1])
            except:
                return 999
        
        sorted_results = sorted(results, key=lambda x: (x.llm_implementation, get_problem_num(x.problem_id)))
        
        # Group by LLM implementation
        llm_groups = {}
        for result in sorted_results:
            if result.llm_implementation not in llm_groups:
                llm_groups[result.llm_implementation] = []
            llm_groups[result.llm_implementation].append(result)
        
        # Generate HTML
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Coverage Reports Index</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }
        h2 {
            color: #555;
            margin-top: 30px;
            background-color: #e8e8e8;
            padding: 10px;
            border-left: 4px solid #4CAF50;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        th {
            background-color: #4CAF50;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }
        td {
            padding: 10px 12px;
            border-bottom: 1px solid #ddd;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        a {
            color: #2196F3;
            text-decoration: none;
            font-weight: 500;
        }
        a:hover {
            text-decoration: underline;
        }
        .coverage-high {
            color: #4CAF50;
            font-weight: bold;
        }
        .coverage-medium {
            color: #FF9800;
            font-weight: bold;
        }
        .coverage-low {
            color: #f44336;
            font-weight: bold;
        }
        .status-pass {
            color: #4CAF50;
            font-weight: bold;
        }
        .status-fail {
            color: #f44336;
            font-weight: bold;
        }
        .summary {
            background-color: white;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .summary-item {
            display: inline-block;
            margin-right: 30px;
            font-size: 16px;
        }
        .summary-label {
            font-weight: bold;
            color: #555;
        }
    </style>
</head>
<body>
    <h1>📊 Coverage Reports Index</h1>
    <div class="summary">
        <div class="summary-item">
            <span class="summary-label">Total Solutions:</span> """ + str(len(results)) + """
        </div>
        <div class="summary-item">
            <span class="summary-label">LLM Implementations:</span> """ + str(len(llm_groups)) + """
        </div>
        <div class="summary-item">
            <span class="summary-label">Generated:</span> """ + str(pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')) + """
        </div>
    </div>
"""
        
        # Generate table for each LLM implementation
        for llm_impl, llm_results in llm_groups.items():
            html_content += f"\n    <h2>{llm_impl}</h2>\n"
            html_content += """    <table>
        <thead>
            <tr>
                <th>Problem</th>
                <th>Tests</th>
                <th>Line Coverage</th>
                <th>Branch Coverage</th>
                <th>Interpretation</th>
                <th>HTML Report</th>
            </tr>
        </thead>
        <tbody>
"""
            
            for result in llm_results:
                problem_num = result.problem_id.split('/')[-1]
                report_path = f"{llm_impl}/HumanEval_{problem_num}/index.html"
                
                # Determine coverage class
                line_class = "coverage-high" if result.line_coverage >= 80 else \
                            "coverage-medium" if result.line_coverage >= 50 else "coverage-low"
                
                branch_class = ""
                branch_display = "N/A"
                if result.branch_coverage is not None:
                    branch_display = f"{result.branch_coverage:.1f}%"
                    branch_class = "coverage-high" if result.branch_coverage >= 80 else \
                                  "coverage-medium" if result.branch_coverage >= 50 else "coverage-low"
                
                # Test status
                test_status = "status-pass" if result.tests_failed == 0 else "status-fail"
                test_display = f"{result.tests_passed}/{result.total_tests}"
                
                html_content += f"""            <tr>
                <td>{result.problem_id}</td>
                <td class="{test_status}">{test_display}</td>
                <td class="{line_class}">{result.line_coverage:.1f}%</td>
                <td class="{branch_class}">{branch_display}</td>
                <td>{result.interpretation}</td>
                <td><a href="{report_path}" target="_blank">View Report →</a></td>
            </tr>
"""
            
            html_content += """        </tbody>
    </table>
"""
        
        html_content += """</body>
</html>"""
        
        # Write index file
        index_path = os.path.join(self.html_output_dir, "index.html")
        with open(index_path, 'w') as f:
            f.write(html_content)
        
        print(f"\nHTML coverage reports saved to: {self.html_output_dir}/")
        print(f"Open {index_path} in your browser to view all reports")


def main():
    """Main execution"""
    print("="*80)
    print("Enhanced Pytest-Cov Coverage Analyzer")
    print("Using smart function handling + pytest-cov for accurate coverage")
    print("="*80)
    
    # Check if custom base path provided
    import sys
    base_path = sys.argv[1] if len(sys.argv) > 1 else "codes"
    
    analyzer = PytestCovAnalyzer()
    results = analyzer.analyze_all_solutions(base_path=base_path)
    analyzer.generate_reports(results)
    
    # Overall statistics
    total_tests = sum(r.total_tests for r in results)
    total_passed = sum(r.tests_passed for r in results)
    avg_line_cov = sum(r.line_coverage for r in results) / len(results) if results else 0
    
    branch_covs = [r.branch_coverage for r in results if r.branch_coverage is not None]
    avg_branch_cov = sum(branch_covs) / len(branch_covs) if branch_covs else 0
    
    print("\n" + "="*80)
    print("OVERALL STATISTICS")
    print("="*80)
    print(f"Total Solutions Analyzed: {len(results)}")
    print(f"Total Test Cases: {total_tests}")
    print(f"Total Tests Passed: {total_passed} ({total_passed/total_tests*100:.1f}%)")
    print(f"Average Line Coverage: {avg_line_cov:.1f}%")
    if branch_covs:
        print(f"Average Branch Coverage: {avg_branch_cov:.1f}%")
    print("="*80)


if __name__ == "__main__":
    main()
