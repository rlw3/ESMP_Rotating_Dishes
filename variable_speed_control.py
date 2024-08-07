from time import sleep
import threading
import RPi.GPIO as GPIO

# Suppress GPIO warnings
GPIO.setwarnings(False)

# Set GPIO numbering mode
GPIO.setmode(GPIO.BCM)

# Constants for rotation direction and steps
CW = 1  # Clockwise
CCW = 0  # Counter-Clockwise
SPR = 800  # Steps per revolution in 1/4 step mode

# Pin assignments and setup for the motor
STEP_PIN = 17
DIR_PIN = 18
MODE = (2, 3, 4)
GPIO.setup([STEP_PIN, DIR_PIN] + list(MODE), GPIO.OUT)

# Set microstepping modes
GPIO.output(MODE, (0, 1, 0))

# Global variable for motor speed and direction
motor_speed = 0.0
motor_direction = CW
running = True

# Function to move motor at a specified speed and direction
def move_motor():
    global motor_speed, motor_direction, running
    while running:
        if motor_speed > 0:
            delay = 1 / (motor_speed * SPR)  # Calculate delay based on speed and steps per revolution
            GPIO.output(DIR_PIN, motor_direction)
            GPIO.output(STEP_PIN, GPIO.HIGH)
            sleep(delay / 2)  # High for half of the delay
            GPIO.output(STEP_PIN, GPIO.LOW)
            sleep(delay / 2)  # Low for half of the delay
        else:
            sleep(0.1)  # Sleep briefly if the motor speed is 0 to avoid busy waiting

# Function to handle user input
def user_input():
    global motor_speed, running
    try:
        while running:
            # Get user input for speed
            speed = float(input("Enter motor speed (0.1 to 20 rps, or 0 to stop): "))
            if 0 <= speed <= 20:
                motor_speed = speed
            else:
                print("Invalid speed. Please enter a value between 0 and 20.")
    except KeyboardInterrupt:
        running = False
    finally:
        GPIO.cleanup()

# Initial setup for direction
try:
    direction_input = input("Enter direction CW:0 CCW:1: ").upper()
    if direction_input == "0":
        motor_direction = CW
    elif direction_input == "1":
        motor_direction = CCW
    else:
        print("Invalid direction. Please enter '0' for CW or '1' for CCW.")
        GPIO.cleanup()
        exit(1)

    # Start the motor control thread
    motor_thread = threading.Thread(target=move_motor)
    motor_thread.start()

    # Handle user input in the main thread
    user_input()

    # Wait for the motor control thread to finish
    motor_thread.join()

    print("Program terminated.")

except KeyboardInterrupt:
    running = False
    GPIO.cleanup()
