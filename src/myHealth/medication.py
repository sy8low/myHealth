"""myMedication stores key information about the patient's medications, including their purpose, dosage, and dose times.

Constants:
    MED_FILENAME        : The name of the csv file in disc used to store data.

Classes:
    Medicine            : Create objects that store all the relevant information about the patient's medications.

Functions:
    med_menu            : Load medications and display the menu for myMedication.
    load_medication     : Load the csv file in disc containing the patient's medications into RAM.
    save_medication     : Save the list of Medicine objects in RAM in a csv file in disc.
    view_menu_med       : Display the options for viewing the Medicine objects, and implements the same.
    query               : Prepare a query of the database based on user input.
    select_medication   : Search the database with the query generated.
    add_medication      : Construct a new Medicine object and append it to the list of Medicine objects, held in RAM.
    edit_medication     : Edit a Medicine object by calling the setters.
    remove_medication   : Remove a Medicine object from the list.
"""

import copy
import csv
from os.path import exists
from tabulate import tabulate
from time import perf_counter

try:
    # If run by interpreter
    import utility    
except ModuleNotFoundError:
    # If run from the test module.
    import myHealth.utility as utility

MED_FILENAME = "myMedication.csv"
"""The name of the csv file in the present working directory that stores the data in disc."""

class Medicine:
    """Create objects that store all the relevant information about the patient's medications.
    
    Attributes (Properties):
        name (str)
        purpose (str)
        dose (float)
        units (str)
        times (dict[str, int])
    
    Class methods:
        create
    
    Static methods:
        get_non_empty_string
        get_string
        get_pfloat
        get_units
        get_pint
    """
    
    MED_HEADERS = ["name", "purpose", "dose", "units", "times"]
    """A list of properties of the Medicine objects."""
    
    UNITS = ["g", "mg", "mcg", "units"]
    
    TIMES = {
        "BB": "before breakfast",
        "AB": "after breakfast",
        "BL": "before lunch",
        "AL": "after lunch",
        "BD": "before dinner",
        "AD": "after dinner",
        "AAWN": "as and when necessary",
    }
    """dict: Dose times and their abbreviations."""
    
    # Note changes made.
    def __init__(self, name: str, purpose: str, dose: float, units: str, times: dict[str, int]):
        """Initialise Medicine objects.

        Args:
            name (str)
            purpose (str): The physiological effects of the Medicine/conditions targeted.
            dose (float): Dose size (without units).
            units (str): Units of the aforementioned dose size.
            times (dict[str, int]): Number of doses to be taken at each dose time.
        """
        
        self.name = name
        self.purpose = purpose
        self.dose = dose
        self.units = units
        self.times = times
    
    def __repr__(self) -> str:
        """Return a string representation of the Medicine data type.

        Returns:
            String representation of the Medicine data type.
        """
        
        return f"A medication named {self.name}."
    
    def __str__(self) -> str:
        """Return a textual description of the Medicine object.

        Returns:
            Textual description of the Medicine object.
        """
        
        if self.purpose == None:
            purpose = "Unavailable"
        else:
            purpose = self.purpose.title()
        
        if self.dose == 0:
            combined_dose = "Unavailable"
        else:
            combined_dose = f"{self.dose} {self.units}"
            
        AAWN = self.times['AAWN']
        
        if AAWN > 0:
            dosage_times = f"Take {AAWN} dose(s) as and when necessary."
            
        else:
            BB, AB, BL, AL, BD, AD = [self.times[time] for time in self.times if time != "AAWN"]
            
            DAILY = sum([BB, AB, BL, AL, BD, AD])
            
            if DAILY == 0:
                dosage_times = f"There is no need to take this medication."
            else:
                dosage_times = (f"{DAILY} dose(s) a day"
                                f"\n\tBefore Breakfast: {BB}\n\tAfter Breakfast: {AB}"
                                f"\n\tBefore Lunch: {BL}\n\tAfter Lunch: {AL}"
                                f"\n\tBefore Dinner: {BD}\n\tAfter Dinner: {AD}")
        
        return (f"Name: {self.name.title()}\nPurpose: {purpose}\nDose: {combined_dose}\n{dosage_times}\n")
    
    # TODO: Print 0 for enter.
    @classmethod
    def create(cls):
        """Construct a Medicine object by prompting the user for input and validating the same.

        Returns:
            Medicine: A new Medicine object.
        """
        
        name = cls.get_non_empty_string("What's the name of the medication?: ")
        purpose = cls.get_string("What's its purpose? ")
        dose = cls.get_pfloat("What's the size of a dose (Without units)? ")
        
        if dose > 0:
            units = cls.get_units("What are the units used? ")
        else:
            units = None
            
        times = {dose_time: cls.get_pint(f"How many doses {cls.TIMES[dose_time]}? ") for dose_time in cls.TIMES if dose_time != "AAWN" }
        
        if not any(times.values()):
            times.update({"AAWN": cls.get_pint(f"How many doses {cls.TIMES['AAWN']}? ")})
        else:
            times.update({"AAWN": 0})
        
        return cls(name, purpose, dose, units, times)

    @staticmethod
    def get_non_empty_string(prompt: str) -> str:
        """Get a non-empty string from the user.

        Args:
            prompt: Instructions to the user.

        Returns:
            The non-empty string.
        """
        
        while True:
            try:
                string = input(prompt).strip().lower()
                if string and string.isascii():
                    return string
                else:
                    raise ValueError("Invalid data.")
            except ValueError:
                utility.display("Please enter valid data.", 2)

    @staticmethod
    def get_string(prompt: str) -> str:
        """Get a string (empty or non-empty) from the user.

        Args:
            prompt: Instructions to the user.

        Returns:
            The non-empty string.
        """
        
        while True:
            try:
                string = input(prompt).strip().lower()
                if not string or string.isascii():
                    return string
                else:
                    raise ValueError("Invalid data.")
            except ValueError:
                utility.display("Please enter valid data.", 2)

    @staticmethod
    def get_pfloat(prompt: str) -> float:
        """Get a positive real number from the user.

        Args:
            prompt: Instructions to the user.

        Returns:
            The positive real number.
        """
        
        while True:
            try:
                dose = input(prompt).strip()
                if not dose:
                    return 0
                else:
                    dose = float(dose)
                    if dose >= 0:
                        return dose
                    else:
                        raise ValueError("Invalid positive real number.")
            except ValueError:
                utility.display("Please enter a valid dose size (numerical value).", 2)
                
    @staticmethod
    def get_units(prompt: str) -> str:
        """Get a unit of measurement (in the list of allowed units) from the user.

        Args:
            prompt: Instructions to the user.

        Returns:
            The unit chosen.
        """
        
        while True:
            try:
                units = input(prompt).strip().lower()
                if not units:
                    return None
                elif units in Medicine.UNITS:
                    return units
                else:
                    raise ValueError("Invalid dose unit.")
            except ValueError:
                utility.display("Please enter a valid dose unit (g/mg/mcg/units).", 2)
    
    @staticmethod
    def get_pint(prompt: str) -> int:
        """Get a positive integer from the user.

        Args:
            prompt: Instructions to the user.

        Returns:
            The positive integer.
        """
        
        while True:
            try:
                integer = input(prompt).strip()
                if not integer:
                    return 0
                else:
                    integer = int(integer)
                    if integer >= 0:
                        return integer
                    else:
                        raise ValueError("Invalid positive integer.")
            except ValueError:
                utility.display("Please enter a valid number of doses (positive integer value).", 2)

    @property
    def name(self) -> str:
        """The name of the Medicine."""
        return self._name
    
    @name.setter
    def name(self, name):
        name = name.strip().lower()
        if name and name.isascii():
            self._name = name
        else:
            raise ValueError("Invalid ASCII name.")
    
    @property
    def name(self) -> str:
        """The name of the Medicine."""
        return self._name
    
    # Unfortunately, I can't reject names composed of symbols only, as many medication names have symbols.
    # A possible (more ambitious) solution is implementing a search bar for users to find medications online.
    @name.setter
    def name(self, name):
        name = name.strip().lower()
        if name and name.isascii():
            self._name = name
        else:
            raise ValueError("Invalid ASCII name.")
    
    @property
    def purpose(self) -> str:
        """The physiological effects of the Medicine/conditions targeted."""
        return self._purpose
    
    @purpose.setter
    def purpose(self, purpose):
        purpose = purpose.strip().lower()
        if not purpose:  # None is stored as an empty string in CSVs.
            self._purpose = None
        elif purpose.isascii():
            self._purpose = purpose
        else:
            raise ValueError("Invalid ASCII entry.")

    @property
    def dose(self) -> float:
        """Dose size (without units)."""
        return self._dose
    
    @dose.setter
    def dose(self, dose):
        dose = float(dose)
        if dose > 0:
            self._dose = dose
        elif dose == 0:
            self._dose = 0
            self._units = None
        else:
            raise ValueError("Invalid positive real number.")

    @property
    def units(self) -> str:
        """Units of the aforementioned dose size."""
        return self._units
    
    @units.setter
    def units(self, units):
        if self.dose > 0:
            if units in Medicine.UNITS:
                self._units = units
            elif not units:
                self._units = None
            else:
                raise ValueError("Invalid units provided.")
        else:
            self._units = None
    
    @property
    def times(self) -> dict[str, int]:
        """Number of doses to be taken at each dose time."""
        return self._times     
   
    @times.setter
    def times(self, times):
        for entry in times:
            times[entry] = int(times[entry])
            if times[entry] < 0:
                raise ValueError("Invalid positive integer.")
        self._times = times


