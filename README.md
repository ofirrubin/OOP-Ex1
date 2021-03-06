# OOP-Ex1
OOP 2021 - Assignment 1

# Elevator Selection Algorithm

## Abstract:
At first I thought I should simulate possibilities using the online algorithm, but in a second thought
I figured it's the same exact problem we learned at the Algorithms course:
A greedy algorithm named Greedy Activity Selector.
Then I had to think of a way of parallel calls, which I chose to solve by looking at the elevator usage at each period of time.

## How to run;
Please make sure you have the packages described at requirements.txt,
you might install them by the following command with pip:


`pip install -r requirements.txt`

**The program was tested using python 3.9 ONLY**

Then you can run single file and case using the following syntax:


**Use the script name instead of `<ProgName>.py`**

`python <ProgName>.py <Building.json> <Calls.csv> <Out.csv>`


For additional help you might use the following command:


`python <ProgName>.py`


## Background & Problem Solving:
At first we had Ex0 which required us to make few algorithms with the following criterias:
- It has to be an online algorithms
- There are 2 algorithms required for the task: elevator selector algorithm and elevator dispatcher algorithm.
- The algorithms must do it in the lowest avg time possible.

But in Ex0, I didn't have the time to debug and find the problems I had in my program, thus, I didn't think I should recycle the algorithm again.
Then I thought about implementing the algorithms described in Ex0 researches - mostly disk scheduling algorithms.
Later, before implementing it, I checked few algorithms and remainded of the Activity Selection Algorithm, which I learned in class.
The algorithm is a greedy algorithm which means it look for the most with the lowest resources. In this case, time.

First, I implemented the algorithm as described in the presentation here:
![](https://github.com/ofirrubin/OOP-Ex1/blob/c3976cbeb03e73e40c55e2f902c860d0b5a399a7/Media/activity%20selection%20algorithm.png) 
This is an optimal algorithm.


But this algorithm don't solve the problem entirely as we need to complete all task - not the most, so I chose to do the following:
For every elevator we are throwing all possible unassigned calls.
We check which elevator can do the most activities in addition to the activities it has already.
Then we choose the elevator with the most activities per time, only to find that we might have few calls left that can't be done in a sequence but requires to disturb the elevator direct and unparallel activities - we need another algorithm to help us choose which elevator we should disturb with the calls left.
For that reason, I used another algorithm which iterates through all elevators and find the elevator with the least usage per time in the required call time for each call left.
Explanation:
We go through each call left;
For each call left (k) we go through every elevator and sum every call assigned to the elevator (c) that in the time frame of direct pick and drop of k,
c has a call time which is the time frame start time, then we calculate for each elevator and a call the time it would take if the elevator were picking the call in time and dropping the call at dest without any stops - I call that start_time:stop_time a time frame.
We will choose the elevator with the most lowest usage at this time frame which theorethically means that we interrupt the least used elevator- by that we are lowering the avg time per call.


# Algorithm:
//First we want to make the most calls in a row, for that I'm using the Activity Selection Algorithm described above.

### Selection-Algo(unassigned calls, elevators):
Make a list of unassigned calls.


Make a variable to save the elevator that can do the most activities at the time, and the activities that can be done in that time (v1, v2 respectively).


While there are calls left:


  For each elevator:

  Run with Activity-Selection-Algorithm to find what are the activities that can be done in a row, the most at the given time.
    
    
    Note that while running Activity-Selection-Algorithm we consider the activities assigned to it already to make sure it doesn't interrupt with them, we are looking for additional activities - not in place.
      If the algorithm gave us most calls that can be done than the highest we have so far, save the elevator as the best for most and the tasks it can do at this time (v1 and v2 respectively)
      
      
  Assign the calls (v2) to elevator that can do the most (v1) and remove the calls from unassigned calls.
  
  
  If we couldn't do any additional activities return Spread-Calls(unassigned calls)

// We want to interrupt the least so find that elevator for each call
### Spread-Calls(unassigned calls, elevators):
For each call k:


  For each elevator:


(minT, minEl) => Check how much time is the elevator been used in the time frame of call k. If it is the lowest of any checked so far save the time and the elevator.


Add the call to the selected elevator and update the calls.



### Export():
For each elevator, go through her assigned activities:


For each activity update its assigned elevator in the output file.
    
  
