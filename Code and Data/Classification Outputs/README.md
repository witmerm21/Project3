Instructions for organizing the output data of NBC into a more useable form. Each Python script will require directories to be changed, they are located at the top of each script.

(This assumes that you already have a folder, containing all the output CSV files from NBC. For refrence, the classification output from this project is provided in the "Output CSVs" folder)

1 - Run output_averages.py, this script opens each CSV file generated for every trial run by NBC and takes the average of all the logarithmic probability values. The code ignores rows where the value is above -5, as these rows are the same row as the header for the following reads. For an unknown reason NBC classify calculates the probabilistic match for these header lines, and are thus considered bad data that needs to be excluded. The output files (output_averages.csv) gives the CSV filename and its total average value.

This CSV can then be expanded on for spreadsheet calculations. The Excel file used for this project is provided (NBC Output Stats.xlsx), where various sub-category averages were calculated. Additionally, the ROC curve and AUC value is also calculated in this spreadsheet. These ROC curves are provided in this folder as JPG files.
