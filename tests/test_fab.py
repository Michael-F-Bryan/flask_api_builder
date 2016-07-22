import warnings
import pytest
import flask_api_builder as fab


@pytest.fixture
def f():
    url = '/tasks/foo'
    method = 'get'
    description = 'Do something'
    return fab.Function(url, method, description)


class TestFunction:
    def test_init_with_defaults(self):
        url = '/tasks/foo'
        method = 'get'
        description = 'Do something'
        f = fab.Function(url, method, description)
        assert f.url == url
        assert f.method == method.upper()
        assert description == f.description

    def test_init_with_custom_stuff(self):
        url = '/tasks/foo'
        method = 'get'
        description = 'Do something'
        blueprint = 'my_cool_api'
        name = 'some_restful_function'
        template = 'insert stuff here {}'
        f = fab.Function(url, method, description, blueprint, name, template)
        assert f.url == url
        assert f.method == method.upper()
        assert description == f.description
        assert f.blueprint == blueprint
        assert f.name == name
        assert f.template == template

    def test_get_args_with_no_args(self, f):
        got = f.get_args()
        should_be = []
        assert got == should_be

    def test_get_args_with_1_arg(self, f):
        f.url = '/todos/<int:todo_id>'
        got = f.get_args()
        should_be = ['todo_id']
        assert got == should_be

    def test_get_args_with_multiple_args(self, f):
        f.url = '/todos/<int:list_id>/items/<int:item_id>'
        got = f.get_args()
        should_be = ['list_id', 'item_id']
        assert got == should_be

    def test_get_args_with_no_type_declaration(self, f):
        f.url = '/todos/<todo_id>'
        got = f.get_args()
        should_be = ['todo_id']
        assert got == should_be

    def test_get_args_invalid_parameter(self, f):
        f.url = '/todos/<todo id>'
        with warnings.catch_warnings(record=True) as w:
            # Make sure all warnings are caught
            warnings.simplefilter("always")

            # Make sure zero parameters are found
            got = f.get_args()
            should_be = []
            assert got == should_be

            # Then make sure the warning was raised
            assert len(w) == 1
            assert issubclass(w[-1].category, fab.MalformedParameterWarning)
            assert 'The number of "<" or ">" is' in str(w[-1].message)
