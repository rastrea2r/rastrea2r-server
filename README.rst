rastrea2r-server
================

Flask based Restful Server to handle requests from rastrea2r


Quickstart
==========

============
Requirements
============
* Python 3.4+
* VirtualEnv

============
Features
============
* Sample Rest Client
* Strong Password Hashing (stored in sqlite DB)
* Rate limiting for safety
* JSONified error handling
* Extensive logging to both stdout and log files

=============
Install Guide
=============

.. note::

    It is best practice to install run Python projects in a virtual
    environment, which can be created and activated as follows using
    Python 3.6+.

* Make sure you have virtualenv and Python3 installed on your system (pip3 install virtualenv)
* Clone the repo: ```https://github.com/rastrea2r/rastrea2r-server.git```
* Install the virtualenv and activate it

 .. code-block:: console

    $ cd rastrea2r-server
    $ make venv
    $ source ./.venv/rastrea2r_server/bin/activate
    (rastrea2r_server) $ 

    * You must activate the virtualenv before starting the server
    * Initialize DB and Add a user 

 .. code-block:: console

    (rastrea2r_server) $./manage_server.py --init
    (rastrea2r_server) $./manage_server.py --add testuser 

* Start the server: 

 .. code-block:: console

    (rastrea2r_server) $./start_server.py


=======
Testing
=======

* Test the info request with a browser:

 .. code-block:: console

    http://localhost:5000/
    http://localhost:5000/rastrea2r/api/v1.0/info
    http://localhost:5000/rastrea2r/api/v1.0/echo?message=test
    http://localhost:5000/rastrea2r/api/v1.0/uptime
    http://localhost:5000/test
    
* Or you could use curl

 .. code-block:: console

    (rastrea2r_server) $curl -d '{"key1":"value1", "key2":"value2"}' -H "Content-Type: application/json" -H "Authorization: Basic dGVzdHVzZXI6dGVzdHBhc3N3ZA==" -X POST http://localhost:5000/rastrea2r/api/v1.0/results

    (rastrea2r_server) $curl -H "Authorization: Basic dGVzdHVzZXI6dGVzdHBhc3N3ZA=="  http://localhost:5000/rastrea2r/api/v1.0/rule?rulename=example.yara

    Note: Basic auth uses the base64 encoded string corresponding to username:password (in this case the username:password combo used was testuser:testpasswd)


.. _api-reference-label:

API Reference
=============
The `API Reference <http://rastrea2r_server.readthedocs.io>`_ provides API-level documentation.


.. include:: ../CHANGELOG.rst


.. _report-bugs-label:

Report Bugs
===========

Report bugs at the `issue tracker <https://github.com/rastrea2r/rastrea2r-server/issues>`_.

.. include:: ../.github/ISSUE_TEMPLATE/bug_report.md


New feautrue requests can be made using the following template in the bug tracker.

.. include:: ../.github/ISSUE_TEMPLATE/feature_request.md