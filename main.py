import argparse
import json
import os

import pandas as pd
from sortedcontainers import SortedSet

basePath = r"/Users/ofirrubin/OOP_2021/Assignments/Ex1/data/Ex1_input/"
OUTPUT_PATH = os.path.join(basePath, r"Ex1_Calls", r"out.csv")
BUILDING_PATH = os.path.join(basePath, r"Ex1_Buildings", r"B5.json")
CALLS_PATH = os.path.join(basePath, r"Ex1_Calls", r"Calls_d.csv")


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
        for ind, call in calls.items():
            activities[ind] = call
            last_selected = calls[ind]
            break
        for ind, call in calls.items():
            if call["time"] >= last_selected["directEndTime"]:
                activities[ind] = call
                last_selected = call
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
    def __remove_calls(calls, calls_to_remove):
        for key in calls_to_remove:
            if key in calls:
                del calls[key]
        return calls

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
            max_activities = []
            max_ele = None
            unassigned = self.df.to_dict('index')

            while len(unassigned) > 0:
                for e in self.b.elevators:
                    ele_max = e.greedy_activity_selector(unassigned)
                    if len(ele_max) > len(max_activities) or (len(ele_max) == len(max_activities) and
                                                              type(max_ele) is not None and
                                                              e.get_n_calls() < max_ele.get_n_calls()):
                        max_activities = ele_max
                        max_ele = e
                for e in self.b.elevators:
                    if e.id == max_ele.id:
                        e.activities = e.activities | max_activities
                        break
                unassigned = LiftAlgo.__remove_calls(unassigned, max_activities)

    def export(self):
        if self.df is None:
            return
        for e in self.b.elevators:
            for ind, c in e.activities.items():
                self.set_ele(ind, e.id)
        if os.path.isfile(self.paths['out']):
            os.remove(self.paths['out'])
        self.df.to_csv(self.paths['out'], index=False, header=False)


def main():
    parser = argparse.ArgumentParser(description="Lift Offline Algorithm")
    parser.add_argument('-building', type=str, help="Building path")
    parser.add_argument('-calls', type=str, help="Calls path")
    parser.add_argument('-output', type=str, help="Output path")
    args = parser.parse_args()
    algo = LiftAlgo(args.building, args.calls, args.output)
    try:
        algo.start()
        algo.export()
    except ValueError as e:
        print("An error occured: ", e)
        exit(-1)
    except FileNotFoundError as e:
        print("File not found: ", e)
        exit(-1)


if __name__ == "__main__":
    main()
