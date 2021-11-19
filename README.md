# OOP-Ex1
OOP 2021 - Assignment 1

Elevator Simulator

Abstract:
At first I thought I should simulate possibilities using the online algorithm, but in a second thought
I figured it's the same exact problem we learned at the Algorithms course:
A greedy algorithm named Greedy Activity Selector which is as described here:
![](https://github.com/ofirrubin/OOP-Ex1/blob/c3976cbeb03e73e40c55e2f902c860d0b5a399a7/Media/activity%20selection%20algorithm.png) 
Then I had to think of a way of parallel calls, which I chose to solve by looking at the elevator usage at each period of time.

How to run;
Please make sure you have the packages described at requirements.txt,
you might install them by the following command with pip:
`pip install -r requirements.txt`

**The program was tested using python 3.9 ONLY**

Then you can run single file and case using the following syntax:
**Use the script name instead of `<ProgName>.py`**


`python <ProgName>.py <Building.json> <Calls.csv> <Out.csv>`
For additional help you might use the following command:
`python <ProgName>.py`
