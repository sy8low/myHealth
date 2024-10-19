"""myVitals tracks the patient's vital signs (blood pressure, pulse, blood glucose levels).

Constants:
    VITALS_HEADERS          : The name of the csv file in disc used to store data.

Functions:
    Preparing vitals records:
        vitals_menu         : Load vitals records and display the menu for myVitals.
        load_vitals         : Load the csv file in disc containing the patient's vitals records into RAM.
        save_vitals         : Save the Pandas DataFrame in RAM in a csv file in disc.
    
    Viewing vitals records:
        view_menu_vitals    : Display the options for viewing the entries in the Pandas DataFrame, and implement the same.
        select_timeframe    : Filter the DataFrame to include only records within a certain time period from the target date.
        select_data         : Filter the DataFrame further to include only the data that the user wants to view. 
        filter_selected_data: Implement the removal of columns that the user is not interested in viewing.
        view_options        : Select how the data is to be visualised, and implements the same.
    
    Searching vitals records:
        search_vitals       : Find the first record in the DataFrame with the desired date using a binary search algorithm,
                              implemented recursively. DataFrame is sliced.
        search_vitals_2     : Find the first record in the DataFrame with the desired date using a binary search algorithm,
                              implemented recursively. DataFrame is not sliced.
        crawler             : Find all records before/after the record found with search_vitals from the same month/day
                              (implemented recursively).
        get_index_record    : Get a date from the user, then get the user to pick a record from the all the records from the
                              same day found.
    
    Manipulating vitals records:
        add_vitals          : Add a record to the DataFrame.
        edit_vitals         : Edit a record in the DataFrame.
        remove_vitals       : Remove a record from the DataFrame.
        
Classes:
    Input                   : Provides helper functions for soliciting and validating user input.

Exceptions:
    NoSelectionError        : Raise an exception if the user chooses not to proceed with an action.
"""

import csv
from datetime import datetime, date, time
import numpy as np
from os.path import exists
import pandas as pd
import re
from tabulate import tabulate
from time import perf_counter
import utility
import visualisation
import warnings

VITALS_HEADERS = ["datetime", "sys", "dia", "pulse", "glucose"]
"""A list of columns in the vitals database."""

VITALS_FILENAME = "myVitals.csv"
"""The name of the csv file in disc used to store data."""

def vitals_menu() -> None:
    """Load vitals records and display the menu for myVitals.
    
    Note:
        The options are: View, Add, Edit, Remove, Undo All Changes, Save and Go Back.
    """
    
    VITAL_MENUS = [
        {"Index": 1, "Action": "View Records"},
        {"Index": 2, "Action": "Add Record"},
        {"Index": 3, "Action": "Edit Record"},
        {"Index": 4, "Action": "Remove Record"},
        {"Index": 5, "Action": "Undo All Changes"},
        {"Index": 6, "Action": "Save and Go Back to myHealth"},
    ]
    
    utility.clear_screen()
    try:
        vitals, message = load_vitals()
        utility.display(message)
        
    except ValueError:
        utility.display("Vitals records failed to load. Returning to My Health...")
        
    except (OSError, FileNotFoundError):
        utility.display("Database does not exist. Returning to My Health...")
    
    else:
        main_backup = vitals.copy(deep=True)
        
        while True:
            utility.clear_screen()
            print("myVitals", tabulate(VITAL_MENUS, headers="keys", tablefmt="simple_grid"), sep="\n")

            try:
                action = int(input("Select an action: ").strip())
                utility.clear_screen()

                match action:
                    case 1:  # View Records
                        view_menu_vitals(vitals)
                    
                    case 2:  # Add Record
                        vitals, message = add_vitals(vitals)
                        utility.clear_and_display(message)
                    
                    case 3:  # Edit Record
                        vitals, message = edit_vitals(vitals)
                        utility.clear_and_display(message)
                        
                    case 4:  # Remove Record
                        vitals, message = remove_vitals(vitals)
                        utility.clear_and_display(message)
                    
                    case 5:  # Undo All Changes
                        vitals = main_backup.copy(deep=True)
                        utility.clear_and_display("All changes have been undone. The original database has been restored.")
                    
                    case 6:  # Save and Go Back to myHealth- Done
                        utility.clear_and_display(save_vitals(vitals))
                        break
                    
                    case _:
                        raise ValueError("Invalid action.")

            except utility.DuplicateError as error:
                utility.display(error.msg)
            
            except (KeyError, RecursionError):
                utility.display("Record not found. Returning to myVitals...")
            
            except ValueError:
                utility.display("Please select a valid action.")
            
            except KeyboardInterrupt:
                utility.display("\nPress '5' to return to My Health.")


def load_vitals() -> tuple[pd.DataFrame, str]:
    """Load the csv file in disc containing the patient's vitals records into RAM.
    
    Note:
        An empty file will be created if one doesn't already exist.
            
    Returns:
        The records as a Pandas DataFrame and a success/failure message to the user.
    """
    
    start = perf_counter()
    
    if not exists(VITALS_FILENAME):
        with open(VITALS_FILENAME, "w") as file:
            writer = csv.DictWriter(file, VITALS_HEADERS)
            writer.writeheader()
    
    # parse_dates=True is broken and has no effect.
    warnings.simplefilter(action='ignore', category=UserWarning)
    vitals = pd.read_csv(VITALS_FILENAME)
    vitals["datetime"] = pd.to_datetime(vitals["datetime"], yearfirst=True)
    vitals.sort_values("datetime", inplace=True, ignore_index=True)
    
    end = perf_counter()
    return vitals, f"Records loaded successfully. {end - start:.5f} seconds."


