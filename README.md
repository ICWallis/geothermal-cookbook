# Geothermal Cookbook

Python methods for geoscientists, geochemists and reservoir engineers working in geothermal resources.

## 3D-well-plot.py

Use matplotib to generate an interactive 3D visualisation of the well path and points along that path, such as a production casing shoe or feedzone(s). A static plot (oblique, section or plan view) may also be exported.

The method requires fractoolbox, which is downloadable from https://github.com/ICWallis/fractoolbox. The fractoolbox folder and testdata-survey.csv need to located in the same folder you run 3D-well-plot.py from.  

testdata-fractures.csv and testdata-survey.csv is real anonymised data kindly provided by Contact Energy. 

## development-US-Basin-and-Range.ipynb

Analysis of installed MWe by in the US Basin and Range province based on publicly available data. 

The Juypter Notebook demonstrates sorted bar plot and histogram methods using matplotlib, as well as probably density functions using a kernel density estimation method. Statistical methods built into Pandas are also used.

You need the .csv data in the same folder you run this .ipynb from:
- development-byplant.csv
- development-byreservoir.csv
- development-byreservoir-trimmed.csv

## ternary-plots.ipynb

Ternary plots are a key tool for geothermal geochemistry. However, these plots are not included in matplotlib. This notebook demonstrates how the [ternary package](https://github.com/marcharper/python-ternary) can be used to generate a ternary plot (geothermal water type example). The ternary package needs to be installed in your environment:

> pip install python-ternary

## wellpath-calculator.ipynb

Work in progress

## License

Apache 2.0 

https://choosealicense.com/licenses/apache-2.0/

## Development

To date, this repository contains code developed by [Irene Wallis](https://www.cubicearth.nz/). 

Feedback and contributions welcome.