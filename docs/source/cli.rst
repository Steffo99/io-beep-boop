################################
Using the command-line interface
################################

:mod:`io_beep_boop` includes a command line interface to (hopefully) facilitate the execution of certain tasks with the IO API.

The interface can be invoked by entering the following in environments where the package is installed:

.. code-block:: console

    (.venv)$ io-beep-boop

All commands can be suffixed with ``--help`` to read their documentation:

.. code-block:: console

    (.venv)$ io-beep-boop --help
    Usage: io-beep-boop [OPTIONS] COMMAND [ARGS]...

    Options:
      -t, --token TEXT  One of the two IO App API tokens of the service you want
                        to use.
      --base-url TEXT   The base URL of the IO App API to use.
      --help            Show this message and exit.

    Commands:
      registered-fast
      registered-slow

All tasks require a valid API key obtained from the `IO Developer website <https://developer.io.italia.it/profile>`_:

.. figure:: tokens.png

    Example key in the IO Developer website.

API keys can be passed programmatically as the ``--token`` parameter, or manually when prompted by the CLI:

.. code-block:: console

    (.venv)$ io-beep-boop --token="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

.. code-block:: console

    (.venv)$ io-beep-boop
    Token: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


Discover who is registered to a given service
=============================================

Given a text file containing a list of fiscal codes separated by newlines, :mod:`io_beep_boop` can find which ones are registered to a certain IO service.


Using the fast method
---------------------

By using the :meth:`~io_beep_boop.api.client.get_subscriptions_on_day` method on all days in a given date range, :mod:`io_beep_boop` can determine the users who registered to the service in those days.

.. code-block:: console

    (.venv)$ io-beep-boop registered-fast

.. warning::

    Internally, this uses the ``/subscription-feed/`` endpoint, which is not enabled by default for all API keys, and requires manual approval by the IO Team.

    If the token is not enabled to access the endpoint, a :class:`httpx.HTTPStatusError` will be raised.

    .. code-block:: console

        $ io-beep-boop registered-fast
        ...
        httpx.HTTPStatusError: Client error '403 Forbidden' for url 'https://api.io.italia.it/api/v1/subscriptions-feed/2022-04-28'
        For more information check: https://httpstatuses.com/403


Using the slow method
---------------------

By using the :meth:`io_beep_boop.api.client.get_profile` methods on all profiles with the given fiscal codes, :mod:`io_beep_boop` can determine which ones of those users are registered to the service and which ones are not.

.. code-block:: console

    (.venv)$ io-beep-boop registered-slow

By default, the method performs a single HTTP request per second, in order to avoid rate limits; this can be changed with the ``--sleep`` option:

.. code-block:: console

    (.venv)$ io-beep-boop registered-slow --sleep 5.0

.. warning::

    This endpoint performs a HTTP request for every single fiscal code in your given input document, which works, but may not be allowed by IO App API Terms of Service due to the extreme amount of requests possibly generated.

    Try to keep the ``--sleep`` delay high!