def med_menu() -> None:
    """Load medications and display the menu for myMedication.
    
    Note:
        The options are: View, Add, Edit, Remove, Undo All Changes, Save and Go Back.
    """
    
    MED_MENUS = [
        {"Index": 1, "Action": "View Medication"},
        {"Index": 2, "Action": "Add Medication"},
        {"Index": 3, "Action": "Edit Medication"},
        {"Index": 4, "Action": "Remove Medication"},
        {"Index": 5, "Action": "Undo All Changes"},
        {"Index": 6, "Action": "Save and Go Back to myHealth"},
    ]
    
    utility.clear_screen()
    try:
        medlist, message = load_medication()
        utility.display(message)
        
    except ValueError:
        utility.display("Medications failed to load. Returning to myHealth...")
    
    # JIC. An empty file will be created if one does not yet exist.    
    except (OSError, FileNotFoundError):
        utility.display("Database does not exist. Returning to myHealth...")
    
    else:
        # Warning: Whenever individual entries are manipulated, you'd better make a deep copy.
        main_backup = copy.deepcopy(medlist)
        
        while True:
            utility.clear_screen()
            print("myMedication", tabulate(MED_MENUS, headers="keys", tablefmt="simple_grid"), sep="\n")

            try:
                action = int(input("Select an action: ").strip())
                utility.clear_screen()

                match action:
                    case 1:  # View Medication
                        view_menu_med(medlist)
                    
                    case 2:  # Add Medication
                        medlist, message = add_medication(medlist)
                        utility.clear_and_display(message)
                    
                    case 3:  # Edit Medication
                        medlist, message = edit_medication(medlist)
                        utility.clear_and_display(message)
                        
                    case 4:  # Remove Medication
                        medlist, message = remove_medication(medlist)
                        utility.clear_and_display(message)
                    
                    case 5:  # Undo All Changes
                        medlist = copy.deepcopy(main_backup)
                        utility.clear_and_display("All changes have been undone. The original list of medications has been restored.")
                    
                    case 6:  # Save and Go Back to Main Menu
                        utility.clear_and_display(save_medication(medlist))
                        break
                    
                    case _:
                        raise ValueError("Invalid action.")

            except KeyError:
                utility.display("Medication not found. Returning to myMedication...")
            
            except ValueError:
                utility.display("Please select a valid action.")
            
            except KeyboardInterrupt:
                utility.display("\nPress '5' to return to myHealth.")


