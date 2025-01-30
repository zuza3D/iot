from config import GPIO, buzzerPin

def buzz(state):
   GPIO.output(buzzerPin, not state)  # pylint: disable=no-member
