import pandas as pd
from Contact import Contact

# This class is the list of Contact, which is learn from metirail online.
class ContactList:

    def __init__(self) -> None:
        # initialize the list.
        self.contact_list = []
        
        # read the first data
        data = pd.read_csv('./contactsIn.csv')

        # interate all the file content and created class to receive them.
        for index, row in data.iterrows():
            contact = Contact(row['Name'], row['Phone'], row['Email'], row['Address'], row['Note'])
            self.contact_list.append(contact)

    # function to add contact.
    def add_contact(self, contact):
        # already have the name
        if self.check_name_duplicate(contact.name):
            return False
        
        # otherwise add to list.
        self.contact_list.append(contact)
        return True

    # function to remove contact.
    def remove_contact(self, contact):
        # already have the name
        if not self.check_name_duplicate(contact.name):
            return 'No Matching Name'
        
        self.contact_list.remove(contact)

    # function to check whether there is already a duplicated name.
    def check_name_duplicate(self, name):
        name_count = sum(1 for contact in self.contact_list if contact.name == name)
        # in count > 1 means already exist, otherwise can be add or retuen value.
        return name_count >= 1
    
     # get the index by name
    def find(self, name):
        for i in range(len(self.contact_list)):
            if self.contact_list[i].name == name:
                return i
    
    # return length of contacts.
    def __len__(self):
        return len(self.contact_list)
