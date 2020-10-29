import time
from server import app


def test_welcome():
    with app.test_client() as c:
        r = c.get("/")
        assert r.status_code == 200
        assert r.data == b"Welcome!"


def test_calculation():
    with app.test_client() as c:
        # send tasks
        r1 = c.get("/calculate?X=7.62")  # some float
        assert r1.status_code == 201
        assert r1.data == b"1"
        r2 = c.get("/calculate?X=")  # empty
        assert r2.status_code == 400
        r3 = c.get("/calculate?X=None")  # None
        assert r3.status_code == 400
        r4 = c.get("/calculate?X=string")  # str
        assert r4.status_code == 400
        r5 = c.get("/calculate?X=-3.53")  # some other float
        assert r5.status_code == 201
        assert r5.data == b"2"

        # get results
        r11 = c.get(f"/result?task_id={int(r1.data)}")  # without pause
        assert r11.status_code == 201
        assert r11.data == b""  # no result yet
        r51 = c.get(f"/result?task_id={int(r5.data)}")  # without pause
        assert r51.status_code == 201
        assert r51.data == b""  # no result yet
        r6 = c.get(f"/result?task_id=115")  # non-existing task id
        assert r6.status_code == 400
        r7 = c.get(f"/result?task_id=abc")  # incorrect task id
        assert r7.status_code == 400

        time.sleep(11)  # 11 seconds pause - time for calculations
        r12 = c.get(f"/result?task_id={int(r1.data)}")
        assert r12.status_code == 200
        assert float(r12.data) == 7.62 * 2.0
        r52 = c.get(f"/result?task_id={int(r5.data)}")
        assert r52.status_code == 200
        assert float(r52.data) == -3.53 * 2.0
