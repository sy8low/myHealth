"""myHealth is the main module which should be executed to run the programme."""

from tabulate import tabulate
import sys
import medication
import vitals
import utility

MAIN_MENU: list[dict]= [
    {"Index": 1, "Menu": "myMedication"},
    {"Index": 2, "Menu": "myVitals"},
    {"Index": 3, "Menu": "Exit"},
]
"""The options in the main menu."""

def main_menu() -> None:
    """Display the main menu of myHealth, redirect to myMedication or myVitals."""
    utility.clear_and_display("Welcome to myHealth.")
    while True:
        utility.clear_screen()
        print("myHealth Main Menu", tabulate(MAIN_MENU, headers="keys", tablefmt="simple_grid"), sep="\n")

        try:
            menu = int(input("Select a menu: ").strip())

            match menu:
                case 1:  # myMedication
                    medication.med_menu()
                case 2:  # myVitals
                    vitals.vitals_menu()
                case 3:  # Exit
                    utility.clear_and_display("Your data has been saved. Goodbye!")
                    sys.exit()
                case _:
                    raise ValueError("Invalid menu.")

        except ValueError:
            utility.display("Please select a valid menu.")
        
        except KeyboardInterrupt:
            utility.display("\nPress '3' to exit.")


def main() -> None:
    main_menu()


if __name__ == "__main__":
    main()