def load_medication() -> tuple[list[Medicine], str]:
    """Load the csv file in disc containing the patient's medications into RAM.
    
    Note:
        An empty file will be created if one doesn't already exist.

    Returns:
        A list of Medicine objects and a success/failure message to the user.
    """
    
    start = perf_counter()
    
    if not exists(MED_FILENAME):
        with open(MED_FILENAME, "w") as file:
            writer = csv.DictWriter(file, Medicine.MED_HEADERS)
            writer.writeheader()
    
    med_data = []
    with open(MED_FILENAME, newline="") as meddb:
        reader = csv.DictReader(meddb)
        
        for med in reader:                
            med_data.append(Medicine(med["name"], med["purpose"], float(med["dose"]), med["units"], eval(med["times"])))
    
    end = perf_counter()
    return med_data, f"Medications loaded successfully. {end - start:.5f} seconds."


def save_medication(med_data: list[Medicine]) -> str:
    """Save the list of Medicine objects in RAM in a csv file in disc.

    Args:
        med_data: The list of Medicine objects, held in RAM.

    Returns:
        A success/failure message to the user.
    """
    
    with open(MED_FILENAME, "w", newline="") as meddb:
        writer = csv.DictWriter(meddb, Medicine.MED_HEADERS)
        writer.writeheader()
        
        start = perf_counter()
        for med in med_data:
            writer.writerow({
                "name": med._name,
                "purpose": med._purpose,
                "dose": med._dose,
                "units": med._units,
                "times": med._times,
            })
    
    end = perf_counter()
    return f"Medications saved successfully, returning to Main Menu. {end - start:.5f} seconds."


