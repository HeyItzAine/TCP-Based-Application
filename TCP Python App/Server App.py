import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageFilter
import socket
import threading

def get_local_ip():
    try:
        # Returns the local IP address of the current machine
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(('8.8.8.8', 1))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print("Error getting local IP:", e)
        return "N/A"

class ServerAppUI:
    def __init__(self, master):
        self.master = master
        master.title("Server App")

        # Load and blur background image
        self.bg_image = Image.open("assets/bg.jpg")
        self.bg_blurred = ImageTk.PhotoImage(self.bg_image.filter(ImageFilter.GaussianBlur(15)))

        # Set initial window size to 30% of the maximum size
        max_width = self.master.winfo_screenwidth()
        max_height = self.master.winfo_screenheight()
        self.window_width = int(max_width * 0.3)
        self.window_height = int(max_height * 0.3)
        self.master.geometry(f"{self.window_width}x{self.window_height}")

        # Display the blurred background
        self.bg_label = tk.Label(master, image=self.bg_blurred)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create a canvas for the glass effect
        self.canvas = tk.Canvas(master, highlightthickness=0)
        self.canvas.place(relx=0.5, rely=0.5, anchor="center", width=self.window_width * 0.75, height=self.window_height * 0.75)

        # Draw a rounded rectangle for the glass effect
        self.rounded_rect = self.create_rounded_rectangle(0, 0, self.window_width * 0.75, self.window_height * 0.75, 20, fill="white", stipple="gray50")

        # Center content frame on the glass rectangle
        self.content_frame = tk.Frame(self.canvas, bg="#FFFFFF", highlightthickness=0)
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center", width=self.window_width * 0.6, height=self.window_height * 0.6)

        # Server status light
        self.status_light = tk.Label(self.content_frame, width=2, height=2, bg="red")
        self.status_light.grid(row=0, column=0, padx=10, pady=5)

        # Server IP label
        self.ip_label = tk.Label(self.content_frame, text=f"Server IP: {get_local_ip()}", fg="#333333", font=("Helvetica", 10, "bold"))
        self.ip_label.grid(row=0, column=1, columnspan=2, sticky="w")

        # Port input
        self.port_label = tk.Label(self.content_frame, text="Port:", fg="#333333", font=("Helvetica", 10, "bold"))
        self.port_label.grid(row=1, column=0, sticky="e", padx=5)
        self.port_entry = ttk.Entry(self.content_frame)
        self.port_entry.grid(row=1, column=1, columnspan=2, pady=5, sticky="ew")

        # Start/Stop server button
        self.server_button = tk.Button(self.content_frame, text="Start Server", command=self.start_stop_server, bg="#007BFF", fg="#FFFFFF", activebackground="#0056b3", font=("Helvetica", 12, "bold"))
        self.server_button.grid(row=2, column=0, columnspan=3, pady=10, sticky="ew")
        self.server_button.bind("<Enter>", lambda e: self.server_button.configure(bg="#0056b3"))
        self.server_button.bind("<Leave>", lambda e: self.server_button.configure(bg="#007BFF"))

        # Terminal output box (initial setup)
        self.terminal_frame = tk.Frame(master, bg="#111111")
        self.terminal_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))  # Added padding

        self.terminal_text = tk.Text(self.terminal_frame, bg="#111111", fg="#FFFFFF", font=("Courier", 10), wrap=tk.WORD)  # Removed fixed height
        self.terminal_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.terminal_scrollbar = ttk.Scrollbar(self.terminal_frame, command=self.terminal_text.yview)
        self.terminal_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.terminal_text.config(yscrollcommand=self.terminal_scrollbar.set)



        self.is_server_running = False
        self.stop_new_connections = False  # <-- Added this line to initialize the attribute
        self.server_socket = None
        self.connections = []
        self.total_connections = 0


        # Resize handling
        master.bind("<Configure>", self.on_resize)

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1 + radius, y1,
            x1 + radius, y1,
            x2 - radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1 + radius,
            x1, y1,
        ]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)

    def start_stop_server(self):
        if not self.is_server_running:
            try:
                port = int(self.port_entry.get())
                self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_socket.bind((get_local_ip(), port))
                self.server_socket.listen(5)
                self.stop_new_connections = False  # Initialize stop flag
                new_connections_thread = threading.Thread(target=self.new_connections, args=(self.server_socket,), daemon=True)
                new_connections_thread.start()
                self.is_server_running = True
                self.status_light.configure(bg="green")
                self.server_button.configure(text="Stop Server")
                self.terminal_text.insert(tk.END, f"Server started on port {port}\n")
                print("Server started on port", port)
            except Exception as e:
                self.terminal_text.insert(tk.END, f"Error starting server: {e}\n")
        else:
            self.stop_new_connections = True  # Signal the thread to stop
            if self.server_socket:
                self.server_socket.close()  # Close the server socket
                self.is_server_running = False
                self.status_light.configure(bg="red")
                self.server_button.configure(text="Start Server")
                self.terminal_text.insert(tk.END, "Server stopped\n")
                print("Server stopped")
            
            # Close all existing connections
            for client in self.connections:
                client.socket.close()  # Close each client socket

    def on_resize(self, event):
        # Resize the canvas and components proportionally based on window size
        new_width = min(event.width, self.master.winfo_screenwidth())
        new_height = min(event.height, self.master.winfo_screenheight())
        self.canvas.config(width=new_width * 0.75, height=new_height * 0.75)

        # Update terminal height to be 20% of the new window height
        terminal_height = int(new_height * 0.20)  # Use 20% of the window height
        self.terminal_frame.config(height=terminal_height)  # Set height of terminal frame
        self.terminal_text.config(height=terminal_height // 10)  # Adjust text widget height as lines (10 pixels per line is typical)

    def new_connections(self, server_socket):
        while not self.stop_new_connections:  # Check the stop flag
            try:
                sock, address = server_socket.accept()
                self.total_connections += 1
                self.connections.append(Client(sock, address, self.total_connections, "Name", True, self))
                self.connections[-1].start()
                self.terminal_text.insert(tk.END, f"New connection at ID {self.total_connections}\n")
            except OSError as e:
                # This will catch the error when server_socket is closed
                if str(e) == "[WinError 10038] An operation was attempted on something that is not a socket":
                    break  # Exit the loop if the socket is no longer valid

class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal, ui):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal
        self.ui = ui

    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(32)
            except:
                self.ui.terminal_text.insert(tk.END, f"Client {self.address} has disconnected\n")
                self.signal = False
                self.ui.connections.remove(self)
                break
            if data != b'':
                self.ui.terminal_text.insert(tk.END, f"ID {self.id}: {data.decode('utf-8')}\n")
                for client in self.ui.connections:
                    if client.id != self.id:
                        client.socket.sendall(data)

def main():
    root = tk.Tk()
    app = ServerAppUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
