import os
import logging

log_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(log_dir, "logs.txt")

class ClientIDAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return f"[client_id={self.extra.get('client_id')}] {msg}", kwargs

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("udp")

def get_client_logger(client_id):
    return ClientIDAdapter(logger, {"client_id": client_id})