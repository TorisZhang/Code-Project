import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from ContactList import ContactList
from Contact import Contact
import pandas as pd

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.resizable(0, 0)
        self.contacts = ContactList()

        self.title("Welcome! There is your personal contacks")

        self.label = tk.Label(self, text="Your Contact").grid(row=0, column=0)

        self.tree = ttk.Treeview(self, columns=("name", "phone", "email", "address", "note"))
        self.tree.grid(row=1, column=0, rowspan=4, padx=10, pady=5)
        # Give name to columns.
        self.tree.heading("#1", text="Name")
        self.tree.heading("#2", text="Phone")
        self.tree.heading("#3", text="Email")
        self.tree.heading("#4", text="Address")
        self.tree.heading("#5", text="Note")
        # set the column width otherwise will be to wild.
        self.tree.column("#0", width=-10)
        self.tree.column("#1", width=100)
        self.tree.column("#2", width=100)
        self.tree.column("#3", width=150)
        self.tree.column("#4", width=200)
        self.tree.column("#5", width=100)
        # set data content to table.
        self.display()

        # self.listbox = tk.Listbox(self, width=50, height=10)

        self.add_button = tk.Button(self, text="Add New", 
                                    command=self.add_contact).grid(row=1, column=1, padx=5, pady=5)

        self.remove_button = tk.Button(self, text="Remove", 
                                       command=self.remove_contact).grid(row=2, column=1, padx=5, pady=5)

        self.remove_button = tk.Button(self, text="Modify", 
                                       command=self.modify_one).grid(row=3, column=1, padx=5, pady=5)

        self.remove_button = tk.Button(self, text="Download File", 
                                       command=self.store_information).grid(row=4, column=1, padx=5, pady=5)

    # most important function which is used for update whenever action is performed.
    def display(self):
        self.tree.delete(*self.tree.get_children())
        for idx in range(len(self.contacts)):
            self.tree.insert("", "end", 
                            values=(self.contacts.contact_list[idx].name, 
                            self.contacts.contact_list[idx].phone, 
                            self.contacts.contact_list[idx].email, 
                            self.contacts.contact_list[idx].address, 
                            self.contacts.contact_list[idx].note))

    # visualize the frame window of adding new
    def add_contact(self):
        newWindow = tk.Toplevel()
        newWindow.title("Please Input the Details.")
        labels = ["Name", "Phone", "Email", "Address", "Note"]
        newWindow.entries = {}
        for i, label in enumerate(labels):
            label_widget = tk.Label(newWindow, text=label + ":", padx=5, pady=10)
            label_widget.grid(row=i, column=0)
            entry = tk.Entry(newWindow)
            entry.grid(row=i, column=1, padx=10, pady=10)
            newWindow.entries[label] = entry

        self.add_button = tk.Button(newWindow, text="Add New Contact", 
                                command=lambda: self.add_opeation(newWindow)
                                ).grid(row=6, column=1, padx=5, pady=5)
        
    # add a new contact and check whether there is a duplicated name already.
    def add_opeation(self, window):
        name = window.entries["Name"].get()
        phone = window.entries["Phone"].get()
        email = window.entries["Email"].get()
        address = window.entries["Address"].get()
        note = window.entries["Note"].get()
        new_contact = Contact(name, phone, email, address, note)

        if not self.contacts.add_contact(new_contact):
            self.show_warning_message(window, 'Duplicated Name!')
        else:
            self.display()
            self.show_warning_message(window, 'Add Sucuess!')

    # delete a contact which initialize a frame first
    def remove_contact(self):
        newWindow = tk.Toplevel()
        newWindow.title("Select the One You Want To Delete!")

        newWindow.listbox = tk.Listbox(newWindow, width=50)
        newWindow.listbox.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        for name in self.contacts.contact_list:
            newWindow.listbox.insert(tk.END, name.name)

        # delete action function
        def delete_contact():
            selected_indices = newWindow.listbox.curselection()
            if selected_indices:
                selected_index = selected_indices[0]
                selected_contact = self.contacts.contact_list[selected_index]
                self.contacts.remove_contact(selected_contact)
                self.display()
                newWindow.listbox.delete(selected_index)

        newWindow.delete_button = tk.Button(newWindow, text="Delete", 
                                            command=delete_contact)
        
        newWindow.delete_button.grid(row=1, column=0, padx=5, pady=10)

        newWindow.close_button = tk.Button(newWindow, text="Close", command=newWindow.destroy)
        newWindow.close_button.grid(row=1, column=1, columnspan=2)

    # function to make modify true. and select more than one will be warning.
    def modify_one(self):
        selected_indices = self.tree.selection()
        if len(selected_indices) != 1:
            self.show_warning_message(None, "Input Error, Just One Can Be Selected!")
        if selected_indices:
            selected_index = selected_indices[0]
            selected_data = self.tree.item(selected_index)
            name = selected_data["values"][0] 

            index = self.contacts.find(name)

            newWindow = tk.Toplevel()
            newWindow.title("Please Input the Change.")
            labels = ["Name", "Phone", "Email", "Address", "Note"]
            newWindow.entries = {}
            for i, label in enumerate(labels):
                label_widget = tk.Label(newWindow, text=label + ":", padx=5, pady=10)
                label_widget.grid(row=i, column=0)
                entry = tk.Entry(newWindow)
                entry.grid(row=i, column=1, padx=10, pady=10)
                entry.insert(0, selected_data["values"][i])

                newWindow.entries[label] = entry

            def modify(window):
                name = window.entries["Name"].get()
                phone = window.entries["Phone"].get()
                email = window.entries["Email"].get()
                address = window.entries["Address"].get()
                note = window.entries["Note"].get()
                self.contacts.contact_list[index] = Contact(name, phone, email, address, note)
                self.display()
                window.destroy()

            self.add_button = tk.Button(newWindow, text="Modify This", 
                                    command=lambda: modify(newWindow)
                                    ).grid(row=6, column=1, padx=5, pady=5)
            
    # function to store the data in csv file.
    def store_information(self):
        contacts = self.contacts.contact_list
        # iterate the data to store in list, which is covinient for storage
        data = {
            "Name": [contact.name for contact in contacts],
            "Phone": [contact.phone for contact in contacts],
            "Email": [contact.email for contact in contacts],
            "Address": [contact.address for contact in contacts],
            "Note": [contact.note for contact in contacts],
        }
        df = pd.DataFrame(data)
        df.to_csv("./contactsIn.csv", index=False)
        self.show_warning_message(None, "Success!")

    def show_warning_message(self, window, message):
        messagebox.showwarning("Warning", message)
        if window is not None:
            window.destroy()

