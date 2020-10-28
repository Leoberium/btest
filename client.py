import requests
import time


def send_task(x: float, url: str = "http://127.0.0.1:5000/"):
    try:
        response = requests.get(
            url + "calculate", params={"X": x}
        )
    except Exception:
        return

    if response.status_code == 201:
        return int(response.text)
    elif response.status_code == 400:
        return "Bad input"


def get_result(task_id: int, url: str = "http://127.0.0.1:5000/"):
    try:
        response = requests.get(
            url + "result", params={"task_id": task_id}
        )
    except Exception:
        return

    if response.status_code == 200:
        return f"task id: {task_id}, result: {response.text}"
    elif response.status_code == 201:
        return f"task id: {task_id}, result: in calculation"
    elif response.status_code == 400:
        return "No such task"


if __name__ == '__main__':
    task1 = send_task(5.52)
    task2 = send_task(6.25)
    task3 = send_task(-3.93)
    print(get_result(task1))
    print(get_result(task2))
    print(get_result(task3))
    time.sleep(10)
    print(get_result(task1))
    print(get_result(task2))
    print(get_result(task3))
