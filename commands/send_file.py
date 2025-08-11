from views.message import Message
from udp_socket import UDPSocket
from models.collections import my_profile
import base64
import time
from pathlib import Path
import config
from verbose import vprint

CHUNK_SIZE = 1024  # bytes

def run(args: list):
    """
    Usage: send_file <receiver_ip> <file_path>
    """
    if len(args) < 2:
        print("Usage: send_file <receiver_ip> <file_path>")
        return

    receiver_ip = args[0]
    file_path = Path(args[1])

    if not file_path.exists():
        print(f"[send_file] File not found: {file_path}")
        return

    profile = my_profile.get_profile()
    if not profile:
        print("[send_file] No profile found.")
        return

    data = file_path.read_bytes()
    file_id = f"{profile.USER_ID}-{int(time.time())}"
    total_chunks = (len(data) + CHUNK_SIZE - 1) // CHUNK_SIZE

    # 1) Send FILE_OFFER
    offer = {
        "TYPE": "FILE_OFFER",
        "FROM": profile.USER_ID,
        "FILE_ID": file_id,
        "FILENAME": file_path.name,
        "FILE_SIZE": len(data),
        "CHUNKS": total_chunks
    }
    raw_offer = Message.raw_message(offer)
    UDPSocket().send(raw_offer, (receiver_ip, config.PORT))

    if vprint("SEND",f"FILE_OFFER sent to {receiver_ip}: {file_path.name} ({len(data)} bytes), {total_chunks} chunks", sender_ip=receiver_ip, msg_type="FILE_OFFER"):
        print(f"[send_file] Offered {file_path.name} ({len(data)} bytes) in {total_chunks} chunks")

    # 2) Send FILE_CHUNKs
    for idx in range(total_chunks):
        chunk = data[idx*CHUNK_SIZE:(idx+1)*CHUNK_SIZE]
        payload = base64.b64encode(chunk).decode()
        msg = {
            "TYPE": "FILE_CHUNK",
            "FILE_ID": file_id,
            "CHUNK_NUM": idx,
            "DATA": payload
        }
        raw_msg = Message.raw_message(msg)
        UDPSocket().send(raw_msg, (receiver_ip, config.PORT))

        if vprint("SEND", f"FILE_CHUNK {idx+1}/{total_chunks} sent to {receiver_ip} for FILE_ID {file_id}", sender_ip=receiver_ip, msg_type="FILE_CHUNK"):
            print(f"[send_file] Sent chunk {idx+1}/{total_chunks}")