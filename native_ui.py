import datetime
import gooeypie as gp
import requests

def get_all_tasks():
    tasks = requests.get("http://127.0.0.1:8000/tasks").json()
    print(tasks)
    table_pending.clear()
    table_completed.clear()

    for task in tasks:
        if task.get('completed'):
            table_completed.add_row([task.get('id'), task.get('task_name'), task.get('task_type'), task.get('completed'), task.get('deadline')])
        else:
            table_pending.add_row([task.get('id'), task.get('task_name'), task.get('task_type'), task.get('completed'), task.get('deadline')])


def add_a_new_task():
    data = {
        "task_name": name_input.text,
        "task_type": type_input.text,
        "deadline": deadline_date.date_str
    }
    task = requests.post("http://127.0.0.1:8000/tasks", json=data)
    if task.status_code == 201:
        print("Task added successfully")

        get_all_tasks()

def toggle_task(event):
    if n := event.widget.selected:
        print(f"Row selected: {n=}")
        requests.patch(f"http://127.0.0.1:8000/tasks/{n[0]}")
        get_all_tasks()
    else:
        print("No row selected, doing nothing")

app = gp.GooeyPieApp("Task Tracker")
app.width = 500
app.set_resizable(False)

label_container_pending = gp.LabelContainer(app, "Pending Tasks")
headings = ["Task ID", "Task Name", "Task Type", "Completed", "Deadline"]
table_pending = gp.Table(label_container_pending, headings)
table_pending.set_column_alignments(*['center'] * 5)
table_pending.add_event_listener("right_click", toggle_task)

label_container_completed = gp.LabelContainer(app, "Completed Tasks")
headings = ["Task ID", "Task Name", "Task Type", "Completed", "Deadline"]
table_completed = gp.Table(label_container_completed, headings)
table_completed.set_column_alignments(*['center'] * 5)
table_completed.add_event_listener("right_click", toggle_task)

add_new_task_window = gp.Window(app, "Add New Task")
name_label = gp.Label(add_new_task_window, "Task Name")
name_input = gp.Input(add_new_task_window)
name_input.text = "Learn SQL"

type_label = gp.Label(add_new_task_window, "Task Type")
type_input = gp.Input(add_new_task_window)
type_input.text = "DBMS Assignment"

deadline_label = gp.Label(add_new_task_window, "Task Deadline")
deadline_date = gp.Date(add_new_task_window)
current_year = datetime.date.today().year
deadline_date.year_range = [current_year, current_year + 5]
deadline_date.set_selector_order('DMY')
save_button = gp.Button(add_new_task_window, "Save", lambda x: add_a_new_task())

add_new_task_window.set_grid(3, 4)
add_new_task_window.add(name_label, 1, 1)
add_new_task_window.add(name_input, 1, 2)
add_new_task_window.add(type_label, 1, 3)
add_new_task_window.add(type_input, 1, 4)
add_new_task_window.add(deadline_label, 2, 1)
add_new_task_window.add(deadline_date, 2, 2)
add_new_task_window.add(save_button, 3, 2)

add_new_button = gp.Button(app, "Add New Task", lambda x: add_new_task_window.show_on_top())

app.set_grid(3, 1)
label_container_pending.set_grid(1, 1)
label_container_completed.set_grid(1, 1)

label_container_pending.add(table_pending, 1, 1)
label_container_completed.add(table_completed, 1, 1)
app.add(label_container_pending, 1, 1)
app.add(label_container_completed, 2, 1)
app.add(add_new_button, 3, 1, align='center')

app.on_open(get_all_tasks)
app.run()