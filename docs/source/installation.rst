############
Installation
############

This page will act as a tutorial on how to safely setup a Python environment on a computer, and on how to install :mod:`io_beep_boop` inside.

.. hint::

    If you are a Python developer, and you intend to use this library to develop new tools, you might be interested to know that:

    - :mod:`io_beep_boop` is distributed through the `Python Package Index <https://pypi.org/>`_, so you can install it with any Python dependency manager and use it in any Python project;
    - :mod:`io_beep_boop` supports :pep:`518`, so it may be installed from source using ``pip install .``;
    - :mod:`io_beep_boop` uses `Poetry <https://python-poetry.org/>`_ as a dependency manager.


Installing Python
=================

:mod:`io_beep_boop` requires Python 3.10 or later.

You can download Python at the `Downloads page of the official website <https://www.python.org/downloads/>`_.

Ensure that "Add Python to the PATH" is checked during installation, or you will not be able to run scripts from the command line!


Creating a :mod:`venv`
======================

To prevent dependency conflicts, it is highly suggested to create a new :mod:`venv` ( *v*\ irtual *env*\ ironment) to install :mod:`io_beep_boop` in.

To do so, open a terminal or command prompt, create a new folder, access it, and when inside run ``python -m venv .venv``:

.. code-block:: console

    $ cd Documents/Workspaces
    $ mkdir IOTools
    $ cd IOTools
    $ python -m venv .venv

Once created, run the following command to access the venv:

.. code-block:: console

    $ source ./.venv/bin/activate

.. code-block:: doscon

    > .\.venv\Scripts\activate

You will have to activate the :mod:`venv` on every subsequent terminal session, or you won't be able to access the packages installed inside it!

.. seealso::

    `Installing packages using pip and virtual environments <https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/>`_ by the Python Packaging Authority.


Installing :mod:`io_beep_boop`
==============================

Once enabled the venv, you can install packages in it by using :mod:`pip`.

Specifically, you'll want to install :mod:`io_beep_boop`:

.. code-block:: console

    (.venv)$ pip install io-beep-boop
    ...
    Successfully installed io-beep-boop-0.1.0

The installation is complete!
You may proceed to :doc:`cli`.