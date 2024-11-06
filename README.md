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
  - Displays connected clients.
- **Client App**:
  - User-friendly interface.
  - Real-time messaging to server with error handling.

## 📦 Dependencies
- **Python libraries**:
  - `tkinter`
  - `socket`
  - `threading`
  - `Pillow` (for image handling)
