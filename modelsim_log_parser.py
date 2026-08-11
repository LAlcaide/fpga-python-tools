from pathlib import Path
import argparse

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

for line in lines:
    line = line.strip()

    if "PASS" in line:
        passed += 1

    elif "FAIL" in line:
        failed += 1

print("ModelSim Log Summary")

print(f"Passed Tests : {passed}")
print(f"Failed Tests : {failed}")
print(f"Total Tests  : {passed + failed}")

if passed + failed > 0:
    success_rate = passed / (passed + failed) * 100
    print(f"Success Rate : {success_rate:.2f}%")