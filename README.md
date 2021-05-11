# Anomaly Detection and Gap Filling System
This system is a machine learning system for outlier detection and gap filling on uni variate and multi variate time-series data. This system provides different anomaly detection algorithm and gap filling detection. User can choose the right algorithm according their needs.After anomaly detection or gap filling the result will be showed through data visualization. This system provides functions such as image export and data visualization.
## Installation
Create virtual environments<br>
Clone the repository:<br>
```
git clone git@github.com:Junxi917/outlier_detection.git
```
Enter into virtual environments<br>
Install locally with `pip`:
```
cd outlier_detection
pip install -r requirements.txt
```
Launch Django:
```
python3 manage.py runserver
```
## Usage
There are three files for testing.(test_pumpSpeed.xlsx, test_Temperature.xlsx and test_flowrate.xlsx)<br>
* Firstly user upload the data set and then click the button submit. 
* User can choose anomaly detection or gap filling.
## Note
Currently this system can only run univariate data, and the function of univariate data will be added later.
