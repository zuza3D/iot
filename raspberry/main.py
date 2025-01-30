from math import ceil
import sys
import os
from contextlib import contextmanager
from time import sleep, time
from devices.encoder import Encoder
from devices.buzzer import buzz
from devices.pixels import set_pixels, setup_pixels
from devices.rfid import RFID
from PIL import Image, ImageDraw, ImageFont
import lib.oled.SSD1331 as SSD1331
from client import *

class Program:
    def __init__(self):
        self.client = MqttClient()

        self.rfid = RFID()
        self.oled = SSD1331.SSD1331()
        self.oled.Init()
        self.oled.clear()
        self.pixels = setup_pixels()
        self.font = ImageFont.truetype('./lib/oled/Font.ttf', 10)
        self.encoder = Encoder(initial_value=50, min_value=50, max_value=1000, step=50)

        self.img = None
        self.name = None
        self.price = None

    def _show_remaining_time(self):
        remaining_seconds = round((time() - self._timer_start))
        if remaining_seconds > 8:
            remaining_seconds = 8
        set_pixels(self.pixels, [(0,0,0)] * remaining_seconds + [(255,0,0)]*(8-remaining_seconds))

    def wait_for_start(self):
        while True:
            msg = self.client.get_message()
            if msg:
                if isinstance(msg, SetNameMsg):
                    self.name = msg.name
                if isinstance(msg, SetPriceMsg):
                    self.price = msg.price
                if isinstance(msg, SetImageMsg):
                    self.img = msg.image
                if isinstance(msg, StartAuctionMsg):
                    if self.name is None:
                        continue
                    if self.price is None:
                        continue
                    if self.img is None:
                        continue
                    return

    def _show_auction_screen(self):
        if self.img.size != (40, 40):
            self.img = self.img.resize((40,40)).convert("RGBA")
            self.img = self.img.rotate(270)
        base_img = Image.new("RGBA", (96, 64), "BLACK")
        draw = ImageDraw.Draw(base_img)

        draw.text((0, 40), f'{self.name}, {self.price}zl', font=self.font, fill="WHITE")
        draw.text((0, 50), f'Podnies {self.encoder.value}zl', font=self.font, fill="WHITE")

        base_img.paste(self.img, (0,0,40,40),self.img)
        self.oled.ShowImage(base_img, 0, 0)

    def _show_winner_screen(self, winner, price):
        self.oled.clear()

        base_img = Image.new("RGBA", (96, 64), "BLACK")
        draw = ImageDraw.Draw(base_img)
        if(winner == '0'):
            draw.text((0, 30), f'Brak ofert', font=self.font, fill="WHITE")
        else:
            draw.text((0, 30), f'Wygrywa {winner}', font=self.font, fill="WHITE")
            draw.text((0, 50), f'Cena {price}zl', font=self.font, fill="WHITE")

        self.oled.ShowImage(base_img, 0, 0)

    def run_auction(self):
        self._timer_start = time()
        while True:
            self._show_auction_screen()
            self._show_remaining_time()

            msg = self.client.get_message()
            if isinstance(msg, SetPriceMsg):
                self._timer_start = time()
                self.price = msg.price
            if isinstance(msg, FinishAuctionMsg):
                return msg.winner, msg.price

            num, uid = self.rfid.rfidRead()
            if uid:
                self.client.send_raise(uid, self.encoder.value)

    def read_rfid(self):
        num, uid = self.rfid.rfidRead()
        

    def finish_auction(self, winner, price):
        self._show_winner_screen(winner, price)
        buzz(True)
        set_pixels(self.pixels, [(0,255,0)]*8)
        sleep(0.5)
        buzz(False)
        sleep(1.5)
        set_pixels(self.pixels, [(0,0,0)]*8)
        self.name = None
        self.price = None
        self.img = None

    def run_single_auction(self):
        self.wait_for_start()
        winner, price = self.run_auction()
        self.finish_auction(winner, price)

if __name__ == '__main__':
    p = Program()
    p._timer_start = time()
    while True:
        p.run_single_auction()
