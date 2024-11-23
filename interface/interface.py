import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from functools import partial
import numpy as np

class GraphApp:
    def __init__(self, root):
        self.root = root

        # Create the first plot
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Create a button to refresh the graph
        self.refresh_button = ttk.Button(root, text="Refresh Graph", command=self.refresh_graph)
        self.refresh_button.pack(pady=10)

        # Initially plot something
        self.plot_graph()

    def plot_graph(self):
        #to do fct to plot the graph


        # Example plot (sine wave)
        x = np.linspace(0, 10, 100) + np.random.rand(100)
        y = np.sin(x)
        self.ax.plot(x, y)
        self.canvas.draw()

    def refresh_graph(self):
        # Clear the current plot
        self.ax.clear()

        # Replot the graph (can modify this to plot new data)
        self.plot_graph()


def clear_content_frame(button_frame, main_frame):
    for widget in button_frame.winfo_children():
        widget.pack_forget()
    for widget in main_frame.winfo_children():
        widget.pack_forget()

def display_translate_window(button_frame, main_frame):
    clear_content_frame(button_frame, main_frame)
    input_box = tk.Text(button_frame, height=16, width=100)
    input_box.pack(padx=10, pady=10)

    output_box = tk.Text(button_frame, height=16, width=100)
    output_box.config(state="disabled")
    output_box.pack(padx=10, pady=10)

    def on_submit():
        user_text = input_box.get(1.0, tk.END)
        # to do : translate
        output_box.config(state="normal")
        output_box.insert(tk.END, user_text)
        output_box.config(state="disabled")


    def on_return():
        rebuild_main_frame(button_frame, main_frame)

    submit_button = ttk.Button(button_frame, text="Submit", command=on_submit, width=30)
    submit_button.pack(side=tk.LEFT, expand=True, padx=20, pady=20)

    return_button = ttk.Button(button_frame, text="Return", command=on_return, width=30)
    return_button.pack(side=tk.LEFT, expand=True, padx=20, pady=20)

def display_message(chat_display, message, sender):
    # Add a message to the chat display
    chat_display.config(state="normal")  # Enable editing to insert text

    if sender == "user":
        # Right-aligned user messages
        chat_display.insert("end", f"{message:>50}\n", "user")
    else:
        # Left-aligned bot messages
        chat_display.insert("end", f"{message}\n", "bot")

    chat_display.tag_config("user", justify="right", foreground="blue")
    chat_display.tag_config("bot", justify="left", foreground="green")
    chat_display.see("end")  # Scroll to the end
    chat_display.config(state="disabled")  # Disable editing after inserting text


def send_message(user_input, chat_display):
    # Handle sending a message
    user_message = user_input.get()
    if user_message.strip():  # If not empty
        display_message(chat_display, user_message, "user")  # Display user's message
        user_input.delete(0, "end")  # Clear input field

        # Simulate a bot response
        bot_response = "lalalala je suis le bot"
        display_message(chat_display, bot_response, "bot")

def display_dialogue_window(button_frame, main_frame):

    clear_content_frame(button_frame, main_frame)

    # Chat display
    chat_display = tk.Text(main_frame, wrap="word", state="disabled", height=20, width=50)
    chat_display.pack(padx=10, pady=10, fill="both", expand=True)

    # User input frame
    input_frame = ttk.Frame(main_frame)
    input_frame.pack(fill="x", padx=10, pady=5)

    # Input box for user message
    user_input = ttk.Entry(input_frame, width=40)
    user_input.pack(side="left", fill="x", expand=True, padx=5)

    # Send button
    send_button = ttk.Button(input_frame, text="Send", command=partial(send_message, user_input, chat_display))
    send_button.pack(side="right", padx=5)

    def on_return():
        rebuild_main_frame(button_frame, main_frame)

    return_button = ttk.Button(button_frame, text="Return", command=on_return, width=30)
    return_button.pack(side=tk.LEFT, expand=True, padx=20, pady=20)

def process_and_update(result_label, graph):

    # do the update of the knowledge graph
    process_success = True

    if process_success:
        result_label.config(text="✅ Process Succeeded", fg="green")
    else:
        result_label.config(text="❌ Process Failed", fg="red")

    #refresh the graph :
    if process_success :
        graph.refresh_graph()

def rebuild_main_frame(button_frame, main_frame):
    """Rebuilds the main interface with two buttons and a graph."""
    for widget in button_frame.winfo_children():
        widget.pack_forget()
    for widget in main_frame.winfo_children():
        widget.pack_forget()

    btn1 = ttk.Button(button_frame, text="Translation mode",
                      command=lambda: display_translate_window(button_frame, main_frame))
    btn1.pack(side=tk.LEFT, padx=5)

    btn2 = ttk.Button(button_frame, text="Conversation mode",
                      command=lambda: display_dialogue_window(button_frame, main_frame))
    btn2.pack(side=tk.LEFT, padx=5)

    # Label to show the result (cross or check)
    result_label = tk.Label(root, text="", font=("Helvetica", 16))
    result_label.pack(side=tk.LEFT, pady=5)

    # Graph
    g = GraphApp(main_frame)

    # Button to process and update the result
    process_button = tk.Button(button_frame, text="Send to Big Brother", command=partial(process_and_update, result_label, g))
    process_button.pack(pady=10)


# Main Tkinter setup
root = tk.Tk()
root.title("Button and Graph Interface")
root.geometry("1300x750")

# Frames
button_frame = ttk.Frame(root, height=20)
button_frame.pack(side=tk.TOP, pady=20)

main_frame = ttk.Frame(root)
main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Buttons
rebuild_main_frame(button_frame, main_frame)

root.mainloop()