# Anomaly Detection and Gap Filling System
This system is a machine learning system for outlier detection and gap filling on unitvariate and multivariate time-series data. This system provides different anomaly detection algotithm and gap filling detection. User can choose the right algorithm according their needs.After anomaly detection or gap filling the result will be showed throught data visulisation.This system provides functions such as image export and data visualization.
## Installation
Clone the repository:<br>
```
git clone git@github.com:Junxi917/outlier_detection.git
```
Install locally with `pip`:
```
cd outlier_detection
pip install -r requirements.txt
```
## Usage
There are three files for testing.(test_pumpSpeed.xlsx, test_Temperature.xlsx and test_flowrate.xlsx)<br>
* Firstly user upload the data set and then click the button submit. 
* User can choose anomaly detection or gap filling.
## Note
Currently this system can only run unitvariate data, and the function of unitvariate data will be added later.
