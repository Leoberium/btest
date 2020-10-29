import threading
import time
from flask import Flask, request


def count(i=1):
    while True:
        yield i
        i += 1


def calculate(task_id: str, x: float):
    time.sleep(10)  # imitate time-consuming task
    results[task_id] = 2.0 * x


gen_task_id = count()  # use counter to generate task id
results = dict()

app = Flask(__name__)


@app.route("/")
def initial_message():
    return "Welcome!"


@app.route("/calculate")
def accept_task():
    try:
        x = float(request.args.get("X"))  # get input
    except (ValueError, TypeError) as e:
        print(e)  # print to server log
        return "error: not float", 400

    task_id = next(gen_task_id)  # create task
    results[task_id] = None

    t = threading.Thread(target=calculate, args=(task_id, x))
    t.start()  # launch task in dedicated thread

    return str(task_id), 201


@app.route("/result")
def get_result():
    try:
        task_id = int(request.args.get("task_id"))  # get task id
    except (ValueError, TypeError) as e:
        print(e)  # print to server log
        return "Wrong format of task id", 400

    if task_id not in results:  # no such task found
        return "No task with such id", 400

    result = results[task_id]
    if result is None:  # not finished: empty result
        return "", 201
    elif isinstance(result, float):  # finished
        return str(result), 200


if __name__ == '__main__':
    app.run()
