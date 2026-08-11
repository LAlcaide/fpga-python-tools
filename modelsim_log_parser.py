from pathlib import Path
import argparse
import csv
import json
import re
from datetime import datetime


REPORT_DIR = Path("verification/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def parse_log(filepath):
    passed = 0
    failed = 0
    failed_tests = []

    pass_pattern = re.compile(r"PASS\s+(.*)", re.IGNORECASE)
    fail_pattern = re.compile(r"FAIL\s+(.*)", re.IGNORECASE)

    with open(filepath, "r") as file:
        for line in file:
            line = line.strip()

            if pass_pattern.search(line):
                passed += 1

            fail_match = fail_pattern.search(line)

            if fail_match:
                failed += 1
                failed_tests.append(fail_match.group(1))

    total = passed + failed

    success_rate = 0.0

    if total:
        success_rate = round((passed / total) * 100, 2)

    return {
        "passed": passed,
        "failed": failed,
        "total": total,
        "success_rate": success_rate,
        "failed_tests": failed_tests
    }


def export_json(all_results, overall):
    report = {
        "modules": all_results,
        "overall": overall
    }

    with open(
        REPORT_DIR / "verification_report.json",
        "w"
    ) as outfile:
        json.dump(report, outfile, indent=4)


def export_csv(all_results, overall):
    with open(
        REPORT_DIR / "verification_report.csv",
        "w",
        newline=""
    ) as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow([
            "Module",
            "Passed",
            "Failed",
            "Total",
            "Success Rate"
        ])

        for module, results in all_results.items():
            writer.writerow([
                module,
                results["passed"],
                results["failed"],
                results["total"],
                f"{results['success_rate']}%"
            ])

        writer.writerow([])

        writer.writerow([
            "OVERALL",
            overall["passed"],
            overall["failed"],
            overall["total"],
            f"{overall['success_rate']}%"
        ])


def export_html(all_results, overall):
    html = f"""
<!DOCTYPE html>
<html>

<head>

<title>ModelSim Verification Report</title>

<style>

body {{
    font-family: Arial, sans-serif;
    margin: 40px;
}}

h1, h2 {{
    color: #222;
}}

table {{
    border-collapse: collapse;
    width: 100%;
}}

th, td {{
    border: 1px solid #ccc;
    padding: 8px;
    text-align: left;
}}

th {{
    background-color: #f2f2f2;
}}

.pass {{
    color: green;
}}

.fail {{
    color: red;
}}

.overall {{
    font-weight: bold;
}}

</style>

</head>

<body>

<h1>ModelSim Verification Report</h1>

<p>
<b>Generated:</b> {datetime.now()}
</p>

<h2>Module Results</h2>

<table>

<tr>
<th>Module</th>
<th>Passed</th>
<th>Failed</th>
<th>Total</th>
<th>Success Rate</th>
</tr>
"""

    for module, results in all_results.items():

        html += f"""
<tr>

<td>{module}</td>

<td class="pass">
{results['passed']}
</td>

<td class="fail">
{results['failed']}
</td>

<td>
{results['total']}
</td>

<td>
{results['success_rate']}%
</td>

</tr>
"""

    html += f"""
<tr class="overall">

<td>
OVERALL
</td>

<td>
{overall['passed']}
</td>

<td>
{overall['failed']}
</td>

<td>
{overall['total']}
</td>

<td>
{overall['success_rate']}%
</td>

</tr>

</table>

<h2>Failed Tests</h2>

<ul>
"""

    any_failures = False

    for module, results in all_results.items():

        for test in results["failed_tests"]:

            any_failures = True

            html += (
                f"<li><b>{module}</b>: {test}</li>\n"
            )

    if not any_failures:
        html += "<li>All tests passed!</li>"

    html += """
</ul>

</body>

</html>
"""

    with open(
        REPORT_DIR / "verification_report.html",
        "w"
    ) as outfile:

        outfile.write(html)


def print_report(all_results, overall):

    print("=" * 60)
    print("             ModelSim Verification Report")
    print("=" * 60)

    for module, results in all_results.items():

        print()
        print(module)
        print("-" * 60)

        print(
            f"Passed Tests : {results['passed']}"
        )

        print(
            f"Failed Tests : {results['failed']}"
        )

        print(
            f"Total Tests  : {results['total']}"
        )

        print(
            f"Success Rate : "
            f"{results['success_rate']:.2f}%"
        )

        if results["failed_tests"]:

            print("Failed Tests:")

            for test in results["failed_tests"]:
                print(f"  • {test}")

    print()

    print("=" * 60)
    print("OVERALL RESULTS")
    print("=" * 60)

    print(
        f"Passed Tests : {overall['passed']}"
    )

    print(
        f"Failed Tests : {overall['failed']}"
    )

    print(
        f"Total Tests  : {overall['total']}"
    )

    print(
        f"Success Rate : "
        f"{overall['success_rate']:.2f}%"
    )

    print("=" * 60)


def main():

    parser = argparse.ArgumentParser(
        description="ModelSim Verification Log Parser"
    )

    parser.add_argument(
        "logfiles",
        type=Path,
        nargs="+",
        help="Paths to ModelSim logs"
    )

    args = parser.parse_args()

    all_results = {}

    total_passed = 0
    total_failed = 0

    for logfile in args.logfiles:

        if not logfile.exists():

            print(
                f"Error: {logfile} does not exist."
            )

            return

        results = parse_log(logfile)

        module_name = logfile.stem

        all_results[module_name] = results

        total_passed += results["passed"]
        total_failed += results["failed"]

    total = total_passed + total_failed

    success_rate = 0.0

    if total:
        success_rate = round(
            (total_passed / total) * 100,
            2
        )

    overall = {
        "passed": total_passed,
        "failed": total_failed,
        "total": total,
        "success_rate": success_rate
    }

    print_report(
        all_results,
        overall
    )

    export_json(
        all_results,
        overall
    )

    export_csv(
        all_results,
        overall
    )

    export_html(
        all_results,
        overall
    )

    print()
    print("Reports generated:")
    print(
        "✓ verification/reports/"
        "verification_report.json"
    )
    print(
        "✓ verification/reports/"
        "verification_report.csv"
    )
    print(
        "✓ verification/reports/"
        "verification_report.html"
    )


if __name__ == "__main__":
    main()