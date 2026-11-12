
#!/usr/bin/python3

import sys
import requests

API_URL = "http://127.0.0.1:8000"
STUDENT_ID = "STU001"


def read_agi_environment():
    while True:
        line = sys.stdin.readline()
        if not line or line in ("\n", "\r\n"):
            break


def agi(command):
    print(command, flush=True)
    return sys.stdin.readline().strip()


def get_result(response):
    if "result=" not in response:
        return ""

    return response.split("result=", 1)[1].split(" ", 1)[0]


def main():
    read_agi_environment()

    # Play custom menu
    agi('STREAM FILE ai-helpdesk ""')

    # Capture menu selection
    response = agi("GET DATA beep 10000 1")
    choice = get_result(response)

    if choice not in ("1", "2", "3"):
        agi('STREAM FILE pbx-invalid ""')
        return

    try:
        if choice == "1":
            result = requests.get(
                f"{API_URL}/students/{STUDENT_ID}/progress",
                timeout=5
            )

        elif choice == "2":
            result = requests.get(
                f"{API_URL}/students/{STUDENT_ID}/attendance",
                timeout=5
            )

        else:
            result = requests.post(
                f"{API_URL}/mentor/request/{STUDENT_ID}",
                timeout=5
            )

        result.raise_for_status()
        data = result.json()

        if "error" in data:
            agi('STREAM FILE vm-sorry ""')
            return

        if choice == "1":
            agi('STREAM FILE good ""')
            agi('SAY ALPHA "' + data["name"] + '" ""')
            agi('STREAM FILE excellent ""' if data["progress"] == "Excellent"
                else 'STREAM FILE good ""')

        elif choice == "2":
            agi('STREAM FILE good ""')
            agi('SAY NUMBER ' + str(data["attendance_percentage"]) + ' ""')
            agi('STREAM FILE digits/percent ""')

        elif choice == "3":
            agi('STREAM FILE vm-saved ""')

    except (requests.RequestException, ValueError, KeyError):
        agi('STREAM FILE vm-sorry ""')


if __name__ == "__main__":
    main()
