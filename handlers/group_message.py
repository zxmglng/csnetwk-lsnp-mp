from models.collections.peers import Peers
from verbose import vprint

def run(data: dict, sender_address: tuple):
    from_id = data.get("FROM", "")
    content = data.get("CONTENT", "")

    if vprint( "RECV", f"{from_id} sent \"{content}\"", sender_ip=sender_address[0], msg_type="GROUP_MESSAGE"):
        print(f'{from_id} sent "{content}"')
