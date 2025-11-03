import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import engine as eng
import thompson as th

# LLM generated this class after vigourous prompting, but I will still have to carve it up to turn it into something usable for our purposes.
class UI:
    
    def __init__(self, root):
        self.examples = {
                    "Homer" : th.V(["000", "0010", "0011", "01", "1000", "1001", "101", "11"],["01", "1100", "1110", "10", "1111", "11011", "00", "11010"]),
                    "Monk" : th.V(["000", "0010", "0011","010", "011", "100", "101", "110","111"], ["100", "1010", "110", "1110", "11110", "01", "00", "11111", "1011"]),
                    "Kermit" : th.V(["000", "0010", "0011", "01", "1000", "1001", "101", "11"], ["01", "1100", "1110", "10", "1111", "11011", "00", "11010"]),

                    "Carl" : th.V(["000", "0010", "00110", "00111", "0100", "0101", "011", "10", "1100", "1101", "111"], ["1001", "010", "011", "110", "10000", "001", "0000", "101", "10001", "0001", "111"]),

                    "Mullet" :  th.V(['00000', '00001', '00010', '000110', '000111', '0010', '0011', '010', '011', '1'], ['11', '001', '0110', '101', '0111', '0101', '0100', '0000', '100', '0001']),

                    "Goofy" : th.V(['0100', '0101', '0000', '0001', '0111', '01100', '01101', '10', '1100', '1101', '1110', '1111', '0010', '0011'],['0111100', '0111101', '1', '01100', '011100', '01101', '011101', '0101', '0000', '0001', '0010', '0011', '011111', '0100']),

                    "Doof" : th.V(th.V.DFS_to_antichain("110111000011000"),th.V.DFS_to_antichain("110111000011000"))
        }

        self.engine = eng.Engine(startup_var=self.examples)

        """Initialize the main application window and GUI components."""
        self.root = root
        self.root.title("Computations in Thompson's group V")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2b2b2b")  # dark background

        # --- Color theme ---
        self.BG_MAIN = "#2b2b2b"
        self.BG_DARK = "#1e1e1e"
        self.FG_TEXT = "#e0e0e0"
        self.ACCENT = "#00c8ff"
        self.ERROR = "#ff4d4d"

        # Current layout mode: 'vertical' or 'horizontal'
        self.layout_mode = "vertical"

        # Initialize GUI components
        self._setup_styles()
        self._setup_header()
        self._setup_input_frame()
        self._build_layout(self.layout_mode)  # initial layout

        # Properly close the app and release resources on exit
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background=self.BG_MAIN, foreground="white", font=("Consolas", 12))
        style.configure("TEntry", fieldbackground="#3b3b3b", foreground="white", padding=6, relief="flat")
        style.configure("TButton", background="#3b3b3b", foreground="white", padding=6, relief="flat")
        style.map("TButton", background=[("active", "#4b4b4b")])

    def _setup_header(self):
        header = ttk.Label(self.root, text="Computations in Thompson's group V:", font=("Segoe UI", 16, "bold"), foreground=self.ACCENT)
        header.pack(pady=(10, 5))
        subheader = ttk.Label(self.root, text="",
                              font=("Consolas", 10))
        subheader.pack(pady=(0, 10))

    def _setup_input_frame(self):
        self.input_frame = tk.Frame(self.root, bg=self.BG_MAIN)
        self.input_frame.pack(fill=tk.X, padx=15, pady=(0, 10))

        ttk.Label(self.input_frame, text=">>>", font=("Consolas", 13)).pack(side=tk.LEFT, padx=(0, 5))
        self.entry = ttk.Entry(self.input_frame, font=("Consolas", 12))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        self.entry.bind("<Return>", self._process_command)

        ttk.Button(self.input_frame, text="Help", command=self._show_help).pack(side=tk.RIGHT)
        ttk.Button(self.input_frame, text="Toggle Layout", command=self._toggle_layout).pack(side=tk.RIGHT, padx=8)

    def _create_repl_frame(self, parent):
        frame = tk.Frame(parent, bg=self.BG_DARK, highlightbackground="#3a3a3a", highlightthickness=1)
        scrollbar = ttk.Scrollbar(frame, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        log = tk.Text(frame, height=10, bg=self.BG_DARK, fg=self.FG_TEXT,
                      insertbackground="white", wrap=tk.WORD, relief="flat",
                      font=("Consolas", 11), yscrollcommand=scrollbar.set)
        log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=8)
        scrollbar.config(command=log.yview)
        log.tag_config("error", foreground=self.ERROR, font=("Consolas", 11, "bold"))
        log.tag_config("success", foreground=self.ACCENT)
        log.tag_config("info", foreground="#bbbbbb")
        return frame, log

    def _create_plot_frame(self, parent):
        """Now create 1 row × 2 column subplots instead of a single one."""
        frame = tk.Frame(parent, bg=self.BG_MAIN)

        # Two subplots side by side
        fig, axes = plt.subplots(1, 2, figsize=(10, 4))
        fig.patch.set_facecolor(self.BG_MAIN)

        for ax in axes:
            ax.set_facecolor("#222222")
            for spine in ax.spines.values():
                spine.set_color("white")
            ax.tick_params(axis="x", colors="white")
            ax.tick_params(axis="y", colors="white")

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        # Force initial canvas draw to prevent first-plot bug
        frame.update_idletasks()
        canvas.draw_idle()

        return frame, fig, axes, canvas

    def _build_layout(self, orientation):
        old_text = getattr(self, 'log', None) and self.log.get("1.0", tk.END)
        if hasattr(self, 'paned') and self.paned is not None:
            self.paned.destroy()

        self.paned = ttk.PanedWindow(self.root, orient=orientation)
        self.paned.pack(fill=tk.BOTH, expand=True, padx=15, pady=(5, 15))

        self.repl_frame, self.log = self._create_repl_frame(self.paned)
        self.plot_frame, self.fig, self.axes, self.canvas = self._create_plot_frame(self.paned)

        self.paned.add(self.repl_frame, weight=1)
        self.paned.add(self.plot_frame, weight=3)

        if old_text:
            self.log.insert(tk.END, old_text)

    def _on_close(self):
        """Cleanly close Tkinter and Matplotlib so the process exits."""
        try:
            self.canvas.get_tk_widget().quit()
            self.canvas.get_tk_widget().destroy()
            plt.close('all')
            self.root.quit()
            self.root.destroy()
        finally:
            raise KeyboardInterrupt

    def _toggle_layout(self):
        self.layout_mode = "horizontal" if self.layout_mode == "vertical" else "vertical"
        self._build_layout(tk.HORIZONTAL if self.layout_mode == "horizontal" else tk.VERTICAL)
        self.log.insert(tk.END, f"Switched layout to {self.layout_mode} mode.\n\n", "info")
        self.log.see(tk.END)

    def _show_help(self):
        help_text = (
            "/show variable_name : plots the tree pair associated with the variable_name \n"
            "/print variable_name : Writes the antichains to the log.\n"
            "/help : Displays the available commands.\n"
            "/clear : Clears the drawns tree pairs\n"
            "/var : Shows the currently available variables.\n"
            "Use 'Toggle Layout' to switch between vertical or side-by-side view."
        )
        self.log.insert(tk.END, help_text + "\n\n", "info")
        self.log.see(tk.END)

    def _process_command(self, event=None):
            command = self.entry.get().strip()
            self.entry.delete(0, tk.END)
            if not command:
                return

            self.log.insert(tk.END, f">>> {command}\n", "info")
            self.log.see(tk.END)

            res = self.engine.parse_string(command, debug=False)
            self.handle_command()

            self.log.see(tk.END)

    def handle_command(self):
        command = self.engine.get_command()
        if command != None:
            variables = self.engine.get_variables()
            # print(command)
            self.log.insert(tk.END, f"Executing command {command}\n")
            if command[0] == "/show":
                # print("executing command", command, variables[command[1][0]])
                for i in command[1]:
                    # self.visualiser.show_element(variables[i]) 
                    print(variables[i].get_element_permutation())
                    self.engine.visualiser.show_element_embedded(variables[i], fig=self.fig,ax=self.axes) 

            elif command[0] == '/makerevealing':
                # I want to change this one to an inline command
                # print("Making tree pair revealing")
                for i in command[1]:
                    variables[i] = variables[i].make_revealing()
            elif command[0] == '/clear':
                for ax in self.axes:
                    ax.clear()
                    # ax.set_facecolor("#222222")
                self.canvas.draw()
                self.log.insert(tk.END, "Cleared both plots.\n\n", "info")
            elif command[0] == "/help":
                self._show_help()
            elif command[0] == "/var":
                self.log.insert(tk.END, "Defined variables:\n")
                self.log.insert(tk.END, str(list(self.engine.get_variables().keys())) + '\n')
            elif command[0] == "/print":
                for i in command[1]:
                    # self.visualiser.show_element(variables[i]) 
                    self.log.insert(tk.END, str(variables[i]) + '\n')




        self.canvas.draw_idle()
        self.root.update_idletasks()


if __name__ == "__main__":
    root = tk.Tk()
    ui = UI(root)
    root.mainloop()
    # root.after_idle(ui.handle_command)
    # running = True
    # while running:
        # try:

            # root.update()
            # root.update_idletasks()
            # ui.handle_command()
            # # string = input()
            # # res = engine.parse_string(string, debug=False)
            # # print(res)
        # except KeyboardInterrupt:
            # print("running stops")
            # running = False
        # except Exception as e:
            # ui.log.insert(tk.END, f"Error: {e}\n\n", "error")


