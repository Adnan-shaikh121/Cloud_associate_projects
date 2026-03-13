import re
import sys
from collections import Counter

def parse_logs(file_path):
    """Parses the log file and extracts the core error messages."""
    error_patterns = []
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # RegEx to capture the descriptive part of the error message 
                # (ignores timestamps and PIDs so identical errors group together)
                match = re.search(r'(?i)(error|failed|critical)[:\]\s]*(.*)', line)
                if match:
                    # Append just the error description
                    error_patterns.append(match.group(2).strip())
                    
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

    return error_patterns

def generate_report(errors):
    """Counts error frequencies and prints a formatted report."""
    print("--- Linux Infrastructure Log Analysis Report ---")
    
    if not errors:
        print("Status: OK. No critical errors found.")
        return
    
    error_counts = Counter(errors)
    print(f"Total Failure Events Detected: {len(errors)}\n")
    print("Top Repeated Error Patterns:")
    
    # Display the top 5 most frequent errors
    for error, count in error_counts.most_common(5):
        print(f"[{count} occurrences] -> {error}")

if __name__ == "__main__":
    # Ensure a log file is passed as an argument
    if len(sys.argv) != 2:
        print("Usage: python3 log_analyzer.py <log_file_path>")
        sys.exit(1)
    
    log_file = sys.argv[1]
    extracted_errors = parse_logs(log_file)
    generate_report(extracted_errors)