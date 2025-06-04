import sys
import functools
import sqlite3
import json
import datetime


def trace(func=None, *, handle=sys.stdout):
    if func is None:
        return lambda func: trace(func, handle=handle)

    @functools.wraps(func)
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        log_entry = {
            'datetime': datetime.datetime.now().isoformat(),
            'func_name': func.__name__,
            'params': str(args),
            'result': str(result)
        }

        if isinstance(handle, str) and handle.endswith('.json'):
            try:
                with open(handle, 'a', encoding='utf-8') as f:
                    json.dump(log_entry, f, ensure_ascii=False)
                    f.write('\n')
            except Exception as e:
                sys.stderr.write(f"Error writing to JSON file: {e}\n")
        elif isinstance(handle, sqlite3.Connection):
            try:
                cur = handle.cursor()
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS logtable (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        datetime TEXT,
                        func_name TEXT,
                        params TEXT,
                        result TEXT
                    )
                """)
                cur.execute("""
                    INSERT INTO logtable (datetime, func_name, params, result)
                    VALUES (?, ?, ?, ?)""",
                            (log_entry['datetime'], log_entry['func_name'], log_entry['params'], log_entry['result'])
                            )
                handle.commit()
            except Exception as e:
                sys.stderr.write(f"Error writing to database: {e}\n")
        else:
            handle.write(f"{log_entry}\n")

        return result

    return inner


def dbc():
    return sqlite3.connect(":memory:")


def showlogs(con: sqlite3.Connection):
    try:
        cur = con.cursor()
        cur.execute("SELECT * FROM logtable")
        logs = cur.fetchall()
        for log in logs:
            print(log)
    except Exception as e:
        sys.stderr.write(f"Error reading from database: {e}\n")


@trace(handle=sys.stderr)
def increm(x):
    """Инкремент"""
    return x + 1


@trace(handle=sys.stdout)
def decrem(x):
    return x - 1


@trace()
def f2(x):
    return x ** 2


@trace(handle='logger.json')
def f3(x):
    return x ** 3


with dbc() as c:
    print(c)

    @trace(handle=c)
    def f4(x):
        return x ** 4


    print(increm.__doc__)
    increm(2)
    decrem(2)
    f2(3)
    f3(4)
    f4(5)

    showlogs(c)

input("enter")
