import threading
import time
from flask import Flask, request


def count(i=1):
    while True:
        yield i
        i += 1


def calculate(task_id: str, x: float):
    time.sleep(10)
    results[task_id] = float(2 * x)


gen_task_id = count()
results = dict()

app = Flask(__name__)


@app.route("/")
def initial_message():
    return "something"


@app.route("/calculate")
def accept_task():
    # get input
    x = request.args.get("X")

    # check input
    try:
        x = float(x)
    except ValueError:
        return "not float", 400

    # create task
    task_id = next(gen_task_id)
    results[task_id] = None

    # launch task
    t = threading.Thread(target=calculate, args=(task_id, x))
    t.start()

    return str(task_id), 201


@app.route("/result")
def return_result():
    # get task id
    task_id = int(request.args.get("task_id"))

    if task_id not in results:  # no such task found
        return "no such task created", 400

    result = results[task_id]
    if result is None:  # not finished
        return "", 201
    elif isinstance(result, float):  # finished
        return str(result), 200


if __name__ == '__main__':
    app.run()
