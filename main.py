import pandas as pd
import json


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


def building():
    with open("/Users/ofirrubin/OOP_2021/Assignments/Ex1/data/Ex1_input/Ex1_Buildings/B5.json", "r") as j_file:
        j = json.load(j_file)
        building = Building(**j)
        print(building)


building()
