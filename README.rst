=================
Flask API Builder
=================

A really simple app that allows you to write out your RESTful APIs spec in a 
logical form and automatically generate stub functions for each endpoint.


Installing
==========

Install from Source
-------------------

To install from source, you will need to first clone the repository from
GitHub::

    git clone XXXX

Then run the `setup.py` file::

    python3 setup.py install


With Pip
--------

Or you can install directly from the Python Packaging Index::

    pip install flask_api_builder


Usage
=====

In order to generate your base API, you first need to write up a spec for it.
The spec contains the definitions for each of your API's end points, as well as
some variables to customize the Blueprint each API endpoint is attached to.


Writing The Spec File
---------------------

The spec file is designed to be quite intuitive to use. It is set out in a
table-like format, with each column being aligned with spaces. Any line
starting with a "#" is interpreted as a comment and ignored by the parser.


Defining Variables
~~~~~~~~~~~~~~~~~~

Defining variables is really easy, just add a line with `variable-name: value`.
The variable names currently supported are:

Blueprint-name
    The name for your blueprint (defaults to "api")
Prepend-with
    The path that all endpoints attached to your API Blueprint are prepended
    with (nothing by default)

All variables are **case insensitive**.


Defining Endpoints
~~~~~~~~~~~~~~~~~~

API Endpoints are defined one per line, in a table-like format. Each line
consists of 3 or 4 fields delimited by two or more whitespace characters. This
means that you need to separate your columns by **at least** two spaces so the
parser will read them correctly.

The fields correspond to an endpoint's METHOD, URL, DESCRIPTION and
(optionally) the NAME of the function generated. If no name is provided then
one will be generated for you given the method and URL parameters (no
guarantees that the generated name will be intelligible though).


Here is an example of a simple spec for a to-do list app::

    blueprint-name: api
    #Method    URL                       Description
    GET       /tasks                     Retrieve list of tasks
    GET       /tasks/<int:task_id>       Retrieve task number <task_id>
    POST      /tasks                     Create a new task 

