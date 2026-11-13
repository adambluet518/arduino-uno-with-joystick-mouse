
import serial
import serial.tools.list_ports
import pyautogui
import time

# Find Arduino automatically
ports = list(serial.tools.list_ports.comports())
arduino_port = None

for port in ports:
    name = (port.device + " " + port.description).lower()
    if any(word in name for word in
           ["usbmodem", "usbserial", "arduino", "ch340", "wch"]):
        arduino_port = port.device
        break

if arduino_port is None:
    print("Arduino not found!")
    raise SystemExit

print("Connecting to:", arduino_port)

arduino = serial.Serial(arduino_port, 115200, timeout=1)
time.sleep(2)
arduino.reset_input_buffer()

# Mouse settings
CENTER_X = 507
CENTER_Y = 516

DEADZONE = 65
MAX_SPEED = 6

screen_width, screen_height = pyautogui.size()

last_button = 1

print("Joystick mouse active!")
print("Press Ctrl+C to stop.")

try:
    while True:
        line = arduino.readline().decode(
            "utf-8", errors="ignore"
        ).strip()

        try:
            x, y, button = map(int, line.split(","))
        except ValueError:
            continue

        dx = x - CENTER_X
        dy = y - CENTER_Y

        # Ignore tiny movements
        if abs(dx) < DEADZONE:
            dx = 0

        if abs(dy) < DEADZONE:
            dy = 0

        # Smooth, slower movement
        move_x = -(dx / 512) ** 3 * MAX_SPEED
        move_y = -(dy / 512) ** 3 * MAX_SPEED

        current_x, current_y = pyautogui.position()

        new_x = max(0, min(screen_width - 1,
                           current_x + move_x))
        new_y = max(0, min(screen_height - 1,
                           current_y + move_y))

        if dx != 0 or dy != 0:
            pyautogui.moveTo(new_x, new_y, _pause=False)

        # Joystick button = left click
        if button == 0 and last_button == 1:
            pyautogui.click()

        last_button = button

except KeyboardInterrupt:
    print("\nMouse control stopped.")

finally:
    arduino.close()
