from enum import Enum
from typing import List

import numpy as np


class JointName(Enum):
    pelvis = 0
    right_hip = 1
    right_knee = 2
    right_foot = 3
    left_hip = 4
    left_knee = 5
    left_foot = 6
    neck = 7
    head = 8
    left_shoulder = 9
    left_elbow = 10
    left_hand = 11
    right_shoulder = 12
    right_elbow = 13
    right_hand = 14


JOINT_CONNECTIONS = (
    (JointName.pelvis, JointName.right_hip),
    (JointName.right_hip, JointName.right_knee),
    (JointName.right_knee, JointName.right_foot),
    (JointName.pelvis, JointName.left_hip),
    (JointName.left_hip, JointName.left_knee),
    (JointName.left_knee, JointName.left_foot),
    (JointName.neck, JointName.pelvis),
    (JointName.head, JointName.neck),
    (JointName.neck, JointName.right_shoulder),
    (JointName.right_shoulder, JointName.right_elbow),
    (JointName.right_elbow, JointName.right_hand),
    (JointName.neck, JointName.left_shoulder),
    (JointName.left_shoulder, JointName.left_elbow),
    (JointName.left_elbow, JointName.left_hand)
)

ABSOLUTE_ANGLE_MAPPING = {
    JointName.right_hand: JointName.right_elbow,
    JointName.right_elbow: JointName.right_shoulder,
    JointName.right_shoulder: JointName.neck,
    JointName.right_foot: JointName.right_knee,
    JointName.right_knee: JointName.right_hip,
    JointName.right_hip: JointName.pelvis,

    JointName.left_hand: JointName.left_elbow,
    JointName.left_elbow: JointName.left_shoulder,
    JointName.left_shoulder: JointName.neck,
    JointName.left_foot: JointName.left_knee,
    JointName.left_knee: JointName.left_hip,
    JointName.left_hip: JointName.pelvis,

    JointName.pelvis: JointName.neck,
    JointName.neck: JointName.pelvis,
    JointName.head: JointName.neck,
}


class Joint:
    def __init__(self, x: float, y: float, z: float, name: JointName):
        self.point = np.array([x, y, z])
        self.name = name

    def to_json(self):
        return {
            'point': self.point.tolist(),
            'name': self.name.name
        }

    @classmethod
    def from_json(cls, data):
        point = data['point']
        return Joint(point[0], point[1], point[2], JointName[data['name']])  # SKAPA ENUM HÄR


class Skeleton3D:
    def __init__(self, joints: List[Joint]):
        self.joints = joints

    def joint_count(self) -> int:
        return len(self.joints)

    def scale(self, scale_factor: float) -> None:
        for joint in self.joints:
            joint.point *= scale_factor

    def joint_distance(self, jn1: JointName, jn2: JointName) -> float:
        j1 = self.joints[jn1.value]
        j2 = self.joints[jn2.value]
        return np.linalg.norm(j1.point - j2.point)

    def get_joints(self) -> List[Joint]:
        return self.joints

    def center_around_origo(self):
        pelvis_point = np.copy(self.joints[JointName.pelvis.value].point)
        for joint in self.joints:
            joint.point -= pelvis_point

    def make_pelvis(self):
        hip_vector = self.joints[JointName.left_hip.value].point + self.joints[JointName.right_hip.value].point
        self.joints[JointName.pelvis.value].point = hip_vector / 2

    def to_json(self):
        return {
            'joints': [joint.to_json() for joint in self.joints]
        }

    @classmethod
    def from_json(cls, data):
        return Skeleton3D([Joint.from_json(joint) for joint in data['joints']])