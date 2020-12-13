# Auto_Navigation_Vehicle

This code is specially written for Raspberry Pi 3 Model B. But can be customised for any raspberry pi model by changing the GPIO pin configurations used in the code according to the model of Pi you are using. GPS can be added Furthermore to make the system more reliable, efficient and robust and to check for the correctness of path and locations. Features like image processing and obstacle avoidance are to be added further.

## Usage:

You will be able to call your Vehicle anywhere you want via the Internet if you are out somewhere and in need and even can ask it to take you anywhere you want with a simple user application which could a web-application or an android/ios/iPhone app. Here you will find two codes one which will be a third party system and could be controlled by any kind of application-specific to any device and second to control (Vehicle/Drones) with the help of a Raspberry Pi.

## Requirements:

1. Python 3 or later 
2. Paramiko installed " pip3 install paramiko " command on cmd to install the library
3. A weaved or remote3.it accounts it's free for a limited number of devices control and can be made from the given link below.
4. A Hosting so that you can connect and maintain the database ( Here I used MySql) for the instructions to be given for navigation.
5. Some other necessary supporting libraries.

Install  [Python](https://www.python.org/downloads/) . Do install Python3 or later.

if facing difficulty in installing libraries here is the link for the HELP:

1. [Paramiko](http://www.paramiko.org/)

2. [WEAVED](https://www.remot3.it/web/)

> Do note down the userName and password of the weaved account that you made. We will need this in code.

> Do modify the source code according to the device you are using to measure the distance travelled by Vehicle/Drone eg for an Odometer you need to improve code accordingly. I have used Reed switch to measure the distance travelled so I have coded accordingly. 

## Instructions and Setup Environment:

- Raspberry Pi should be properly configured as per the instructions that are given in the weaved. Instructions(http://forum.weaved.com/t/how-to-get-started-with-remot3-it-for-pi/1029/6)
- Raspberry should have the codes named Navigationpi.py and initial_check.py at a particular location.
- The Auto_Navigation_Vehicle.py should be checked and edited manually for changing source and destination by a valid source and destination as same as that coming on Google maps which are to be automated for the actual application so that these fields get updated by an app or some application by some valid possible coordinates to find the perfect path.
- The location of Navigationpi.py on Pi is to be updated in Auto_Navigation_Vehicle.
- Check the Database connectivity of the database you are using after changing the credentials for connectivity in the main code.
- Check Device containing Auto_Navigation_Vehicle.py and pi is all connected to some public network.
- Change the credentials for the Weaved account (If you do not have a weaved account create that).
- Do verify various locations and name of files mentioned in the source code.
- You need to only run Auto_Navigation_Vehicle.py manually and rest of the code will run automatically on pi if all of the systems is Online.
- You can verify the path as the whole of the path that vehicle will follow will be printed before the Vehicle/Drone start's moving.

## Run:

```
  python Auto_Navigation_Vehicle.py
```
