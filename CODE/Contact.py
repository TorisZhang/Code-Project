import pandas as pd

# inner class with only information on every contact.
class Contact:
    def __init__(self, name, phone, email, address, note) -> None:
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.note = note
