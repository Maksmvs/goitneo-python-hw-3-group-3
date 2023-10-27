import json
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def get_name(self):
        return self.value

    def set_name(self, name):
        self.value = name

class Phone(Field):
    def get_name(self):
        return self.value

    def set_name(self, phone):
        self.value = phone

    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Недійсний формат номера телефону")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        
        if not self.is_valid_birthday(value):
            raise ValueError("Невірний формат дня народження (DD.MM.YYYY)")
        super().__init__(value)

    def is_valid_birthday(self, value):
        try:
            day, month, year = map(int, value.split('.'))
            return 1 <= month <= 12 and 1 <= day <= 31
        except (ValueError, IndexError):
            return False

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.get_name() != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.get_name() == old_phone:
                phone.set_name(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.get_name() == phone:
                return p.get_name()

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = "; ".join([str(p) for p in self.phones])
        birthday = f", День народження: {self.birthday}" if self.birthday else ""
        return f"Ім'я контакту: {self.name.get_name()}, номери телефонів: {phones}{birthday}"

class AddressBook(UserDict):
    def save_to_file(self, filename):
        data_to_save = {}
        for name, record in self.data.items():
            data_to_save[name] = {
                'name': record.name.get_name(),
                'phones': [str(phone) for phone in record.phones],
                'birthday': str(record.birthday) if record.birthday else None
            }

        with open(filename, 'w') as file:
            json.dump(data_to_save, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)

            self.data = {}
            for name, info in data.items():
                record = Record(info['name'])
                for phone in info['phones']:
                    record.add_phone(phone)
                if info['birthday']:
                    record.add_birthday(info['birthday'])
                self.add_record(record)
        except FileNotFoundError:
            self.data = {}

    def add_record(self, record):
        self.data[record.name.get_name()] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_birthdays_per_week(self):
        pass

if __name__ == "__main__":
    book = AddressBook()
    book.load_from_file("address_book.json")
    new_contact = Record("Аліса")
    new_contact.add_phone("1234567890")
    new_contact.add_birthday("01.01.1990")
    book.add_record(new_contact)
    book.find("Аліса").edit_phone("1234567890", "9999999999")
    book.delete("Джон")


    john = book.find("Джон")

  
    book.save_to_file("address_book.json")


    for name, record in book.data.items():
        print(record)