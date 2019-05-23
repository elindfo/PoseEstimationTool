"""
Created on Dec 20 17:39 2016

@author: Denis Tome'
"""

import __init__

from lifting import PoseEstimator
from lifting.utils import draw_limbs
from lifting.utils import plot_pose

import json
import cv2
import matplotlib.pyplot as plt
from os.path import dirname, realpath, basename, join, splitext


DIR_PATH = dirname(realpath(__file__))
PROJECT_PATH = realpath(DIR_PATH + '/..')
IMAGE_FILE_PATH = PROJECT_PATH + '/data/images/test_image.png'
SAVED_SESSIONS_DIR = PROJECT_PATH + '/data/saved_sessions'
SESSION_PATH = SAVED_SESSIONS_DIR + '/init_session/init'
PROB_MODEL_PATH = SAVED_SESSIONS_DIR + '/prob_model/prob_model_params.mat'


def get_pose_from_image(file_path):
    image = cv2.imread(file_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # conversion to rgb

    # create pose estimator
    image_size = image.shape

    pose_estimator = PoseEstimator(image_size, SESSION_PATH, PROB_MODEL_PATH)

    # load model
    pose_estimator.initialise()

    # estimation
    pose_2d, visibility, pose_3d = pose_estimator.estimate(image)

    # close model
    pose_estimator.close()

    # Save to JSON
    if pose_2d is None:
        pose_2d = []
    else:
        pose_2d = pose_2d.tolist()
    if pose_3d is None:
        pose_3d = []
    else:
        pose_3d = pose_3d.tolist()

    results = {'2d': pose_2d, '3d': pose_3d}

    file_name, file_ext = splitext(file_path)
    with open(join('/shared/estimations', basename(file_name) + '.json'), 'w') as results_file:
        print 'Writing to file ' + file_path + '.json'
        results_file.write(json.dumps(results))


def main():
    import argparse
    import glob

    parser = argparse.ArgumentParser()
    parser.add_argument('directory')
    parser.add_argument('extension')
    args = parser.parse_args()

    if args.directory and args.extension:
        files = glob.glob(args.directory + '/*.' + args.extension)
        print 'Number files found: ' + str(len(files))
        print files
        for file in files:
            get_pose_from_image(file)
    else:
        print('Url not set')
        sys.exit(1)


if __name__ == '__main__':
    import sys
    sys.exit(main())
