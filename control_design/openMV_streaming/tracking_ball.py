import sensor, image, time

# Initialization
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)  # 320x240
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)  # must be turned off for color tracking
sensor.set_auto_whitebal(False)  # must be turned off for color tracking
clock = time.clock()

# Color Thresholds
white_threshold = (94, 100, -128, 127, -128, 60)  # Adjusted thresholds for white

min_area = 10  # Minimum area for the ball blob
max_area = 1000  # Maximum area for the ball blob

# Reference point (dead center of the frame)
frame_center_x = 320 // 2
frame_center_y = 240 // 2

while(True):
    clock.tick()
    img = sensor.snapshot()

    # Find the white ball
    balls = img.find_blobs([white_threshold], pixels_threshold=min_area, area_threshold=min_area, merge=True)
    valid_balls = [b for b in balls if min_area <= b.area() <= max_area]

    if valid_balls:
        ball = max(valid_balls, key=lambda b: b.area())  # Assuming the largest white blob is the ball
        img.draw_rectangle(ball.rect(), color=(0, 255, 0))
        ball_center_x, ball_center_y = ball.cx(), ball.cy()

        # Calculate position of the ball relative to the frame center
        relative_position_x = ball_center_x - frame_center_x
        relative_position_y = ball_center_y - frame_center_y

        # Print the relative position to the OpenMV IDE terminal
        print("Relative Position: X =", relative_position_x, "Y =", relative_position_y)
    else:
        print("Ball not found")
