import os
import argparse
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from pose_data import Skeleton3D, Joint, JOINT_CONNECTIONS
from typing import Dict, List

HEIGHT_INDEX_NAME = {
    -1: 'below',
    0: 'centered',
    1: 'above'
}


plt.rcParams.update({'font.size': 8})


def get_max(joints: List[Joint]) -> float:
    current_max = float('-inf')
    for joint in joints:
        point = joint.point
        m = max(point[0], point[1], point[2])
        if m > current_max:
            current_max = m
    return current_max


def get_min(joints: List[Joint]) -> float:
    current_min = float('inf')
    for joint in joints:
        point = joint.point
        m = min(point[0], point[1], point[2])
        if m < current_min:
            current_min = m
    return current_min


def generate_figures(args: argparse.Namespace) -> None:
    skeleton = read_from_file(args)
    max_val = get_max(skeleton.joints)
    min_val = get_min(skeleton.joints)

    fig = plt.figure()
    plt.tight_layout()

    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlim3d(min_val, max_val)
    ax.set_ylim3d(min_val, max_val)
    ax.set_zlim3d(min_val, max_val)

    x = [joint.point[0] for joint in skeleton.joints]
    y = [joint.point[1] for joint in skeleton.joints]
    z = [joint.point[2] for joint in skeleton.joints]

    np_x = np.array(x)
    np_y = np.array(y)
    np_z = np.array(z)

    for connection in JOINT_CONNECTIONS:
        ax.plot(
            [np_x[connection[0].value], np_x[connection[1].value]],
            [np_y[connection[0].value], np_y[connection[1].value]],
            'ro-',
            zs=[np_z[connection[0].value],
                np_z[connection[1].value]]
        )

    ax.scatter(x, y, z, c='r', marker='o')
    i = 1
    for height in range(-1, 2):
        for angle in range(270, 360 + 270, 45):
            ax.view_init(elev=height*30, azim=angle)
            save_image(args, height, (angle - 270))


def read_from_file(args: argparse.Namespace) -> Skeleton3D:
    skeleton = None
    with open(args.input_file, 'r') as f:
        data = json.load(f)
        skeleton = Skeleton3D.from_json(data['skeleton'])
    return skeleton


def save_image(args: argparse.Namespace, height_index: int, angle_index: int) -> None:
    file_name = '{}-{}'.format(HEIGHT_INDEX_NAME[height_index], angle_index)
    file_path = os.path.join(args.output_directory, file_name + '.png')
    plt.savefig(file_path, format='png', dpi=100)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('output_directory')
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    generate_figures(args)


if __name__ == '__main__':
    main()
