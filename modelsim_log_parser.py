from pathlib import Path
import argparse
import re

parser = argparse.ArgumentParser(
    description="Parse ModelSim simulation logs."
)

parser.add_argument(
    "logfile",
    type=Path,
    help="Path to the ModelSim log file"
)

args = parser.parse_args()

# Check if the file exists
if not args.logfile.exists():
    print(f"Error: '{args.logfile}' does not exist.")
    exit()

# Open and read the file
with open(args.logfile, "r") as file:
    lines = file.readlines()

print("Contents of the log file:\n")

passed = 0
failed = 0
failed_tests = []

pass_pattern = re.compile(r"PASS\s+(.*)")
fail_pattern = re.compile(r"FAIL\s+(.*)")

for line in lines:
    line = line.strip()

    if pass_pattern.search(line):
        passed += 1

    fail_match = fail_pattern.search(line)

    if fail_match:
        failed += 1
        failed_tests.append(fail_match.group(1))

# Report

total = passed + failed

print("        ModelSim Verification Report")

print(f"Passed Tests : {passed}")
print(f"Failed Tests : {failed}")
print(f"Total Tests  : {total}")

if total > 0:
    print(f"Success Rate : {(passed / total) * 100:.2f}%")

print()

if failed_tests:
    print("Failed Tests")

    for test in failed_tests:
        print(f"• {test}")

else:
    print("All tests passed!")