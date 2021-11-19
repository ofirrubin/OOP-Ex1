import sys
import os
import subprocess


def print_help():
    print("""Please use the following syntax
    <ProgName>.py <Target>.py <BuildingsPath> <CallsPath> <OutputPath>
    Where <ProgName> is the file path of this runner
    <Target>.py is the Ex1 algorithm program - file path
    <BuildingPath> is a directory path contains all buildings .json you want to run
    <CallsPath> is a directory path contains all calls .csv you want to run
    <OutputPath> is a directory path you want to output all cases to.""")


def list_files(dir_path, ends_with):
    files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(ends_with):
                files.append(os.path.join(root, file))
    return files


def list_buildings(dir_path):
    return list_files(dir_path, '.json')


def list_calls(dir_path):
    return list_files(dir_path, '.csv')


def output_name(building_path, case_path):
    return os.path.basename(building_path) + "_" + os.path.basename(case_path)


def call_algo(algo_path, building, case, output_path):
    process = subprocess.Popen(["python3", algo_path, building, case, output_path])
    process.communicate()


def main():
    args = sys.argv[1:]
    print(len(args))
    if len(args) != 4:
        print_help()
    else:
        algo = args[0]
        buildings = list_buildings(args[1])
        calls = list_calls(args[2])
        output_path = args[3]
        for b in buildings:
            for c in calls:
                call_algo(algo, b, c, os.path.join(output_path, output_name(b, c)))


if __name__ == "__main__":
    main()
