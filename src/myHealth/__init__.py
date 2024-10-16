"""myHealth is a Python app that helps patients generate simple personal medical history reports for doctor's appointments.

Note:
    The modules are:
    
    myHealth        : The main module which should be executed to run the programme.
    medication      : Implements myMedication, which stores key information about the patient's medications,
                      including their purpose, dosage, and dose times.
    vitals          : Implements myVitals, which tracks the patient's vital signs (blood pressure, pulse, blood glucose levels).
    utility         : Implements helper functions and exceptions used in the user interface.
    visualisation   : Graphs the patient's vitals records with beautiful, colourful charts.
"""

# Important to ensure the plotting window of Matplotlib shows up:
# 1. Create a virtual environment in myHealth_package: python3 -m venv .venv
# 2. Activate it: . .venv/bin/activate
# 3. Download all dependencies listed in requirements.txt.
# 2. Ensure tkinter is installed, though it should already be: sudo apt-get install python3-tk