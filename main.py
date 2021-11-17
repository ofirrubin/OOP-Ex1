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

        self.calls_inWay = SortedSet()
        self.calls_aWay = SortedSet()
        self.last_call = None

    def add_call(self):
        pass

    def hyp_add(self):
        pass

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


class Lift:
    def __init__(self, ele: Elevator):
        self.ele = ele
        self.in_way = SortedSet()
        self.an_way = SortedSet()

    # def add_call(self, call: Call):


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

    def start(self):
        # (re)load data from file
        self.__set_building()
        self.__set_dataframe()

        if self.df['src'].min() < self.b.minFloor or self.df['dest'].min() < self.b.minFloor or\
           self.df['src'].max() > self.b.maxFloor or self.df['dest'].max() > self.b.maxFloor:
            raise ValueError("There is a call out of range")
        # Create list calls

        # Sort all calls in call order

        # Update dataframe selected elevator for each call

        #
        pass

    def export(self):
        if self.df is None:
            return
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
