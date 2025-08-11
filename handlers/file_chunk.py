import base64
from views.message import Message
from models.collections import my_profile
import os

from .file_offer import _sessions  # share session data

OUT_DIR = "received_files"
os.makedirs(OUT_DIR, exist_ok=True)

def run(data: dict, sender_address: tuple):
    file_id = data.get("FILE_ID")
    if file_id not in _sessions:
        return

    sess = _sessions[file_id]
    idx = int(data.get("CHUNK_NUM", -1))
    chunk_data = base64.b64decode(data.get("DATA", ""))

    if idx not in sess["chunks"]:
        sess["chunks"][idx] = chunk_data
        sess["received"] += 1
        total = int(sess["meta"]["CHUNKS"])
        print(f"[file_chunk] Received chunk {idx+1}/{total}")

        if sess["received"] == total:
            _assemble_file(file_id, sender_address)

def _assemble_file(file_id, sender_address):
    from udp_socket import UDPSocket
    meta = _sessions[file_id]["meta"]
    total = int(meta["CHUNKS"])
    filename = meta["FILENAME"]
    filepath = os.path.join(OUT_DIR, filename)

    with open(filepath, "wb") as f:
        for i in range(total):
            f.write(_sessions[file_id]["chunks"][i])

    print(f"[file_chunk] File assembled → {filepath}")

    profile = my_profile.get_profile()
    if not profile:
        return

    ack = {
        "TYPE": "FILE_RECEIVED",
        "FILE_ID": file_id,
        "TO": meta["FROM"],
        "FROM": profile.USER_ID
    }
    UDPSocket().send(Message.raw_message(ack), sender_address)
    del _sessions[file_id]