"""utility implements helper functions and exceptions used in the user interface.

Functions:
    clear_screen
    clear_line
    clear_screen_deco   : Decorate a function such that the screen is cleared before its execution.
    repeat              : Decorate a function such that it is executed multiple times.
    clear_5_lines
    display             : Print a line of text on the terminal window and clear it after the stipulated period.
    clear_and_display   : Clear the screen before printing a line of text for a stipulated period.
    yes_or_no           : Implement a simple command-line "yes-or-no" selector.
    backtrack           : Allow the user to press the "enter" key to return to the parent menu.
    default_response (Not in use)

Exceptions:
    DuplicateError          : Raise an exception if the user tries to create a duplicate Medicine object/vitals record.
"""

import time

def clear_screen() -> None:
    print("\033c", "\033[H", sep="", end="")


def clear_line() -> None:
    print("\033[2K", "\033[1F", "\033[0K", sep="", end="")


# TODO: @functools.wrap(func)

def clear_screen_deco(func):
    """Decorate a function such that the screen is cleared before its execution.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The decorated function.
    """
    
    def wrapper(*args, **kwargs):
        clear_screen()
        func(*args, **kwargs)
    return wrapper


def repeat(reps: int=2):
    """Decorate a function such that it is executed multiple times.

    Args:
        reps (int, optional): The number of repetitions. Defaults to 2.
    """
    def deco_repeat(func):
        # TODO: @functools.wrap(func)
        def wrapper_repeat(*args, **kwargs):
            for _ in range(reps):
                value = func(*args, **kwargs)
            return value
        return wrapper_repeat
    return deco_repeat


@repeat(5)
def clear_5_lines() -> None:
    print("\033[2K", "\033[1F", "\033[0K", sep="", end="")


def display(text, pause: int=3) -> None:
    """Print a line of text on the terminal window and clear it after the stipulated period.

    Args:
        text: The line of text to be displayed.
        pause (optional): The time to elapse before the text is cleared.
            Defaults to 3.
    """
    print(text)
    time.sleep(pause)
    print("\033[2F", "\033[0J", sep="", end="")


@clear_screen_deco
def clear_and_display(text, pause: int=3) -> None:
    """Clear the screen before printing a line of text for a stipulated period.

    Args:
        text: The line of text to be displayed.
        pause (optional): The time that will elapse before the text is cleared.
                               Defaults to 3.
    """
    print(text)
    time.sleep(pause)
    print("\033[2F", "\033[0J", sep="", end="")

    
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
                clear_line()
                return True
            case "n":
                clear_line()
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
            clear_line()

            
def default_response(default= "0") -> None:
    pass


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