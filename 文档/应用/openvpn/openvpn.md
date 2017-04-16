桥接不推荐使用:
	VPN桥接操作: http://blog.csdn.net/dog250/article/details/6839585
以下操作均为路由操作:
操作:
    通用操作:
        1. 安装依赖     yum install gcc gcc-c++  lzo-devel openssl openssl-devel pam pam-devel pkcs11-helper pkcs11-helper-devel -y
        2. 下载软件     wget http://oss.aliyuncs.com/aliyunecs/openvpn-2.2.2.tar.gz 
        3. 编译安装     ./configure && make && make install
        
    服务器端:
        0. 启用路由转发   echo 1 > /proc/sys/net/ipv4/ip_forward
        1. 编辑vars    easy-rsa/2.0/vars   #主要从于生成证书时的默认配置
        2. 生成证书
            1.  ./clean-all   #清空前面的数据
            2.  ./build-ca    #生成ca证书
            3.  ./build-key-server #生成服务器证书
                    ./build-key-server server-key-name
            4.  ./build-key   #生成客户端证书
                    ./build-key client-key-name 
            5.  ./build-dh    #生成防攻击秘钥
            6. 拷贝证书到固定的目录  cp -a keys/*  keys_save_dirs
        3. 生成配置文件    cp sample-config-files/server.conf   server-config-dir
        4. 启动   openvpn server.conf  
        5. 配置文件关键参数
            local 0.0.0.0                  #指定地址
            port 1194                      #指定端口
            proto udp                      #指定vpn之间的传输协议[udp,tcp]
            dev tap0                       # dev tun 创建ip通道, dev tap创建以太网通道
            ca  ca.crt                     #ca证书的路径
            cert server.crt                #服务器证书的路径
            key  server.key                #服务器秘钥的路径
            dh   dh1024.pem                #与安全相关
            server  ip netmask             #创建客户端分配的地址，此方式表明是路由
            ifconfig-pool-persist ipp.txt  #固定分配地址, 格式: hostname ip
            push "route ip netmask"        #推送路由到vpn客户端
            client-to-client               #客户端直接相互连接
            keepalive 10 120               #保持连接, 每10s测试连接一次, 超时连接120s
            cipher AES-256-CBC             #证书加密算法, 这个要和客户端的算法保持一致，
            comp-lzo                       #启用压缩数据，这个要和客户端的算法保持一致
            status openvpn-status.log      #状态日志文件
            log         openvpn.log        #日志文件
            verb 3                         #默认不改变
              
    客户端:
        1.  生成配置文件和证书
            启动: openvpn --config client.opvn
            
        2. 配置文件
            client
            dev tap0                       #和服务端保持一致
            proto udp
            remote 219.232.35.144 1194     #指定服务端的主机和端口
            resolv-retry infinite
            persist-key
            persist-tun
            ca ca.crt
            cert dubbo.crt
            key dubbo.key
            remote-cert-tls server         #服务器端认证
            cipher AES-256-CBC             #和服务器保持一致
            comp-lzo                       #和服务器保持一致
            verb 3                         #默认不改变
            
  证书吊销:
	0. 低版本openvpn, 需要注销openssl.cnf 的最后6行
	1. ./revoke-fulll certi-key-name
	2. cat index.txt 中第一个标记V变成 R， 表示已注销用户
	3. server.cnf
		crl-verify /etc/openvpn/keys/crl.pem
	4. 重启openvpn生效
	