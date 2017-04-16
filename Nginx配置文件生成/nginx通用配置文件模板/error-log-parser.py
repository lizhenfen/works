with open('error.log', 'r') as fd:
    '''
    {
        'err': '错误日志和日志'
        'client': '客户端地址'
        'server': '请求的服务器'
        'request': '请求的url',
        'upstream': '后台'
        'host': '访问主机',
        'refer': '访问来源, 可能有也可能没有'
    }
    '''
    for line in fd:
        line = line.rstrip().split(',')
        if len(line) < 5:
            continue
        err = line[0]
        client = line[1].split(':')[-1]
        server = line[2].split(':')[-1]
        request = line[3] + ','.join([ l for l in line[4:] if ':' not in l ])
        if request:
            request = ':'.join(request.split(':')[1:])
        upstream = [ l for l in line[4:] if 'upstream:' in l  ]
        if upstream:
            upstream = ':'.join(upstream[0].split(':')[1:])
        host =  [l for l in line[4:] if 'host:' in l ]
        if host:
            host = ':'.join(host[0].split(':')[1:])
        referrer = [l for l in line[4:] if 'referrer:' in l ]
        if referrer:
            referrer = ':'.join(referrer[0].split(':')[1:])
        data = {
        'errlog': err,
        'client':client,
        'server': server,
        'request':request,
        'upstream': upstream,
        'host': host,
        'referrer': referrer,
        }
        print(data)
