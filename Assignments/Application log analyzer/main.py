import os
from datetime import datetime
from collections import Counter

input_file = os.path.join("data", "application.log")
output_folder = "output"

summary_file = os.path.join(output_folder, "log_summary.txt")
invalid_file = os.path.join(output_folder, "invalid_lines.txt")

sample_logs = [
    "2026-10-01 09:10:00 INFO Application started",
    "2026-10-01 09:12:14 WARNING Retry attempt 1",
    "2026-10-01 09:13:05 ERROR Database connection failed",
    "2026-10-01 09:14:20 ERROR Database connection failed",
    "2026-10-01 09:15:00 INFO Request completed",
    "2026-10-01 09:16:00 ERROR Payment failed",
    "2026-10-01 09:17:00 WARNING Slow response detected",
    "2026-10-01 09:18:00 ERROR Database connection failed",
    "2026-10-01 09:19:00 INFO User logged in",
    "2026-10-01 09:20:00 ERROR Payment failed",
    "2026-10-01 09:21:00 ERROR API request failed",
    "2026-10-01 09:22:00 ERROR Database connection failed",
    "2026-10-01 09:23:00 DEBUG Debug message",
    "This is a malformed log line",
    "2026-10-01 09:24:00 INFO Application stopped"
]

os.makedirs("data", exist_ok=True)
if not os.path.exists(input_file):
    with open(input_file, "w", encoding="utf-8") as file:
        for log in sample_logs:
            file.write(log + "\n")
    print("sample log file created successfully!")

# output folder
os.makedirs(output_folder, exist_ok=True)

log_counts = {
    "info": 0,
    "warning": 0,
    "error": 0
}

error_messages = Counter()
invalid_lines = []

earliest_time = None
latest_time = None

valid_entries = 0

with open(input_file, "r", encoding="utf-8") as file:
    for line_number, line in enumerate(file, start=1):
        line = line.strip()

        parts = line.split(maxsplit=3)

        if len(parts) != 4:
            invalid_lines.append(f"line {line_number}: {line}")
            continue
        date_text = parts[0]
        time_text = parts[1]
        level = parts[2].lower()
        message = parts[3]

        try:
            timestamp = datetime.strptime(
                date_text + " " + time_text,
                "%Y-%m-%d %H:%M:%S"
            )
        except ValueError:
            invalid_lines.append(f"line {line_number}: {line}")
            continue

        if level not in log_counts:
            invalid_lines.append(f"line {line_number}: {line}")
            continue

        log_counts[level] += 1
        valid_entries += 1

        if level == "error":
            error_messages[message] += 1

        if earliest_time is None or timestamp < earliest_time:
            earliest_time = timestamp
        if latest_time is None or timestamp > latest_time:
            latest_time = timestamp

top_error = error_messages.most_common(5)

with open(summary_file, "w", encoding="utf-8") as file:
    file.write("application log analysis report\n")
    file.write("=" * 40 + "\n")

    file.write(f"total valid entries: {valid_entries}\n")
    file.write("LOG LEVEL SUMMARY\n")
    for level, count in log_counts.items():
        file.write(f"{level}: {count}\n")

    file.write("\nTIMESTAMP RANGE\n")
    if earliest_time is not None:
        file.write(f"farliest timestamp: {earliest_time}\n")
        file.write(f"latest timestamp: {latest_time}\n")
    else:
        file.write("no valid log entries found. \n")

    file.write("\ntop 5 frequent error messages\n")
    if top_error:
        for message, count in top_error:
            file.write(f"{message}: {count} times\n")
    else:
        file.write("no error message found.")

    file.write(f"\ninvalid line: {len(invalid_lines)}\n")

with open(invalid_file, "w", encoding="utf-8") as file:

    if invalid_lines:

        for invalid in invalid_lines:

            file.write(invalid + "\n")

    else:

        file.write("No invalid lines found.\n")
print("\n" + "=" * 40)
print("LOG ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 40)

print("\nTotal valid entries:", valid_entries)

print("INFO:", log_counts["info"])
print("WARNING:", log_counts["warning"])
print("ERROR:", log_counts["error"])

print("\nInvalid lines:", len(invalid_lines))

print("\nFiles generated:")
print("1.", input_file)
print("2.", summary_file)
print("3.", invalid_file)
