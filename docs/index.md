# tbdump

The aim of this library is to provide an option of post-mortem debugging for
the application which would crash on a remote machine, for instance on customer
site.

Project is influenced by [pydump](https://github.com/elifiner/pydump) and
powered by [dill](https://github.com/uqfoundation/dill). This also results in
some [limitations](#known-issues).

## Faulty Application

As an example let's take this code of a simple calculator:

```python
import sys

def div(x, y):
    return x / y

if __name__ == '__main__':
    x = int(sys.argv[1])
    y = int(sys.argv[2])
    print(div(x, y))
```

It will certainly raise an exception when divisor is 0.

```sh
python divide.py 5 0
```

```
Traceback (most recent call last):
  File "divide.py", line 9, in <module>
    print(div(x, y))
  File "divide.py", line 4, in div
    return x / y
ZeroDivisionError: division by zero
```

## Traceback Capturing

We have following options to take traceback down into a file:

1. We can use *tbdump* module in place of *python* interpreter. This will
capture any unhandled `Exception`:

    ```sh
    python -m tbdump divide.py 5 0
    ```

    ```
    ZeroDivisionError: division by zero
    Traceback dumped into: traceback.pkl
    ```

    It is suitable when we have a chance to change the way how Python script is
    invoked. This is also how *tbdump* can be activated from shebang:

    ```python
    #!/usr/bin/env -S python -m tbdump
    ```

2. Alternatively we can install *tbdump* as exception hook using its default
implementation:

    ```python
    import sys
    import tbdump
    tbdump.set_excepthook()

    def div(x, y):
        return x / y

    if __name__ == '__main__':
        x = int(sys.argv[1])
        y = int(sys.argv[2])
        print(div(x, y))
    ```

    ```sh
    python divide.py 5 0
    ```

    ```
    ZeroDivisionError: division by zero
    Traceback dumped into: traceback.pkl
    ```

3. Finally, we can customize exception handler by preparing its custom
implementation:

    ```python
    import sys
    from tbdump import dump_exception

    def div(x, y):
        return x / y

    if __name__ == '__main__':
        try:
            x = int(sys.argv[1])
            y = int(sys.argv[2])
            print(div(x, y))
        except  Exception as exc:
            try:
                dumpfile = 'traceback.pkl'
                dump_exception(exc, dumpfile)
                print(f'{type(exc).__name__}: {exc}')
                print(f'Traceback dumped into: {dumpfile}')
            except Exception:
                print('Failed to dump traceback')
    ```

    ```sh
    python divide.py 5 0
    ```

    ```
    ZeroDivisionError: division by zero
    Traceback dumped into: traceback.pkl
    ```

No matter which option we choose, we should get a `traceback.pkl` file in case
of an exception.

## Traceback Analysis

1. Some developers may prefer to launch their favourite debugger right
away:

    ```sh
    poetry run python -m tbdebug traceback.pkl
    ```

    *tbdebug* uses `breakpoint()`. Behaviour of this function can be adjusted
    using [`PYTHONBREAKPOINT`](https://www.python.org/dev/peps/pep-0553/) variable.

2. Alternatively, simple helper script can be used by hose who would
like to apply any preprocessing in prior to that:

    ```python
    import tbdump
    dump = tbdump.load('traceback.pkl')
    # any preprocessing here
    breakpoint()
    ```

3. Last option is for these developers who are familiar with
[peepshow](https://gergelyk.github.io/peepshow/) and may prefer calling it:

    ```sh
    poetry run python -m tbpeep traceback.pkl
    ```

    ![](assets/peep1.png)
    ![](assets/peep2.png)
    ![](assets/peep3.png)
    ![](assets/peep4.png)


## Limitations

There are a few data types which [dill](https://github.com/uqfoundation/dill)
doesn't pickle by definition. At the time of writing these include generator,
Frame, Traceback.

??? note

    Top-level traceback and corresponding frames are translated into
    substitutionary objects.

Moreover, there are a few open issues with pickling
[enums](https://github.com/uqfoundation/dill/issues/250) and
[namespace packages](https://github.com/uqfoundation/dill/issues/389).

Last but not least, modules which were captured on a remote host but are not
available in local environment are substituted by dummy objects in the process
of loading dump files.
