import sys
import json
import os

import pandas as pd


class Elevator:
    def __init__(self, _id, _speed, _minFloor, _maxFloor, _closeTime, _openTime, _startTime, _stopTime):
        self.id = _id
        self.speed = _speed
        self.minFloor = _minFloor
        self.maxFloor = _maxFloor
        self.closeTime = _closeTime
        self.openTime = _openTime
        self.startTime = _startTime
        self.stopTime = _stopTime

        self.activities = {}

    def get_time(self, src, dest, stops=1):
        # Assuming src and dest are valid inputs, time calculated as described in the Google Docs
        return self.closeTime + self.startTime + (abs(dest - src) / self.speed) + self.stopTime + self.openTime

    def get_n_calls(self):
        return len(self.activities)

    def is_overlaps(self, call_a, call_b):
        # Input must be valid, existing keys
        if (call_a["time"] < call_b["time"] and call_a["directEndTime"] < call_b["directEndTime"]) or \
                (call_b["time"] < call_a["time"] and call_b["directEndTime"] < call_a["directEndTime"]):
            return True
        return False

    def greedy_activity_selector(self, calls_dict: dict):
        if len(calls_dict) == 0:
            return {}
        for call in calls_dict.values():  # Calculate direct finish time.
            call["directEndTime"] = call["time"] + self.get_time(call["src"], call["dest"])

        # We are removing calls that overlaps calls already assigned to this elevator.
        calls = {}
        for ind, new_call in calls_dict.items():
            if True in [self.is_overlaps(new_call, existing_call) for existing_call in self.activities.values()]:
                continue
            else:
                calls[ind] = new_call
        calls = calls | self.activities

        # Sort by finish time
        calls = dict(sorted(calls.items(), key=lambda item: item[1]["directEndTime"]))
        activities = {}

        first_ind = list(calls.keys())[0]
        activities[first_ind] = calls[first_ind]
        last_selected = calls[first_ind]
        # By the activity selector greedy algorithm:
        for ind, call in calls.items():
            if call["time"] >= last_selected["directEndTime"]:
                activities[ind] = call
                last_selected = call
        # We want to return ONLY the activities were added.
        activities = LiftAlgo.remove_calls(activities, self.activities)
        return activities

    def __repr__(self):
        return "Elevator(id: " + str(self.id) + " speed:" + str(self.speed) + " min:" + str(self.minFloor) + " max:" \
               + str(self.maxFloor) + " close:" + str(self.closeTime) + " open:" + str(self.openTime) \
               + " start:" + str(self.startTime) + " stop:" + str(self.stopTime) + ")"


class Building:
    def __init__(self, _minFloor, _maxFloor, _elevators):
        self.minFloor = _minFloor
        self.maxFloor = _maxFloor
        self.elevators = []
        for e in _elevators:
            ele = Elevator(**e)
            if ele.maxFloor > _maxFloor or ele.minFloor < _minFloor:
                raise ValueError("This elevator maximum / minimum is out of range.")
            else:
                self.elevators.append(ele)

    def __str__(self):
        return "Building(" + "min:" + str(self.minFloor) + ", max:" + str(self.maxFloor) + ", elevators:" \
               + self.elevators.__repr__() + ")"

    def __iter__(self):
        return self.elevators.__iter__()

    def __getitem__(self, x):
        return self.elevators[x]


