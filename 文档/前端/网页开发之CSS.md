第一节:
    div:
        内部样式 style=""
        px
        background-color
        height, weight：  px 或 100%  # 100%表示占满网页
        
 第二课:
    #div
    position: absolute  绝对位置
    top, left  
    
第三课:
    #关于字体
    font-size
    font-family
    text-align: center, left, right  #对齐方式
    color
第四课:
    line-height: 行高
    border: 
        border-width
        border-style:
            dotted, solid, double, dashed
        border-color: 
第五课：
    overflow:  #div中 段溢出的处理方式
        auto
        scroll
        hidden
    padding:   #内边距
        padding-top
        padding-bottom
    margin:    #外边距.  上右下左
    opacity: 0.0-1.0  #透明度 
    display: none #隐藏div
    
第六课；
    z-index: -1  # div嵌套时，内部的div设置此css, 会自动到下面
    # 内部的div的 位置是基于外部的div的左上点开始计算的
    
第七课:
    id=""   #唯一标识符, 定义div的名称
第八课
    让div盒子自动居中:  margin: 10px auto
第九课
    并列div,
    position: absolute #默认是以浏览器左上角为基点定位
    position: relative  # 当前div中包含的div都是以本div为基点定位
    <div style=" position:relative ">
        <div style=" position: absolute ">
        </div>
    </div>
 第十课
    <img src="xxxx/xxx" />
第十一课
    <a style="
    display: block #显示为div格式的块
    background: url(image/xxx.gif) no-repeat 015px #背景图片可以点击到url超链接; 不重复; 左右距离0， 上下距离15
    " href="xxxx" > </a>
    
    全局样式:
        a:link {
            text-decoration: none  #去掉超链接的下划线
        }
        a:visited {
            text-decoration: none  #访问过的连接的配置
        }
		
第十二课
    #事件触发
    #div_id a:hover {    #div_id 块的超链接
                #当鼠标经过超链接 a时，触发内部的css
        }
第十三课
    <ul id="menu">
        <li>
            <a href="xx" > <a>
        </li>
    </ul>
    
    #去掉默认样式
    li,ul { list-style-type: none ; height: 0 ; margin: 0px; padding:0px; }
    # 重新设置样式
    #menu li { float: left #从左到右依次排列
            height: 40px; width: 40px #设置宽和高
                }
                
第十四课
    border: 1px solid white  #边框的粗细，样式，颜色
    onMouseOver="xx" ,onMouseOut=“xx” #javascript触发鼠标在字体上和离开字体的动作
   
---javascript   
第十五课
    句子以 ; 号结尾
   alert("")  #浏览器弹出对话框、
   if () {
   }
   
第十六课
    var name = 1  #声明变量
    prompt()  #弹出一个对话框
    
第十七课
    x = dom.getElementById("xx")  #根据id获取对象
    console.log(x.style.样式名)  #获取样式的的值
   
第十八课
    // 单行注释
第十九课
    a = document.createElement("div")  #创建成对的属性
    a.style.position = "absolute"  #设置css属性值
    # 网页中显示
    document.body.appendChild(a)
    a.innerHTML("显示文字")  #会覆盖前面的设置
    
第二十课
    var z = [document.createElement("div"),document.createElement("div"),document.createElement("div")]
    for (var i=0; i< z.length; i++){
        var t = z[i].style
        var y = 20 + i*20 
    }
    
第二十一课
    this: 调用函数的那个对象
    <script type="text/javascript" src="*.js">

第二十二课
    <p> </p>  #段落
    background: url(image/xx.gif) repeat-x  #重复
    word-wrap: break-word  #牺牲词语的完整性强制换行
    break-word: normal    # 词语拆分的规则
    
第二十三课
    border-radius: 5px 5px 0 0 弧度左右上下 边框的角修改成圆角； 
	span
	clear: both 清除上层的div的浮动(float属性); 需要在新<div>内增加
    
第二十四课
	letter-spacing: 字符间的距离、
	<b> </b>:

第二十五课
	<strong> </strong> #字体加粗
	
	