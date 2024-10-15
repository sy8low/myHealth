# 🩺 myHealth

**🩺 myHealth** is a Python app that helps patients generate simple personal medical history reports for doctor's appointments.

It’s made up of two mini apps:

- **💊 myMedication**, which stores key information about the patient's medications, including their purpose, dosage, and dose times; and

- **🫀 myVitals**, which tracks the patient’s vital signs.

Click **[here](https://www.youtube.com/watch?v=v23E7wb9Ykc)** to watch a video explaining the project.

Click **[here](src/myHealth/myHealth.py)** to view the source code for **🩺 myHealth**, the main module. You can run the program with the Linux command `python myHealth.py`.

The package comes with two csv files, [myMedication.csv](src/myHealth/myMedication.csv) and [myVitals.csv](src/myHealth/myVitals.csv), which contain sample data that you can use to try out **🩺 myHealth**. If you'd like to start afresh, you can either delete the files or rename them.

Check out my **[Notion Wiki](https://tinyurl.com/myHealthNotionWiki)** to see my implementation roadmap.

## 💊 myMedication

Click **[here](src/myHealth/medication.py)** to view the source code of the `medicine` module, where **💊 myMedication** is implemented.

### Menus & Exceptions

To build menus that are interactive and easy to use, I employed extensive **exception handling** blocks to deal with invalid selections by users and guide them in navigating the menus.

- The menus in **🩺 myHealth** are **'nested'**, with layered exception handling. This means that 'lower-level' menus will handle some exceptions, and 'bubble' the rest up to 'higher-level' menus where they are handled.

  This makes it easier to redirect the user and stop certain processes when there are 'fatal errors'.

- If processes are stopped prematurely, the data may be damaged. I prevented this by making two copies of the data before every process that manipulates it (adding, editing, removing), a **working copy** and a **backup copy**.

  If the process is completed successfully, the manipulated **working copy** overrides the original; else, the **backup copy** is returned.

- To ensure that every type of invalid input is mapped to a unique exception, I defined two custom exceptions, `DuplicateError` and `NoSelectionError`.

I used **‘match-case’** blocks to redirect users to pages where they can make changes to their medications.

- The available options are displayed using the [tabulate](https://pypi.org/project/tabulate/) library.

- These pages are implemented either as functions or other menus.

### Medicine Class

I employed an **object-oriented paradigm** to represent medications in my program, by defining a `Medicine` class.

- Each medication is an **instance** of the class, but exists as a unique object.

- The details of the medications are stored as **attributes** of their corresponding objects.

- The `Medicine` class provides several handy **methods** which guide users in creating and modifying `Medicine` objects.

### File I/O

Let’s look at what happens under the hood when a user interacts with **💊 myMedication**.

When the user loads the database, a **comma-separated value (csv)** file containing information about the medications is converted into a list of `Medicine` objects with a **serialiser** I implemented with the help of Python’s `csv` module.

When the user quits the app, the `Medicine` objects are written into the csv file using another serialiser.

### Creating Medicine Objects

1. When the user adds a new medication, a **class method** of the `Medicine` class named `create` prompts the user for its details.

2. Then, it calls the special `__init__` **constructor method** in the background to create a new `Medicine` object.

### Input Validation

**💊 myMedication** carries out robust input validation using two mechanisms:

1. When a new medication is added, the `create` class method calls the **static methods** of the `Medicine` class to perform checks and re-prompt the user if necessary.

2. When a medication is edited, **setter methods** are called instead. Since the attributes of the Medicine objects are designated as **‘properties’**, they cannot be changed without passing their corresponding setter’s checks. These will raise exceptions when invalid input is detected.

> I didn’t rely on the **setters** earlier when creating new `Medicine` objects, as it would be impossible to handle multiple exceptions simultaneously and re-prompt the user in a user-friendly manner.

## 🔧 utility

Click **[here](src/myHealth/utility.py)** to view the source code of the `utility` module, where helper functions are implemented.

### Helper Functions & Decorators

To maintain a neat user interface, I used a helper function named `clear_and_display` to clear the screen whenever a new page is to be displayed.

I abstracted away the screen clearing functionality by implementing it as a **decorator**. The decorator works by treating the helper function as a **‘first-class object’**: it takes the function as an argument, and wraps it with the screen clearing functionality. This made my code more readable, and allowed the functionality to be reused.

## 🧪 test_medicine

Click **[here](test/test_medication.py)** to view the source code of the `test_medicine` module, where the unit tests for the `medicine` module are implemented.
You can run the tests with [Pytest](https://docs.pytest.org/en/8.2.x/index.html) using the Linux command `pytest test_medication.py`, or with [unittest](https://docs.python.org/3/library/unittest.html) using the Linux command `python test_medication.py`.

### Unit Testing

It is important for my app to be tested in a controlled environment where the states of the Medicine objects are certain. I achieved this using the `unittest.mock` library, which allowed me to:

- substitute real `Medicine` objects with **mock objects**, whose attributes are predetermined.

- The library also allowed me to **‘patch’**, that is simulate, real objects, functions, and modules, so that I could create **‘fixtures’**, which are predictable behaviors, side effects & return values.

- Moreover, I was able to confirm that my code worked as expected, by **‘asserting’** the number of calls made to the patched functions.

## 🫀 myVitals

Click **[here](src/myHealth/vitals.py)** to view the source code of the `vitals` module, where **🫀 myVitals** is implemented.

### File I/O

While it also stores data in a csv file, it converts the data into a **[Pandas](https://pandas.pydata.org/)** `DataFrame`. This makes it much more convenient to access the data and make changes to it than if a data type native to Python was used.

### Input Validation & Regular Expressions

**🫀 myVitals** also validates user input, but uses **regular expressions** instead of simple conditionals, which not only makes the code more concise, but also more maintainable as they can be explained by and checked with 3rd party validators such as [regexr](https://regexr.com/) and [regex101](https://regex101.com/).

### Binary Search Algorithm & Recursion

Instead of using Panda’s query function or SQL to find records from a particular day or month, I decided to experiment with implementing a **binary search algorithm recursively** using Pandas and [NumPy](https://numpy.org/doc/stable/index.html).

1. **🫀 myVitals** calls a function named `search_vitals`, which checks the record in the middle of the `DataFrame`. If it is not from the day or month desired, the algorithm disregards all the records that come either before or after it, and repeats the process.

2. Once a match is found, the `crawler` function is called. It will gather all the records from the same day or month, by checking adjacent records recursively.

### Graphing with Matplotlib

Click **[here](src/myHealth/visualisation.py)** to view the source code of the `visualisation` module, where the graphing is implemented.

To help the patient and their doctor interpret the data conveniently, I used [Matplotlib](https://matplotlib.org/stable/) to present the data as beautiful, colourful charts.

#### Blood Pressure & Pulse Rate

![BP scatter](media/BP%20scatter.png)

- I plotted **line graphs** of the patient’s blood pressure and pulse rate in the same figure but on **separate axes**, so that their trends can be compared.

- The **shaded band** indicates the patient’s pulse pressure, while the **dotted guidelines** signal whether the patient’s blood pressure and pulse rate are within healthy limits.
  These can assist doctors in diagnosing the patient’s risk of heart disease.

#### Blood Glucose Levels

I chose to present the data on the patient’s blood glucose level in two ways:

1. As a **scatterplot**, with data points colored according to a **colormap**.

   To make it easier to monitor the trend, I plotted a **line graph** of the **3-reading moving average**.

   ![Glucose scatter](media/Glucose%20scatter.png)

2. As a **histogram**, which shows the **proportion** of readings that are too high, too low, or within the healthy range.

   ![Glucose histogram](media/Glucose%20hist.png)

## Where to Find

If you’d like to download **🩺 myHealth**, you can find it on:

- [**GitHub**](https://github.com/sy8low/myHealth)
- [**Python Package Index (PYPI)**](https://pypi.org/project/myHealth/1.0/)

You can also download it through your command line using the **package installer for Python**, by executing the following Linux command:

`pip install myHealth==1.0`

The documentation for **🩺 myHealth** can be found on [ReadtheDocs](https://myhealth.readthedocs.io/en/latest/) (in development).