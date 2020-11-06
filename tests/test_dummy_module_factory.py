import pytest
from tbdump.loader import DummyModuleFactory, ModuleStub, Dummy


def test_import_module():
    with DummyModuleFactory():
        import some_nonexisting_module

    assert type(some_nonexisting_module) == ModuleStub


def test_import_submodule():
    with DummyModuleFactory():
        import some_nonexisting_module.submodule

    assert type(some_nonexisting_module.submodule) == ModuleStub


def test_import_from_module():
    with DummyModuleFactory():
        from some_nonexisting_module import something

    assert type(something) == Dummy


def test_import_from_submodule():
    with DummyModuleFactory():
        from some_nonexisting_module.submodule import something

    assert type(something) == Dummy


def test_import_failure():
    with pytest.raises(ImportError):
        import some_other_nonexisting_module

