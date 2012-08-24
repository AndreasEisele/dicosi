dicosi
======

DIstributed COmputation -- made SImple


dicosi is a simple platform for distributed computation, meant to
support interoperability between programming languages and operating
systems. It is based on redis for managing the inter-process
communication and queueing.

Initial support exists for Python; support for Perl, Java, and C(++)
will be added later.

Server Usage
--------------

    >>> from dicosi import serve_forever
    >>> serve_forever([function1, function2])

Client Usage
--------------

    >>> from dicosi import call, multiCall
    >>> result1 = call("function1","argument1","argument2")
    >>> results = multiCall("function",[("argument1","argument2"),("argument1","argument2","argument3")])

