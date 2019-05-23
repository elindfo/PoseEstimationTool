import numpy as np
from pose_data import Joint, JointName, Skeleton3D
import argparse
import json
import os


joint_angle_definitions = {
    'right_knee': (JointName.right_foot, JointName.right_knee, JointName.right_hip),
    'left_knee': (JointName.left_foot, JointName.left_knee, JointName.left_hip),

    'right_elbow': (JointName.right_hand, JointName.right_elbow, JointName.right_shoulder),
    'left_elbow': (JointName.left_hand, JointName.left_elbow, JointName.left_shoulder),

    'right_shoulder': (JointName.right_elbow, JointName.right_shoulder, JointName.neck),
    'left_shoulder': (JointName.left_elbow, JointName.left_shoulder, JointName.neck),

    'right_neck': (JointName.right_shoulder, JointName.neck, JointName.head),
    'left_neck': (JointName.left_shoulder, JointName.neck, JointName.head),

    'right_pelvis': (JointName.right_hip, JointName.pelvis, JointName.neck),
    'left_pelvis': (JointName.left_hip, JointName.pelvis, JointName.neck),

    'right_hip': (JointName.right_knee, JointName.right_hip, JointName.pelvis),
    'left_hip': (JointName.left_knee, JointName.left_hip, JointName.pelvis),
}


def unit_vector(vector: np.array) -> np.array:
    return vector / np.linalg.norm(vector)


def vector(j1: Joint, j2: Joint) -> np.array:
    return j2.point - j1.point


def angle_relative(v1: np.array, v2: np.array) -> float:
    uv1 = unit_vector(v1)
    uv2 = unit_vector(v2)
    return np.rad2deg(np.arccos(np.clip(np.dot(uv1, uv2), -1.0, 1.0)))


def calculate_angles(args: argparse.Namespace) -> None:
    with open(args.input_file, 'r') as f:
        skeleton = Skeleton3D.from_json(json.load(f)['skeleton'])

    results = {}
    for k, v in joint_angle_definitions.items():
        to_1, center, to_2 = v
        limb1 = vector(skeleton.get_joints()[center.value],
                       skeleton.get_joints()[to_1.value])
        limb2 = vector(skeleton.get_joints()[center.value],
                       skeleton.get_joints()[to_2.value])
        results[k] = angle_relative(limb1, limb2)

    input_name, _input_ext = os.path.splitext(args.input_file)
    with open(os.path.join(args.output_directory, os.path.basename(input_name) + '.json'), 'w') as f:
        json.dump(results, f)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('output_directory')
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    calculate_angles(args)

if __name__ == '__main__':
    main()
