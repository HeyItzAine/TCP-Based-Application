import tkinter as tk
import socket
import threading
import sys
from PIL import Image, ImageTk
import os
import tkinter.messagebox as messagebox


class ChatApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chat Application")
        self.resizable(True, True)

        # Load the background image
        bg_path = os.path.join("assets", "bg.jpg")
        self.bg_image = Image.open(bg_path)
        self.bg_image_width, self.bg_image_height = self.bg_image.size
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Set the window size to 30% of the background size
        initial_width = int(self.bg_image_width * 0.3)
        initial_height = int(self.bg_image_height * 0.3)
        self.geometry(f"{initial_width}x{initial_height}")
        self.maxsize(self.bg_image_width, self.bg_image_height)

        # Create a label for the background image
        self.bg_label = tk.Label(self, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create the connection page
        self.connection_page = ConnectionPage(self)
        self.connection_page.place(relx=0.5, rely=0.5, anchor="center")

        # Create the chat page
        self.chat_page = ChatPage(self)

        # Bind the resize event to update sizes
        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        # Update the size of all elements based on the new window size
        self.update_sizes()

    def update_sizes(self):
        # Calculate the scale factor based on the current size
        width_ratio = self.winfo_width() / self.bg_image_width
        height_ratio = self.winfo_height() / self.bg_image_height
        scale_factor = min(width_ratio, height_ratio)

        # Resize background
        resized_width = int(self.bg_image_width * scale_factor)
        resized_height = int(self.bg_image_height * scale_factor)
        resized_bg = self.bg_image.resize((resized_width, resized_height), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(resized_bg)
        self.bg_label.config(image=self.bg_photo)

        # Resize connection page elements
        self.connection_page.update_sizes(scale_factor)

        # Resize chat page elements
        self.chat_page.update_sizes(scale_factor)

    def show_chat_page(self):
        self.connection_page.place_forget()
        self.chat_page.place(relx=0.5, rely=0.5, anchor="center")

class ConnectionPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Create the title label
        self.title_label = tk.Label(self, text="Connect to Server", font=("Arial", 24, 'bold'))
        self.title_label.pack(pady=(20, 10))

        # Create the host and port entry fields
        self.host_label = tk.Label(self, text="Host:", font=("Arial", 16, 'bold'))
        self.host_label.pack(anchor="w", padx=10)

        self.host_entry = tk.Entry(self, font=("Arial", 16, 'bold'))
        self.host_entry.pack(pady=10, padx=10)

        self.port_label = tk.Label(self, text="Port:", font=("Arial", 16, 'bold'))
        self.port_label.pack(anchor="w", padx=10)

        self.port_entry = tk.Entry(self, font=("Arial", 16, 'bold'))
        self.port_entry.pack(pady=10, padx=10)

        # Create the name entry field
        self.name_label = tk.Label(self, text="Your Name:", font=("Arial", 16, 'bold'))
        self.name_label.pack(anchor="w", padx=10)

        self.name_entry = tk.Entry(self, font=("Arial", 16, 'bold'))
        self.name_entry.pack(pady=10, padx=10)

        # Create the connect button
        self.connect_button = tk.Button(self, text="Connect to Server", font=("Arial", 16, 'bold'), command=self.connect_to_server)
        self.connect_button.pack(pady=(20, 10))

    def update_sizes(self, scale_factor):
        # Update font sizes and other element sizes based on the scale factor
        font_size_title = int(24 * scale_factor)
        font_size_entry = int(16 * scale_factor)
        self.title_label.config(font=("Arial", font_size_title, 'bold'))
        self.host_label.config(font=("Arial", font_size_entry, 'bold'))
        self.host_entry.config(font=("Arial", font_size_entry, 'bold'))
        self.port_label.config(font=("Arial", font_size_entry, 'bold'))
        self.port_entry.config(font=("Arial", font_size_entry, 'bold'))
        self.name_label.config(font=("Arial", font_size_entry, 'bold'))
        self.name_entry.config(font=("Arial", font_size_entry, 'bold'))
        self.connect_button.config(font=("Arial", font_size_entry, 'bold'))

    def connect_to_server(self):
        host = self.host_entry.get()
        port = int(self.port_entry.get())
        self.username = self.name_entry.get()

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
            self.parent.show_chat_page()
            self.parent.chat_page.update_connection_info(host, port, self.username)
            
            # Save the thread reference for later use
            self.parent.chat_page.receive_thread = threading.Thread(target=self.receive, args=(self.sock, True))
            self.parent.chat_page.receive_thread.start()
        except Exception as e:
            # Show an error message box instead of using input()
            messagebox.showerror("Connection Error", f"Could not make a connection to the server:\n{e}")

    def receive(self, socket, signal):
        while signal:
            try:
                data = socket.recv(1024)  # Buffer size increased for larger messages
                message = str(data.decode("utf-8"))
                self.parent.chat_page.display_message(message)
                if message == "ACK":
                    self.show_notification("Message Received")
            except:
                print("You have been disconnected from the server")
                signal = False
                break

    def show_notification(self, message):
        notification = tk.Toplevel(self)
        notification.title("Notification")
        notification.geometry("240x80+{}+{}".format(self.winfo_x() + self.winfo_width() - 260, self.winfo_y() + self.winfo_height() - 100))
        notification.resizable(False, False)
        notification.attributes("-topmost", True)

        label = tk.Label(notification, text=message, font=("Arial", 16))
        label.pack(pady=20)

class ChatPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Create the chat area
        self.chat_area = tk.Text(self, font=("Arial", 14), height=15, width=50)
        self.chat_area.pack(padx=20, pady=10)
        self.chat_area.config(state="disabled")

        # Create a frame for the message entry and buttons
        self.entry_frame = tk.Frame(self)
        self.entry_frame.pack(pady=10)

        # Create the message entry
        self.message_entry = tk.Entry(self.entry_frame, font=("Arial", 14), width=40)
        self.message_entry.pack(side="left", padx=10)

        # Create the send button
        self.send_button = tk.Button(self.entry_frame, text="\u2709", font=("Arial", 16, 'bold'), command=self.send_message)
        self.send_button.pack(side="left", padx=5)

        # Create the back button
        self.back_button = tk.Button(self.entry_frame, text="Back", font=("Arial", 16, 'bold'), command=self.go_back)
        self.back_button.pack(side="left", padx=5)

        # Connection info label
        self.connection_info_label = tk.Label(self, text="", font=("Arial", 16, 'bold'))
        self.connection_info_label.pack(pady=10)

    def update_sizes(self, scale_factor):
        # Update font sizes based on the scale factor
        font_size_chat = int(14 * scale_factor)
        font_size_entry = int(14 * scale_factor)
        font_size_button = int(16 * scale_factor)

        self.chat_area.config(font=("Arial", font_size_chat))
        self.message_entry.config(font=("Arial", font_size_entry))
        self.send_button.config(font=("Arial", font_size_button))
        self.back_button.config(font=("Arial", font_size_button))
        self.connection_info_label.config(font=("Arial", font_size_button))

    def send_message(self):
        message = self.message_entry.get()
        if message:
            # Send the message prefixed by the username
            full_message = f"{self.parent.connection_page.username}: {message}"
            self.parent.connection_page.sock.sendall(str.encode(full_message))
            self.message_entry.delete(0, tk.END)
            self.display_message(full_message)

    def display_message(self, message):
        self.chat_area.config(state="normal")
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state="disabled")
        self.chat_area.see(tk.END)  # Scroll to the end

    def update_connection_info(self, host, port, username):
        self.connection_info_label.config(text=f"Connected to {host}:{port} as {username}")

    def go_back(self):
        # Disconnect from the server before going back
        if hasattr(self.parent.connection_page, 'sock'):
            self.parent.connection_page.sock.close()
        
        # Terminate the receive thread if it's running
        if hasattr(self.parent.connection_page, 'receive_thread'):
            self.parent.connection_page.receive_thread.join(timeout=1)

        self.parent.connection_page.place(relx=0.5, rely=0.5, anchor="center")
        self.place_forget()  # Change from self.grid_forget() to self.place_forget()


if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()
