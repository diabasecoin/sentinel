# Diabase Sentinel

[![Test Status](https://github.com/diabasepay/sentinel/actions/workflows/test.yml/badge.svg)](https://github.com/diabasepay/sentinel/actions/workflows/test.yml)

> An automated governance helper for Diabase Masternodes.

Sentinel is an autonomous agent for persisting, processing and automating Diabase governance objects and tasks. It is a Python application which runs alongside the DiabaseCore instance on each Diabase Masternode.

## Table of Contents
- [Install](#install)
  - [Dependencies](#dependencies)
- [Usage](#usage)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Maintainer](#maintainer)
- [Contributing](#contributing)
- [License](#license)

## Install

These instructions cover installing Sentinel on Ubuntu 18.04 / 20.04.

### Dependencies

Update system package list and install dependencies:

    $ sudo apt-get update
    $ sudo apt-get -y install git python3 virtualenv

Make sure Python version 3.6.x or above is installed:

    python3 --version

Make sure the local DiabaseCore daemon running is at least version 0.15.0.

    $ diabased --version | head -n1

### Install Sentinel

Clone the Sentinel repo and install Python dependencies.

    $ git clone https://github.com/diabasepay/sentinel.git && cd sentinel
    $ virtualenv -p $(which python3) ./venv
    $ ./venv/bin/pip install -r requirements.txt

## Usage

Sentinel is "used" as a script called from cron every minute.

### Set up Cron

Set up a crontab entry to call Sentinel every minute:

    $ crontab -e

In the crontab editor, add the lines below, replacing '/path/to/sentinel' to the path where you cloned sentinel to:

    * * * * * cd /path/to/sentinel && ./venv/bin/python bin/sentinel.py >/dev/null 2>&1

### Test Configuration

Test the config by running tests:

    $ ./venv/bin/py.test ./test

With all tests passing and crontab setup, Sentinel will stay in sync with diabased and the installation is complete

## Configuration

Configuration is done via environment variables. Example:

```sh
$ RPCUSER=diabase RPCPASSWORD=password RPCHOST=127.0.0.1 RPCPORT=17675 ./venv/bin/python bin/sentinel.py
```

A path to a `diabase.conf` file can be specified in `sentinel.conf`:

    # warning: deprecated
    diabase_conf=/path/to/diabase.conf

This is now deprecated and will be removed in a future version. Users are encouraged to update their configurations to use environment variables instead.


## Troubleshooting

To view debug output, set the `SENTINEL_DEBUG` environment variable to anything non-zero, then run the script manually:

    $ SENTINEL_DEBUG=1 ./venv/bin/python bin/sentinel.py

## Maintainer

[@nmarley](https://github.com/nmarley)

## Contributing

Please follow the [DiabaseCore guidelines for contributing](https://github.com/diabasepay/diabase/blob/master/CONTRIBUTING.md).

Specifically:

* [Contributor Workflow](https://github.com/diabasepay/diabase/blob/master/CONTRIBUTING.md#contributor-workflow)

    To contribute a patch, the workflow is as follows:

    * Fork repository
    * Create topic branch
    * Commit patches

    In general commits should be atomic and diffs should be easy to read. For this reason do not mix any formatting fixes or code moves with actual code changes.

    Commit messages should be verbose by default, consisting of a short subject line (50 chars max), a blank line and detailed explanatory text as separate paragraph(s); unless the title alone is self-explanatory (like "Corrected typo in main.cpp") then a single title line is sufficient. Commit messages should be helpful to people reading your code in the future, so explain the reasoning for your decisions. Further explanation [here](http://chris.beams.io/posts/git-commit/).

### Code Style

Please use `black` to format code automatically before opening a PR:

```sh
./venv/bin/black .
```

## License

Released under the MIT license, under the same terms as DiabaseCore itself. See [LICENSE](LICENSE) for more info.
