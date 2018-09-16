from state import State

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
    def __init__(self):
        print ('Current state:', str(self))
        """
        robot = sdk_conn.wait_for_robot()
        robot.camera.image_stream_enabled = True
        robot.camera.color_image_enabled = False
        robot.camera.enable_auto_exposure()

        robot.set_head_angle(cozmo.util.degrees(0)).wait_for_completed()

        myargs = sys.argv[1:]
        
        if len(myargs) <= 1:
            sys.exit("Incorrect arguments")

        time.sleep(.5)
        latest_image = robot.world.latest_image
        new_image = latest_image.raw_image

        robot.say_text(stateName).wait_for_completed()

        timestamp = datetime.datetime.now().strftime("%dT%H%M%S%f")

        new_image.save("./lab2imgs/" + str(type) + "_" + timestamp + ".bmp")

        time.sleep(4)
        
    
    num_images_per_type = int(myargs[0])  # number of images to take of each type of object
    """
    def on_event(self, event):
        if event == 'drone':
            stateName = 'drone'
            return DroneState()
        if event == 'order':
            stateName = 'order'
            return OrderState()
        if event == 'inspection':
            stateName = 'inspection'
            return InspectionState()

        return self

class DroneState(State):
    """
        The robot should locate one of the cubes (one will be placed in front of it within view),
        pick up the cube, drive forward with the cube for 10cm, put down the cube, and drive backward
        10cm. Then return to Idle state. 
    """

    def __init__(self):
        print ('Current state:', str(self))

    def return_to_idle(self):
        return IdleState()

class OrderState(State):
    """
        Use the drive_wheels function to have the robot drive in a circle with an
        approximate radius of 10cm. Then return to Idle state.
    """
    def __init__(self):
        print ('Current state:', str(self))
        
    def return_to_idle(self):
        return IdleState()

class InspectionState(State):
    """
        Have the robot drive in a square, where each side of the square is approximately 20 cm.
        While driving, the robot must continuously raise and lower the lift, but do so slowly (2-3 seconds
        to complete lowering or raising the lift). Lower the lift at the end of the behavior, and return to
        Idle state
    """
    def __init__(self):
        print ('Current state:', str(self))
        
    def return_to_idle(self):
        return IdleState()