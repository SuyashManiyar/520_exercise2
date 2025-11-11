
# 520_exercise2

## Project Overview

This project analyzes HumanEval code implementations with coverage analysis and testing workflows.

## Project Structure

```
.
├── codes/                          # Source code implementations
│   ├── gemma_self_edit/
│   ├── gemma_Self_Planning/
│   ├── llama_self_edit/
│   └── llama_self_planning/
├── coverage_html_reports/          # Generated coverage reports
├── Task2/                          # Test case generation and execution
└── Task3/                          # Buggy code analysis and reports
```

## Workflow

### Step 1: Generate Coverage Reports

First, run the enhanced analysis on the code implementations to generate coverage reports:

```bash
python run_enhanced_analysis.py
```

This will analyze the code in the `codes/` directory and generate HTML coverage reports in `coverage_html_reports/`.

### Step 2: Task 2 - Test Case Generation

Navigate to the `Task2/` folder for test case generation and execution workflows.

### Step 3: Task 3 - Buggy Code Analysis

Navigate to the `Task3/` folder for buggy code analysis and reporting.

## Files

- `code_enhancer.py` - Code enhancement utilities
- `pytest_cov_enhanced_analyzer.py` - Enhanced coverage analyzer
- `run_enhanced_analysis.py` - Main analysis script
- `selected_problems_testcases.json` - Test case definitions
- `pytest_cov_coverage_report.csv` - Coverage report (CSV format)
- `pytest_cov_coverage_report.xlsx` - Coverage report (Excel format)