class LiftAlgo:
    def __init__(self, building_path, calls_path, out_path):
        self.paths = {"building": building_path, "calls": calls_path, "out": out_path}
        self.b = None
        self.df = None

    def __set_building(self):
        with open(self.paths['building'], "r") as j_file:
            j = json.load(j_file)
            self.b = Building(**j)

    def __set_dataframe(self):
        if os.path.isfile(self.paths['out']):
            os.remove(self.paths['out'])
        with open(self.paths['out'], "a+") as out:
            out.write("elevatorCall,time,src,dest,status,ele\n")  # To make it easier.
            with open(self.paths['calls'], "r") as src:
                data = src.read()
            out.write(data)
        self.df = pd.read_csv(self.paths['out'])  # , usecols=["time", "src", "dest", "ele"]

    def set_ele(self, ind, ele_id):
        self.df.at[ind, 'ele'] = ele_id

    def __fill_all(self, ele_id):  # Fill all elevators with specific id, for single elevator use.
        for ind, val in self.df.iterrows():
            self.set_ele(ind, ele_id)

    @staticmethod
    def busy_time(ele, call):  # Returns the busy time of direct calls at call direct time
        # The function returns sum of all calls time frames within the start and finish time of a call.
        # By this we know the 'usage' of time in each call: call['time'] - call['directEndTime'] is the time it takes
        # to complete a call if it was delivered directly at the time of call, we will call it tf.
        # by looking at the tf we can look for the most unused elevator at the time, we calculate how much time is used
        # in that tf.
        calls_time = 0
        for i_call, e_call in ele.activities.items():  # The first time is a dup, I know.
            if e_call["time"] < call["time"]:
                # We want to count all calls started before and ends before this call ends.
                continue
            elif e_call["directEndTime"] < call["directEndTime"]:
                # This e_call starts after the call starts and ends before call ends.
                calls_time += e_call["directEndTime"] - e_call["time"]  # Direct Call Time
            else:
                return calls_time
        return calls_time

    def spread_calls(self, calls):
        # We know for a fact that the call with the smallest finish line was selected first thus it won't be here.
        for ind in calls:
            min_ele = self.b.elevators[0]
            min_time = -1  # Direct call time
            for ele in self.b.elevators:
                calls_time = self.busy_time(ele, calls[ind])
                if min_time == -1:
                    min_ele = ele
                    min_time = calls_time
                elif calls_time < min_time:
                    min_ele = ele
                    min_time = calls_time
            self.set_ele(ind, min_ele.id)
            for e in self.b.elevators:
                if e.id == min_ele.id:
                    e.activities = e.activities | {ind: calls[ind]}
                    break

    @staticmethod
    def remove_calls(calls, calls_to_remove):
        for key in calls_to_remove:
            if key in calls:
                del calls[key]
        return calls

    def greedy_algo(self):
        unassigned = self.df.to_dict('index')
        while len(unassigned) > 0:
            max_activities = {}
            max_ele = None
            for e in self.b.elevators:  # Find the algorithm that has the most assigned at once.
                ele_max = e.greedy_activity_selector(unassigned)
                if len(ele_max) > len(max_activities) or (len(ele_max) == len(max_activities) and
                                                          max_ele is not None and
                                                          e.get_n_calls() < max_ele.get_n_calls()):
                    max_activities = ele_max
                    max_ele = e
            if len(max_activities) == 0:
                return self.spread_calls(unassigned)
            for e in self.b.elevators:
                if e.id == max_ele.id:
                    e.activities = e.activities | max_activities
                    break
            unassigned = LiftAlgo.remove_calls(unassigned, max_activities)

    def start(self):
        # (re)load data from file
        self.__set_building()
        self.__set_dataframe()
        if self.df['src'].min() < self.b.minFloor or self.df['dest'].min() < self.b.minFloor or \
                self.df['src'].max() > self.b.maxFloor or self.df['dest'].max() > self.b.maxFloor:
            raise ValueError("There is a call out of range")
        # Create list calls
        if len(self.b.elevators) == 0:
            raise ValueError("There are no available elevators")
        elif len(self.b.elevators) == 1:
            self.__fill_all(self.b.elevators[0].id)
        else:
            self.greedy_algo()

    def export(self):
        if self.df is None:
            return
        for e in self.b.elevators:
            for ind, c in e.activities.items():
                self.set_ele(ind, e.id)
        if os.path.isfile(self.paths['out']):
            os.remove(self.paths['out'])
        self.df.to_csv(self.paths['out'], index=False, header=False)


def print_help():
    print("Lift Algorithm")
    print("Please use the following syntax:")
    print("ProgName <Building.json> <Calls.csv> <output.csv>")
    print("""Where:
     Ex1 is the program name
     <Building.json> is valid as described at the task, json file.
     <Calls.csv> is a valid csv using the columns <elevatorCall,time,src,dest,status,ele>
     where elevatorCall is str, time is int, src is int, dest is int, status is boolean int <0 = False, 1= True>
     status is ignored thus doesn't mather, ele is int>
     All inputs must be valid.
     <output.csv> is the output file and can be in any name but will be exported in the format of .csv
          """)


def main():
    args = sys.argv[1:]
    if len(args) == 0:
        print_help()
    elif len(args) != 3:
        print("Invalid syntax, use the help:")
        print_help()
    else:
        algo = LiftAlgo(args[0], args[1], args[2])
        try:
            algo.start()
            algo.export()
        except ValueError as e:
            print("An error occured: ", e)
            exit(-1)
        except FileNotFoundError as e:
            print("File not found: ", e)
            exit(-1)
        except Exception as e:
            print("Unexpected error accured, please report back with the following exception\n", e)
            exit(-1)


if __name__ == "__main__":
    main()
