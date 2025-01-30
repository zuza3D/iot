from config import GPIO, encoderLeft, encoderRight

class Encoder:
    def __init__(
        self,
        initial_value=0,
        min_value=0,
        max_value=10,
        step=1,
        bounce_time = 100,
        left=encoderLeft,
        right=encoderRight,
    ):
        self.value = initial_value
        self.min = min_value
        self.max = max_value
        self.step = step
        self.left = left
        self.right = right

        self.lastRight = 0
        self.lastLeft = 0

        GPIO.add_event_detect(
            left,
            GPIO.FALLING,
            callback=self.turn_encoder,
            bouncetime=bounce_time,
        )
        GPIO.add_event_detect(
            right,
            GPIO.FALLING,
            callback=self.turn_encoder,
            bouncetime=bounce_time,
        )

    def turn_encoder(self, _):
        leftState = GPIO.input(self.left)
        rightState = GPIO.input(self.right)

        if self.lastLeft == 1 and leftState == 0:
            self.turnRight()
        if self.lastRight == 1 and rightState == 0:
            self.turnLeft()

        self.lastLeft = leftState
        self.lastRight = rightState

    def turnLeft(self):
        self.value -= self.step
        if self.value < self.min:
            self.value = self.min

    def turnRight(self):
        self.value += self.step
        if self.value > self.max:
            self.value = self.max
