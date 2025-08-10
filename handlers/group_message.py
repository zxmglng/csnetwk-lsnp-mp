from models.collections.peers import Peers

def run(data: dict, sender_address: tuple):
    from_id = data.get("FROM", "")
    content = data.get("CONTENT", "")

    print(f'{from_id} sent "{content}"')
