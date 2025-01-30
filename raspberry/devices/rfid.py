from mfrc522 import MFRC522
from time import time

class RFID:
    def __init__(self):
        self.last_read = None
        self.debounce = 0

    def _read(self):
        MIFAREReader = MFRC522()

        (status, _) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        if status != MIFAREReader.MI_OK:
            return None,None
        (status, uid) = MIFAREReader.MFRC522_Anticoll()
        if status != MIFAREReader.MI_OK:
            return None, None

        num = 0
        for i in range(0, len(uid)):
            num += uid[i] << (i*8)

        return uid, num

    def rfidRead(self):
        uid, num = self._read()

        if num != self.last_read:
            if time() - self.debounce > 1:
                self.last_read = num
                self.debounce = time()
                return uid, num
        else:
            self.debounce = time()
        
        return None, None
