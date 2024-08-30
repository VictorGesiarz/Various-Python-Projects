from math import pi, cos, sin, sqrt
import time

robot_x = 3
robot_y = 1
robot_yaw = 0

initial_x = robot_x
initial_y = robot_y
initial_yaw = robot_yaw

moving = True
circle = True
velocity_x = 0.2
velocity_yaw = 0
distance_move = 1
angle_move = pi / 2


while circle:

    if moving:
        diff_x = robot_x - initial_x
        diff_y = robot_y - initial_y
        pitagoras = sqrt(diff_x**2 + diff_y**2)

        if pitagoras >= 1:
            moving = False
            velocity_x = 0
            velocity_yaw = pi / 20
            initial_yaw = robot_yaw

    else:
        if robot_yaw >= initial_yaw + angle_move:
            moving = True
            velocity_x = 0.2
            velocity_yaw = 0
            initial_x = robot_x
            initial_y = robot_y

    if robot_yaw >= 2 * pi:
        robot_yaw -= 2 * pi

    print(robot_x, robot_y, robot_yaw)

    robot_x = round(robot_x + velocity_x * cos(robot_yaw), 8)
    robot_y = round(robot_y + velocity_x * sin(robot_yaw), 8)
    robot_yaw += velocity_yaw

    time.sleep(1)
