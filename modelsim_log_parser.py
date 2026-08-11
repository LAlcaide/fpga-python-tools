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

for line in lines:
    print(line.strip())