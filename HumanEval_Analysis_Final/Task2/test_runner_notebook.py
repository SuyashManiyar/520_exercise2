"""
Test Runner for Jupyter Notebooks
Simple copy-paste into notebook cells
"""

import importlib.util
from typing import List, Dict


def run_tests(code_file: str, test_cases: List[str]) -> Dict:
    """
    Run test cases and return results.
    
    Usage in notebook:
        from test_runner_notebook import run_tests
        
        result = run_tests(
            code_file="path/to/code.py",
            test_cases=[
                "assert candidate('input') == 'output'",
                "assert candidate('test') == 'result'"
            ]
        )
        
        print(f"Passed: {result['pass_rate']:.1f}%")
    """
    # Load module
    spec = importlib.util.spec_from_file_location("test_module", code_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Get candidate function
    candidate = getattr(module, 'candidate', None)
    if not candidate:
        for name in dir(module):
            obj = getattr(module, name)
            if not name.startswith('_') and callable(obj):
                candidate = obj
                break
    
    # Run tests
    passed = []
    failed = []
    
    for i, test_case in enumerate(test_cases):
        try:
            test_code = test_case.strip()
            if not test_code.startswith('assert'):
                test_code = f"assert {test_code}"
            
            exec(test_code, {'candidate': candidate})
            passed.append(i)
            
        except Exception as e:
            failed.append((i, str(e)))
    
    pass_rate = (len(passed) / len(test_cases)) * 100 if test_cases else 0
    
    return {
        'passed': passed,
        'failed': failed,
        'total': len(test_cases),
        'pass_rate': pass_rate,
        'passed_count': len(passed),
        'failed_count': len(failed),
        'failed_tests': [(i, test_cases[i], error) for i, error in failed]
    }


def print_results(result: Dict):
    """Print test results in a clean format."""
    print(f"\n{'='*60}")
    print(f"TEST RESULTS")
    print(f"{'='*60}")
    print(f"Total: {result['total']}")
    print(f"Passed: {result['passed_count']} ({result['pass_rate']:.1f}%)")
    print(f"Failed: {result['failed_count']} ({100-result['pass_rate']:.1f}%)")
    print(f"{'='*60}\n")
    
    if result['failed_tests']:
        print("FAILED TESTS:")
        for idx, test, error in result['failed_tests']:
            print(f"\nTest {idx+1}:")
            print(f"  {test[:70]}...")
            print(f"  Error: {error[:100]}")


# Quick usage example
if __name__ == "__main__":
    # Example
    result = run_tests(
        code_file="Task2/APPS_codes/final.py",
        test_cases=[
            "assert candidate('3 1 100 100\\n1 3 8') == '12'",
            "assert candidate('3 100 1 100\\n1 3 8') == '9'"
        ]
    )
    print_results(result)
