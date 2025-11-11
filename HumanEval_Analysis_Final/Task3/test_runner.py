#!/usr/bin/env python3
"""
Test Runner - Shows exact test cases that failed with expected vs actual output
"""

import importlib.util
import sys
from typing import List, Dict


def run_tests_and_report(code_file: str, test_cases: List[str]) -> Dict:
    """
    Run test cases and report which ones pass/fail with actual vs expected values.
    
    Args:
        code_file: Path to Python file with the function
        test_cases: List of test assertions like ["assert candidate(...) == ...", ...]
        
    Returns:
        Dictionary with:
        - passed: List of passed test indices
        - failed: List of failed test indices with error messages
        - total: Total number of tests
        - pass_rate: Percentage of tests passed
    """
    print(f"\n{'='*80}")
    print(f"Running Tests")
    print(f"{'='*80}\n")
    print(f"Code file: {code_file}")
    print(f"Total tests: {len(test_cases)}\n")
    
    # Load the module
    try:
        spec = importlib.util.spec_from_file_location("test_module", code_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Get the candidate function
        if hasattr(module, 'candidate'):
            candidate = module.candidate
        else:
            # Find first non-private function
            candidate = None
            for name in dir(module):
                obj = getattr(module, name)
                if not name.startswith('_') and callable(obj):
                    candidate = obj
                    break
            
            if candidate is None:
                raise ValueError("No function found in module")
        
        print(f"Testing function: {candidate.__name__}\n")
        
    except Exception as e:
        print(f"✗ Error loading module: {e}")
        return {
            'passed': [],
            'failed': [(i, str(e)) for i in range(len(test_cases))],
            'total': len(test_cases),
            'pass_rate': 0.0
        }
    
    # Run tests
    passed = []
    failed = []
    
    for i, test_case in enumerate(test_cases):
        test_num = i + 1
        
        try:
            # Clean up test case
            test_code = test_case.strip()
            if not test_code.startswith('assert'):
                test_code = f"assert {test_code}"
            
            # Execute test
            exec(test_code, {'candidate': candidate})
            
            # Test passed - show expected output
            try:
                import re
                match = re.search(r"candidate\((.*?)\)\s*==\s*(.+)", test_code)
                if match:
                    expected = match.group(2).strip()
                    passed.append(i)
                    print(f"✓ Test {test_num:3d}: PASSED - Expected: {expected}")
                else:
                    passed.append(i)
                    print(f"✓ Test {test_num:3d}: PASSED")
            except:
                passed.append(i)
                print(f"✓ Test {test_num:3d}: PASSED")
            
        except AssertionError as e:
            # Test failed - get actual vs expected
            try:
                import re
                match = re.search(r"candidate\((.*?)\)\s*==\s*(.+)", test_code)
                if match:
                    input_val = match.group(1)
                    expected = match.group(2).strip()
                    # Get actual output
                    actual = candidate(eval(input_val))
                    failed.append((i, f"Expected: {expected}, Got: {repr(actual)}"))
                    print(f"✗ Test {test_num:3d}: FAILED - Expected {expected}, Got {repr(actual)}")
                else:
                    failed.append((i, f"Assertion failed"))
                    print(f"✗ Test {test_num:3d}: FAILED - Assertion error")
            except Exception as ex:
                failed.append((i, f"Assertion failed: {str(ex)}"))
                print(f"✗ Test {test_num:3d}: FAILED - {str(ex)}")
            
        except Exception as e:
            # Test failed - other error
            failed.append((i, f"Error: {type(e).__name__}: {str(e)}"))
            print(f"✗ Test {test_num:3d}: FAILED - {type(e).__name__}: {str(e)}")
    
    # Summary
    pass_rate = (len(passed) / len(test_cases)) * 100 if test_cases else 0
    
    print(f"\n{'='*80}")
    print("TEST SUMMARY")
    print(f"{'='*80}")
    print(f"Total Tests: {len(test_cases)}")
    print(f"Passed: {len(passed)} ({pass_rate:.1f}%)")
    print(f"Failed: {len(failed)} ({100-pass_rate:.1f}%)")
    print(f"{'='*80}\n")
    
    if failed:
        print("FAILED TESTS:")
        print("-" * 80)
        for idx, error in failed:
            print(f"\nTest {idx+1}:")
            print(f"  {test_cases[idx]}")
            print(f"  {error}")
    
    return {
        'passed': passed,
        'failed': failed,
        'total': len(test_cases),
        'pass_rate': pass_rate,
        'passed_tests': [test_cases[i] for i in passed],
        'failed_tests': [(test_cases[i], error) for i, error in failed]
    }


def print_detailed_report(result: Dict):
    """Print a detailed report of test results."""
    print(f"\n{'='*80}")
    print("DETAILED REPORT")
    print(f"{'='*80}\n")
    
    if result['passed']:
        print(f"✓ PASSED TESTS ({len(result['passed'])}):")
        print("-" * 80)
        for test in result['passed_tests']:
            print(f"  {test}")
        print()
    
    if result['failed']:
        print(f"✗ FAILED TESTS ({len(result['failed'])}):")
        print("-" * 80)
        for test, error in result['failed_tests']:
            print(f"  Test: {test}")
            print(f"  {error}")
            print()


# Example usage
if __name__ == "__main__":
    # Edit these values
    code_file = "/Users/suyashmaniyar/Desktop/UMass/Courses/SoftwareEngineering/Assignment_02/HumanEval_Analysis_Final/Task3/Buggy_code_files/HumanEval_114.py"
    
    test_cases =    [
        "assert candidate([2, 3, 4, 1, 2, 4]) == 1",
        "assert candidate([-1, -2, -3]) == -6",
        "assert candidate([-1, -2, -3, 2, -10]) == -14",
        "assert candidate([0, 10, 20, 1000000]) == 0",
        "assert candidate([-1, -2, -3, 10, -5]) == -6",
        "assert candidate([100, -1, -2, -3, 10, -5]) == -6",
        "assert candidate([10, 11, 13, 8, 3, 4]) == 3",
        "assert candidate([100, -33, 32, -1, 0, -2]) == -33",
        "assert candidate([1, -1]) == -1"
    ]
    result = run_tests_and_report(code_file, test_cases)
    print_detailed_report(result)
