class PhoneRecord:
    name = ""
    phone = ""

    def __init__(self, data_string: str):
        self.parse(data_string)

    def to_string(self):
        return f"{self.name}#{self.phone}"

    def parse(self, data_string: str):
        parsed = data_string.split('#')

        if len(parsed) != 2:
            raise Exception("Invalid data line size")
        else:
            self.name = parsed[0]
            self.phone = parsed[1]
