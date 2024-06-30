"""visualisation graphs the patient's vitals records with beautiful, colourful charts.

Constants:
    GLUCOSE_COLOURS (np.array)
    BP_COLOURS (dict)

Functions:
    bp_scatter          : Create a scatterplot of the patient's systolic and diastolic blood pressure and/or pulse rate.
    glucose_scatter     : Create a scatterplot of the patient's blood glucose level.
    glucose_colourmap   : Implement a ListedColormap for use in the blood glucose level scatterplot.
    glucose_hist        : Create a histogram of the patient's blood glucose levels.
""" 

from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import utility

GLUCOSE_COLOURS = np.array([
    [0/256, 255/256, 255/256, 1],  # Turquoise
    [0/256, 204/256, 0/256, 1],  # Green
    [255/256, 255/256, 0/256, 1],  # Yellow
    [255/256, 0/256, 0/256, 1],  # Red
])  # (4, 4) array of RGBA codes.

BP_COLOURS = {
        "sys": [255/256, 0/256, 0/256, 1],  # Red.
        "dia": [0/256, 0/256, 204/256, 1],  # Blue.
        "pulse": [0/256, 204/256, 0/256, 1] # Green.
}

def bp_scatter(data: pd.DataFrame):
    """Create a scatterplot of the patient's systolic and diastolic blood pressure and/or pulse rate.
    
    Features:
        a. Title, axis labels, axis ticks, line labels.
        b. Coloured line graphs of blood pressure and pulse rate on separate axes.
        c. Shaded band between the systolic and diastolic blood pressures.
        d. Guidelines showing the healthy limits.
        e. Legends.

    Args:
        data: The filtered DataFrame.
    """
    
    # pd.DataFrames are passed by reference!
    data_copy = data.copy(deep=True)
    
    # Should be dropped in one go in the beginning, as data_copy[""] returns a static Series.
    if "sys" in data_copy.columns and "dia" in data_copy.columns:
        if "pulse" in data_copy.columns:
            data_copy.dropna(subset=["sys", "dia", "pulse"], inplace=True, how="any")
        else:
            data_copy.dropna(subset=["sys", "dia"], inplace=True, how="any")
            
    x = data_copy["datetime"]
    xmin, xmax = x.min(), x.max()
        
    fig, ax1 = plt.subplots()
    ax1.set_xlabel("Datetime")
    
    if "sys" in data_copy.columns and "dia" in data_copy.columns:           
        sys, dia = data_copy["sys"], data_copy["dia"]   
        ax1.set_ylabel("Blood Pressure (mmHg)")
        ax1.set_title(f"Chart of Blood Pressure from {xmin} to {xmax}")
        
        ax1.set_ylim(0, 300)
        ax1.tick_params("y")
        ax1.plot(x, sys, c=BP_COLOURS["sys"], scaley=True, label="Systolic")
        ax1.axhline(y=150, c=BP_COLOURS["sys"], alpha=0.5, ls="--", label="Hypertension (Systolic)")
        ax1.plot(x, dia, c=BP_COLOURS["dia"], scaley=True, label="Diastolic")
        ax1.axhline(y=90, c=BP_COLOURS["dia"], alpha=0.5, ls="--", label="Hypertension (Diastolic)")
        ax1.fill_between(x, sys, dia, color="0.8", alpha=0.5)  # The alias "c" cannot be used. Please check the docs when passing args.
        ax1.legend(loc="upper left")
        
    if "pulse" in data_copy.columns:
        pulse = data_copy["pulse"]
        ax1.set_title(f"Chart of Blood Pressure and Pulse Rate from {xmin} to {xmax}")
                
        ax2 = ax1.twinx()
        ax2.set_ylabel("Pulse Rate (BPM)")
        ax2.set_ylim(0, 200)
        ax2.tick_params("y")
        ax2.plot(x, pulse, c=BP_COLOURS["pulse"], scaley=True, label="Pulse")
        ax2.axhline(y=90, c=BP_COLOURS["pulse"], alpha=0.5, ls="--", label="Tachycardia")  # Shifted down from 100 for visibility.
        ax2.legend(loc="upper right")
        
    else:
        data_copy.dropna(subset="pulse", inplace=True)
        pulse = data_copy["pulse"]
        ax1.set_title(f"Chart of Pulse Rate from {xmin} to {xmax}")
            
        ax1.set_ylabel("Pulse Rate (BPM)")
        ax1.set_ylim(0, 200)
        ax1.tick_params("y")
        ax1.plot(x, pulse, c=BP_COLOURS["pulse"], scaley=True, label="Pulse")
        ax1.axhline(y=90, c=BP_COLOURS["pulse"], alpha=0.5, ls="--", label="Tachycardia")
        ax1.legend(loc="upper left")
            
    # If you call plt.legend() at the end, it will only plot the legend for the current axes.
        
    utility.display("Generating chart...")
    plt.show()  # The external window pauses code execution.
    plt.close(fig)


