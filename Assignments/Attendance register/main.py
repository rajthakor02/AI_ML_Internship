import csv
import os
from datetime import datetime
from collections import defaultdict

input_file = "Attendance.csv"
output_file = "attendance_summary.csv"
report_file = "attendance_report.txt"

sample_data = [
    ["employee_id", "date", "status"],

    ["E101", "2026-10-01", "Present"],
    ["E101", "2026-10-02", "Present"],
    ["E101", "2026-10-03", "Absent"],
    ["E101", "2026-10-04", "Leave"],
    ["E101", "2026-10-05", "Present"],

    ["E102", "2026-10-01", "Present"],
    ["E102", "2026-10-02", "Absent"],
    ["E102", "2026-10-03", "Present"],
    ["E102", "2026-10-04", "Present"],
    ["E102", "2026-10-05", "Present"],

    ["E103", "2026-10-01", "Absent"],
    ["E103", "2026-10-02", "Present"],
    ["E103", "2026-10-03", "Leave"],
    ["E103", "2026-10-04", "Present"],
    ["E103", "2026-10-05", "Present"],

    ["E104", "2026-10-01", "Present"],
    ["E104", "2026-10-02", "Present"],
    ["E104", "2026-10-03", "Present"],
    ["E104", "2026-10-04", "Absent"],
    ["E104", "2026-10-05", "Present"],

    ["E105", "2026-10-01", "Leave"],
    ["E105", "2026-10-02", "Present"],
    ["E105", "2026-10-03", "Present"],
    ["E105", "2026-10-04", "Present"],
    ["E105", "2026-10-05", "Absent"]
]

if not os.path.exists(input_file):
    with open(input_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(sample_data)

    print("attendance.csv created successfully!")
else:
    print("attendance.csv already exists!")

month = input("Enter month (yyyy-mm): ").strip()

try:
    datetime.strptime(month, "%Y-%m")
except ValueError:
    print("Invalid month entered! please enter yyyy-mm")
    raise SystemExit

summary = defaultdict(lambda: {
    "Present": 0,
    "Absent": 0,
    "Leave": 0
})

seen_record = set()
duplicate_rows = []
error_rows = []
rejected_rows = 0

try: 
    with open(input_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        required_columns = {"employee_id", "date", "status"}

        if not reader.fieldnames or not required_columns.issubset(
            set(reader.fieldnames)
        ):
            print("csv must contain employee id, date and status.")
            raise SystemExit

        for row_number, row in enumerate(reader, start= 2):

            employee_id = (row.get("employee_id")or "").strip()
            date_text = (row.get("date")or "").strip()
            status = (row.get("status")or "").strip()

            if not employee_id:
                message = f"row {row_number}: missing employee ID!"
                error_rows.append(message)
                rejected_rows += 1
                continue

            try:
                attendance_date = datetime.strptime(
                    date_text, "%Y-%m-%d"
                )
            except ValueError:
                message = f"row {row_number}: invalid date '{date_text}'."
                error_rows.append(message)
                rejected_rows += 1
                continue

            if attendance_date.strftime("%Y-%m") != month:
                continue

            if status not in ["Present","Absent", "Leave"]:
                message = f"row {row_number}: invalid status '{status}'"
                error_rows.append(message)
                rejected_rows += 1
                continue

            record_key = (employee_id, date_text)

            if record_key in seen_record:
                message = (
                    f"row {row_number}: duplicate record for "
                    f"{employee_id} on {date_text}."
                )
                duplicate_rows.append(message)
                rejected_rows += 1
                continue

            seen_record.add(record_key)

            summary[employee_id][status] += 1

except FileNotFoundError:
    print("file not found.")
    raise SystemExit

with open(output_file, "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Employee ID",
        "Present",
        "Absent",
        "Leave",
        "Total Days",
        "Attendance Percentage"
    ])

    for employee_id, counts in sorted(summary.items()):

        present = counts["Present"]
        absent = counts["Absent"]
        leave = counts["Leave"]

        total_days = present + absent + leave

        if total_days > 0:
            percentage = (present / total_days) * 100
        else:
            percentage = 0

        writer.writerow([
            employee_id,
            present,
            absent,
            leave,
            total_days,
            round(percentage, 2)
        ])


# --------------------------------
# STEP 6: CREATE TEXT REPORT
# --------------------------------

with open(report_file, "w", encoding="utf-8") as file:

    file.write("MONTHLY ATTENDANCE REPORT\n")
    file.write("=" * 40 + "\n")
    file.write(f"Selected Month: {month}\n\n")

    for employee_id, counts in sorted(summary.items()):

        present = counts["Present"]
        absent = counts["Absent"]
        leave = counts["Leave"]

        total_days = present + absent + leave

        if total_days > 0:
            percentage = (present / total_days) * 100
        else:
            percentage = 0

        file.write(f"Employee ID: {employee_id}\n")
        file.write(f"Present: {present}\n")
        file.write(f"Absent: {absent}\n")
        file.write(f"Leave: {leave}\n")
        file.write(f"Total Days: {total_days}\n")
        file.write(f"Attendance: {percentage:.2f}%\n")
        file.write("-" * 30 + "\n")

    file.write("\nATTENDANCE FORMULA\n")
    file.write("Present / (Present + Absent + Leave) * 100\n")

    file.write(f"\nRejected Rows: {rejected_rows}\n")

    file.write("\nVALIDATION ERRORS\n")
    if error_rows:
        for error in error_rows:
            file.write(error + "\n")
    else:
        file.write("No validation errors.\n")

    file.write("\nDUPLICATE RECORDS\n")
    if duplicate_rows:
        for duplicate in duplicate_rows:
            file.write(duplicate + "\n")
    else:
        file.write("No duplicate records.\n")


# --------------------------------
# STEP 7: DISPLAY FINAL RESULT
# --------------------------------

print("\n" + "=" * 40)
print("MONTHLY ATTENDANCE REPORT")
print("=" * 40)

for employee_id, counts in sorted(summary.items()):

    present = counts["Present"]
    absent = counts["Absent"]
    leave = counts["Leave"]

    total_days = present + absent + leave

    percentage = (
        (present / total_days) * 100 if total_days > 0 else 0
    )

    print(f"\nEmployee: {employee_id}")
    print(f"Present: {present}")
    print(f"Absent: {absent}")
    print(f"Leave: {leave}")
    print(f"Attendance: {percentage:.2f}%")

print("\nRejected Rows:", rejected_rows)
print("\nFiles created successfully:")
print("1.", input_file)
print("2.", output_file)
print("3.", report_file)