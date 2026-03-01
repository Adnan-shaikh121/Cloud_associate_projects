import re
from collections import Counter

LOG_FILE = "system.log"   # change to your log file path
TOP_N = 10                # number of top errors to show

def extract_error_message(line):
    """
    Extract meaningful error message from a log line.
    Customize regex based on log format.
    """
    # Common keywords in Linux/app logs
    error_keywords = r"(error|failed|failure|critical|panic)"
    if re.search(error_keywords, line, re.IGNORECASE):
        return line.strip()
    return None

def analyze_logs(log_file):
    error_counter = Counter()

    with open(log_file, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            error_msg = extract_error_message(line)
            if error_msg:
                error_counter[error_msg] += 1

    return error_counter

def main():
    errors = analyze_logs(LOG_FILE)

    if not errors:
        print("No errors found.")
        return

    print(f"\nTop {TOP_N} Error Messages:\n")
    for message, count in errors.most_common(TOP_N):
        print(f"[{count}] {message}")

if __name__ == "__main__":
    main()
