import json
from collections import UserDict

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Введіть ім'я та номер телефону, будь ласка."
        except KeyError as e:
            return f"Контакт '{e.args[0]}' не знайдено."
        except IndexError:
            return "Невірний формат команди. Будь ласка, використовуйте 'додати [ім'я] [телефон]' або 'змінити [ім'я] [новий телефон]'."

    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

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

@input_error
def add_contact(args, contacts):
    if len(args) != 2:
        raise IndexError
    name, phone = args
    contacts[name] = phone
    return "Контакт додано."

@input_error
def change_contact(args, contacts):
    if len(args) != 2:
        raise IndexError
    name, new_phone = args
    if name in contacts:
        contacts[name] = new_phone
        return "Контакт оновлено."
    else:
        raise KeyError(name)

@input_error
def show_phone(args, contacts):
    if len(args) != 1:
        raise IndexError
    name = args[0]
    if name in contacts:
        return contacts[name]
    else:
        raise KeyError(name)

@input_error
def show_all(contacts):
    if not contacts:
        raise IndexError
    result = "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])
    return result

def main():
    contacts = {}
    print("Ласкаво просимо до бота-асистента!")
    while True:
        user_input = input("Введіть команду: ")
        command, args = parse_input(user_input)

        if command in ["закрити", "вихід"]:
            print("До побачення!")
            break
        elif command == "привіт":
            print("Як я можу вам допомогти?")
        elif command == "додати":
            print(add_contact(args, contacts))
        elif command == "змінити":
            print(change_contact(args, contacts))
        elif command == "телефон":
            result = show_phone(args, contacts)
            print(result)
        elif command == "всі":
            result = show_all(contacts)
            print(result)
        else:
            print("Невірна команда.")

if __name__ == "__main__":
    main()