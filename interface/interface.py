import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
from functools import partial


class AudioPanel:
    """Class to handle the audio panel functionality."""

    def __init__(self, parent_frame, rebuild_main_frame):
        self.parent_frame = parent_frame
        self.stream = None
        self.running = False
        self.figure, self.ax = plt.subplots(figsize=(5, 2))
        self.ax.set_ylim([-1, 1])
        self.ax.set_xlim([0, 1024])
        self.line, = self.ax.plot([], [], lw=2)
        self.canvas = FigureCanvasTkAgg(self.figure, self.parent_frame)
        self.canvas.get_tk_widget().pack()

        # Buttons
        start_button = ttk.Button(
            self.parent_frame, text="Start Speaking", command=self.start_audio_stream
        )
        start_button.pack(side=tk.LEFT, padx=5)

        stop_button = ttk.Button(
            self.parent_frame, text="Stop Speaking", command=self.stop_audio_stream
        )
        stop_button.pack(side=tk.RIGHT, padx=5)

        return_button = ttk.Button(
            self.parent_frame, text="return", command= rebuild_main_frame
        )
        return_button.pack(side=tk.RIGHT, padx=5)

    def audio_callback(self, indata, frames, time, status):
        """Audio callback function to update the waveform."""
        if not self.running:
            return
        data = indata[:, 0]
        self.line.set_ydata(data)
        self.line.set_xdata(np.arange(len(data)))
        self.ax.set_xlim(0, len(data))
        self.canvas.draw()

    def start_audio_stream(self):
        """Start the audio stream."""
        self.running = True
        self.stream = sd.InputStream(
            callback=self.audio_callback, channels=1, samplerate=44100, blocksize=1024
        )
        self.stream.start()

    def stop_audio_stream(self):
        """Stop the audio stream."""
        self.running = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None


class GraphApp:
    """Class to handle graph display and updates."""

    def __init__(self, root):
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Plot the initial graph
        self.plot_graph()

    def plot_graph(self):
        """Plot the graph."""
        x = np.linspace(0, 10, 100) + np.random.rand(100)
        y = np.sin(x)
        self.ax.plot(x, y)
        self.canvas.draw()

    def refresh_graph(self):
        """Refresh the graph."""
        self.ax.clear()
        self.plot_graph()


class DialogueWindow:
    """Class to handle dialogue window functionality."""

    def __init__(self, main_frame):
        self.main_frame = main_frame

    def display(self, rebuild_main_frame):
        """Display the dialogue window."""
        chat_display = tk.Text(
            self.main_frame, wrap="word", state="disabled", height=20, width=50
        )
        chat_display.pack(padx=10, pady=10, fill="both", expand=True)

        input_frame = ttk.Frame(self.main_frame)
        input_frame.pack(fill="x", padx=10, pady=5)

        user_input = ttk.Entry(input_frame, width=40)
        user_input.pack(side="left", fill="x", expand=True, padx=5)

        send_button = ttk.Button(
            input_frame,
            text="Send",
            command=partial(self.send_message, user_input, chat_display),
        )
        send_button.pack(side="right", padx=5)

        return_button = ttk.Button(
            self.main_frame, text="return", command= rebuild_main_frame
        )
        return_button.pack(side=tk.RIGHT, padx=5)

    def send_message(self, user_input, chat_display):
        """Handle sending and receiving messages."""
        user_message = user_input.get()
        if user_message.strip():
            self.display_message(chat_display, user_message, "user")
            user_input.delete(0, "end")
            bot_response = "lalalala je suis le bot"
            self.display_message(chat_display, bot_response, "bot")

    def display_message(self, chat_display, message, sender):
        """Display messages in the chat."""
        chat_display.config(state="normal")
        if sender == "user":
            chat_display.insert("end", f"{message:>50}\n", "user")
        else:
            chat_display.insert("end", f"{message}\n", "bot")
        chat_display.tag_config("user", justify="right", foreground="blue")
        chat_display.tag_config("bot", justify="left", foreground="green")
        chat_display.see("end")
        chat_display.config(state="disabled")


class MainApp:
    """Main application class."""

    def __init__(self, root):
        self.root = root
        self.root.title("Button and Graph Interface")
        self.root.geometry("1300x750")

        self.button_frame = ttk.Frame(self.root, height=20)
        self.button_frame.pack(side=tk.TOP, pady=20)

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.rebuild_main_frame()

    def clear_content_frame(self):
        """Clear all widgets in the frames."""
        for widget in self.button_frame.winfo_children():
            widget.pack_forget()
        for widget in self.main_frame.winfo_children():
            widget.pack_forget()

    def rebuild_main_frame(self):
        """Rebuild the main interface with buttons and a graph."""
        self.clear_content_frame()

        btn1 = ttk.Button(
            self.button_frame,
            text="Translation Mode",
            command=self.display_translate_window,
        )
        btn1.pack(side=tk.LEFT, padx=5)

        btn2 = ttk.Button(
            self.button_frame,
            text="Conversation Mode",
            command=self.display_dialogue_window,
        )
        btn2.pack(side=tk.LEFT, padx=5)

        result_label = tk.Label(self.root, text="", font=("Helvetica", 16))
        result_label.pack(side=tk.LEFT, pady=5)

        graph = GraphApp(self.main_frame)

        process_button = tk.Button(
            self.button_frame,
            text="Send to Big Brother",
            command=partial(self.process_and_update, result_label, graph),
        )
        process_button.pack(pady=10)

        audio_button = tk.Button(
            self.button_frame, text="Speaking", command=self.display_audio_panel
        )
        audio_button.pack(pady=10)

        refresh_button = tk.Button(
            self.button_frame, text="refresh graph", command=graph.refresh_graph
        )
        refresh_button.pack(pady=10)

    def display_audio_panel(self):
        """Display the audio panel."""
        self.clear_content_frame()
        AudioPanel(self.main_frame, self.rebuild_main_frame)

    def display_dialogue_window(self):
        """Display the dialogue window."""
        self.clear_content_frame()
        DialogueWindow(self.main_frame).display(self.rebuild_main_frame)

    def on_submit(self, input_box, output_box):
        user_text = input_box.get(1.0, tk.END)
        # to do : translate
        output_box.config(state="normal")
        output_box.insert(tk.END, user_text)
        output_box.config(state="disabled")

    def display_translate_window(self):
        """Display the translation window."""
        self.clear_content_frame()
        input_box = tk.Text(self.button_frame, height=16, width=100)
        input_box.pack(padx=10, pady=10)

        output_box = tk.Text(self.button_frame, height=16, width=100)
        output_box.config(state="disabled")
        output_box.pack(padx=10, pady=10)

        return_button = ttk.Button(
            self.button_frame, text="submit", command=partial(self.on_submit, input_box, output_box)
        )
        return_button.pack(side=tk.RIGHT, padx=5)

        return_button = ttk.Button(
            self.button_frame, text="return", command= self.rebuild_main_frame
        )
        return_button.pack(side=tk.RIGHT, padx=5)

    def process_and_update(self, result_label, graph):
        """Process and update the graph."""
        result_label.config(text="✅ Process Succeeded", fg="green")
        graph.refresh_graph()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
