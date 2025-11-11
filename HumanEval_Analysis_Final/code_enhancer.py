#!/usr/bin/env python3
"""
Code Enhancer - Applies smart function handling corrections to all solution files
Creates enhanced versions with proper function names and aliases
"""

import os
import ast
import shutil
from pathlib import Path
from typing import Dict, List, Tuple


class CodeEnhancer:
    """Enhances code files with smart function handling"""

    def __init__(self, source_dir: str = "codes", target_dir: str = "codes_enhanced"):
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.enhancements_made = []

    def get_function_info(self, file_path: str, problem_id: str) -> Tuple[str, List[str]]:
        """Extract function name and identify needed aliases"""
        try:
            with open(file_path, "r") as f:
                content = f.read()

            # Parse AST to find function names
            tree = ast.parse(content)
            function_names = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if not node.name.startswith("_"):
                        function_names.append(node.name)

            if not function_names:
                return None, []

            # Primary function is the first non-helper function
            primary_func = function_names[0]

            # Determine needed aliases
            aliases = []

            # Always add 'candidate' alias if not already the function name
            if primary_func != "candidate":
                aliases.append("candidate")

            # Special case for HumanEval/94
            if problem_id == "HumanEval/94" and primary_func != "skjkasdkd":
                aliases.append("skjkasdkd")

            return primary_func, aliases

        except Exception as e:
            print(f"    Warning: Could not parse {file_path}: {e}")
            return None, []

    def enhance_file(
        self, source_path: str, target_path: str, problem_id: str
    ) -> bool:
        """Enhance a single file with function aliases"""
        try:
            with open(source_path, "r") as f:
                content = f.read()

            # Get function info
            primary_func, aliases = self.get_function_info(source_path, problem_id)

            if not primary_func or not aliases:
                # No enhancement needed, just copy
                shutil.copy2(source_path, target_path)
                return False

            # Check if aliases already exist
            existing_aliases = [alias for alias in aliases if alias in content]
            needed_aliases = [alias for alias in aliases if alias not in content]

            if not needed_aliases:
                # Aliases already exist, just copy
                shutil.copy2(source_path, target_path)
                return False

            # Add aliases at the end of the file
            enhanced_content = content.rstrip() + "\n\n"
            enhanced_content += "# Auto-generated aliases for test compatibility\n"

            for alias in needed_aliases:
                enhanced_content += f"{alias} = {primary_func}\n"

            # Write enhanced file
            with open(target_path, "w") as f:
                f.write(enhanced_content)

            return True

        except Exception as e:
            print(f"    Error enhancing {source_path}: {e}")
            # Copy original on error
            shutil.copy2(source_path, target_path)
            return False

    def enhance_all_codes(self):
        """Enhance all code files in the source directory"""
        print("=" * 80)
        print("Code Enhancement Process")
        print("=" * 80)
        print(f"Source: {self.source_dir}")
        print(f"Target: {self.target_dir}")
        print()

        # Clean and create target directory
        if os.path.exists(self.target_dir):
            shutil.rmtree(self.target_dir)
        os.makedirs(self.target_dir)

        llm_implementations = [
            "gemma_Self_Planning",
            "gemma_self_edit",
            "llama_self_edit",
            "llama_self_planning",
        ]

        total_files = 0
        enhanced_files = 0

        for llm_impl in llm_implementations:
            source_impl_dir = os.path.join(self.source_dir, llm_impl)
            target_impl_dir = os.path.join(self.target_dir, llm_impl)

            if not os.path.exists(source_impl_dir):
                continue

            # Create target implementation directory
            os.makedirs(target_impl_dir, exist_ok=True)

            print(f"\n{llm_impl}:")

            # Process all Python files
            for filename in sorted(os.listdir(source_impl_dir)):
                if not filename.endswith(".py"):
                    continue

                source_file = os.path.join(source_impl_dir, filename)
                target_file = os.path.join(target_impl_dir, filename)

                # Extract problem ID from filename
                problem_num = filename.replace("HumanEval_", "").replace(".py", "")
                problem_id = f"HumanEval/{problem_num}"

                total_files += 1

                # Enhance the file
                was_enhanced = self.enhance_file(source_file, target_file, problem_id)

                if was_enhanced:
                    enhanced_files += 1
                    print(f"  ✓ {filename} - Enhanced with function aliases")
                    self.enhancements_made.append(
                        {"llm": llm_impl, "file": filename, "problem": problem_id}
                    )
                else:
                    print(f"  → {filename} - Copied (no enhancement needed)")

        print("\n" + "=" * 80)
        print("Enhancement Summary")
        print("=" * 80)
        print(f"Total files processed: {total_files}")
        print(f"Files enhanced: {enhanced_files}")
        print(f"Files copied as-is: {total_files - enhanced_files}")
        print(f"\nEnhanced code saved to: {self.target_dir}/")
        print("=" * 80)

        return self.enhancements_made


def main():
    """Main execution"""
    enhancer = CodeEnhancer()
    enhancer.enhance_all_codes()


if __name__ == "__main__":
    main()
