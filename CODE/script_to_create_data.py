import pandas as pd

# create data script.
data = {
    'Name': ['Alice Lee', 'Eric Lee', 'Jade Lee'],
    'Phone': ['86136123456', '86136123456', '86136123456'],
    'Email': ['123@gmail.com', '123@gmail.com', '123@gmail.com'],
    'Address': ['Street Armstrong, No5', 'Street Armstrong, No5', 'Street Armstrong, No5'],
    'Note': ['Mother', 'Father', 'Sister']
}

# Create DataFrame
df = pd.DataFrame(data)

# Store the data in CSV file.
df.to_csv('contactsIn.csv', index=False)
