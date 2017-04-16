def ip2int(ip):
    num = 0
    ip_list = ip.split('.')
    for i in range(4):
        num += int(ip_list[i]) * 256**(3-i)
    return num

def int2ip(num):
    ip_list = []
    for i in range(4):
        num, res = divmod(num, 256)
        ip_list.append(str(res))
    ip_list.reverse()
    return '.'.join(ip_list)

if __name__ == "__main__":
    num = ip2int('192.168.100.20')
    print(int2ip(num))