import os

_sessions = {}

def run(data: dict, sender_address: tuple):
    file_id = data.get("FILE_ID")
    if not file_id:
        return

    _sessions[file_id] = {
        "meta": data,
        "chunks": {},
        "received": 0
    }

    print(f"[file_offer] Incoming file '{data.get('FILENAME')}' "
          f"({data.get('FILE_SIZE')} bytes, {data.get('CHUNKS')} chunks) from {data.get('FROM')}")