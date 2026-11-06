"""
Attendance Tracker
Data structure: a dictionary mapping each student name to a list of
attendance marks, e.g. {"Asha": ["P", "A", "P"]}  (P = Present, A = Absent)

Run menu:   python attendance_tracker.py
Run tests:  python attendance_tracker.py --test
"""
import sys

VALID = {"P": "Present", "A": "Absent"}


def add_student(records, name):
    """Add a new student with an empty attendance list."""
    name = name.strip().title()
    if not name:
        return "Name cannot be empty."
    if name in records:
        return f"{name} already exists."
    records[name] = []
    return f"Added {name}."


def mark_attendance(records, name, status):
    """Append today's attendance (P/A) for a student."""
    name, status = name.strip().title(), status.strip().upper()
    if name not in records:
        return f"{name} not found."
    if status not in VALID:
        return "Status must be P or A."
    records[name].append(status)
    return f"Marked {name} as {VALID[status]}."


def update_attendance(records, name, day, status):
    """Correct the attendance of a student on a given day (1-based)."""
    name, status = name.strip().title(), status.strip().upper()
    if name not in records:
        return f"{name} not found."
    if status not in VALID:
        return "Status must be P or A."
    if not 1 <= day <= len(records[name]):
        return f"Day must be between 1 and {len(records[name])}."
    records[name][day - 1] = status
    return f"Updated {name}, day {day} -> {VALID[status]}."


def percentage(marks):
    """Attendance percentage for one list of marks."""
    if not marks:
        return 0.0
    return marks.count("P") / len(marks) * 100


def display(records):
    """Print all records in a table."""
    if not records:
        print("No students yet.")
        return
    width = max(len(n) for n in records) + 2
    print(f"\n{'Name':<{width}}{'Present':>8}{'Total':>7}{'%':>9}   Record")
    print("-" * (width + 40))
    for name, marks in sorted(records.items()):
        print(f"{name:<{width}}{marks.count('P'):>8}{len(marks):>7}"
              f"{percentage(marks):>8.1f}%   {' '.join(marks)}")
    print()


def below_threshold(records, threshold=75):
    """Return {name: percentage} for students under the threshold."""
    return {n: round(percentage(m), 1)
            for n, m in records.items() if percentage(m) < threshold}


def run_tests():
    print("Running test scenarios...\n")

    # Scenario 1: normal mixed attendance
    r = {}
    for n in ["asha", "ravi", "meena"]:
        add_student(r, n)
    for day in range(4):
        mark_attendance(r, "Asha", "P")
        mark_attendance(r, "Ravi", "A" if day < 2 else "P")
        mark_attendance(r, "Meena", "A")
    assert percentage(r["Asha"]) == 100
    assert percentage(r["Ravi"]) == 50
    assert percentage(r["Meena"]) == 0
    print("1. Mixed attendance percentages: PASS")

    # Scenario 2: threshold detection
    low = below_threshold(r, 75)
    assert set(low) == {"Ravi", "Meena"}
    print(f"2. Below 75% -> {low}: PASS")

    # Scenario 3: updating a record changes the percentage
    update_attendance(r, "Ravi", 1, "P")
    update_attendance(r, "Ravi", 2, "P")
    assert percentage(r["Ravi"]) == 100
    assert "Ravi" not in below_threshold(r, 75)
    print("3. Update raises Ravi to 100%: PASS")

    # Scenario 4: invalid inputs are rejected
    assert "already exists" in add_student(r, "Asha")
    assert "not found" in mark_attendance(r, "Zed", "P")
    assert "must be P or A" in mark_attendance(r, "Asha", "X")
    assert "Day must be" in update_attendance(r, "Asha", 99, "P")
    print("4. Invalid input handling: PASS")

    # Scenario 5: edge case - student with no records
    add_student(r, "Kiran")
    assert percentage(r["Kiran"]) == 0.0
    print("5. Student with no records (no divide-by-zero): PASS")

    # Scenario 6: boundary - exactly at threshold is NOT below it
    b = {}
    add_student(b, "Sam")
    for s in "PPPA":
        mark_attendance(b, "Sam", s)
    assert below_threshold(b, 75) == {}
    print("6. Exactly 75% is not flagged: PASS")

    print("\nFinal table:")
    display(r)
    print("All tests passed.")


def menu():
    records = {}
    while True:
        print("""
=== Attendance Tracker ===
1. Add student
2. Mark today's attendance
3. Update a past attendance entry
4. Display records
5. Show students below threshold
6. Exit""")
        choice = input("Choose: ").strip()
        if choice == "1":
            print(add_student(records, input("Student name: ")))
        elif choice == "2":
            print(mark_attendance(records, input("Student name: "),
                                  input("Status (P/A): ")))
        elif choice == "3":
            name = input("Student name: ")
            try:
                day = int(input("Day number: "))
            except ValueError:
                print("Day must be a number.")
                continue
            print(update_attendance(records, name, day, input("New status (P/A): ")))
        elif choice == "4":
            display(records)
        elif choice == "5":
            try:
                t = float(input("Threshold % (e.g. 75): "))
            except ValueError:
                print("Enter a number.")
                continue
            low = below_threshold(records, t)
            if low:
                for n, p in low.items():
                    print(f"  {n}: {p}%")
            else:
                print("Nobody is below the threshold.")
        elif choice == "6":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    run_tests() if "--test" in sys.argv else menu()
