# Anomaly Detection and Gap Filling System
This system is a machine learning system for outlier detection and gap filling on uni variate and multi variate time-series data. This system provides different anomaly detection algorithm and gap filling detection. User can choose the right algorithm according their needs.After anomaly detection or gap filling the result will be showed through data visualization. This system provides functions such as image export and data visualization.
## Installation
It is recommended to use python3.7.9 version

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
                        
                       
 Important!
 In the latest update, I added the pdf printing feature, but in order to use this feature, you must first install the relevant dependencies.
 You must install phantomjs, node.js and snapshot-phantomjs. Node.js is easy  to install.  snapshot-phantomjs. has been involved into requirements.txt, so it will be installed after  the operation of"pip install -r requirements.txt". Here the phantomjs download tutorial will be provided under the linux plattform.
 
 Open a terminal and udpate Apt cache first:
 ```
sudo apt-get update 
```

Then install required packages:
 ```
sudo apt-get install build-essential chrpath libssl-dev libxft-dev 
sudo apt-get install libfreetype6 libfreetype6-dev libfontconfig1 libfontconfig1-dev 
```
Now download the latest FantomJS from its official website. 
 ```
wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 
sudo tar xvjf phantomjs-2.1.1-linux-x86_64.tar.bz2 -C /usr/local/share/ 
```
Now simply create a soft link phantomjs binary file to systems bin dirctory as below:
 ```
 sudo ln -sf /usr/local/share/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin 

```
After completing installation, let’s verify the installed version of phantomjs.
 ```
phantomjs --version 
```
If the version number appears, the download was successful.
 
