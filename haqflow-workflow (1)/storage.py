
import json
import os

from models import ActionItem


STORAGE_FILE = "/content/haqflow-workflow/tasks.json"


def save_tasks(tasks):

    data = []

    for task in tasks:
        data.append(task.to_dict())

    with open(STORAGE_FILE, "w") as file:
        json.dump(data, file, indent=4)

    return True


def load_tasks():

    if not os.path.exists(STORAGE_FILE):
        return []

    with open(STORAGE_FILE, "r") as file:
        data = json.load(file)

    tasks = []

    for item in data:

        task = ActionItem(
            id=item["id"],
            title=item["title"],
            priority=item["priority"],
            status=item["status"],
            related_program_id=item.get("related_program_id"),
            related_program_name=item.get("related_program_name"),
            source=item.get("source")
        )

        task.validate()
        tasks.append(task)

    return tasks
