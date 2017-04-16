vrrp: virtual router redundancy protocol
	1. 专门用于实现lvs的高可用
	2. vrrp解决静态路由出现的单点故障， 通过竞选协议机制实现将路由的任务交与某台vrrp服务器； 设置优先级
		所有的协议报文通过IP多播(224.0.0.18)形式发送，虚拟路由器VRID(0~255)和一组IP组成，一组vrrp对外提供相同的MAC和IP，
		使用了加密协议
	
	两大功能:
		failover
		healthcheck  #专门用于lvs
			1. 直接在keepalive中配置实现lvs
			2. 对lvs后的集群进行健康检查
	原理：
		通过vrrp协议实现，主节点不断的发送心跳消息，告诉备节点还活着，当备节点接收不到消息时，就调用自身程序接管主节点的IP资源和服务，当主节点恢复
		后，备节点释放主节点故障时的资源，恢复到备用角色
		
源码安装:
	0. yum install kernel-devel -y
	1. ln -s /usr/src/kernels/`uname -r` /usr/src/linux