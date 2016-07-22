"""
A really simple app that allows you to write out your RESTful API's spec
in a logical form and automatically generate the necessary boilerplate.`
"""

from collections import namedtuple
import re
import jinja2
import warnings


class MalformedParameterWarning(Warning):
    pass


Rule = namedtuple('Rule', ('method', 'url', 'description', 'name'))

FUNCTION_TEMPLATE = jinja2.Template('''
@{{ blueprint }}.route('{{ url }}', methods=['{{ method|default('GET') }}'])
def {{ name }}({{ args_list|join(', ') }}):
    """
    {{ docstring }}
    """
    # TODO: Complete me!
    raise NotImplemented''')

PREAMBLE_TEMPLATE = jinja2.Template("""
from flask import Blueprint

{{ blueprint }} = Blueprint({{ bp_args|join(', ') }})
""")


class Function:
    def __init__(self, url, method, description, blueprint='api',
            name=None, template=None):
        self.url = url
        self.method = method.upper()
        self.description = description
        self.blueprint = blueprint
        self.name = name or None
        self.template = template or FUNCTION_TEMPLATE

    def get_args(self):
        """
        Find all the arguments in the url. These are usually bits
        that look like "<int:task_id>" and so on...
        """
        parameters = re.findall(r'<(?:[\w_]+:)?([\w_]+)>', self.url)

        if (self.url.count('<') != len(parameters) or
            self.url.count('<') != len(parameters)):
            warnings.warn(
                    'The number of "<" or ">" is different from the number of '
                    'parameters found. Make sure parameters look like '
                    '"<int:task_id>"',
                    MalformedParameterWarning)

        return parameters

    def generate_name(self, args):
        """
        Try to create a stock name for the function given the information
        provided.

        The idea is to create names like the following:
        * get_tasks
        * get_tasks_by_id
        * delete_task_by_id

        Most of the time you'll probably get gibberish, but there's a reason
        you are given the option of specifying a name in your spec.
        """
        name = []
        name.append(self.method.lower())

        # Get the last "word" in the url that isn't a parameter
        for word in reversed(self.url.split('/')):
            if '<' in word or '>' in word:
                continue
            else:
                name.append(word)
                break

        # If there are any arguments, then add "by_[last arg]"
        if args:
            name.append('by')
            name.append(args[-1])

        return '_'.join(name)

    def render(self):
        """
        Render the template given the information we already have.
        """
        args = self.get_args()
        name = name or self.generate_name(args)

        func = self.template.render(
                blueprint=self.blueprint,
                url=self.url,
                method=self.method,
                name=name,
                args_list=args,
                docstring=self.description)
        return func

    def __repr__(self):
        return '<{}: url="{}" method="{}">'.format(
                self.__class__.__name__,
                self.url,
                self.method)



class APIGenerator:
    def __init__(self, config, function_template=None):
        self.config = config
        self.blueprint = config.get('blueprint-name', 'api')
        self.rules = self.config['rules']
        self.function_template = function_template

    def preamble(self):
        """
        Generate the import statements and the blueprint definition.
        """
        bp_args = []
        bp_args.append(repr(self.blueprint))
        bp_args.append('__name__')

        if 'prepend-with' in self.config:
            bp_args.append('url_prefix="{}"'.format(self.config['prepend-with']))

        return PREAMBLE_TEMPLATE.render(
                blueprint=self.blueprint,
                bp_args=bp_args)

    def functions(self):
        """
        Turn each of the function "Rules" into their corresponding Function
        representations.
        """
        funcs = []
        for rule in self.rules:
            f = Function(
                    rule.url,
                    rule.method.upper(),
                    rule.description,
                    blueprint=self.blueprint,
                    name=rule.name,
                    template=self.function_template)
            funcs.append(f)
        return funcs

    def render(self):
        """
        Generate our API file.
        """
        lines = []

        # Add the preamble
        lines.append(self.preamble())

        # Give it a bit of space
        lines.append('')
        lines.append('')

        lines.extend(f.render()+'\n' for f in self.functions())

        return '\n'.join(lines).strip()


def parse_spec(spec):
    config = {}
    config['rules'] = []

    for i, line in enumerate(spec.splitlines()):
        # Remove trailing whitespace
        line = line.strip()

        # Skip comments and empty lines
        if line.startswith('#') or not line:
            continue

        # Split by multiple space sections
        groups = re.split(r'\s\s+', line)

        if len(groups) == 1:
            # It's an option
            left, right = groups[0].split(':')

            # If it fails, throw syntax error
            config[left.strip().lower()] = right.strip()
        elif len(groups) == 3:
            method, url, description = groups
            new_rule = Rule(method, url, description, None)
            config['rules'].append(new_rule)
        elif len(groups) == 4:
            method, url, description, name = groups
            new_rule = Rule(method, url, description, name)
            config['rules'].append(new_rule)
        else:
            raise SyntaxError('Too many fields on line {}'.format(i+1))

    return config
