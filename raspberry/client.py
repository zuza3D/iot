import io
import paho.mqtt.client as mqtt
from queue import Queue
from time import sleep
from dataclasses import dataclass
from typing import Optional

from PIL import Image

class Message:
    pass

@dataclass
class SetNameMsg(Message):
    name :str

@dataclass
class SetPriceMsg(Message):
    price :int

@dataclass
class SetImageMsg(Message):
    image :Image.Image

@dataclass
class FinishAuctionMsg(Message):
    winner :str
    price :int

@dataclass
class StartAuctionMsg(Message):
    pass

class MqttClient:
    def on_message(self, client, userdata, msg):
        message = None
        if msg.topic == 'set_item_name':
            message = SetNameMsg(name = msg.payload.decode())
        if msg.topic == 'set_item_price':
            message = SetPriceMsg(price = int(msg.payload.decode()))
        if msg.topic == 'set_item_image':
            img_data = msg.payload
            image = Image.open(io.BytesIO(img_data))
            message = SetImageMsg(image)
        if msg.topic == 'finish_auction':
            winner, price = msg.payload.decode().split('.')
            winner = winner
            price = int(price)
            message = FinishAuctionMsg(winner = winner, price = price)
        if msg.topic == 'start_auction':
            message = StartAuctionMsg()

        if message is not None:
            self.messages.put(message)

    def send_raise(self, owner, amount):
        self.client.publish('raise', f"{owner}.{amount}")

    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect("localhost", 1883, 60)
        self.client.subscribe('set_item_name')
        self.client.subscribe('set_item_price')
        self.client.subscribe('set_item_image')
        self.client.subscribe('start_auction')
        self.client.subscribe('finish_auction')
        self.client.loop_start()
        self.messages = Queue()

    def shutdown(self):
        self.client.loop_stop()

    def get_message(self) -> Optional[Message]:
        if not self.messages.empty():
            return self.messages.get()
        