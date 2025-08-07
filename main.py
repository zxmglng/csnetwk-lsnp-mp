from udp_socket import UDPSocket
from command_router import send
import config
from commands.ping import auto_ping_loop
from models.collections.peers import Peers 
import threading
    
def main():
    
    config.USERNAME = input("Enter your username: ").strip()
    send("profile", [])
    
    threading.Thread(target=auto_ping_loop, daemon=True).start()
    threading.Thread(target=Peers().start_auto_cleanup, daemon=True).start()
    
    udp = UDPSocket()
    udp.receive_loop()

    while True:
        try:
            user_input = input("> ").strip()
            if user_input.lower() == "exit":
                break
            if not user_input:
                continue

            parts = user_input.split()
            command = parts[0]
            args = parts[1:]

            send(command, args)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"⚠️ Error: {e}")

    udp.close()
    print("Closing udp")

if __name__ == "__main__":
    main()