def save_vitals(vitalsdb: pd.DataFrame) -> str:
    """Save the Pandas DataFrame in RAM in a csv file in disc.

    Args:
        vitalsdb: The vitals records, held in RAM.

    Returns:
        A success/failure message to the user.
    """
    
    # Make sure the file is not open in Excel, otherwise a PermissionError will be raised.
    start = perf_counter()
    vitalsdb.to_csv(VITALS_FILENAME, index=False)
    del vitalsdb
    
    end = perf_counter()
    return f"Records saved successfully, returning to Main Menu. {end - start:.5f} seconds."


def view_menu_vitals(vitalsdb: pd.DataFrame) -> None:
    """Display the options for viewing the entries in the Pandas DataFrame, and implement the same.

    Note:
        The options are: View All, View Latest, Find, Back to myVitals.
    
    Implementation:
        1. Get a date from the user (if necessary).
        2. Filter by the user's desired time period.
        3. Filter by the user's desired columns.
        4. Select how the data is to be visualised.
    
    Args:
        vitalsdb: The Pandas DataFrame of the vitals records, held in RAM.
    """
    
    VIEW_MENUS_VITALS = [
        {"Index": 1, "Action": "View All Records"},
        {"Index": 2, "Action": "View the Latest Record"},
        {"Index": 3, "Action": "Find a Record"},
        {"Index": 4, "Action": "Back to myVitals"},
    ]
    
    while True:
        utility.clear_screen()
        print("View Vitals", tabulate(VIEW_MENUS_VITALS, headers="keys", tablefmt="simple_grid"), sep="\n")

        try:
            action = int(input("Select an option: ").strip())
            utility.clear_screen()

            match action:
                case 1:  # View All Records
                    selected_timeframe = vitalsdb
                
                case 2:  # View the Latest Record
                    target: int = vitalsdb.index[-1]
                    utility.clear_and_display(f"The record for {vitalsdb.at[target, 'datetime']} has been selected...")
                    
                    selected_timeframe = select_timeframe(vitalsdb, target)
                                
                case 3:  # Find a Record
                    target_date: pd.Timestamp = Input.get_datetime()
                    # A shallow copy will do as we're not manipulating entries.
                    start = perf_counter()
                    target: int = search_vitals_2(vitalsdb, target_date)
                    end = perf_counter()
                    utility.clear_and_display(f"{target_date.date()} has been selected... {end - start:.5f} seconds.")
                                       
                    selected_timeframe = select_timeframe(vitalsdb, target)
                        
                case 4:  # Back to myVitals
                    utility.clear_and_display("Returning to myVitals...")
                    break
                
                case _:
                    raise ValueError("Invalid option.")
            
            # Alternative: if selected_timeframe: selected_data = select_data(selected_timeframe) if selected_data: viewer(selected_data)
            selected_data = select_data(selected_timeframe)
            records = len(selected_data.index)
    
            if records == 0:
                utility.display("There are no records available for viewing.")
            
            elif 10 <= records <= 100:
                view_options(selected_data)

            else:
                print(selected_data.to_string())
                utility.clear_and_display(utility.backtrack("View Vitals"))
        
        except NoSelectionError as error:
            utility.display(error.msg)
            
        except (KeyError, RecursionError):
            utility.display("Record not found. Returning to View Vitals...")
        
        except ValueError:
            utility.display("Please select a valid option.")
        
        except KeyboardInterrupt:
            utility.display("\nPress '4' to return to myVitals.")


