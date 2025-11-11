#!/usr/bin/env python3
"""
Enhanced Analysis Pipeline
1. Enhances code files with smart function handling
2. Runs pytest-cov analysis on enhanced code
3. Generates comprehensive reports
"""

import sys
from code_enhancer import CodeEnhancer
from pytest_cov_enhanced_analyzer import PytestCovAnalyzer


def main():
    print("\n" + "=" * 80)
    print("ENHANCED CODE ANALYSIS PIPELINE")
    print("=" * 80)
    print()

    # Step 1: Enhance code files
    print("STEP 1: Enhancing code files with smart function handling")
    print("-" * 80)
    enhancer = CodeEnhancer(source_dir="codes", target_dir="codes_enhanced")
    enhancements = enhancer.enhance_all_codes()

    print("\n" + "=" * 80)
    print()

    # Step 2: Run analysis on enhanced code
    print("STEP 2: Running pytest-cov analysis on enhanced code")
    print("-" * 80)
    analyzer = PytestCovAnalyzer(
        test_cases_file="selected_problems_testcases.json",
        html_output_dir="coverage_html_reports_enhanced",
    )

    # Run analysis on enhanced code
    results = analyzer.analyze_all_solutions(base_path="codes_enhanced")
    analyzer.generate_reports(results)

    print("\n" + "=" * 80)
    print("PIPELINE COMPLETE")
    print("=" * 80)
    print(f"Enhanced code: codes_enhanced/")
    print(f"HTML reports: coverage_html_reports_enhanced/")
    print(f"Excel report: pytest_cov_coverage_report.xlsx")
    print(f"CSV report: pytest_cov_coverage_report.csv")
    print("=" * 80)


if __name__ == "__main__":
    main()
