def run(data: dict, sender_address: tuple):
    file_id = data.get("FILE_ID")
    print(f"[file_received] Receiver confirmed file {file_id} was received.")