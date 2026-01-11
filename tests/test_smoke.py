import pytest
import reslik
from reslik import ResLikUnit

def test_import():
    assert reslik.__version__ is not None

def test_wrapper_instantiation():
    wrapper = ResLikUnit(input_dim=10)
    assert wrapper.input_dim == 10

def test_cpp_binding_existence():
    # Attempt to import the internal core module
    try:
        from reslik import _core
    except ImportError:
        pytest.fail("Could not import _core extension module")
