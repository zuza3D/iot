from customtkinter import *
from PIL import Image, ImageOps


class AuctionFrame(CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.blue_image = Image.new("RGBA", (200, 200), (31, 106, 165, 255))
        self.auction_image = CTkImage(light_image=self.blue_image, size=(200, 200))

        self.img_label = CTkLabel(self, image=self.auction_image, text="")
        self.img_label.pack(pady=10)

        self.name_label = CTkLabel(self, text="Nazwa: ---", font=("Arial", 14))
        self.name_label.pack(pady=5)

        self.price_label = CTkLabel(self, text="Cena: 0.00", font=("Arial", 14))
        self.price_label.pack(pady=10)

        self.customer_label = CTkLabel(self, text="", font=("Arial", 14))
        self.customer_label.pack(pady=5)

    def update_auction(self, name, price, img_path):
        self.name_label.configure(text=f"Nazwa: {name}")
        self.price_label.configure(text=f"Cena: {price:.2f} zł")
        self.customer_label.configure(text="")
        if img_path:
            with Image.open(f"{img_path}") as img:
                img = ImageOps.exif_transpose(img)
                self.auction_image = CTkImage(light_image=img, size=(200, 200))
                self.img_label.configure(image=self.auction_image, text="")
        else:
            self.auction_image = CTkImage(light_image=self.blue_image, size=(200, 200))
            self.img_label.configure(image=self.auction_image)
        self.show_auction_detail()

    def update_current_offer(self, price, customer):
        self.price_label.configure(text=f"Cena: {price:.2f} zł")
        self.customer_label.configure(text=f"Najwyższa oferta: {str(customer)}")

    def hide_auction_details(self):
        self.name_label.pack_forget()
        self.img_label.pack_forget()
        self.price_label.pack_forget()
        self.customer_label.forget()

    def show_auction_detail(self):
        self.name_label.pack(pady=10)
        self.img_label.pack(pady=10)
        self.price_label.pack(pady=10)
        self.customer_label.pack(pady=10)

    def set_customer(self, customer):
        self.customer_label.configure(text=customer)
