from config import MESSAGE_TERMINATOR

class Message:
    
    @staticmethod
    def raw_message(data: dict) -> str:
        lines = [f"{key}: {value}" for key, value in data.items()]
        return "\n".join(lines) + MESSAGE_TERMINATOR

    @staticmethod
    def parsed_message(raw: str) -> dict:
        lines = raw.strip().splitlines()
        data = {}
        for line in lines:
            if ": " in line:
                key, value = line.split(": ", 1)
                data[key.strip()] = value.strip()
        return data