import tkinter as tk
from tkinter import simpledialog, messagebox


class AllInOneApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("All-in-One App")

        tk.Button(self, text="Notepad", command=self.open_notepad).pack(pady=10)
        tk.Button(self, text="Task List", command=self.open_task_list).pack(pady=10)
        tk.Button(self, text="Calculator", command=self.open_calculator).pack(pady=10)
        tk.Button(self, text="Messages", command=self.open_messages).pack(pady=10)

    def open_notepad(self):
        Notepad(self)

    def open_task_list(self):
        TaskList(self)

    def open_calculator(self):
        Calculator(self)

    def open_messages(self):
        Messages(self)


class Notepad(tk.Toplevel):

    def __init__(self, master=None):
        super().__init__(master)
        self.title("Notepad")

        self.text = tk.Text(self, wrap=tk.WORD)
        self.text.pack(expand=1, fill=tk.BOTH)

        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save_note)
        file_menu.add_command(label="Open", command=self.open_note)

    def save_note(self):
        with open("note.txt", "w") as file:
            file.write(self.text.get(1.0, tk.END))
        messagebox.showinfo("Notepad", "Note saved successfully!")

    def open_note(self):
        try:
            with open("note.txt", "r") as file:
                self.text.delete(1.0, tk.END)
                self.text.insert(tk.INSERT, file.read())
        except FileNotFoundError:
            messagebox.showerror("Notepad", "No saved notes found!")


class TaskList(tk.Toplevel):

    def __init__(self, master=None):
        super().__init__(master)
        self.title("Task List")

        self.task_var = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.task_var)
        self.entry.pack(pady=10)

        self.add_button = tk.Button(self, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=10)

        self.tasks = tk.Listbox(self)
        self.tasks.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.remove_button = tk.Button(self, text="Remove Task", command=self.remove_task)
        self.remove_button.pack(pady=10)

    def add_task(self):
        task = self.task_var.get()
        if task:
            self.tasks.insert(tk.END, task)
            self.task_var.set("")

    def remove_task(self):
        try:
            index = self.tasks.curselection()[0]
            self.tasks.delete(index)
        except IndexError:
            pass


class Calculator(tk.Toplevel):

    def __init__(self, master=None):
        super().__init__(master)
        self.title("Calculator")

        self.result_var = tk.StringVar()
        self.result_entry = tk.Entry(self, textvariable=self.result_var, font=("Arial", 24), bd=10, insertwidth=4,
                                     width=14, justify='right')
        self.result_entry.grid(row=0, column=0, columnspan=4)

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('0', 4, 1),
            ('+', 1, 3), ('-', 2, 3), ('*', 3, 3), ('/', 4, 3),
            ('.', 4, 0), ('C', 4, 2), ('=', 5, 3)
        ]

        for (btn_text, row, col) in buttons:
            self.create_button(btn_text, row, col)

    def create_button(self, text, row, col):
        btn = tk.Button(self, text=text, padx=20, pady=20, command=lambda: self.on_button_click(text))
        btn.grid(row=row, column=col)

    def on_button_click(self, char):
        current_text = self.result_var.get()

        if char == 'C':
            self.result_var.set("")
        elif char == '=':
            try:
                result = eval(current_text)
                self.result_var.set(result)
            except Exception:
                self.result_var.set("Error")
        else:
            new_text = current_text + char
            self.result_var.set(new_text)


class Messages(tk.Toplevel):

    def __init__(self, master=None):
        super().__init__(master)
        self.title("Messages")

        self.message_var = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.message_var)
        self.entry.pack(pady=10)

        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.pack(pady=10)

        self.messages_display = tk.Text(self, wrap=tk.WORD, height=10)
        self.messages_display.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def send_message(self):
        message = self.message_var.get()
        if message:
            self.messages_display.insert(tk.END, message + "\n")
            self.message_var.set("")


if __name__ == "__main__":
    app = AllInOneApp()
    app.mainloop()
