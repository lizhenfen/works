/**
 * Created by Administrator on 2017/4/11.
 */

//index页
function showAtRight(url) {
            var xmlHttp;
            if (window.XMLHttpRequest) {
                // code for IE7+, Firefox, Chrome, Opera, Safari
                xmlHttp=new XMLHttpRequest();    //创建 XMLHttpRequest对象
            }
            else {
                // code for IE6, IE5
                xmlHttp=new ActiveXObject("Microsoft.XMLHTTP");
            }

            xmlHttp.onreadystatechange=function() {
                //onreadystatechange — 当readystate变化时调用后面的方法

                if (xmlHttp.readyState == 4) {
                    //xmlHttp.readyState == 4    ——    finished downloading response

                    if (xmlHttp.status == 200) {
                        //xmlHttp.status == 200        ——    服务器反馈正常

                        document.getElementById("content").innerHTML=xmlHttp.responseText;    //重设页面中id="content"的div里的内容
                        executeScript(xmlHttp.responseText);    //执行从服务器返回的页面内容里包含的JavaScript函数
                    }
                    //错误状态处理
                    else if (xmlHttp.status == 404){
                        alert("出错了☹   （错误代码：404 Not Found），……！");
                        /* 对404的处理 */
                        return;
                    }
                    else if (xmlHttp.status == 403) {
                        alert("出错了☹   （错误代码：403 Forbidden），……");
                        /* 对403的处理  */
                        return;
                    }
                    else {
                        alert("出错了☹   （错误代码：" + request.status + "），……");
                        /* 对出现了其他错误代码所示错误的处理   */
                        return;
                    }
                }

              }

            //把请求发送到服务器上的指定文件（url指向的文件）进行处理
            xmlHttp.open("GET", url, true);        //true表示异步处理
            xmlHttp.send();
        }



//index页, 点击执行
function executeScript(html){

            var reg = /<script[^>]*>([^\x00]+)$/i;
            //对整段HTML片段按<\/script>拆分
            var htmlBlock = html.split("<\/script>");
            for (var i in htmlBlock)
            {
                var blocks;//匹配正则表达式的内容数组，blocks[1]就是真正的一段脚本内容，因为前面reg定义我们用了括号进行了捕获分组
                if (blocks = htmlBlock[i].match(reg))
                {
                    //清除可能存在的注释标记，对于注释结尾-->可以忽略处理，eval一样能正常工作
                    var code = blocks[1].replace(/<!--/, '');
                    try
                    {
                        eval(code) //执行脚本
                    }
                    catch (e)
                    {
                    }
                }
            }
        }

//index页，点击时，蓝色显示
function ButtonClickBlue() {
            $('ul.nav > li').click(function (e) {
                //e.preventDefault();    加上这句则导航的<a>标签会失效
                $('ul.nav > li').removeClass('active');
                $(this).addClass('active');
            });
        }
