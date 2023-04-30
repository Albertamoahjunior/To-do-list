from tkinter import*

FONT = ("arial", 18, "normal")


class ParentPage(Tk):
    def __init__(self, title=None, size=None, colour=None):
        super().__init__()
        self.title(title)
        self.geometry(size)
        self.config(bg=colour)
        self.resizable(False, False)


class HomePage(Frame):
    def __init__(self, parent, add_task, our_data, clear_data, clear_task=None,
                 open_task=None, add_subtask=None):
        super().__init__(master=parent)
        self.config(bg="green")
        self.clear_data = clear_data
        self.clear_stask = clear_task
        self.inside_task = open_task
        self.add_subtask = add_subtask
        self.column = 0
        self.row = 0

        first_text = Label(master=self, text="Tasks list:", borderwidth=0, bg="green", fg="white", font=FONT)
        first_text.grid(column=0, row=0, sticky="nw")

        home_exit = ClassyButton(parent=self)
        home_exit.config(text="add", command=add_task)
        home_exit.grid(sticky="ne", column=1, row=0)

        if len(our_data) == 0:
            self.empty_tasks()
        else:
            self.task_platform = TaskPlate(parent=self)
            self.task_platform.grid(column=0, row=1, columnspan=2)
            for task in our_data:
                name = our_data[task]["name"]
                due_time = our_data[task]["due_time"]
                task_tab = TaskTab(parent=self.task_platform, task_name=name, due_time=due_time,
                                   command=lambda: self.open_task(task_name=name),
                                   clear_task=self.clear_stask, add_subtask=self.add_subtask)
                task_tab.grid(column=self.column, row=self.row, columnspan=2, pady=2)
                self.row += 1

            clear_task = ClassyButton(parent=self.task_platform)
            clear_task.config(text="clear tasks", command=self.clear_task)
            clear_task.grid(sticky="se", column=1, row=self.row)

    def empty_tasks(self):
        canvas = Canvas(master=self, bg="green", height=200, width=200)
        canvas.create_text(100, 100, text="No tasks")
        canvas.grid(column=0, row=1, columnspan=2)

    def clear_task(self):
        self.task_platform.clear_tasks()
        self.empty_tasks()
        self.clear_data()

    def open_task(self, task_name):
        subtasks = self.inside_task(task_name)
        inside_task = Tk()
        if subtasks is not None:
            for sub in subtasks:
                column = 0
                row = 0
                name = sub["name"]
                due_time = sub["due_time"]
                task_tab = TaskTab(parent=inside_task, task_name=name, due_time=due_time,
                                   clear_task=self.clear_stask)
                task_tab.grid(column=column, row=row, columnspan=2, pady=2)
                row += 1
        else:
            print("wow")
        inside_task.mainloop()

    def exit_page(self):
        self.destroy()


class TaskCreationPage(Frame):
    def __init__(self, parent, save):
        super().__init__(master=parent)
        self.subtask_row = 0
        self.subtasks = []
        self.save = save
        self.config(height=100, width=60, bg="green", )
        task_desc = Label(master=self, text="Task Name: ")
        task_desc.config(borderwidth=0, bg="green", fg="white")
        task_desc.grid(column=0, row=0, columnspan=2, padx=5)

        task_label = Label(master=self, text="Task Name: ")
        task_label.config(borderwidth=0, bg="green", fg="white")
        task_label.grid(column=0, row=1, padx=5, pady=5)
        self.task_name = Entry(master=self)
        self.task_name.grid(column=1, row=1, padx=5, pady=5)
        self.task_name.focus()

        task_time_label = Label(master=self, text="Task due time: ")
        task_time_label.config(borderwidth=0, bg="green", fg="white")
        task_time_label.grid(column=0, row=2, padx=5, pady=5)
        self.task_time = Entry(master=self)
        self.task_time.grid(column=1, row=2, padx=5, pady=5)

        self.add_subtask_button = Button(master=self, text="Add Subtasks", command=self.add_subtask)
        self.add_subtask_button.grid(column=1, row=3, pady=10)

        self.save_task_button = Button(master=self, text="Save task", command=self.save)
        self.save_task_button.grid(column=0, row=3, pady=10)

    def add_subtask(self):
        self.subtask_row = 4
        subtask_label = Label(master=self, text="Subtask Name: ")
        subtask_label.config(borderwidth=0, bg="green", fg="white")
        subtask_label.grid(column=0, row=self.subtask_row, padx=5, pady=5)
        subtask_name = Entry(master=self)
        subtask_name.grid(column=1, row=self.subtask_row, padx=5, pady=5)
        subtask_name.focus()
        self.subtask_row += 1
        subtask_time_label = Label(master=self, text="Subtask due time: ")
        subtask_time_label.config(borderwidth=0, bg="green", fg="white")
        subtask_time_label.grid(column=0, row=self.subtask_row, padx=5, pady=5)
        subtask_time = Entry(master=self)
        subtask_time.grid(column=1, row=self.subtask_row, padx=5, pady=5)
        self.subtask_row += 1

        def add_another_subtask():
            subtask = {
                "name": subtask_name.get(),
                "time": subtask_time.get(),
            }
            self.subtasks.append(subtask)
            subtask_name.delete(0, END)
            subtask_time.delete(0, END)
        self.save_task_button.grid(column=0, row=self.subtask_row, pady=10)
        self.add_subtask_button.config(command=add_another_subtask)

    def save_task(self):
        task = {
            "task": self.task_name.get(),
            "time": self.task_time.get(),
            "subtasks": self.subtasks,
        }
        return task

    def exit_page(self):
        self.destroy()


