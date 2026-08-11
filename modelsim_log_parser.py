from pathlib import Path
import argparse


parser = argparse.ArgumentParser(
    description="Parse ModelSim simulation logs."
)

parser.add_argument(
    "logfile",
    type=Path,
    help="Path to ModelSim log file"
)

args = parser.parse_args()

print(args.logfile)