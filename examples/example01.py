#!/usr/bin/env -S python -m tbdump

def bar(x, y):
    return x / y


def foo(y):
    try:
        bar(123, y)
    except Exception as exc:
        raise Exception('Unexpected error') from exc


if __name__ == '__main__':
    foo(0)
