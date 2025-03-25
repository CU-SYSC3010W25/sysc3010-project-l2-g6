from sense_hat import SenseHat
import time

sense = SenseHat()
sense.set_rotation(180)  # Adjust the rotation if needed

# Define text and color
message = "Hello, Pi!"
text_color = (255, 0, 0)  # Red text
bg_color = (0, 0, 0)  # Black background

# Display the message
sense.show_message(message, text_colour=text_color, back_colour=bg_color, scroll_speed=0.1)

time.sleep(1)
sense.clear()

