from doit import doit, get_tasks, Task
from textwrap import dedent
import tempfile

    # expected = [Task(description='launchers', subtasks=[
    #     Task(description='say hello', subtasks=[
    #         Task(description='command: echo "hello" | festival --tts'),
    #         Task(description='icon: sayHello.png'),
    #     ]),
    #     Task(description='say world', subtasks=[
    #         Task(description='command: echo "world" | festival --tts'),
    #         Task(description='icon: sayWorld.png'),
    #     ]),
    #     Task(description='wait', subtasks=[
    #         Task(description='command: for ((x = 0; x < 10; ++x)); do :; done'),
    #         Task(description='icon: wait.png'),
    #     ]),
    # ])]

def test_get_tasks():
    test_case = '''
    - launchers
        - say hello
            - command: echo "hello" | festival --tts
            - icon: sayHello.png
        - say world
            - command: echo "world" | festival --tts
            - icon: sayWorld.png
        - wait
            - command: for ((x = 0; x < 10; ++x)); do :; done
            - icon: wait.png
    '''
    expected = [
        (0, Task(description='launchers')),
        (1, Task(description='say hello')),
        (2, Task(description='command: echo "hello" | festival --tts')),
        (2, Task(description='icon: sayHello.png')),
        (1, Task(description='say world')),
        (2, Task(description='command: echo "world" | festival --tts')),
        (2, Task(description='icon: sayWorld.png')),
        (1, Task(description='wait')),
        (2, Task(description='command: for ((x = 0; x < 10; ++x)); do :; done')),
        (2, Task(description='icon: wait.png')),
    ]

    tmp = tempfile.NamedTemporaryFile()
    with open(tmp.name, 'w') as f:
        f.write(dedent(test_case))

    assert get_tasks(tmp.name) == expected

    test_case = '''
    - do this (2)
        - but this first (1)
            - but this even before everything (0)
    - this is less important (3)
    '''
    expected = [
        (0, Task(description='do this (2)')),
        (1, Task(description='but this first (1)')),
        (2, Task(description='but this even before everything (0)')),
        (0, Task(description='this is less important (3)')),
    ]

    tmp = tempfile.NamedTemporaryFile()
    with open(tmp.name, 'w') as f:
        print(test_case)
        f.write(dedent(test_case))
    assert get_tasks(tmp.name) == expected


def test_doit():
    test_case = '''
    - do this (2)
        - but this first (1)
            - but this even before everything (0)
    - this is less important (3)
    '''
    expected = [
        "but this even before everything (0)",
        "but this first (1)",
        "do this (2)",
        "this is less important (3)",
    ]

    tmp = tempfile.NamedTemporaryFile()
    with open(tmp.name, 'w') as f:
        f.write(dedent(test_case))
    assert doit(get_tasks(tmp.name)) == expected
