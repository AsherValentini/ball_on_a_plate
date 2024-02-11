import sensor, image, time

# Initialization for PID control
previous_error_x, previous_error_y = 0, 0
integral_x, integral_y = 0, 0

# Initialization for the camera
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)  # 320x240
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)  # must be turned off for color tracking
sensor.set_auto_whitebal(False)  # must be turned off for color tracking
clock = time.clock()

# Color Thresholds
white_threshold_temp = (94, 100, -128, 127, -128, 60)  # Adjusted thresholds for white
white_threshold = (95, 36, -128, 127, -128, 60)  # Adjusted thresholds for white (dark room with lights) 

min_area = 10  # Minimum area for the ball blob
max_area = 1000  # Maximum area for the ball blob

inclusion_zone = (80, 40, 150, 150)  

# Reference point (dead center of the frame)
frame_center_x = 320 // 2
frame_center_y = 240 // 2


def pid_update(error, dt, pid_coefficients, angle_range, axis, previous_error, integral):
    Kp, Ki, Kd = pid_coefficients
    
    # PID calculations
    proportional = Kp * error
    integral += error * dt
    derivative = (error - previous_error) / dt
    
    # PID output before clipping
    pid_output = proportional + (Ki * integral) + (Kd * derivative)
    
    # Clip PID output to defined angle range
    clipped_output = max(min(pid_output, angle_range[1]), angle_range[0])
    
    # Return the updated PID output and state variables
    return clipped_output, error, integral

while(True):
    clock.tick()
    img = sensor.snapshot()

    # Find the white ball
    balls = img.find_blobs([white_threshold], pixels_threshold=min_area, area_threshold=min_area, merge=True, roi=inclusion_zone)
    valid_balls = [b for b in balls if min_area <= b.area() <= max_area]

    if valid_balls:
        ball = max(valid_balls, key=lambda b: b.area())
        img.draw_rectangle(ball.rect(), color=(0, 255, 0))
        ball_center_x, ball_center_y = ball.cx(), ball.cy()

        # Calculate position of the ball relative to the frame center
        relative_position_x = ball_center_x - frame_center_x
        relative_position_y = ball_center_y - frame_center_y

        # PID coefficients and angle range
        angle_range = (-45, 45)  # degrees
        pid_coefficients = (1.0, 1.0, 0.1)  # Example PID coefficients

        # Error calculation
        error_x = relative_position_x
        error_y = relative_position_y
        dt = 1.0 / clock.fps()

        # Inside the loop, when calling pid_update:
        angle_adjust_x, previous_error_x, integral_x = pid_update(error_x, dt, pid_coefficients, angle_range, 'x', previous_error_x, integral_x)
        angle_adjust_y, previous_error_y, integral_y = pid_update(error_y, dt, pid_coefficients, angle_range, 'y', previous_error_y, integral_y)

        # Print or use the angle adjustments as needed
        print("Angle Adjust X:", angle_adjust_x, "Y:", angle_adjust_y)
    else:
        print("Ball not found")
