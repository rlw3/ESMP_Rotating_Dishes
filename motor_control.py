from time import sleep
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

# Function to move motor at a specified speed and direction
def move_motor(speed, direction):
    GPIO.output(DIR_PIN, direction)
    delay = 1 / (speed * SPR)  # Calculate delay based on speed and steps per revolution

    while True:
        GPIO.output(STEP_PIN, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP_PIN, GPIO.LOW)
        sleep(delay)

try:
    # Get user input for speed and direction
    while True:
        print("Select speed (1-5):")
        # print("1: 0.25 rps")
        # print("2: 0.5 rps")
        # print("3: 1 rps")
        # print("4: 1.5 rps")
        # print("5: 2 rps")
        speed_option = int(input("Enter speed option: "))

        if speed_option == 1:
            speed = 1
        elif speed_option == 2:
            speed = 2.5
        elif speed_option == 3:
            speed = 5
        elif speed_option == 4:
            speed = 7.5
        elif speed_option == 5:
            speed = 10

        else:
            print("Invalid option. Please enter a number between 1 and 5.")
            continue

        direction_input = input("Enter direction CW:0 CCW:1: ").upper()
        if direction_input == "0":
            direction = CW
        elif direction_input == "1":
            direction = CCW
        else:
            print("Invalid direction. Please enter 'CW' or 'CCW'.")
            continue

        move_motor(speed, direction)

except KeyboardInterrupt:
    print("\nProgram terminated.")
finally:
    GPIO.cleanup()
