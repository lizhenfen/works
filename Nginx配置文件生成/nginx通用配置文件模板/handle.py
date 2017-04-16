def check_url(url):
    res_dict = {}
    domain_ip, domain_uri, other_uri = url.split("/", maxsplit=2)
    if ":" in domain_ip:
        ip, port = domain_ip.split(":")
        port = int(port)
    else:
        ip = domain_ip
        port = 80

    if "-" in domain_uri:
        uri = domain_uri.split("-")[-1]
    else:
        uri = domain_uri

    res_dict = {
        "ip": ip,
        "port": port,
        "uri": uri
    }
    return res_dict

if __name__ == "__main__":
    user_url = "192.168.15.37:3300/vats-api-order/xxx/pp"
    print(check_url(user_url))