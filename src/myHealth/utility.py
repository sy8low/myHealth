"""utility implements helper functions and exceptions used in the user interface.

Functions:
    repeat              : Decorate a function such that it is executed multiple times. 
    clear_lines         : Clear a specified number of lines.
    clear_screen        : Clear the entire terminal window.
    clear_screen_deco   : Decorate a function such that the screen is cleared before its execution.
    display             : Print a line of text on the terminal window and clear it after the stipulated period.
    clear_and_display   : Clear the screen before printing a line of text for a stipulated period.
    yes_or_no           : Implement a simple command-line "yes-or-no" selector.
    backtrack           : Allow the user to press the "enter" key to return to the parent menu.
    
Exceptions:
    DuplicateError          : Raise an exception if the user tries to create a duplicate Medicine object/vitals record.
"""

from functools import wraps
from time import sleep

def repeat(reps: int=2):
    """Decorate a function such that it is executed multiple times.

    Args:
        reps (optional): The number of repetitions. Defaults to 2.
    """
    
    def deco_repeat(func):
        @wraps(func)
        def wrapper_repeat(*args, **kwargs):
            for _ in range(reps):
                value = func(*args, **kwargs)
            return value
        return wrapper_repeat
    return deco_repeat


def clear_lines(lines: int=1) -> None:
    """Clear a specified number of lines.

    Args:
        lines (optional): The number of lines to be cleared. Defaults to 1.
    """
    
    @repeat(lines)
    def clear_multiple_lines() -> None:
        print("\033[2K", "\033[1F", "\033[2K", sep="", end="")
    
    clear_multiple_lines()


def clear_screen() -> None:
    """Clear the entire terminal window."""
    print("\033[2J", "\033[H", sep="", end="")
    

def clear_screen_deco(func):
    """Decorate a function such that the screen is cleared before its execution.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The decorated function.
    """
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        clear_screen()
        func(*args, **kwargs)
    return wrapper


def display(text, pause: int=3) -> None:
    """Print a line of text on the terminal window and clear it after the stipulated period.

    Args:
        text: The line of text to be displayed.
        pause (optional): The time to elapse before the text is cleared.
            Defaults to 3.
    """
        
    print(text)
    sleep(pause)
    for _ in range(2):
        print("\033[1F", "\033[2K", sep="", end="")


@clear_screen_deco
def clear_and_display(text, pause: int=3) -> None:
    """Clear the screen before printing a line of text for a stipulated period.

    Args:
        text: The line of text to be displayed.
        pause (optional): The time that will elapse before the text is cleared.
                               Defaults to 3.
    """
    
    print(text)
    sleep(pause)
    print("\033[1F", "\033[2K", sep="", end="")

    
def yes_or_no(prompt: str) -> bool:
    """Implement a simple command-line "yes-or-no" selector.

    Args:
        prompt: The instructions to be displayed.

    Returns:
        The user's choice.
    """
    
    while True:
        response = input(prompt + "(Y/N) ").lower().strip()
        match response:
            case "y":
                clear_lines()
                return True
            case "n":
                clear_lines()
                return False
            case _:
                display("Please provide a valid response.")


def backtrack(target: str) -> str:
    """Allow the user to press the "enter" key to return to the parent menu.

    Args:
        target (str): The name of the parent menu.
    
    Returns:
        str: A redirection message to the user.
    """
    
    while True:
        if not input(f"\nPress enter to return to {target}."):
            return f"Returning to {target}..."
        else:
            clear_lines()


class DuplicateError (Exception):
    """Raise an exception if the user tries to create a Medicine object with a name that is already taken.

    Attributes:
        msg (str): The error message to displayed.
    """
    
    def __init__(self, name: str, destination: str) -> None:
        """Instantiate a DuplicateError exception.

        Args:
            name: The name/datetime that is already taken.
            destination: The name of the menu where the user will be redirected to.
        """
        
        self.msg = f"A record for {name} already exists. Returning to {destination}..."