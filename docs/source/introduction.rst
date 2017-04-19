Introduction
============

The eContext Authentication API allows provides an application and user management platform
allowing and allows authentication and (eventually) authorization controls that can be used
to control access to various resources.

Input Format
------------

The input format to the eContext Authentication API is specified using the HTTP Content-Type
header  (:rfc:`2616#section-14.17`). A Content-Type of ``application/json`` is preferred, and
there is no guarantee that other Content-Types will be honored.

Output Format
-------------

The output format is generally set by using the HTTP Accept header (:rfc:`2616#section-14.1`).
The default output format for the eContext API is JSON (``application/json``). As the default
output format, all examples in this documentation are displayed using JSON.

The following output formats are currently supported:

* application/json (:rfc:`4627`)