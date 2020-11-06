from tbdump import dump_exception


def bar(x, y):
    return x / y


def foo(y):
    try:
        bar(123, y)
    except Exception as exc:
        raise Exception('Unexpected error') from exc


if __name__ == '__main__':
    try:
        foo(0)
    except  Exception as exc:
        try:
            dump_exception(exc)
            print(f'{type(exc).__name__}: {exc}')
            print('Traceback dumped')
        except Exception:
            print('Failed to dump traceback')
