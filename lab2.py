''' Lab 2
Chingyeu Andy Leekung
Mingyang Zhu
'''

import sys
import cozmo
import datetime
import time
import numpy as np
from sklearn.externals import joblib
from skimage import io, feature, filters, exposure, color

import simple_device

def run(sdk_conn):
    clf = joblib.load('classifier.pkl')

    robot = sdk_conn.wait_for_robot()
    robot.camera.image_stream_enabled = True
    robot.camera.color_image_enabled = False
    robot.camera.enable_auto_exposure()

    robot.set_head_angle(cozmo.util.degrees(0)).wait_for_completed()

    # instantiate simple device in Idle State
    device = SimpleDevice()

    while True:
        time.sleep(4)
        raw_image = robot.world.latest_image.raw_image
        features = extract_image_features([np.array(raw_image)])
        predicted_label = clf.predict(features)[0]
        print(predicted_label)
        if predicted_label != 'none':
            robot.say_text(predicted_label).wait_for_completed()
            device.on_event(predicted_label)


def extract_image_features(data):
    l = []
    for im in data:
        im_gray = color.rgb2gray(im)
    
        im_gray = filters.gaussian(im_gray, sigma=0.4)
        
        f = feature.hog(im_gray, orientations=10, pixels_per_cell=(48, 48), cells_per_block=(4, 4), feature_vector=True, block_norm='L2-Hys')
        l.append(f)
    

    feature_data = np.array(l)
    return(feature_data)

def 

if __name__ == '__main__':
    cozmo.setup_basic_logging()

    try:
        cozmo.connect(run)
    except cozmo.ConnectionError as e:
        sys.exit("A connection error occurred: %s" % e)