def select_timeframe(vitalsdb: pd.DataFrame, target: int) -> pd.DataFrame:
    """Filter the DataFrame to include only records within a certain time period from the target date.

    Note:
        The options are: View Selected Record, View All from the Same Day/Month, View Records Before it, Go Back.
    
    Args:
        vitalsdb: The full Pandas DataFrame.
        target: The index of the record found.

    Raises:
        NoSelectionError: If the user chooses to return to View Vitals (the previous menu).

    Returns:
        The filtered DataFrame.
    """
    
    TIMEFRAME_MENUS = [
        {"Index": 1, "Action": "View the selected record"},
        {"Index": 2, "Action": "View all records from the same day"},
        {"Index": 3, "Action": "View all records from the same month"},
        {"Index": 4, "Action": "View records before it"},
        {"Index": 5, "Action": "Back to View Vitals"},
    ]
    
    while True:
        utility.clear_screen()
        print("Select Timeframe", tabulate(TIMEFRAME_MENUS, headers="keys", tablefmt="simple_grid"), sep="\n")
        
        try:
            action = int(input("Select a timeframe: ").strip())
            utility.clear_screen()

            match action:
                case 1:  # View the selected record
                    selected_indices = [target]
                
                case 2:  # View all records from the same day
                    start = perf_counter()
                    start_index = crawler(vitalsdb, target, False)
                    end_index =  crawler(vitalsdb, target)
                    
                    if start_index == end_index:
                        selected_indices = [target]
                    else:
                        selected_indices = list(range(start_index, end_index + 1))
                    
                    end = perf_counter()
                    utility.clear_and_display(f"{end - start:.5f} seconds.")
                
                case 3:  # View all records from the same month
                    start = perf_counter()
                    start_index = crawler(vitalsdb, target, False, "m")
                    end_index =  crawler(vitalsdb, target, True, "m")

                    selected_indices = list(range(start_index, end_index + 1))
                    
                    end = perf_counter()
                    utility.clear_and_display(f"{end - start:.5f} seconds.")

                case 4:  # View records before it
                    while True:
                        try:
                            number = int(input("How many records should be viewed? "))
                            if number > 0:
                                break
                            
                        except ValueError:
                            utility.display("Please enter a valid number of records")
                    
                    if number > (target + 1):
                        number = target + 1
                        utility.display(f"There are only {number} record(s) before this. Only {number} record(s) will be shown.")
                    
                    selected_indices = list(range(target - number + 1, target + 1))

                case 5:  # Back to View Vitals
                    raise NoSelectionError("View Vitals")
                
                case _:
                    raise ValueError("Invalid timeframe.")
            
            # DataFrame.at can only access single cells.
            selected_timeframe = pd.DataFrame(vitalsdb.loc[selected_indices])
                
        except KeyError:
            utility.display("The selected timeframe cannot be accessed. Please try again.")
            
        except ValueError:
            utility.display("Please select a valid timeframe.")
        
        except KeyboardInterrupt:
            utility.display("\nPress '5' to return to View Vitals.")
            
        else:
            utility.clear_and_display(f"{len(selected_indices)} record(s) will be shown.")
            return selected_timeframe


def select_data(selected_timeframe: pd.DataFrame) -> pd.DataFrame:
    """Filter the DataFrame further to include only the data that the user wants to view. 

    Note:
        The options are: View 1. All; 2. Blood Glucose; 3. BP; 4. Pulse; 5. BP and Pulse; 6. Go Back.
    
    Args:
        selected_timeframe: The DataFrame filtered by time.

    Raises:
        NoSelectionError: If the user chooses to return to View Vitals (the previous menu).

    Returns:
        The DataFrame filtered by time and columns.
    """
    
    DATA_MENUS = [
        {"Index": 1, "Action": "View All Data"},
        {"Index": 2, "Action": "View Blood Glucose Levels"},
        {"Index": 3, "Action": "View Blood Pressure"},
        {"Index": 4, "Action": "View Pulse Rate"},
        {"Index": 5, "Action": "View Blood Pressure and Pulse Rate"},
        {"Index": 6, "Action": "Back to View Vitals"},
    ]
    
    while True:
        utility.clear_screen()
        print("Select Data", tabulate(DATA_MENUS, headers="keys", tablefmt="simple_grid"), sep="\n")
        
        try:
            action = int(input("Select the data to be viewed: ").strip())
            utility.clear_screen()

            match action:
                case 1:  # View All Data
                    selected_timeframe.dropna(subset=["sys", "dia", "pulse", "glucose"], how="all", inplace=True)
                    filtered_data = selected_timeframe
                
                case 2:  # View Blood Glucose Levels
                    filtered_data = filter_selected_data(selected_timeframe, ["datetime", "glucose"])
                
                case 3:  # View Blood Pressure
                    filtered_data =  filter_selected_data(selected_timeframe, ["datetime", "sys", "dia"])
                
                case 4:  # View Pulse Rate
                    filtered_data =  filter_selected_data(selected_timeframe, ["datetime", "pulse"])
                
                case 5:  # View Blood Pressure and Pulse Rate
                    filtered_data =  filter_selected_data(selected_timeframe, ["datetime", "sys", "dia", "pulse"])

                case 6:  # Back to myVitals
                    raise NoSelectionError("View Vitals")
                
                case _:
                    raise ValueError("Invalid option.")
        
        except ValueError:
            utility.display("Please select a valid option.")
        
        except KeyboardInterrupt:
            utility.display("\nPress '6' to return to View Vitals.")
            
        else:
            utility.clear_and_display(f"{len(filtered_data.index)} record(s) will be shown.")
            return filtered_data


