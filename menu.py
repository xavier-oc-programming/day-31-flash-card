import os
import sys
import subprocess
from pathlib import Path

from art import LOGO

ORIGINAL = Path(__file__).parent / "original" / "main.py"
ADVANCED = Path(__file__).parent / "advanced" / "main.py"

while True:
    os.system("cls" if os.name == "nt" else "clear")
    print(LOGO)
    print("  French Flashcard App — Day 31")
    print()
    print("  1. Original build  (course solution)")
    print("  2. Advanced build  (OOP + config)")
    print("  q. Quit")
    print()

    choice = input("Select: ").strip().lower()

    if choice == "1":
        subprocess.run([sys.executable, str(ORIGINAL)], cwd=str(ORIGINAL.parent))
    elif choice == "2":
        subprocess.run([sys.executable, str(ADVANCED)], cwd=str(ADVANCED.parent))
    elif choice == "q":
        break
    else:
        print("Invalid choice. Try again.")
