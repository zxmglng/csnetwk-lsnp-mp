# 🛰️ [Group 6] Machine Project

This is our implementation of **LSNP** using **Python**, for our CSNETWK machine project.

---

## 🧩 Project Description
**LSNP** is a lightweight, decentralized protocol built entirely on UDP, with no servers, designed for local peer-to-peer communication. It enables peer discovery, messaging, file sharing, group interaction, and gameplay, all secured through token validation. The system sends messages over UDP port 50999, using a UTF-8 key-value format, and delivers them either to all peers (broadcast) or to a specific peer (unicast), depending on the message type.
*— based on "RFC XXXX: Local Social Networking Protocol (LSNP)", authored by Prof. Ann Franchesca Laguna, and provided by Prof. Glenn Rommel Salaguste, 2025*

---

## 🐍 Language & Tools

- **Python 3.10+**
- Modules: `socket`, `threading`, `argparse`, `time`, `base64`, `os`, `uuid`
- Custom-built message parsers and token validators

---

## 🧠 Distribution of Tasks

| Member                | Primary Responsibilities                                                                                      |
|------------------------|---------------------------------------------------------------------------------------------------------------|
| CHUA,&nbsp;Yosh       | UDP socket setup, core messaging (POST, DM, LIKE, FOLLOW), packet loss handling (Game & File), terminal grid display, parsing validation, RFC & project report |
| COLCOL,&nbsp;Massimo  | mDNS discovery, file transfer (OFFER, CHUNK, ACK), message parsing & debug output, inter-group testing       |
| COLOBONG,&nbsp;Franz  | IP address logging, Tic Tac Toe (with recovery), verbose mode                                                 |
| MAGALING,&nbsp;Zoe    | Group creation/messaging, ACK/retry handling, token expiry & IP match, milestone tracking & deliverables     |

---

## 📅 Timeline & Milestones

---

### 🟩 Milestone 1 — Basic Functionality

| Task Description                                            | Assigned Member(s)   | Status         |
|-------------------------------------------------------------|-----------------------|----------------|
| Set up UDP socket on port 50999                             | CHUA                  |     ✅ Done    |
| Broadcast `PING` and `PROFILE` every 300 seconds            | CHUA                  |     ✅ Done    |
| Correctly parse and validate LSNP key-value messages        | CHUA, COLCOL          |     ✅ Done    |
| Log source IP address of each message                       | COLOBONG              |     ✅ Done    |
| Display verbose and non-verbose logs                        | COLOBONG              |     ✅ Done    |
| Organize code structure with MVC pattern                    | MAGALING              |     ✅ Done    |

---

### 🟨 Milestone 2 — Discovery & Messaging

| Task Description                                            | Assigned Member(s)   | Status         |
|-------------------------------------------------------------|-----------------------|----------------|
| Implement `POST`, `DM`, `LIKE`, and `FOLLOW`                | CHUA                  |     ✅ Done    |
| Implement mDNS discovery and peer detection                 | COLCOL                |     ✅ Done    |
| Token validation (expiry, scope, IP match)                  | MAGALING              |     ✅ Done    |
| Display terminal message logs + debug output                | COLCOL, COLOBONG      |     ✅ Done    |
| Inter-group testing with another group                      | COLCOL                |     ✅ Done    |
| Milestone 2 tracking & README updates                       | MAGALING              |     ✅ Done    |

---

### 🟥 Milestone 3 — Advanced Features

| Task Description                                            | Assigned Member(s)   | Status         |
|-------------------------------------------------------------|-----------------------|----------------|
| Implement file transfer: OFFER, CHUNK, RECEIVED, ACK        | COLCOL                |     ✅ Done    |
| Group creation, messaging, and updates                      | MAGALING              |     ✅ Done    |
| Tic Tac Toe game over LSNP with recovery                    | COLOBONG              |     ✅ Done    |
| Token validation: scope checking, expiration, IP source     | MAGALING              |     ✅ Done    |
| Handle ACK-based message retry/resend logic                 | MAGALING              |     ✅ Done    |
| Simulate packet loss in game and file transfer              | CHUA                  |     ✅ Done    |
| Display Tic Tac Toe grid on terminal                        | CHUA, COLOBONG        |     ✅ Done    |
| Log and debug advanced actions in verbose mode              | COLOBONG              |     ✅ Done    |
| Final milestone tracking and project report                 | CHUA, MAGALING        |     ✅ Done    |

---

## 🤖 AI Usage Note

We used **ChatGPT** and **BLACKBOX** throughout the making of this project to help clarify concepts, generate initial code structures, and assist in debugging. All AI-generated content was carefully reviewed, tested, and refined by our group to ensure full comprehension. 

---

## 📐 Build & Run Instructions

```bash
#1 Install Python 3.10+ from their official site:
https://www.python.org/downloads/

#2 Verify installation:
python --version

#3 Download or clone the entire repository/source files to your machine

#4 Open your command prompt and navigate to the directory where the files are saved, for example:
cd path/to/your/project-directory

#5 Run the LSNP program (replace with your IPs and user info):
py main.py


# Notes:
# The program uses custom message parsers and token validators as specified in the project.
# Make sure firewall or VPNs do not block UDP port 50999 for proper network communication.

```

---

## 🗂️ MVC

```bash
csnetwk-lsnp-mp/
│
├── commands/                     # Command interpreter and input routing
│   └── (command files)           # Handles user command parsing and dispatching
│
├── handlers/                     # Message type handlers (profile, ping, dm, post, etc.)
│   └── (individual message handlers)
│
├── models/                       # Data models 
│   └── (model files)
│
├── views/                        # CLI output formatting and display helpers
│   └── (view helper files)
│
├── verbose.py                   # Optional logging/verbose output utility
├── config.py                    # Configuration variables and constants
├── handle_message.py            # Central message parsing and routing logic
├── main.py                      # Entry point: sets up args, initializes, runs main loop
├── udp_socket.py                # UDP socket abstraction (send/receive)
├── command_router.py            # Main command routing logic (moved under commands/ in old version)
├── README.md                    # Project overview and setup instructions