def glucose_scatter(data: pd.DataFrame):
    """Create a scatterplot of the patient's blood glucose level.

    Features:
        a. Title, axis labels, axis ticks.
        b. Scatterplot of blood glucose readings and line graph of 3-reading rolling mean.
        c. Data points coloured according to a colourmap to indicate whether they are within healthy limits.
        d. Guidelines showing the healthy limits.
        e. Colourbar.
        f. Legend.
        g. The latest 3-reading moving average.

    Args:
        data: The filtered DataFrame.
    """
    
    data_copy = data.copy(deep=True)
    data_copy.dropna(subset="glucose", inplace=True)
    x, y = data_copy["datetime"], data_copy["glucose"]
    xmin, xmax = x.min(), x.max()
        
    # Alt: forward-looking window. indexer = pd.api.indexers.FixedForwardWindowIndexer(window_size=3). Does not support "closed".
    y_roll_mean = y.rolling(window=3, min_periods=1, center=False, closed="neither").mean()
            
    plt.figure()
    plt.xlabel("Datetime")
    plt.ylabel("Blood Glucose Level (mmol/L)")
    plt.title(f"Chart of Blood Glucose Levels from {xmin} to {xmax}")
    plt.ylim(0, 30)
    plt.yticks(np.arange(0, 30, 2), np.arange(0, 30, 2))
    
    # Note: Plots can only take a single colour in its arguments (no arrays or cmaps); alternatively, set using format strings.
    plt.scatter(x, y, c=y, cmap=glucose_colourmap(GLUCOSE_COLOURS), vmin=0, vmax=30)
    plt.plot(x, y_roll_mean, "k", label="Moving average (last 3 records)")
    plt.colorbar(ticks=[0, 6, 10, 15, 30])
    plt.axhline(y=6, c="0.8", alpha=0.8, ls="--", label="Hypoglycemia")  # No such thing as glucose_colourmap.colours[1]
    plt.axhline(y=10, c="0.8", alpha=0.8, ls="--", label="Normal")
    plt.axhline(y=15, c="0.8", alpha=0.8, ls="--", label="Hyperglycemia")
        
    # Do not index into Series like when indexing into lists/arrays! Need to use at or loc. Also, negative indexing is only allowed for integer methods.
    y_roll_mean.dropna(inplace=True)
    plt.text(x=xmin, y= 28, s=f"The latest 3-reading moving average is {y_roll_mean.iat[-1]:.1f} mmol/L.")
    plt.legend()
            
    utility.display("Generating chart...")
    plt.show()
    plt.close()


def glucose_colourmap(colours: np.array) -> ListedColormap:
    """Implement a discrete ListedColormap for use in the blood glucose level scatterplot.

    Args:
        colours: The colour scheme to be used.

    Returns:
        The ListedColormap created.
    """
    
    N = 30
    mapping = np.ones((N, 4))  # (30, 4) array, containing only 1s.
    # The second colon is important (means "every individual item")! Omitting it will replace the entire slice with a single object, as opposed to one-for-one.
    mapping[:6, :] = colours[0]
    mapping[6:10, :] = colours[1]
    mapping[10:15, :] = colours[2]
    mapping[15:, :] = colours[3]
        
    return ListedColormap(mapping)


def glucose_hist(data: pd.DataFrame):
    """Create a histogram of the patient's blood glucose levels.

    Features:
        a. Title, axis labels, axis ticks.
        b. Coloured histogram of blood glucose levels, showing the proportion of readings within healthy/unhealthy ranges.
        c. Guidelines showing the healthy limits.

    Args:
        data: The filtered DataFrame.
    """
    
    data_copy = data.copy(deep=True)
    data_copy.dropna(subset="glucose", inplace=True)
    x, y = data_copy["datetime"], data_copy["glucose"]
    xmin, xmax = x.min(), x.max()
        
    plt.figure()
    plt.xlabel("Blood Glucose Level (mmol/L)")
    plt.ylabel("Percentage of Readings (%)")
    plt.title(f"Historgram of Blood Glucose Levels from {xmin} to {xmax}")
    plt.ylim(0, 1)
    plt.xlim(0, 30)
        
    values, edges = np.histogram(y, bins=[0, 6, 10, 15, 30])  # edges == np.array(bins)
    probabilities = values / values.sum()
    width = np.diff(edges)
    
    plt.bar(edges[:-1], height=probabilities,
            width=width, align="edge", color=GLUCOSE_COLOURS,
            edgecolor=(0, 0, 0, 1), linewidth=2)
        
    percentages = list(map(int, (probabilities * 100)))
        
    plt.xticks((np.diff(edges) / 2) + edges[:-1],
               [f"Below 6\n(Hypoglycemia)\n{int(percentages[0])}%",
                f"6-10 \n(Normal)\n{percentages[1]}%",
                f"10-15\n(Mild Hyperglycemia)\n{percentages[2]}%",
                f"Above 15\n(Severe Hyperglycemia)\n{percentages[3]}%"])
        
    plt.yticks(np.arange(0, 1.1, 0.1), np.arange(0, 110, 10))  # Half-closed interval!
    # Alt: Stair plot or histogram plt.hist(y, bins=[0, 6, 10, 15, 30], density=True, histtype="step")                  
        
    utility.display("Generating histogram...")
    plt.show()
    plt.close()