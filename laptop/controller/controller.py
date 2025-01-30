import os

from model import Auction
from view.app import App
import shutil
from mqtt.server import *
from PIL import Image

class Controller:
    def __init__(self):
        self.ended_auction_query = None
        self.app = App()
        self.timer_id = None
        self.current_auction = None
        self.mqtt = Server()

        self.images_path = fr"{os.getcwd()}\images"

        self.app.form_frame.add_button.configure(command=self.add_product)
        self.app.form_frame.file_button.configure(command=self.upload_action)

        self.start_next_auction()
        self.update_archive()
        self.app.after(100, self.check_messages)
        self.app.mainloop()

    def check_messages(self):
        msg = self.mqtt.get_message()
        if msg is not None:
            self.raise_bid_mqtt(msg)
        self.app.after(100, self.check_messages)

    @staticmethod
    def validate_product_data(name, price, img_path):
        if isinstance(name, str) and name.strip() and isinstance(price, (float, int)) and isinstance(
                img_path, str) and img_path.strip():
            return True
        return False

    def _get_img_path(self) -> str:
        text_path = self.app.form_frame.img_path_label.cget("text")
        img_path = None
        if text_path:
            img_path = 'images/' + self.app.form_frame.img_path_label.cget("text")
        return img_path

    def add_product(self):
        name = self.app.form_frame.name_entry.get()
        price = self.app.form_frame.price_entry.get()
        img_path = self._get_img_path()

        try:
            price = float(price)
        except ValueError:
            return

        if self.validate_product_data(name, price, img_path):
            Auction.create(name=name, price=price, img_path=img_path, zakonczona=False, customer=None)
            self.app.form_frame.clear_form()
            if self.current_auction is None:
                self.start_next_auction()

    def start_next_auction(self):
        self.stop_timer()
        self.current_auction = Auction.select().where(~Auction.ended).first()
        if self.current_auction:
            self.app.auction_title_frame.set_title("Aktualna oferta")
            self.app.auction_frame.update_auction(
                name=self.current_auction.name,
                price=self.current_auction.price,
                img_path=self.current_auction.img_path,
            )
            self._send_auction_details(self.current_auction)
            self.start_timer()
        else:
            self.app.auction_title_frame.set_title("Brak ofert")
            self.app.auction_frame.hide_auction_details()

    def _send_auction_details(self, auction :Auction):
        self.mqtt.send_item_name(auction.name)
        self.mqtt.send_item_price(int(auction.price))
        image = Image.open(auction.img_path)
        self.mqtt.send_item_image(image)
        image.close()
        self.mqtt.send_start_auction()

    def raise_bid_mqtt(self, msg: RaiseMsg):
        if self.current_auction:
            self.current_auction.price += msg.raise_amount
            self.current_auction.customer = msg.card_num
            self.current_auction.save()
            self.app.auction_frame.update_current_offer(
                price = self.current_auction.price,
                customer = self.current_auction.customer
            )
            self.reset_timer()
            self.mqtt.send_item_price(self.current_auction.price)

    def start_timer(self):
        self.timer_id = self.app.after(10000, self.end_auction)

    def reset_timer(self):
        self.stop_timer()
        self.start_timer()

    def stop_timer(self):
        if self.timer_id is not None:
            self.app.after_cancel(self.timer_id)
            self.timer_id = None

    def end_auction(self):
        if self.current_auction:
            self.current_auction.ended = True
            self.current_auction.save()
            new_archive_data = f"{self.current_auction.name} --- {self.current_auction.price:.2f} zł ---" \
                               f"{'nie było ofert' if not self.current_auction.customer else f'wylicytował: {self.current_auction.customer}'}"
            self.app.archive_frame.add_new_archive_data(new_archive_data)

            customer = 0
            if self.current_auction.customer:
                customer = self.current_auction.customer
            self.mqtt.send_finish_auction(customer, self.current_auction.price)
        self.start_next_auction()

    def upload_action(self):
        file_path = self.app.open_file_dialog()
        if file_path:
            shutil.copy(file_path, self.images_path)
        filename = os.path.split(file_path)[1]
        self.app.form_frame.set_img_path_label_text(filename)

    def update_archive(self):
        self.ended_auction_query = Auction.select().where(Auction.ended).order_by(Auction.id.desc())
        archive_data = []
        for row in self.ended_auction_query:
            archive_data.append(f"{row.name} --- {row.price:.2f} zł "
                                f"--- {'nie było ofert' if not row.customer else f'wylicytował: {row.customer}'}")
        self.app.archive_frame.fill_archive_data(archive_data)
