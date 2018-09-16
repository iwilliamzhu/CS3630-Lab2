import sys
sys.path.append('../')
from state import State
import time
import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps
import cozmo.behavior
import classifyimage
import time

class IdleState(State):
    """
        Monitor stream of images from the camera. Classify each image using the model you
        developed in Lab1. If one of the symbols is recognized (i.e. not “none”), use the built-in text-tospeech
        functionality to have the robot say the name of the recognized symbol, then switch to the
        appropriate state (see below). Note that the SDK can provide both grayscale and color images, at
        resolutions of 320 × 240 and 160 × 240, respectively. More specifically, the SDK reduces the        
        width resolution of color images by half, transfers them from the robot, then resizes color to match
        the grayscale at 320 × 240. You are welcome to use the color images if you find it helpful, but be    
        aware that as a result of rescaling they are not as detailed as the grayscale images.
    """
    stateName = ''
    def __init__(self, robot):
        self.robot = robot
        print ('Current state:', str(self))
        while True:
            time.sleep(4)
            robot.set_head_angle(cozmo.util.degrees(0)).wait_for_completed()
            raw_image = robot.world.latest_image.raw_image
            predicted_label = classifyimage.classify_image(raw_image)
            print(predicted_label)
            if predicted_label != 'none':
                robot.say_text(predicted_label).wait_for_completed()
                self.on_event(predicted_label, robot)

    def on_event(self, event, robot):
        if event == 'drone':
            stateName = 'drone'
            return DroneState(robot)
        if event == 'order':
            stateName = 'order'
            return OrderState(robot)
        if event == 'inspection':
            stateName = 'inspection'
            return InspectionState(robot)

        return self

class DroneState(State):
    """
        The robot should locate one of the cubes (one will be placed in front of it within view),
        pick up the cube, drive forward with the cube for 10cm, put down the cube, and drive backward
        10cm. Then return to Idle state. 
    """

    def __init__(self, robot):
        self.robot = robot
        print ('Current state:', str(self))
        """
        Do action here
        """
        lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
        cube = robot.world.wait_until_observe_num_objects(num=1, object_type=cozmo.objects.LightCube, timeout=10)
        lookaround.stop()
        # ideally have a check here)

        if len(cube) == 1:
            current_action = robot.pickup_object(cube[0], num_retries=3)
            current_action.wait_for_completed()
            if current_action.has_failed:
                code, reason = current_action.failure_reason
                result = current_action.result
                print("Pickup Cube failed: code=%s reason='%s' result=%s" % (code, reason, result))
                return
            robot.drive_straight(distance_mm(100), speed_mmps(50)).wait_for_completed()
            robot.place_object_on_ground_here(cube[0], num_retries=0).wait_for_completed()
            robot.drive_straight(distance_mm(-100), speed_mmps(50)).wait_for_completed()


        self.return_to_idle()

    def return_to_idle(self):
        return IdleState(self.robot)

class OrderState(State):
    """
        Use the drive_wheels function to have the robot drive in a circle with an
        approximate radius of 10cm. Then return to Idle state.
    """
    def __init__(self, robot):
        self.robot = robot
        print ('Current state:', str(self))
        """
        Do action here
        """
        current action = robot.drive_straight(25, 50)
        time.sleep(3)



        self.return_to_idle()
        
    def return_to_idle(self):
        return IdleState(self.robot)

class InspectionState(State):
    """
        Have the robot drive in a square, where each side of the square is approximately 20 cm.
        While driving, the robot must continuously raise and lower the lift, but do so slowly (2-3 seconds
        to complete lowering or raising the lift). Lower the lift at the end of the behavior, and return to
        Idle state
    """
    def __init__(self, robot):
        self.robot = robot
        print ('Current state:', str(self))
        """
        Do action here
        """
        count_turns = 0
        while count_turns <= 4:
            action1 = robot.drive_straight(distance_mm(200), speed_mmps(30), in_parallel=True)
            action2 = robot.set_lift_height(1.0, in_parallel=True, duration=3.0)
            action1.wait_for_completed()
            action2.wait_for_completed()
            action2 = robot.set_lift_height(0.0, in_parallel=True, duration=3.0)
            action2.wait_for_completed()
            action1 = robot.turn_in_place(degrees(90), in_parallel=True).wait_for_completed()

            count_turns = count_turns + 1

        action1 = robot.turn_in_place(degrees(90), in_parallel=True)
        action1.wait_for_completed()
        action2 = robot.set_lift_height(0.0, in_parallel=True, duration=3.0).wait_for_completed()
        self.return_to_idle()
        
    def return_to_idle(self):
        return IdleState(self.robot)