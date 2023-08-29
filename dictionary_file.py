import os

from phone_record import PhoneRecord


class DictionaryFile:
    lines = list()
    records = list()

    def __init__(self):
        mode = "w+"
        if os.path.exists('phone_dictionary.txt'):
            mode = "r"

        file = open('phone_dictionary.txt', mode)
        self.lines = file.readlines()

        for line in self.lines:
            self.records.append(PhoneRecord(line))

        file.close()

    def get(self, index):
        if len(self.records) < index:
            raise Exception('Invalid index')
        else:
            return self.records[index]

    def find(self, phone):
        for record in self.records:
            if record.phone == phone:
                return record.phone

        return None

    def clean(self):
        self.records.clear()
        self.update()

    def update(self):
        os.remove('phone_dictionary.txt')
        file = open('phone_dictionary.txt', 'w+')
        self.lines.clear()
        for record in self.records:
            self.lines.append(record.to_string())

        file.writelines(self.lines)
        file.close()