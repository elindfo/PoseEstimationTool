import argparse
import csv
import json
import os
from glob import glob
from typing import Dict

from pose_data import Joint, JointName, Skeleton3D


def lifting_from_the_deep(args: argparse.Namespace) -> None:
    data = read_from_file(args)
    x, y, z = [data['3d'][0][0], data['3d'][0][1], data['3d'][0][2]]
    for rem_index in [9, 7]:
        del x[rem_index]
        del y[rem_index]
        del z[rem_index]
    joint_points = []
    for i in range(len(x)):
        joint_points.append(Joint(x[i], y[i], z[i], JointName(i)))

    skeleton = Skeleton3D(joint_points)
    skeleton.make_pelvis()
    skeleton.center_around_origo()

    write_to_file(skeleton, args)


def read_from_file(args: argparse.Namespace) -> Dict:
    file_type = os.path.splitext(args.input_file)[1]
    data = {}
    with open(args.input_file, 'r') as f:
        if file_type == '.csv':
            reader = csv.reader(f)
            next(reader, None)  # skip the headers
            for row in reader:
                data[row[0]] = row[1:]
        elif file_type == '.json':
            data = json.load(f)
    return data


def write_to_file(skeleton: Skeleton3D, args: argparse.Namespace) -> None:
    files_in_dir = len(glob(os.path.join(args.output_dir, '*.json')))
    output_file = os.path.join(args.output_dir, '{}.json'.format(files_in_dir))
    with open(output_file, 'w') as f:
        json.dump({
            'skeleton': skeleton.to_json()
        }, f)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('output_dir')
    parser.add_argument('-i', '--file_index', dest='file_index', required=False)
    return parser.parse_args()


def main(args: argparse.Namespace) -> None:
    lifting_from_the_deep(args)

if __name__ == '__main__':
    main(parse_arguments())
