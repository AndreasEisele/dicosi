from redis import Redis
import sys



DBclosed=14
DBopen=15
redisHost='91.206.143.247'

r = Redis(db=DBopen,host=redisHost)

class dicosiException(Exception): pass



# print r.keys('*')


def func2pair(function):
    "normalise a function to a pair (name,function)"
    if isinstance(function, basestring):
        return function,eval(function)
    elif callable(function):
        return function.__name__,function
    else:
        return function
    

def serve_forever(functions):
    """establish a server for the given functions

    functions can be callables, strings denoting callables, or
    pairs of the form (name, callable) """

    name2function = dict(map(func2pair,functions))
    names = list(set(name2function)) # only the keys
    if len(names) < len(functions):
        raise ValueError('function name(s) repeated')
    
    serverID = r.incr('last-server-id')
    print >> sys.stderr, "server-%s serving functions %s to %s" % (
        serverID, names, r)
    # should give host/port, but where to find it?

    count = count_err = 0
    queues = ['call:%s'%n for n in names]+['shutdown:%s' % serverID]
    for n in names: r.incr('server-count:%s'%n)
    while True:
        request,id = r.blpop(queues)
        reqType,name = request.split(':',1)
        if reqType == 'shutdown': break
        # else assume it is a call
        recordID = 'request:%s'%id
        arg = r.hget(recordID,"arg")
        debug = r.hget(recordID,"debug")
        if debug: print >> sys.stderr,name,id,arg
        count += 1
        try:
            result = name2function[name](arg)
            status = "done"
        except Exception,e:
            status = "error"
            result = "%s"%e
            count_err += 1
        r.hset(recordID,"result",result)
        r.hset(recordID,"status",status)
        r.rpush('result:%s'%id,status)
    for n in names: r.decr('server-count:%s'%n)
    print >> sys.stderr,"server-%s terminated after processing %s requests (%s of which failed)" % (
        serverID, count, count_err)

def shutdown(serverID):
    r.rpush('shutdown:%s'%serverID,'*')
    # should be restricted to existing servers 

def multi_call(function, args, wait_for_server=False):
    if not wait_for_server:
        assert r.get('server-count:%s'%function)>0
    ids = []
    for arg in args:
        resultID = r.incr('last-result-id')
        r.hmset('request:%s'%resultID,{'function':function,'arg':arg,'status':'todo'})
        r.rpush('call:%s'%function,resultID)
        ids.append(resultID)

    _done = [r.blpop('result:%s'%id) for id in ids]
    results = []
    for id in ids:
        rId = 'request:%s'%id
        result = r.hget(rId,'result')
        if r.hget(rId,'status')=='done':
            r.hset(rId,'status','delivered')
            results.append(result)
        else:
            r.hset(rId,'status','error-delivered')
            results.append(dicosiException(result))
        r.move(rId,DBclosed)
    return results
