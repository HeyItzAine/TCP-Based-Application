# TCP-Based-Application
This Application allows for TCP communication between a server and client.

# 🖥️ Server and Client Chat Application
This project is made up of two applications: a server and a client app.

## 📝 Table of Contents
- [Overview](#overview)
- [How It Works](#how-it-works)
- [Setup and Run Instructions](#setup-and-run-instructions)
- [Features](#features)
- [Dependencies](#dependencies)
- [Notes](#notes)

## 📖 Overview
This project consists of:
- **Server App**: Accepts client connections and facilitates communication between the server and multiple clients.
- **Client App**: Connects to the server to send chat messages in real-time.

## ⚙️ How It Works
- The **Server App**:
  - Runs on a chosen port.
  - Displays incoming messages and connections.
- The **Client App**:
  - Connects to the server using the the Server IP, Server Port, and a Custom Name.
  - Displays chat history and allows the user to send messages.

## 🚀 Setup and Run Instructions
### Prerequisites
Ensure you have the latest **Python** and **pip** installed.

### 1. Clone this repository:
```bash
git clone https://github.com/HeyItzAine/TCP-Based-Application.git
cd TCP-Based-Application
```

### 2. Install dependencies:
```bash
pip install Pillow
```

### 3. Run the applications:
- **Server App**:
  ```bash
  python ServerApp.py
  ```
- **Client App**:
  ```bash
  python ClientApp.py
  ```

## ✨ Features
- **Server App**:
  - User-friendly interface
  - Displays connected clients in a terminal UI
  - Displays messages from connected clients.
- **Client App**:
  - User-friendly interface.
  - Real-time messaging to server with error handling.
  - Clicking 'Back' disconnects the client from the server.

## 📦 Dependencies
- **Python libraries**:
  - `tkinter`
  - `socket`
  - `threading`
  - `Pillow` (for image handling)
 
## 📝 Notes
  Upon running Server App, the app will automatically set the Server IP to the computers IPv4 and when running the server on any chosen port (under 2^16 or 65536) the server will start listening for messages from clients that connect to the Server. It is possible to run both the server and client app on the same computer (if using wireshark to monitor packets, this will not show the incoming/outgoing packets unless run on two different computers/IP). For more information feel free to contact the author of this repository.
