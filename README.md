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
Currently this system can run univariate data and multivariate data, but for univariate data, it can only accept sensor type: "KLT11_flowRate1",
                  "KLT12_flowRate1",
                  "KLT13_flowRate1",
                  "KLT14_flowRate1",
                  "KLT11_flowRate2",
                  "KLT12_flowRate2",
                  "KLT13_flowRate2",
                  "KLT14_flowRate2",
                  "IT Power Consumption (W)",
                  "Outside Temperature (°C)",
                  "KLT11_pumpSpeed_p1",
                  "KLT12_pumpSpeed_p1",
                  "KLT13_pumpSpeed_p1",
                  "KLT14_pumpSpeed_p1",
                  "KLT11_pumpSpeed_p2",
                  "KLT12_pumpSpeed_p2",
                  "KLT13_pumpSpeed_p2",
                  "KLT14_pumpSpeed_p2",
                  "KLT11_Fan1Speed_HZ",
                  "KLT12_Fan1Speed_HZ",
                  "KLT13_Fan1Speed_HZ",
                  "KLT14_Fan1Speed_HZ",
                  "KLT11_Fan2Speed_HZ",
                  "KLT12_Fan2Speed_HZ",
                  "KLT13_Fan2Speed_HZ",
                  "KLT14_Fan2Speed_HZ",
                  "KLT13_inletTempBeforeHydraulicGate",
                  "KLT11_inletTempBeforeHydraulicGate",
                  "KLT12_inletTempBeforeHydraulicGate",
                  "KLT14_inletTempBeforeHydraulicGate",
                  "wetBulb",
                  "dryBulb",
                  "P_WW", 
for the multivariate data, it can accept the combination: "KLT11_pumpSpeed_p1 and KLT11_pumpSpeed_p2",
                        "KLT12_pumpSpeed_p1 and KLT12_pumpSpeed_p2",
                        "KLT13_pumpSpeed_p1 and KLT13_pumpSpeed_p2",
                        "KLT14_pumpSpeed_p1 and KLT14_pumpSpeed_p2",
                        "KLT11_Fan1Speed_HZ and KLT11_Fan2Speed_HZ",
                        "KLT12_Fan1Speed_HZ and KLT12_Fan2Speed_HZ",
                        "KLT13_Fan1Speed_HZ and KLT13_Fan2Speed_HZ",
                        "KLT14_Fan1Speed_HZ and KLT14_Fan2Speed_HZ".