def filter_selected_data(selected_data: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Implement the removal of columns that the user is not interested in viewing.

    Args:
        selected_data: The DataFrame filtered by time.
        columns: The columns containing the data the user is interested in

    Returns:
        The DataFrame filtered by time and columns.
    """
    
    # Passing in a list returns a DataFrame, but passing in comma-separated items returns a specific cell.
    # Remember that the axis is "rows", not "columns".
    selected_data = selected_data[columns]
    
    columns.remove("datetime")  # Done in place.
    selected_data.dropna(subset=columns, how="all", inplace=True)  # If axis = 0, rows will be dropped.
    
    return selected_data


def view_options(filtered_data: pd.DataFrame) -> None:
    """Select how the data is to be visualised, and implements the same.

    Note:
        The options are: Table, Graph, Go Back.
        
    Args:
        filtered_data: The DataFrame filtered by time and columns.
    """
    
    VIEW_OPTIONS_MENUS = [
        {"Index": 1, "Action": "Table View"},
        {"Index": 2, "Action": "Graph View"},
        {"Index": 3, "Action": "Back to View Vitals"},
    ]
    
    while True:
        utility.clear_screen()
        print("Select View Options", tabulate(VIEW_OPTIONS_MENUS, headers="keys", tablefmt="simple_grid"), sep="\n")

        try:
            action = int(input("Select an view option: ").strip())
            utility.clear_screen()

            match action:               
                case 1:  # Table View
                    print(filtered_data.to_string())
                
                case 2:  # Graph View                    
                    if "glucose" not in filtered_data.columns:  # Index object.
                        visualisation.bp_scatter(filtered_data)
                    
                    elif filtered_data.columns.size == 2 and "glucose" in filtered_data.columns:
                        visualisation.glucose_scatter(filtered_data)
                        visualisation.glucose_hist(filtered_data)

                    # Alt: filtered_data.columns == pd.Index(["datetime", "sys", "dia", "pulse", "glucose"])
                    # If all data are viewed, the conditional returns True.
                    # However, if only a selection of data is viewed, the conditional cannot be evaluated. ValueError: Lengths must match to compare.
                    # Furthermore, what if the columns are somehow out of order?
                    else:
                        visualisation.bp_scatter(filtered_data)
                        visualisation.glucose_scatter(filtered_data)
                        visualisation.glucose_hist(filtered_data)
                        
                case 3:  # Back to View Vitals
                    utility.clear_and_display("Returning to View Vitals...")
                    break
                
                case _:
                    raise ValueError("Invalid option.")

            utility.clear_and_display(utility.backtrack("View Options"))
        
        except ValueError as error:
            utility.display(error) #"Please select a valid option."
        
        except KeyboardInterrupt:
            utility.display("\nPress '3' to return to myVitals.")


def search_vitals(vitalsdb: pd.DataFrame, target_date: pd.Timestamp, date_only: bool=True) -> int:
    # Remember to only pass in copies of the original database.
    # Be careful when passing objects as arguments into functions: it is actually the reference that is passed in.
    # Methods applied to them in place will be applied to the underlying object outside of the scope.
    """Find a record in the DataFrame with the desired date using a binary search algorithm, implemented recursively. DataFrame is sliced.
    
    Implementation:
        1. If there are no more records left in the DataFrame, raise an exception.
        2. The date/datetime of the middle index is compared to the target_date/datetime.
            a. If the middle index is dated later, everything that comes after it is discarded,
               and the algorithm is repeated with the truncated DataFrame.
            b. If the middle index is dated earlier, everything that comes before it is discarded,
               and the algorithm is repeated with the truncated DataFrame.
            c. If the middle index is dated to the target_date/datetime, a match is found, and the middle index is returned.
    
    Args:
        vitalsdb            : The DataFrame being searched. Must be a copy when first called. (Previously, this function  
                              performs the copying. However, this is memory intensive as copying takes place after every recursion.)
        target_date         : The date/datetime to be matched.
        date_only (optional): Indicates if only the date should be matched, or the full datetime. Defaults to True.
               
    Raises:
        KeyError      : If the DataFrame cannot be sliced further (no matches can possibly be found).
        RecursionError: If no matches are produced after 1000 calls (extremely unlikely for a match to be found). Only occurs if there are >2^1000 records.
    
    Returns:
        The index of the first record found by the algorithm.
    """
    
    # Not possible to find the median of Index objects directly. ndarrays are easier to work with than lists.
    index_array: np.ndarray = vitalsdb.index.to_numpy()
    
    # If a record does not exist, eventually the database will be sliced until it becomes an empty array.
    if index_array.size == 0:
        raise KeyError("Record not found.")
    
    # In the case that there is an even number of indices, truncation returns the low median.
    middle_index = int(np.median(index_array))
    
    # at favoured over loc for single cell searches.
    checked_date: pd.Timestamp = vitalsdb.at[middle_index, "datetime"]
    # target_date needs to be passed into recursive calls. We shouldn't change it.
    target_date_compare: pd.Timestamp = target_date
    
    # Forgetting to extract the date portion means that matches may never be found.
    if date_only:
        # Method, not an attribute. Returns a datetime.date object.
        checked_date: date = checked_date.date()
        target_date_compare: date= target_date.date()
    
    # Overshot: Disregard every entry including and after the middle_index.
    if checked_date > target_date_compare:
        # range returns a range object, not a list.
        # RangeIndex is ascending.
        # Being able to get min and max is the advantage of using ndarrays.
        discard = list(range(middle_index, index_array.max() + 1))
        # Doing it in place avoids the memory-intensive copying process.
        vitalsdb.drop(discard, inplace=True)
        # Recursion: make sure returned call has all the required arguments.
        return search_vitals(vitalsdb, target_date, date_only)
    
    # Not there yet: Disregard every entry including and before the middle_index.
    elif checked_date < target_date_compare:
        discard = list(range(index_array.min(), middle_index + 1))
        vitalsdb.drop(discard, inplace=True)
        return search_vitals(vitalsdb, target_date, date_only)
    
    # Found
    else:
        return middle_index
    
    # Returning an array of all checked indices is a complicated nightmare: returning directly results in tuples within tuples;
    # appending to an outside array introduces too many moving parts.
    # Think carefully about the arguments that the function should take, and be clear about the data types involved.


# Having separate parameters for start and end indices is better than a single (start, end) list. More straightforward.
def search_vitals_2(vitalsdb: pd.DataFrame, target_date: pd.Timestamp, date_only: bool=True, start_index: int=None, end_index: int=None, index_array: np.ndarray=None) -> int:
    """Find a record in the DataFrame with the desired date using a binary search algorithm, implemented recursively. DataFrame is not sliced.
    
    Implementation:
        1. If there are no more records left in the DataFrame, raise an exception.
        2. The date/datetime of the middle index is compared to the target_date/datetime.
            a. If the middle index is dated later, everything that comes after it is disregarded,
               and the algorithm is repeated with the truncated DataFrame.
            b. If the middle index is dated earlier, everything that comes before it is disregarded,
               and the algorithm is repeated with the truncated DataFrame.
            c. If the middle index is dated to the target_date/datetime, a match is found, and the middle index is returned.
    
    Args:
        vitalsdb            : The DataFrame being searched. This doesn't need to be a copy, as the DataFrame is not sliced.
        target_date         : The date/datetime to be matched.
        date_only (optional): Indicates if only the date should be matched, or the full datetime. Defaults to True
        start_index         : The first index to be checked. Defaults to None.
        end_index           : The last index to be checked. Defaults to None.
        index_array         : The index of the DataFrame. Defaults to None.
               
    Raises:
        KeyError      : If there are no matches but no more records to be checked.
        RecursionError: If no matches are produced after 1000 calls (extremely unlikely for a match to be found). Only occurs if there are >2^1000 records.
    
    Returns:
        The index of the first record found by the algorithm.
    """

    if index_array is None:
        index_array: np.ndarray = vitalsdb.index.to_numpy()
    
    if not start_index:
        start_index = index_array.min()
    
    if not end_index:
        end_index = index_array.max()
    
    # This scenario arises after the start and end indices are equal (only 1 record left to be checked) but there's no match.
    # Alternatively, it arises from a call error.
    # Must raise an exception, or else checking will go on forever as we're not slicing the DataFrame this time.
    # KeyError won't be raised by the interpreter.
    # Note however that this is a matter of efficiency, as this scenario will still trigger a RecursionError after 1000 iterations,
    # which we've already taken care of.
    if start_index > end_index:
        raise KeyError("Record not found.")
    
    middle_index = int((start_index + end_index) / 2)
    
    checked_date: pd.Timestamp = vitalsdb.at[middle_index, "datetime"]
    target_date_compare: pd.Timestamp = target_date
    
    if date_only:
        checked_date: date = checked_date.date()
        target_date_compare: date= target_date.date()
    
    # Overshot: Disregard every entry including and after the middle_index.
    if checked_date > target_date_compare:
        return search_vitals_2(vitalsdb, target_date, date_only, start_index=start_index, end_index=(middle_index - 1), index_array=index_array)
    
    # Not there yet: Disregard every entry including and before the middle_index.
    elif checked_date < target_date_compare:
        return search_vitals_2(vitalsdb, target_date, date_only, start_index=(middle_index + 1), end_index=end_index, index_array=index_array)
    
    # Found
    else:
        return middle_index


# FIXME: Seem to keep running into empty slices.
# https://pandas.pydata.org/docs/user_guide/indexing.html
# https://www.dataquest.io/blog/settingwithcopywarning/
def search_vitals_3(vitalsdb: pd.DataFrame, target_date: pd.Timestamp, date_only: bool=True) -> int:
    """Find a record in the DataFrame with the desired date using a binary search algorithm, implemented recursively. DataFrame is sliced.
    
    Implementation:
        1. If there are no more records left in the DataFrame, raise an exception.
        2. The date/datetime of the middle index is compared to the target_date/datetime.
            a. If the middle index is dated later, everything that comes after it is discarded,
               and the algorithm is repeated with the truncated DataFrame.
            b. If the middle index is dated earlier, everything that comes before it is discarded,
               and the algorithm is repeated with the truncated DataFrame.
            c. If the middle index is dated to the target_date/datetime, a match is found, and the middle index is returned.
    
    Args:
        vitalsdb            : The DataFrame being searched. Must be a copy when first called. (Previously, this function  
                              performs the copying. However, this is memory intensive as copying takes place after every recursion.)
        target_date         : The date/datetime to be matched.
        date_only (optional): Indicates if only the date should be matched, or the full datetime. Defaults to True.
               
    Raises:
        KeyError      : If the DataFrame cannot be sliced further (no matches can possibly be found).
        RecursionError: If no matches are produced after 1000 calls (extremely unlikely for a match to be found). Only occurs if there are >2^1000 records.
    
    Returns:
        The index of the first record found by the algorithm.
    """
    
    index_array: np.ndarray = vitalsdb.index.to_numpy()
    
    if index_array.size == 0:
        raise KeyError("Record not found.")
    
    middle_index = int(np.median(index_array))
    
    checked_date: pd.Timestamp = vitalsdb.at[middle_index, "datetime"]
    target_date_compare: pd.Timestamp = target_date
    
    if date_only:
        checked_date: date = checked_date.date()
        target_date_compare: date= target_date.date()
    
    # Overshot: Disregard every entry including and after the middle_index.
    if checked_date > target_date_compare:
        # No need to use iloc.
        return search_vitals_3(vitalsdb[:middle_index], target_date, date_only)
    
    # Not there yet: Disregard every entry including and before the middle_index.
    elif checked_date < target_date_compare:
        return search_vitals_3(vitalsdb[middle_index + 1:], target_date, date_only)
    
    # Found
    else:
        return middle_index


# Non-default arguments must come before defaults.
def crawler(vitalsdb: pd.DataFrame, current_index: int, search_downwards: bool=True, mode: str="d") -> int:
    """Find all records before/after the record found with search_vitals from the same month/day (implemented recursively).
    
    Implementation:
        1. If there are no records before/after the record found, its index is returned.
        2. Check the adjacent record.
            a. If it is from the same month/day, the algorithm is repeated with it as the index to compare.
            b. If it is not from the same month/day, the current index is returned.
    
        Thus, the index returned belongs to the farthest record before/after the target record from the same month/day.
        Repeating with search_downwards set to the opposite gives the range of indices from the same month/day.

    Args:
        vitalsdb: The full DataFrame being searched.
        current_index: The index of the first record to be compared.
        search_downwards (optional): Indicates whether records before or after the target record should be searched. Defaults to True.
        mode (optional): Indicates whether the day or month should be compared. Defaults to "d".

    Raises:
        ValueError: If the caller does not provide a valid mode.
        
    Returns:
        The index of the farthest record before/after the target record from the same month/day.
    """
    
    if search_downwards:
        next_index = current_index + 1
        # The size of a DataFrame is the total number of elements, not the number of rows.
        if next_index == vitalsdb.index.size:
            return current_index
        
    else:
        next_index = current_index - 1
        if next_index == -1:
            return current_index
    
    # Alt: mode == "day" or mode == "d"; be careful: if the second condition is just "d", it will be interpreted as True.
    if mode in ["day", "d"]:    
        current_entry = vitalsdb.at[current_index, "datetime"].date()  # Already Timestamps.
        next_entry = vitalsdb.at[next_index, "datetime"].date()
        
    elif mode in ["month", "m"]:
        # Distinguish between attributes and methods; know you need to call.
        # date and time need to be called; year, month, and day do not.
        current_entry = vitalsdb.at[current_index, "datetime"].month
        next_entry = vitalsdb.at[next_index, "datetime"].month
    
    else:
        raise ValueError("Invalid mode provided.")
    
    if current_entry == next_entry:
        return crawler(vitalsdb, next_index, search_downwards, mode)
    
    else:
        return current_index


def get_index_record(vitalsdb: pd.DataFrame, message: str) -> tuple[int, pd.Series]:
    """Get a date from the user, then get the user to pick a record from the all the records from the same day found.
    
    Args:
        vitalsdb: The full DataFrame to be searched.
        message: The action to be taken with the record selected.

    Returns:
        The index of the record selected, and the Pandas Series of the record.
    """
    
    target_date: pd.Timestamp = Input.get_datetime()
    start_1 = perf_counter()
    target: int = search_vitals_2(vitalsdb, target_date)
    end_1 = perf_counter()
    
    start_2 = perf_counter()
    start_index = crawler(vitalsdb, target, False)
    end_index =  crawler(vitalsdb, target)
        
    if start_index == end_index:
        selected_indices = [target]
        
    else:
        selected_indices = list(range(start_index, end_index + 1))
    end_2 = perf_counter()
    
    # No need to transpose, even if length is 1. Providing indices as a list solves the problem.
    selected_data = pd.DataFrame(vitalsdb.loc[selected_indices])
    utility.clear_screen()
    print(f"These are the entries for {target_date.date()}:\n", selected_data.to_string(), f"{end_1 - start_1:.5f} seconds to search.", f"{end_2 - start_2:.5f} seconds to crawl.", sep="\n")
    
    while True:
        try:
            selected_index = int(input(f"\nEnter the index of the record you want to {message} (number in the left-most column): "))
            if selected_index in selected_data.index:
                break
            else:
                raise ValueError("Invalid index.")
                
        except ValueError:
            utility.display("Please enter one of the indices shown above.")
        
    selected_record = selected_data.loc[selected_index]
    
    utility.clear_screen()
    print(f"This is the existing record for {selected_record.at['datetime']}:\n", selected_record, sep="\n")
        
    return selected_index, selected_record


def add_vitals(vitalsdb: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    """Add a record to the DataFrame.

    Args:
        vitalsdb: The DataFrame containing all vitals records, held in RAM.

    Raises:
        DuplicateError: If a record from the same datetime already exists.

    Returns:
        The updated DataFrame and a success/failure message to the user.
    """
    
    backup = vitalsdb.copy(deep=True)
    
    target_datetime: pd.Timestamp = Input.get_datetime(True, True)
    
    try:
        search_vitals_2(vitalsdb, target_datetime, False)
    
    # An entry cannot be found.
    except (RecursionError, KeyError):
        pass
    
    else:
        raise utility.DuplicateError(target_datetime, "myVitals")
    
    utility.clear_and_display(f"A record for {target_datetime} will be created.")
    
    while True:
        try:
            print(f"Please enter the details for {target_datetime}:")
            
            # Be careful with array shapes when creating DataFrames. If using all scalar values, you must pass an index.
            # Alt: Use dicts of singleton arrays to create single-row DataFrames.
            record = {
                "datetime": target_datetime,
                "sys": Input.get_bp("sys"),
                "dia": Input.get_bp("dia"),
                "pulse": Input.get_pulse(),
                "glucose": Input.get_glucose(),
            }
            
            # pd.NA has no boolean value; any operations on it will return itself.
            # Empty strings are interpreted as "objects" by the DF constructor. Use pd.NA to avoid data type conflicts with the other values.
            # Note that all numerical datatypes are float64.
            if all([isinstance(record[detail], pd.NA) for detail in record if detail != "datetime"]):  # Don't mix up keys and values.
                raise ValueError("All empty.")
            
            new_row = pd.DataFrame(record, index=[0])
            # Merge is used for SQL-style joining.
            new_vitalsdb = pd.concat([vitalsdb, new_row], ignore_index=True)
            new_vitalsdb.sort_values("datetime", inplace=True, ignore_index=True)

            return new_vitalsdb, f"The record for {target_datetime} has been successfully added. Returning to myVitals..."
            
        except ValueError:
            utility.clear_and_display("A valid record must contain at least one detail. Please try again.")
        
        except KeyboardInterrupt:
            return backup, "\nAction disrupted. No changes will be made. Returning to myVitals..."


def edit_vitals(vitalsdb: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    """Edit a record in the DataFrame.

    Args:
        vitalsdb: The DataFrame containing all vitals records, held in RAM.

    Returns:
        The updated DataFrame and a success/failure message to the user.
    """
    
    if vitalsdb.empty:
        return vitalsdb, "No records for editing."
    
    else:
        backup = vitalsdb.copy(deep=True)
        working_copy = vitalsdb.copy(deep=True)
        
        try:
            index_to_edit, record_to_edit = get_index_record(vitalsdb, "edit")
            
            while True:
                try:
                    if utility.yes_or_no(f"Do you want to change the date? "):
                        existing_time: time = record_to_edit.at["datetime"].time()
                        new_date: date = Input.get_datetime().date()
                        working_copy.at[index_to_edit, "datetime"] = pd.Timestamp.combine(new_date, existing_time)
                    
                    if utility.yes_or_no(f"Do you want to change the time? "):
                        existing_date: date = record_to_edit.at["datetime"].date()
                        new_time: time = Input.get_datetime(False, True).time()
                        working_copy.at[index_to_edit, "datetime"] = pd.Timestamp.combine(existing_date, new_time)

                    if utility.yes_or_no(f"Do you want to change the systolic blood pressure? "):
                        working_copy.at[index_to_edit, "sys"] = Input.get_bp("sys")
                    
                    if utility.yes_or_no(f"Do you want to change the diastolic blood pressure? "):
                        working_copy.at[index_to_edit, "dia"] = Input.get_bp("dia")
                        
                    if utility.yes_or_no(f"Do you want to change the pulse rate? "):
                        working_copy.at[index_to_edit, "pulse"] = Input.get_pulse()
                    
                    if utility.yes_or_no(f"Do you want to change the blood glucose level? "):
                        working_copy.at[index_to_edit, "glucose"] = Input.get_glucose()
                
                    if all ([
                        isinstance(detail, pd.NA) for detail in working_copy.loc[
                            index_to_edit, ["sys", "dia", "pulse", "glucose"]
                        ]
                    ]):
                        raise ValueError("All empty.")
                    
                    working_copy.sort_values("datetime", inplace=True, ignore_index=True)
                    break
                        
                except ValueError:
                    utility.clear_and_display("A valid record must contain at least one entry. Please try again.")

        except KeyboardInterrupt:
            return backup, "\nAction disrupted. No changes will be made. Returning to myVitals..."
        
        except (KeyError, RecursionError):
            return backup, "\nNo record can be found for editing. Returning to myVitals..."
        
        else:
            return working_copy, f"The record for {record_to_edit.at['datetime']} has been successfully edited. Returning to myVitals..."


def remove_vitals(vitalsdb: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    """Remove a record from the DataFrame.

    Args:
        vitalsdb: The DataFrame containing all vitals records, held in RAM.

    Returns:
        The updated DataFrame and a success/failure message to the user.
    """
    
    if vitalsdb.empty:
        return vitalsdb, "No records for removing."
    
    else:
        backup = vitalsdb.copy(deep=True)
        working_copy = vitalsdb.copy(deep=True)
        
        try:
            index_to_remove, record_to_remove = get_index_record(vitalsdb, "remove")
                
            if utility.yes_or_no(f"Are you sure you want to remove the record for {record_to_remove.at['datetime']}? "):
                working_copy.drop(index_to_remove, inplace=True)
                working_copy.sort_values("datetime", inplace=True, ignore_index=True)
                
                return working_copy, f"The record for {record_to_remove.at['datetime']} has been successfully deleted. Returning to myVitals..."
            
            else:
                return backup, f"The record for {record_to_remove.at['datetime']} will not be removed. No changes will be made. Returning to myVitals..."
        
        except KeyboardInterrupt:
            return backup, "\nAction disrupted. No changes will be made. Returning to myVitals..."
        
        except (KeyError, RecursionError):
            return backup, "\nNo record can be found for removal. Returning to myVitals..."


class Input:
    """Provides helper functions for soliciting and validating user input.
    
    Static Methods:
        get_datetime    : Get a valid date/datetime/time from the user.
        get_bp          : Get a valid blood pressure from the user.
        get_pulse       : Get a valid pulse rate from the user.
        get_glucose     : Get a valid blood glucose level from the user.
    """
    
    @staticmethod
    def get_datetime(date: bool=True, time: bool=False) -> pd.Timestamp:
        """Get a valid date/datetime/time from the user.

        Args:
            date (optional): Whether a date should be obtained. Defaults to True.
            time (optional): _description_. Defaults to False.

        Raises:
            ValueError: If the caller does not ask for at least a date or time to be solicited.

        Returns:
            A Timestamp/datetime object.
        """
        
        if not (date or time):
            raise ValueError("The function should get at least a date or time.")
        
        if date:
            while True:
                try:
                    year_entered = input("Enter the year in YYYY format: ").strip()
                    year_regex = r"20(?:\d){2}"
                    if year := re.fullmatch(year_regex, year_entered):
                        year = int(year.group())
                        break
                    else:
                        raise ValueError("Invalid year.")
                        
                except ValueError:
                    utility.display("Please enter a valid year.")
                
            while True:
                try:
                    month_entered = input("Enter the month in MM / M format: ").strip()
                    month_regex = r"0?[1-9]|1[0-2]"
                    if month := re.fullmatch(month_regex, month_entered):
                        month = int(month.group())
                        break
                    else:
                        raise ValueError("Invalid month.")
                        
                except ValueError:
                    utility.display("Please enter a valid month.")
                
            while True:
                try:
                    day_entered = input("Enter the day in DD / D format: ").strip()
                    day_regex = r"0?[1-9]|[12]\d|3[01]"
                    if day := re.fullmatch(day_regex, day_entered):
                        day = int(day.group())
                        break
                    else:
                        raise ValueError("Invalid day.")
                        
                except ValueError:
                    utility.display("Please enter a valid day.")
        
        else:
            now = datetime.today()
            year, month, day = now.year, now.month, now.day
            
        if time:
            while True:
                try:
                    time_entered = input("Enter the time in the HH:MM / H:MM 24-hour format: ").strip()
                    time_regex = r"(?P<hour>0?[1-9]|1\d|2[0-3]):(?P<minute>[0-5][0-9])"
                        
                    if match := re.fullmatch(time_regex, time_entered):
                        hour = int(match.group("hour"))
                        minute = int(match.group("minute"))
                        break
                        
                    else:
                        raise ValueError("Invalid time.")
                        
                except ValueError:
                    utility.display("Please enter a valid time.")
                    
        else:
            hour, minute = 0, 0
            
        try:
            return pd.Timestamp(year, month, day, hour, minute)
            
        except ValueError: 
            utility.clear_and_display("Invalid date. Please try again.")
    
    @staticmethod
    def get_bp(mode: str) -> int:
        """Get a valid blood pressure from the user.

        Args:
            mode: Indicates whether the systolic or diatolic blood pressure is being solicited.

        Raises:
            ValueError: If an invalid mode is provided.

        Returns:
            The blood pressure as an integer.
        """
        
        if mode == "sys":
            mode = "systolic"
        elif mode == "dia":
            mode = "diastolic"
        else:
            raise ValueError("Invalid mode.")
        
        while True:
            bp = input(f"What's the {mode} blood pressure in mmHg (Press enter to skip)? ")
            
            try:
                if bp:
                    bp = int(bp)
                    if not (20 < bp < 300):
                        raise ValueError("Invalid blood pressure.")
                else:
                    bp = pd.NA
                    
            except ValueError:
                utility.display("Please enter a valid blood pressure.")
            
            else:
                return bp

    @staticmethod
    def get_pulse() -> int:
        """Get a valid pulse rate from the user.

        Returns:
            The pulse rate as an integer.
        """
        
        while True:
            pulse = input(f"What's the pulse rate (Press enter to skip)? ")
            
            try:
                if pulse:
                    pulse = int(pulse)
                    if not (10 < pulse < 200):
                        raise ValueError("Invalid pulse rate.")
                else:
                    pulse = pd.NA
                    
            except ValueError:
                utility.display("Please enter a valid pulse rate.")
            
            else:
                return pulse

    @staticmethod
    def get_glucose() -> float:
        """Get a valid blood glucose level from the user.

        Returns:
            The blood glucose level as a float.
        """
        
        while True:
            glucose = input(f"What's the glucose level (Press enter to skip)? ")
            
            try:
                if glucose:
                    glucose = round(float(glucose), 1)
                    if not (0 < glucose < 30):
                        raise ValueError("Invalid glucose level.")
                else:
                    glucose = pd.NA
                    
            except ValueError:
                utility.display("Please enter a valid glucose level.")
            
            else:
                return glucose


class NoSelectionError (Exception):
    """Raise an exception if the user chooses not to proceed with an action.

    Attributes:
        msg (str): The error message to displayed.
    """
    
    def __init__(self, destination: str) -> None:
        """Instantiate a NoSelectionError exception.

        Args:
            destination: The name of the menu where the user will be redirected to.
        """
        
        self.msg = f"No selection made. Returning to {destination}..."