# TODO: Display as table.
def view_menu_med(meddb: list[Medicine]) -> None:
    """Display the options for viewing the Medicine objects, and implements the same.

    Note:
        The options are: View All, Find, Back to myMedication.
        
    Args:
        The list of Medicine objects, held in RAM.
    """
    
    VIEW_MENUS_MED = [
        {"Index": 1, "Action": "View All Medications"},
        {"Index": 2, "Action": "Find a Medication"},
        {"Index": 3, "Action": "Back to myMedication"},
    ]
    
    while True:
        utility.clear_screen()
        print("View Medication", tabulate(VIEW_MENUS_MED, headers="keys", tablefmt="simple_grid"), sep="\n")

        try:
            action = int(input("Select an action: ").strip())
            utility.clear_screen()

            match action:
                case 1:  # View All Medications
                    utility.clear_and_display("Displaying all Medications...")
                    
                    if meddb:
                        start = perf_counter()
                        for med in meddb:
                            print(med)
                            
                        end = perf_counter()
                        print(f"{end - start:.5f} seconds.")
                        
                    else:
                        print("No medications to view.")
                        
                    utility.clear_and_display(utility.backtrack(f"View Medication"))
                    
                case 2:  # Find a Medication
                    if meddb:
                        category, search = query()
                        
                        start = perf_counter()
                        results = select_medication(category, search, meddb)
                        end = perf_counter()
                        
                        for index in results:
                            print(meddb[index])
                                                
                        print(f"{end - start:.5f} seconds.")
                        
                    else:
                        print("No medications to view.")
                    
                    utility.clear_and_display(utility.backtrack("View Medication"))
                        
                case 3:  # Back to myMedication
                    utility.clear_and_display("Returning to myMedication...")
                    break
                
                case _:
                    raise ValueError("Invalid action.")

        except KeyError:
            utility.display("Medication not found. Returning to View Medication...")
        
        except ValueError:
            utility.display("Please select a valid action.")
        
        except KeyboardInterrupt:
            utility.display("\nPress '3' to return to myMedication.")


def query() -> tuple[str, str]:
    """Prepare a query of the database based on user input.

    Returns:
        The column to be searched and the search term provided.
    """
    
    utility.clear_screen()
    while True:
        category = Medicine.get_non_empty_string("What category are you trying to search (Name/Purpose/Times)? ")
        if category in Medicine.MED_HEADERS:
            break
        else:
            utility.display("Category does not exist.")
    
    while True:
        match category:
            case "name":
                search = Medicine.get_non_empty_string("Which medication are you trying to find? ")
                break
            
            case "purpose":
                search = Medicine.get_non_empty_string("What class of medications are you trying to find? ")
                break
            
            case "dose":
                utility.display("Finding medications based on dosage is not supported.")
                
            case "units":
                utility.display("Finding medications based on units of measurement is not supported.")
                
            case "times":
                while True:
                    search = input(
                        "Which dosage time are you trying to find?\n"
                        "BB: Before Breakfast\tAB: After Breakfast\n"
                        "BL: Before Lunch\tAL: After Lunch\n"
                        "BD: Before Dinner\tAD: After Dinner\n"
                        "AAWN: As and when necessary\n"
                    ).strip().upper()
                    if search in Medicine.TIMES:
                        break
                    else:
                        utility.display("Invalid input. Please try again.")
                        utility.clear_5_lines()
                break
                 
    return category, search


