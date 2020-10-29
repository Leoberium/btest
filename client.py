import requests
import time


def send_task(x: float, url: str = "http://127.0.0.1:5000/"):
    response = requests.get(f"{url}calculate", params={"X": x})

    if response.status_code == 201:
        print(f"Successfully sent task with X={x}, task id is {response.text}")
        return int(response.text)  # task id
    elif response.status_code == 400:
        print(f"Failed to send task with X={x}, {response.text}")
    else:
        print(f"Failed to send task with X={x}, something went wrong")


def get_result(task_id: int, url: str = "http://127.0.0.1:5000/"):
    response = requests.get(f"{url}result", params={"task_id": task_id})

    if response.status_code == 200:
        print(f"Task id: {task_id}, result: {response.text}")
    elif response.status_code == 201:
        print(f"Task id: {task_id}, result: not calculated yet")
    elif response.status_code == 400:
        print(f"{response.text} (task_id: {task_id})")


if __name__ == '__main__':
    tasks = list(map(send_task, [5.52, 6, -3.93, "edk", "", None]))
    print("\nResults without pause:")
    for task in tasks:
        get_result(task)
    time.sleep(10)
    print("\nResults after 10 seconds pause:")
    for task in tasks:
        get_result(task)
    get_result(-1)
