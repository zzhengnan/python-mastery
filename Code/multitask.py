from collections import deque

tasks = deque()


def run():
    while tasks:
        task = tasks.popleft()
        try:
            task.send(None)
            tasks.append(task)
        except StopIteration:
            print(f'Task done {repr(task)}')


def countdown(n):
    while n > 0:
        print(f'T minus {n}')
        yield
        n -= 1


def countup(n):
    x = 0
    while x < n:
        print(f'Up we go {x}')
        yield
        x += 1


if __name__ == '__main__':
    tasks.append(countdown(10))
    tasks.append(countdown(5))
    tasks.append(countup(20))
    run()
