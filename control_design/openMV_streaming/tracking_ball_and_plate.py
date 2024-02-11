#this script tracks the balls pos relative to the tracked outline for the plate: not needed in the control logic since we do not care about the plate, but only about the ball. 

import sensor, image, time

# Initialization
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)  # must be turned off for color tracking
sensor.set_auto_whitebal(False)  # must be turned off for color tracking
clock = time.clock()

# Color Thresholds
black_threshold = (0, 50, -25, 25, -25, 25)  # Example thresholds for black
white_threshold = (94, 100, -128, 127, -128, 60)  # Adjusted thresholds for white

min_area = 10  # Minimum area for the ball blob
max_area = 1000  # Maximum area for the ball blob

# Inclusion zone - Assuming we want to include the entire screen: (0, 0, 320, 240)  # x, y, w, z
inclusion_zone = (80, 40, 200, 150)  # x, y, w, z

while(True):
    clock.tick()
    img = sensor.snapshot()

    # Find the black plate within the inclusion zone
    plates = img.find_blobs([black_threshold], pixels_threshold=200, area_threshold=200, merge=True, roi=inclusion_zone)
    if plates:
        plate = max(plates, key=lambda b: b.area())  # Assuming the largest black blob is the plate
        img.draw_rectangle(plate.rect(), color=(255, 0, 0))
        plate_center_x, plate_center_y = plate.cx(), plate.cy()

        # Find the white ball within the inclusion zone
        balls = img.find_blobs([white_threshold], pixels_threshold=min_area, area_threshold=min_area, merge=True, roi=inclusion_zone)
        valid_balls = [b for b in balls if min_area <= b.area() <= max_area]

        if valid_balls:
            ball = max(valid_balls, key=lambda b: b.area())  # Assuming the largest white blob is the ball
            img.draw_rectangle(ball.rect(), color=(0, 255, 0))
            ball_center_x, ball_center_y = ball.cx(), ball.cy()

            # Calculate position of the ball relative to the plate
            relative_position_x = ball_center_x - plate_center_x
            relative_position_y = ball_center_y - plate_center_y

            # Print the relative position to the OpenMV IDE terminal
            print("Relative Position: X =", relative_position_x, "Y =", relative_position_y)
        else:
            print("Ball not found")
