import pandas as pd
import json
import os


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


def get_df(src_path: str, out_path: str):
    if os.path.isfile(out_path):
        os.remove(out_path)
    with open(out_path, "a+") as out:
        out.write("elevatorCall,time,src,dest,status,ele\n")  # To make it easier.
        with open(src_path, "r") as src:
            data = src.read()
        out.write(data)
    df = pd.read_csv(out_path, usecols=["time", "src", "dest", "ele"])
    return df


def building(path: str):
    with open(path, "r") as j_file:
        j = json.load(j_file)
        return Building(**j)


def elements_parser(building_path: str, calls_path: str, output_path: str):
    b = building(building_path)
    df = get_df(calls_path, output_path)
    # To fix:
    if df['src'].min() < b.minFloor or df['dest'].min() < b.minFloor or df['src'].max() > b.maxFloor or df['dest'].max() > b.maxFloor:
        raise ValueError("There is a call out of range")
    return b, df


basePath = r"/Users/ofirrubin/OOP_2021/Assignments/Ex1/data/Ex1_input/"
OUTPUT_PATH = os.path.join(basePath, r"Ex1_Calls", r"out.csv")
BUILDING_PATH = os.path.join(basePath, r"Ex1_Buildings", r"B5.json")
CALLS_PATH = os.path.join(basePath, r"Ex1_Calls", r"Calls_d.csv")


if __name__ == "__main__":
    try:
        elements_parser(building_path=BUILDING_PATH, calls_path=CALLS_PATH, output_path=OUTPUT_PATH)
    except ValueError as e:
        print("An error occured: ", e)
        exit(-1)
