prompt("xx") #弹出一个对话框让用户输入

注释: 
	单行: /
	多行: /*  */

第一课： 字符串 
	字符串合并: + 
	长度: str.length
	toUpperCase() | toLowerCase()  #大写/ 小写
	索引位置: indexOf("xxx")
	截取字符串: str.substring(start, end)  #截取位置
	提取整数部分: parseInt("10xxx")  #result: 10 
第二课: 数组
	var arr2 = [1, "hello", [2,3]]
	arr[1] = "jello world"
	最后一个数组: arr[arr.length - 1]
	数组的拼接: concat # arr1.concat(arr2)
	末尾增加元素:  arr.push("xxx")
	头部增加元素: arr.unshift("xx")
	末尾去掉元素: arr.pop()
	头部去掉元素: arr.shift()
	arr.splice(start,del_num,add_xxx)  # arr.splice(3,1,"xx") #从第3个值开始，去掉一个，增加xxx
	slice(start,end) #截取数组
	转换成字符: arr.join("_")
	分割字符串: str.split("_")
	
第三课 对象操作(字典)
	var obj = {a:1, b:2}
	b[1] 或 b.2 
	obj.x = 'xx' #若无则增加，有则修改
	删除属性: delete obj.x 
第四课: 数据类型判断
	typeof xxx
	object.prototype.toSting.call(xx) #更详细的判断，可以区别 [] 和 {}
	
第五课 函数
	# 网页加载完成，函数即存在
	function func_name(args){
		return xx;
	}
	# 运行到此处时，函数才存在
	func_name = function(args){
		return xx;
	}
	通过window对象加载
		window.func_name  #显示定义内容
		window.func_name("xx") 或 window['func_name']("xx")  #执行
	变量作用域: var 表示局部变量
	
	日期:
		d = new Date()
		d.getFullYear()
第六课	
	setTimeout(func, time) #延时执行任务
	setInterval(func, time) #设置定时任务
	
第七课
	#流程控制
	if(条件){
		执行1;
	}else if(条件){
		执行2;
	}
	else{
		执行3;
	}
	#for循环
	for(var i=1;i<=100;i++){
		执行;
		console.log(i)
		
	实例:
		var createDiv = document.createElement("div")
		document.body.appendChild(createDiv)
		createDiv.innerHTML("xx")
	}
	
第八课
	==:  不关注数据类型, 内容相同为true
	===: 全等于，数据类型和内容必须相同
	!=:
	!==: 完全不等于
	>, >=, <, <=
	!: 取反
	&& , || : 与高优先级
	() : 控制优先级
	实例
		a=false
		b='0'
		c=''
		d=0
		b == c #结果 false, '0'字符串不等于空字符串
		a == b; a==d; a==d; #结果均为true
	实例
		function addup(a,b){
			#设置默认值
			if(!b){
				b = 3.14;
			}
			return a*b;
		}
		function addup(a,b){
			#设置默认值
			b = b ||3.14;
			return a*b;
		}
		
第八课	
	switch(value){
		case v1:
			语句;
			break;
		default:
			语句;
	}
	
第九课
	#jquery
	$('#id').css('border','1px solid #ddd')
	节点的添加
		prependTo()
		appendTo()
		insertAfter()
	节点属性调整
		attr()
	节点的删除
		remove()
	节点的复制
		clone()
	实例:
		$("<div>1</div>").attr("id","id_name").prependTo("body")  #插入到body的第一个div
		$("<div>1</div>").attr("id","id_name").appendTo("body")  #插入到body的最后一个div
		
	事件管理	 
		click() #点击事件
		mouseover() #鼠标在上面
		mouseout()  #鼠标离开
		animat()  #动画效果
		fadeToggle(n_ms)  #触发渐变效果的时间
	数据传输

第十课
	document.createElement()
	document.getElementById()
	appendChild() #在当前节点下追加节点
	removeChild() #删除子节点
	push()
	pop()
	实例:
		var liArr = [];
		var add = function(){
			li = document.createElement('li');
			liArr.push(li);
			ul = document.getElementById("#ul");
			ul.appendChild(liArr[liArr.length - 1]);
		}
		var reduce = function(){
			index = liArr.length -1;
			if (index<0){
				return;
			}
			else{
				ul.removeChild(liArr[index]);
				liArr.pop();
			}
		}
