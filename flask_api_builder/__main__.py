"""
Generate the basic functionality required to create a Flask RESTful API given
a spec file written in the appropriate format.

Usage: flask_api_builder [options] <spec_file>

Options:
    -o=OUT --out-file=OUT           The path of the generated spec
                                    [Default: stdout]
    -e --example                    Shows an example spec file
    -h --help                       Print this help text
    -V --version                    Print the version information
"""

import os
import docopt
import flask_api_builder as fab


def _main(args):
    spec_file = os.path.abspath(args['<spec_file>'])
    spec = open(spec_file).read()

    api_as_str = fab.make_api(spec)

    if args['--out-file'] == 'stdout':
        print(api_as_str)
    else:
        with open(args['--out-file'], 'w') as f:
            f.write(api_as_str)


def main():
    # We need to do this mucking around with main() and _main() so that
    # you can use the API generator with both the "python -m" syntax and from
    # the commandline entry point
    args = docopt.docopt(__doc__, version=fab.__version__)
    _main(args)


if __name__ == "__main__":
    main()
