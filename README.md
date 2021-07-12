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
Currently this system can run univariate data and multivariate data, but for univariate data, it can only accept sensor type: "KLT12_flowRate1 (l/min)", "IT Power Consumption (W)", "Outside Temperature (°C)",
               "KLT11_pumpSpeed_p1 (Hz)",
               "KLT11_Fan1Speed_HZ (Hz)",
               "KLT13_inletTempBeforeHydraulicGate (°C)", 
for the multivariate data, it can accept: "KLT14_pumpSpeed_p1" and "KLT14_pumpSpeed_p2", "KLT14_Fan1Speed_HZ" and  "KLT14_Fan2Speed_HZ".
