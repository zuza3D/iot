import io
import paho.mqtt.client as mqtt
from typing import Optional
from time import sleep
from PIL import Image
from dataclasses import dataclass

class Message:
    pass

@dataclass
class RaiseMsg(Message):
    card_num :int
    raise_amount :int


class Server:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_message = self._process_message
        self.client.connect("169.254.238.109", 1883, 60)
        self.client.subscribe('raise')
        self.client.loop_start()
        self.raise_msg = None

    def send_item_name(self, name :str):
        self.client.publish("set_item_name", name)

    def send_item_price(self, price :int):
        self.client.publish("set_item_price", int(price))

    def send_item_image(self, image :Image.Image):
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="JPEG")
        img_byte_arr = img_byte_arr.getvalue() 
        self.client.publish("set_item_image", img_byte_arr)

    def send_start_auction(self):
        self.client.publish("start_auction", "")

    def send_finish_auction(self, winner :int, price :int):
        self.client.publish("finish_auction", f'{int(winner)}.{int(price)}')

    def get_message(self) -> Optional[RaiseMsg]:
        t = self.raise_msg
        self.raise_msg = None
        return t
    
    def shutdown(self):
        self.client.loop_stop()
        self.client.disconnect()

    def _process_message(self, client, userdata, message):
        if message.topic == 'raise':
            sender, amount = message.payload.decode().split('.')
            sender = int(sender)
            amount = int(amount)
            self.raise_msg = RaiseMsg(sender, amount)
