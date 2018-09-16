''' Lab 2
Chingyeu Andy Leekung
Mingyang Zhu
'''

import sys

sys.path.append('./State')

import cozmo
import datetime
import time
import numpy as np
from sklearn.externals import joblib
from skimage import io, feature, filters, exposure, color

from state_machine import StateMachine
import classifyimage

def run(sdk_conn):
    clf = joblib.load('classifier.pkl')

    robot = sdk_conn.wait_for_robot()
    robot.camera.image_stream_enabled = True
    robot.camera.color_image_enabled = False
    robot.camera.enable_auto_exposure()

    robot.set_head_angle(cozmo.util.degrees(0)).wait_for_completed()

    # instantiate simple device in Idle State
    device = StateMachine()

    while True:
        time.sleep(4)
        raw_image = robot.world.latest_image.raw_image
        predicted_label = classifyimage.classify_image(raw_image)
        print(predicted_label)
        if predicted_label != 'none':
            robot.say_text(predicted_label).wait_for_completed()
            device.on_event(predicted_label)

if __name__ == '__main__':
    cozmo.setup_basic_logging()

    try:
        cozmo.connect(run)
    except cozmo.ConnectionError as e:
        sys.exit("A connection error occurred: %s" % e)
