import re
from pathlib import Path
from collections import Counter

ERROR_PATTERN = re.compile(r"\[(?P<time>.*?)\]\s+ERROR\s+(?P<code>E\d+):\s+(?P<msg>.*)")

def parse_error_logs(filepath: str):
    error_count = 0
    codes = Counter()
    first_failure_time = None

    with open(filepath, "r") as f:
        for line in f:
            match = ERROR_PATTERN.search(line)
            if match:
                error_count += 1
                code = match.group("code")
                codes[code] += 1

                if first_failure_time is None:
                    first_failure_time = match.group("time")

    return {
        "total_errors": error_count,
        "unique_error_codes": list(codes.keys()),
        "error_frequencies": dict(codes),
        "first_failure_time": first_failure_time,
    }

# Example usage:
result = parse_error_logs("system.log")
print(result)