class ClassyButton(Button):
    def __init__(self, parent):
        super().__init__(master=parent)


class TaskTab(Frame):
    def __init__(self, parent, task_name, due_time, command=None, clear_task=None, add_subtask=None):
        super().__init__(master=parent)
        self.parent = parent
        self.task_name = task_name
        self.clear_task = clear_task
        self.add_sub = add_subtask
        task_button = ClassyButton(parent=self)
        task_button.config(text=f"{task_name} \t\t time:{due_time}", command=command, bg="blue", borderwidth=0)
        task_button.grid(column=0, row=0)

        delete_button = ClassyButton(parent=self)
        delete_button.config(text="del", command=self.complete)
        delete_button.grid(column=1, row=0)

        add_button = ClassyButton(parent=self)
        add_button.config(text="add", command=self.add_subtask)
        add_button.grid(column=2, row=0)

    def complete(self):
        self.parent.parent.row -= 1
        self.clear_task(name=self.task_name)
        self.destroy()
        if self.parent.parent.row < 1:
            self.parent.parent.empty_tasks()

    def add_subtask(self):
        self.parent.parent.exit_page()
        new_subtask = SubtaskCreation(save=self.add_sub, p_task=self.task_name)
        new_subtask.pack(pady=25)


class SubtaskCreation(Frame):
    def __init__(self, save, p_task, parent=None):
        super().__init__(master=parent)
        self.save = save
        self.p_task = p_task
        self.config(height=100, width=60, bg="green", )
        task_desc = Label(master=self, text="Task Name: ")
        task_desc.config(borderwidth=0, bg="green", fg="white")
        task_desc.grid(column=0, row=0, columnspan=2, padx=5)

        task_label = Label(master=self, text="Task Name: ")
        task_label.config(borderwidth=0, bg="green", fg="white")
        task_label.grid(column=0, row=1, padx=5, pady=5)
        self.task_name = Entry(master=self)
        self.task_name.grid(column=1, row=1, padx=5, pady=5)
        self.task_name.focus()

        task_time_label = Label(master=self, text="Task due time: ")
        task_time_label.config(borderwidth=0, bg="green", fg="white")
        task_time_label.grid(column=0, row=2, padx=5, pady=5)
        self.task_time = Entry(master=self)
        self.task_time.grid(column=1, row=2, padx=5, pady=5)

        self.save_task_button = Button(master=self, text="Save task", command=self.save_subtask)
        self.save_task_button.grid(column=0, row=3, pady=10)

    def save_subtask(self):
        subtask = {
            "name": self.task_name.get(),
            "task_time": self.task_time.get(),
        }
        self.destroy()
        self.save(name=self.p_task, subtask=subtask)


class TaskPlate(Frame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.parent = parent
        self.config(height=100, width=20, bg="green")

    def clear_tasks(self):
        self.destroy()
    