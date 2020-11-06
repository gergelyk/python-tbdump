import os
import sys
from tbdump import dump_exception, load


from tbdump.loader import DummyModuleFactory, ModuleStub, Dummy


def test_import_module():
    with DummyModuleFactory():
        import some_nonexisting_module

    assert type(some_nonexisting_module) == ModuleStub

def test_dump():
    import examples.example01
    try:
        examples.example01.foo(0)
    except Exception as exc:
        dump_exception(exc)


    tb = load()

    tb['system'] == {
        'sys.version': sys.version,
        'os.name': os.name,
        'os.uname': os.uname,
        }

    assert len(tb['exceptions']) == 2

    exc0 = tb['exceptions'][0]
    assert exc0.str == 'division by zero'
    assert exc0.type == ZeroDivisionError
    assert len(exc0) == 2

    exc0fr0 = exc0[0]
    assert exc0fr0._code_line == 'bar(123, y)'
    assert exc0fr0._func_name == 'foo'
    assert exc0fr0._filename == examples.example01.__file__
    assert exc0fr0._lineno == 9
    assert set(exc0fr0.keys()) == {'bar', 'foo', 'y'}

    exc0fr1 = exc0[1]
    assert exc0fr1._code_line == 'return x / y'
    assert exc0fr1._func_name == 'bar'
    assert exc0fr1._filename == '/home/kendo/wrk/python-tbdump/examples/example01.py'
    assert exc0fr1._lineno == 4
    assert set(exc0fr1.keys()) == {'bar', 'foo', 'x', 'y'}


    exc1 = tb['exceptions'][1]
    assert exc1.str == 'Unexpected error'
    assert exc1.type == Exception
    assert len(exc1) == 2

    exc1fr0 = exc1[0] # contains pytest variables
    assert exc1fr0._code_line == 'examples.example01.foo(0)'
    assert exc1fr0._func_name == 'test_dump'
    assert exc1fr0._filename == '/home/kendo/wrk/python-tbdump/tests/test_dumper.py'
    assert exc1fr0._lineno == 18

    exc1fr1 = exc1[1]
    assert exc1fr1._code_line == "raise Exception('Unexpected error') from exc"
    assert exc1fr1._func_name == 'foo'
    assert exc1fr1._filename == '/home/kendo/wrk/python-tbdump/examples/example01.py'
    assert exc1fr1._lineno == 11
    assert set(exc0fr1.keys()) == {'bar', 'foo', 'x', 'y'}



