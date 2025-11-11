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

#### 📊 View Coverage Reports

After running the analysis, open the interactive coverage dashboard:

```bash
open coverage_html_reports/index.html
```

The dashboard provides:
- **40 Total Solutions** across 4 LLM implementations
- **Interactive Tables** with test results, line coverage, and branch coverage
- **Color-coded Metrics** for quick assessment
- **Direct Links** to detailed coverage reports for each problem

**Coverage Summary by Implementation:**

| Implementation | Problems | Avg Line Coverage | Avg Branch Coverage |
|----------------|----------|-------------------|---------------------|
| gemma_Self_Planning | 10 | 97.1% | 94.3% |
| gemma_self_edit | 10 | 89.2% | 95.1% |
| llama_self_edit | 10 | 88.4% | 90.6% |
| llama_self_planning | 10 | 87.7% | 90.3% |

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