def select_medication(category: str, search: str, med_data: list[Medicine]) -> list[int]:
    """Search the database with the query generated.

    Args:
        category: The column to be searched.
        search: The search term to be found.
        med_data: The list of Medicine objects, held in RAM.

    Raises:
        KeyError: If the search term yields no matches.
    
    Returns:
        The indices of the Medicine objects found.
    """
    
    results = []
    
    match category:
        case "name":
            for i in range(len(med_data)):
                if search in med_data[i].name:
                    results.append(i)
                    
        case "purpose":
            for i in range(len(med_data)):
                if med_data[i].purpose and search in med_data[i].purpose:
                    results.append(i)
                    
        case "times":
            for i in range(len(med_data)):
                if med_data[i].times[search] != 0:
                    results.append(i)
    
    if results:
        return results
    else:
        raise KeyError("Medication not found.")


def add_medication(med_data: list[Medicine]) -> tuple[list[Medicine], str]:
    """Construct a new Medicine object and append it to the list of Medicine objects, held in RAM.

    Args:
        med_data: The list of Medicine objects, held in RAM.

    Returns:
        The updated list of Medicine objects and a success/failure message to the user.
    """
    
    # med_data is passed in as a reference to an object.
    # If amended, the underlying list itself will be amended in place without the need for a return value.
    
    new_med_data = copy.deepcopy(med_data)
    backup = copy.deepcopy(med_data)
    
    try:
        new_med = Medicine.create()
        
        start = perf_counter()
        for med in new_med_data:
            if med.name == new_med.name:
                raise utility.DuplicateError(new_med.name, "myMedication")
        
        new_med_data.append(new_med)
        
        end = perf_counter()
        return new_med_data, f"{new_med.name.title()} successfully added. Returning to myMedication... {end - start:.5f} seconds."
    
    except KeyboardInterrupt:
        return backup, "\nAction disrupted. No changes will be made. Returning to myMedication..."

    except utility.DuplicateError as error:
        return backup, error.msg


