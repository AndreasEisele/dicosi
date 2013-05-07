dicosi
======

DIstributed COmputation -- made SImple


dicosi is a simple-to-use platform for distributed computation, meant
to support interoperability between programming languages and operating
systems. It is based on redis for managing the inter-process
communication and queueing.

Initial support exists for Unix shells and Python; support for Perl, Java, and C(++)
will be added later.

# Unix shells:
## Server Usage
    $ dServer fName cmdLine 
    
## Client Usage
    $ dClient fName  

# Python:
## Server Usage
    >>> from dicosi import serve_forever
    >>> serve_forever([function1, function2])

## Client Usage
    >>> from dicosi import call, multi_call
    >>> result1 = call("function1","argument1","argument2")
    >>> results = multi_call("function",[("argument1","argument2"),("argument1","argument2","argument3")])

