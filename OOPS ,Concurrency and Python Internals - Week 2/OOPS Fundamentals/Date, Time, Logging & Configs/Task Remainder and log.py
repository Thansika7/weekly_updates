import json
import os
import schedule
import logging
import time
import asyncio
from plyer import notification
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
file_name = os.path.join(current_dir, "tasks.json")
log_file = os.path.join(current_dir, "task_reminder.log")

if not os.path.exists(file_name):
    with open(file_name, "w") as f:
        json.dump([], f)

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Task Reminder Application Started")


def load_tasks():
    try:
        with open(file_name, "r") as f:
            return json.load(f)
    except:
        return []

def save_tasks(tasks):
    with open(file_name, "w") as f:
        json.dump(tasks, f, indent=4)

def task_reminder(task):

    notification.notify(
        title="Task Reminder",
        message=f"TASK: {task['task_name']}",
        timeout=10
    )
    print("Task Reminder")
    print(f"Task : {task['task_name']}")
    print(f"Time : {datetime.now().strftime('%d-%m-%y %H:%M')}")

    logging.info(f"Reminder triggered for task: {task['task_name']}")

    return schedule.CancelJob

def schedule_tasks():

    schedule.clear() 
    
    tasks=load_tasks()
    
    for task in tasks:
        task_time = datetime.strptime(task["datetime"], "%d-%m-%Y %H:%M")
        delay = (task_time - datetime.now()).total_seconds()

        if delay > 0:
            schedule.every(delay).seconds.do(task_reminder, task=task)

def add_task():
    task_name=input("Enter Task to remind:")
    date=input("Enter date (DD-MM-YYYY): ")
    time=input("Enter Time (HH:MM): ")

    task_date_time=(f"{date} {time}")

    try:
        datetime.strptime(task_date_time, "%d-%m-%Y %H:%M")
    except:
        print("Invalid date/time format")

        logging.error("Invalid date/time entered")
        return

    tasks=load_tasks()

    tasks.append({
        "task_name": task_name,
        "datetime": task_date_time
    })

    save_tasks(tasks)
    schedule.clear()
    schedule_tasks()

    logging.info(f"Task added: {task_name} at {task_date_time}")

    print("Task added Successfully")

def delete_task():
    tasks = load_tasks()

    if not tasks:
        print("No tasks available")
        return

    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task['task_name']} - {task['datetime']}")

    try:
        choice = int(input("Select task number to delete: "))
        removed = tasks.pop(choice - 1)
        save_tasks(tasks)

        schedule.clear()
        schedule_tasks()

        print("Task deleted")
        logging.info(f"Task deleted: {removed['task_name']}")
    except:
        print("Invalid selection")

async def scheduler_loop():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)



async def menu_loop():
    while True:
        try:
            print("\n1. Add Tasks")
            print("2. Delete Task")
            print("3. Exit")

            loop = asyncio.get_running_loop()
            choice = await loop.run_in_executor(None, input, "Enter Your Choice: ")

            if choice == "1":
                await loop.run_in_executor(None, add_task)

            elif choice == "2":
                await loop.run_in_executor(None, delete_task)

            elif choice == "3":
                logging.info("Application exited by user")
                print("Exited")
                break

            else:
                print("Invalid Choice")
                logging.warning("Invalid menu choice entered")

        except KeyboardInterrupt:
            print("\nOperation cancelled. Back to menu...")
            logging.info("User pressed Ctrl+C, returned to menu")
            await asyncio.sleep(0.2)
            continue

async def main():
    schedule_tasks()
    await asyncio.gather(
        scheduler_loop(),
        menu_loop()
    )

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("\nApplication interrupted. Returning to menu is not possible after full stop.")
    logging.info("Application stopped using Ctrl+C")