def edit_medication(med_data: list[Medicine]) -> tuple[list[Medicine], str]:
    """Edit a Medicine object by calling the setters.

    Args:
        med_data: The list of Medicine objects, held in RAM.

    Raises:
        KeyError: No Medicine object with the given name can be found.

    Returns:
        The updated list of Medicine objects and a success/failure message to the user.
    """
    
    if not med_data:
        print("No medications to edit.")
        return med_data, utility.backtrack("myMedication")
    
    else:
        new_med_data = copy.deepcopy(med_data)
        backup = copy.deepcopy(med_data)
        target = None
        
        try:
            search = Medicine.get_non_empty_string("Which medication are you trying to edit? ")
            
            start = perf_counter()
            for i in range(len(new_med_data)):
                if search in new_med_data[i].name:
                    target = new_med_data[i]
                    break
            end = perf_counter()
            utility.display(f"{end - start:.5f} seconds.")
            
            if target:
                print(f"This is the entry for {target.name.title()}", target, sep="\n")
                
                if utility.yes_or_no(f"Do you want to change the name of {target.name.title()}? "):
                    while True:
                        try:
                            target.name = input(f"What's the new name of {target.name.title()}? ")
                            break
                        except ValueError:
                            utility.display("Please enter a valid alphanumeric name.")

                if utility.yes_or_no(f"Do you want to change the purpose of {target.name.title()}? "):
                    while True:
                        try:
                            target.purpose = input(f"What's the new purpose of {target.name.title()}? ")
                            break
                        except ValueError:
                            utility.display("Please enter a valid alphanumeric entry.")
                            
                if utility.yes_or_no(f"Do you want to change the dose size of {target.name.title()}? "):
                    while True:
                        try:
                            target.dose = input(f"What's the new dose size of {target.name.title()} (Without units)? ")
                            break
                        except ValueError:
                            utility.display("Please enter a valid dose size.")
                    
                    if target.dose > 0:
                        while True:
                            try:
                                target.units = input(f"Please provide the units. ")
                                break
                            except ValueError:
                                utility.display("Please enter a valid unit.")
                    else:
                        target.units = None

                if utility.yes_or_no(f"Do you want to change the dosage times of {target.name.title()}? "):
                    while True:
                        updated_times = copy.deepcopy(target.times)
                        
                        while True:
                            try:
                                time_to_change = input("Which dosage time are you trying to change?\n"
                                                    "BB: Before Breakfast\tAB: After Breakfast\n"
                                                    "BL: Before Lunch\tAL: After Lunch\n"
                                                    "BD: Before Dinner\tAD: After Dinner\n"
                                                    "AAWN: As and when necessary\n"
                                                    "Press enter if there are no further changes to be made.\n").strip().upper()

                                if time_to_change in Medicine.TIMES or not time_to_change:
                                    break
                                else:
                                    raise KeyError("Invalid dosage time selected.")
                                
                            except KeyError:
                                utility.display("Please select a valid dosage time to be changed.")
                                utility.clear_5_lines()
                        
                        if time_to_change in Medicine.TIMES:
                            while True:
                                try:                                
                                    if time_to_change == "AAWN":
                                        updated_times["AAWN"] = input("How many doses should be taken as and when necessary? ")
                                        for other_times in Medicine.TIMES:
                                            if not "AAWN": updated_times[other_times] = 0
                                        utility.display("All other dosage times will be set to 0.")
                                        
                                    else:
                                        updated_times[time_to_change] = input(f"How many doses should be taken {Medicine.TIMES[time_to_change]}? ")
                                        if updated_times[time_to_change] != 0 and updated_times["AAWN"] != 0:
                                            updated_times["AAWN"] = 0
                                            utility.display("AAWN will be set to 0.")
                                    
                                    target.times = updated_times
                                    break

                                except ValueError:
                                    utility.display("Please enter a valid number of doses.")
                                    
                        else:
                            break

                print(f"This is the new entry for {target.name.title()}", target, sep="\n")
                
                return new_med_data, utility.backtrack("myMedication")
            
            else:
                raise KeyError("Medication not found.")
            
        except KeyboardInterrupt:
            return backup, "\nAction disrupted. No changes will be made. Returning to myMedication..."


def remove_medication(med_data: list[Medicine]) -> tuple[list[Medicine], str]:
    """Remove a Medicine object from the list.

    Args:
        med_data: The list of Medicine objects, held in RAM.

    Raises:
        KeyError: No Medicine object with the given name can be found.

    Returns:
        The updated list of Medicine objects and a success/failure message to the user.
    """
    
    if not med_data:
        print("No medications to remove.")
        return med_data, utility.backtrack("myMedication")
    
    else:
        new_med_data = copy.deepcopy(med_data)
        target = None
        target_index = None
        
        try:
            search = Medicine.get_non_empty_string("Which medication are you trying to delete? ")
            
            start = perf_counter()
            for i in range(len(new_med_data)):
                if search in new_med_data[i].name:
                    target = new_med_data[i]
                    target_index = i
                    break
                
            end = perf_counter()
            utility.display(f"{end - start:.5f} seconds.")
            
            if target:
                utility.clear_screen()
                print(f"This is the entry for {target.name.title()}", target, sep="\n")
                
                if utility.yes_or_no(f"Are you sure you want to delete {target.name.title()}? "):
                    # Pop makes changes in place and returns the deleted object.
                    message = f"The entry for {target.name.title()} has been deleted successfully."
                    del new_med_data[target_index]
                
                else:
                    message = f"The entry for {target.name.title()} will not be deleted."
                
                return new_med_data, message + " Returning to myMedication..."
                
            else:  # Should not return any value afterwards. Don't use "finally".
                raise KeyError("Medication not found.")
            
        except KeyboardInterrupt:
            return new_med_data, "\nAction disrupted. No changes will be made. Returning to myMedication..."