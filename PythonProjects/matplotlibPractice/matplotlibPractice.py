#Use this as a reference for matplotlib

#Import modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Main Script
if __name__ == "__main__":
    #Creates arrays of values evenly spaced between the first number and second number, the third integer is how many values are to be generated
    xArray = np.linspace(0, 10, 10)
    
    #Y is a function of x where y = x^2 + 3 y = f(x)
    yArray = xArray ** 2 + 3
    
    #Z is a function of x where z = x^3 - 2*x
    zArray = xArray ** 3 - 2 * xArray

    #Simple Plot
    '''
    #Sample plot of data Takes 2 parameters which are both arrays.
    plt.plot(xArray, yArray)
    
    #Labeling
    plt.title("Sample Data Chart")
    plt.xlabel("X Values")
    plt.ylabel("Y Values")
    
    #Create Graph
    plt.show()   
    '''
    
    #Basic Subplots
    '''
    plt.subplot(2, 1, 1)
    plt.plot(xArray, yArray, 'r')
    plt.subplot(2, 1, 2)
    plt.plot(xArray, yArray, 'b')
    plt.show()
    '''
    
    #Figures
    '''
    figure_1 = plt.figure(figsize=(5, 5), dpi=100) #Dpi is the size of the window figsize is (width[inches], height[inches])
    
    axes_1 = figure_1.add_axes([0.1, 0.1, 0.8, 0.9]) #Values are between 0 and 1 and are equal to [left, bottom, width, height]
    
    #Set axis labels and title
    axes_1.set_xlabel("X-Values")
    axes_1.set_ylabel("Y-Values")
    axes_1.set_title("Sample Data Figure")
    
    #Add a plot of data, with x-data and y-data, and a label
    axes_1.plot(xArray, yArray, label="y = f(x)")
    axes_1.plot(xArray, zArray, label="z = f(x)")
    axes_1.legend(loc = 0) #0 Program finds best place 1-Upper Right 2-Upper Left 3-Lower Right 4-Lower Left
    
    #Create a second axes to put over the figure
    axes_2 = figure_1.add_axes([0.225, 0.45, 0.4, 0.3])
    axes_2.set_xlabel("X-Values")
    axes_2.set_ylabel("Y-Values")
    axes_2.set_title("Sample Data Figure")
    axes_2.plot(xArray, yArray, 'r', label="y = f(x)")
    axes_2.text(0, 75, 'Hello World!')
    
    #Create Window
    figure_1.show()
    plt.show()
    '''
    
    '''
    #Subplots and Figures
    figure_2, axes_3 = plt.subplots(figsize=(8,4), nrows=1, ncols=3)
    plt.tight_layout() #If things are overlapping this often puts the correct spacing between plots
    
    #Label and plot data for the second index figure
    axes_3[1].set_title("X V.S. Y")
    axes_3[1].set_xlabel("X")
    axes_3[1].set_ylabel("Y")
    axes_3[1].plot(xArray, yArray)
    
    #Open window
    plt.show()
    '''
    
    #Appearance Options For Plotting
    '''
    #Deafult Colors: b-blue g-green r-red c-cyan m-magenta y-yellow k-black w-white
    #Color=0.75: Num between 0-1 that affects the gray-scale I.E. 0.75 = 75% gray
    #You can also use Hex values I.E. color="eeefff"
    #More colors can be found at https://en.wikipedia.org/wiki/Web_colors
    
    #Line Styles (lw-width default value is 1, ls-line style, more styles found in line to right): https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html
    #Markers: https://matplotlib.org/stable/api/markers_api.html
    #Marker size: Size of each marker for points on the line
    #Marker face color (fill color)
    #Marker edge color (stroke/border color)
    #Marker edge width (stroke/border thickness)
    
    #Create new figure, and add axes. Plot data with cosmetic changes documented above
    figure_3 = plt.figure(figsize=(8, 4))
    axes_4 = figure_3.add_axes([0.1, 0.125, 0.8, 0.8])
    axes_4.plot(xArray, yArray, color='navy', alpha=0.75, lw=3, ls='-.', marker='o', markersize=7, markerfacecolor='y', markeredgecolor='y', markeredgewidth=4) 
    
    #Set x-axis and y-axis limits
    axes_4.set_xlim([0, 3])
    axes_4.set_ylim([0, 10])
    
    #Create background grid and colorto figure
    axes_4.grid(True, color='0.5', dashes=(5, 3, 1, 2))
    axes_4.set_facecolor("#FAEBD7")
    
    #Title and axis labels
    axes_4.set_xlabel("X-Values")
    axes_4.set_ylabel("Y-Values")
    axes_4.set_title("Sample Data Graph")
    plt.show()
    '''
    
    #Saving a figure to a file
    '''
    #Create new figure and axes, add axis labels/titles, and plot the data
    figure_4 = plt.figure(figsize=(6, 6))
    axes_5 = figure_4.add_axes([0.1, 0.1, 0.8, 0.9])
    axes_5.set_xlabel("X-Values")
    axes_5.set_ylabel("Y-Values")
    axes_5.set_title("Sample Data Graph")
    axes_5.plot(xArray, yArray, 'b')
    '''
    
    #Save figure to file For some reason if this is commented out, it doesn't work
    #figure_4.savefig(r"c:\Users\Gabe\Documents\GitHub\MyCodingWork\PythonProjects\matplotlibPractice\ExampleFigure.png")
    
    
    #Combining matplotlib with pandas why does commenting this jawn out not work?
    
    #Import data frame
    #df = pd.read_csv(r'c:\Users\Gabe\Documents\GitHub\MyCodingWork\PythonProjects\matplotlibPractice\exampleDatabase.csv')
    '''
    df = df.sort_values(by='Temperature')

    # Convert from Pandas data frame to NumPy array
    npArray = df.values

    # Get x & y values and put in array (2D matrix)
    xArray2 = npArray[:,0]
    yArray2 = npArray[:,1]

    #Create figure and axes, label title and axis, and plot data.
    figure_5 = plt.figure(figsize=(6,4))
    axes_6 = figure_5.add_axes([0.1,0.1,0.8,0.8])
    axes_6.set_title('Ice Cream Sales vs. Temperature')
    axes_6.set_xlabel('Temperature')
    axes_6.set_ylabel('Ice Cream Sales')
    axes_6.plot(xArray2, yArray2)
    
    #Add arrow on the chart
    axes_6.annotate("Best Month!", xy=(81, 543), xytext=(60, 540), arrowprops=dict(facecolor="black", shrink = 0.05))
    
    plt.bar(xArray2, yArray2)
    plt.show()
    '''
    
    #TeX Markup
    '''
    #Create sample figure
    figure_6 = plt.figure(figsize=(6,4))
    axes_7 = figure_6.add_axes([0.1,0.1,0.8,0.8])
    axes_7.set_title('Ice Cream Sales vs. Temperature')
    axes_7.set_xlabel('Temperature')
    axes_7.set_ylabel('Ice Cream Sales')
    
    # All listed plus kappa, iota, zeta, nu, rho, eta, xi, omicron, gamma, tau, phi, 
    # chi, psi, delta (Capitalize the first letter for uppercase)
    axes_7.text(0, 100, r'$\alpha \beta \sigma \omega \epsilon \mu \pi \theta \lambda$', fontsize=18)
    
    # Subscripts, multiletter superscript, sum, fractions, binomial
    axes_7.text(0, 80, r'$\delta_i \gamma^{ij} \sum_{i=0}^\infty x_i \frac{3}{4} \binom{3}{4}$', fontsize=18)
    
    # Another fraction, sqrt, cbrt, trig functions : 
    axes_7.text(0, 60, r'$\frac{8 - \frac{x}{5}}{8} \sqrt{9} \sin(\pi) \sqrt[3]{8} \acute a \div$', fontsize=18)
    axes_7.text(0, 40, r'$\bar a \hat a \tilde a \vec a \overline {a} \lim_{x \to 2} f(x) = 5$', fontsize=18)
    axes_7.text(0, 20, r'$\geq \leq \ne$', fontsize=18)
    axes_7.plot(xArray, yArray)
    
    plt.show()
    '''
    