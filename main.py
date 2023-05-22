from threading import Thread
from Pages import*
import json
from datetime import datetime
import time as delay


our_data = {}
try:
    with open("data.json", "r") as file:
        our_data = json.load(file)
except ValueError:
    with open("data.json", "w") as file:

        json.dump(our_data, file)


tasks = {
    "name": " ",
    "due_time": " ",
    "subtasks": [],
}


def comb_ourdata():
    not_yet = True
    while not_yet:
        now = str(datetime.now())
        now = now.split(" ")

        time = now[1].split(".")[0]
        time = time[:5]
        for task in our_data:
            task_time = our_data[task]["name"]
            task_time = our_data[task]["due_time"]
            if task_time == time:
                dispInfo(info_title="Time Up", info="f{name} task's time is due")
                not_yet = False
            else:
                print("It ain't timee")
            delay.sleep(30)


def update_ourdata():
    global our_data
    with open("data.json", "r") as update_file:
        our_data = json.load(update_file)


def inside_task(name):
    for task in our_data:
        if task == name:
            subtasks = our_data[name]["subtasks"]
            if len(subtasks) == 0:
                return None
            else:
                return subtasks


def delete_task(name):
    for task in our_data:
        if task == name:
            del our_data[name]
            with open("data.json", "w") as update_file:
                json.dump(our_data, update_file,  indent=4)
            update_ourdata()
            break


def delete_subtask(name, subtask):
    for task in our_data:
        if task == name:
            our_data[name]["subtasks"].remove(subtask)
            with open("data.json", "w") as update_file:
                json.dump(our_data, update_file,  indent=4)
            update_ourdata()
            break


def main_page():
    def back_to_home(taskpage=None):
        if taskpage is not None:
            taskpage.exit_page()
        new_homepage = HomePage(parent=platform, add_task=lambda: create_task(new_homepage),
                                our_data=our_data, clear_data=clear_all_tasks, clear_task=delete_task)
        new_homepage.pack(pady=25)

    def add_subtask(name, subtask):
        for task in our_data:
            if task == name:
                our_data[name]["subtasks"].append(subtask)
                with open("data.json", "w") as update_file:
                    json.dump(our_data, update_file, indent=4)
                update_ourdata()
                break
        back_to_home()

    def clear_all_tasks():
        global our_data
        our_data = {}
        with open("data.json", "w") as new_file:
            json.dump(our_data, new_file, indent=4)

    def save_tasks(task_obj):
        global our_data
        task_content = task_obj.save_task()
        tasks["name"] = task_content["task"]
        tasks["due_time"] = task_content["time"]
        tasks["subtasks"] = task_content["subtasks"]
        our_data[tasks["name"]] = tasks

        with open("data.json", "w") as new_file:
            json.dump(our_data, new_file, indent=4)

        update_ourdata()
        back_to_home(taskpage=task_obj)

    def create_task(home=None):
        if home is not None:
            home.exit_page()
        else:
            homepage.exit_page()
        task_page = TaskCreationPage(parent=platform, save=lambda: save_tasks(task_obj=task_page))
        task_page.pack(pady=25)

    platform = ParentPage(title="To do list", size="400x400", colour="#023645")

    homepage = HomePage(parent=platform, add_task=create_task, our_data=our_data, clear_data=clear_all_tasks,
                        clear_task=delete_task, add_subtask=add_subtask, open_task=inside_task)
    homepage.pack(pady=25)

    platform.mainloop() 


if __name__ == "__main__":
    main_thread = Thread(target=main_page)
    side_thread = Thread(target=comb_ourdata)

    main_thread.start()
    side_thread.start()

    main_thread.join()
    side_thread.join()
