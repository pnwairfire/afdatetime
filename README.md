# afdatetime

This package contains utilities for working with python's datetime
package.

***This software is provided for research purposes only. Use at own risk.***

## Development

### Clone Repo

Via ssh:

    git clone git@github.com:pnwairfire/afdatetime.git

or http:

    git clone https://github.com/pnwairfire/afdatetime.git

### Install Dependencies

Run the following to install required python packages as well
as test and useful dev packages:

    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    pip install -r requirements-test.txt

### Setup Environment

To import afdatetime in development, you'll have to add the repo
root directory to the search path.

## Running tests

You can run tests with pytest:

    py.test
    py.test ./test/unit/afdatetime/
    py.test ./test/unit/afdatetime/test_parsing.py

You can also use the ```--collect-only``` option to see a list of all tests.

    py.test --collect-only

Use the '-s' option to see output:

    py.test -s

## Installation

### Installing With pip

First, install pip (with sudo if necessary):

    apt-get install python-pip

Then, to install, for example, v2.0.0, use the following (with sudo if
necessary):

    pip install --extra-index https://pypi.airfire.org/simple afdatetime==2.0.0

If you get an error like    ```AttributeError: 'NoneType' object has no attribute 'skip_requirements_regex```, it means you need in upgrade pip.  One way to do so is with the following:

    pip install --upgrade pip

## Usage:

Run each script with the `-h` option to see its usage.
