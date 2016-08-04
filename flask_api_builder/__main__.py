"""
Generate the basic functionality required to create a Flask RESTful API given
a spec file written in the appropriate format.

Usage: flask_api_builder [options]

Options:
    -s=SPEC --spec-file=SPEC        The spec file to read from
                                            [Default: api.spec]
    -o=OUT --out-file=OUT           The path of the generated spec
                                            [Default: stdout]
    -e --example                    Shows an example spec file
    -f --force                      Overwrite the output file if it already
                                    exists [Default: False]
    -h --help                       Print this help text
    -V --version                    Print the version information
"""

import os
import sys
import docopt
import flask_api_builder as fab


def _main(args):
    if args.get('--example'):
        # We need to print the example to the screen
        file_path = os.path.join(os.path.dirname(__file__),
                                 'examples/basic_api.spec')
        with open(file_path) as f:
            print(f.read())
            sys.exit(0)

    spec_file = os.path.abspath(args['--spec-file'])

    if not os.path.exists(spec_file):
        print('File not found: {}'.format(spec_file))
        print('You can specify the spec file with the "--spec-file" option')
        sys.exit(1)

    spec = open(spec_file).read()

    api_as_str = fab.make_api(spec)

    if args['--out-file'] == 'stdout':
        print(api_as_str)
    else:
        out_file = args['--out-file']
        if os.path.exists(out_file) and not args['--force']:
            print('File already exists: {}'.format(out_file))
            sys.exit(1)

        with open(out_file, 'w') as f:
            f.write(api_as_str)


def main():
    # We need to do this mucking around with main() and _main() so that
    # you can use the API generator with both the "python -m" syntax and from
    # the commandline entry point
    args = docopt.docopt(__doc__, version=fab.__version__)
    _main(args)


if __name__ == "__main__":
    main()
