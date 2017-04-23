/**
 * Created by Administrator on 2017/4/11.
 */
// 个人柱状图，拜访次数统计
function LoadPersonColumnGraph(req) {
        $.post("/employee/visit/count",req, function (data) {
            data = $.parseJSON(data);
            var x = data["x_series"];
            var y = data["y_series"];
        //此处开始图表展示
        var myChart = echarts.init(document.getElementById('main'));
        option = {
            color: ['#3398DB'],
            tooltip : {
                trigger: 'axis',
                axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                    type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                }
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '15%',
                containLabel: true
            },
            xAxis : [
                {
                    axisLabel :{
                    interval:0, //显示所有的x轴的数据
                    //rotate: -45,  //逆时针旋转45
                    margin: 5
                } ,
                    type : 'category',
                    data : x,
                    axisTick: {
                        alignWithLabel: true
                    }
                }
            ],
            yAxis : [
                {
                    // type : 'category',
                    // data : ['10','20','30','40'],
                    axisTick: {
                        alignWithLabel: true
                    }
                }
            ],
            series : [
                {
                    name:'直接访问',
                    type:'bar',
                    barWidth: '40%',
                    data:y
                }

            ],
            label: {
                    normal: {
                        show: true,
                        position: 'top',
                        formatter: '{c}'
                    }
                },
            itemStyle: {
                        normal: {

                            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                offset: 0,
                                color: 'rgba(17, 168,171, 1)'
                            }, {
                                offset: 1,
                                color: 'rgba(17, 168,171, 0.1)'
                            }]),
                            shadowColor: 'rgba(0, 0, 0, 0.1)',
                            shadowBlur: 10
                        }
                    }
        };
        myChart.setOption(option); // 到此 图表展示结束
        //此处开始展示表格
        $('#cusTable').bootstrapTable('destroy');
                $(function () {
					$('#cusTable').bootstrapTable({
					    columns: [{
                                    field: 'PK_CORP',
                                    title: '公司'
                                }, {
                                    field: 'PSNNAME',
                                    title: '姓名'
                                }, {
                                    field: 'VDATE',
                                    title: '开始时间'
                                }],
						data: data["buckets"]
					});
				});
        }); //此处 ajax的get方法结束

    }

//公司柱状图，拜访次数统计
function LoadCompanyColumnGraph(req) {
        $.post("/company/visit/count",req, function (data) {
            data = $.parseJSON(data);
            console.log(data);
            var x = data["x_series"];
            var y = data["y_series"];
        //此处开始图表展示
        var myChart = echarts.init(document.getElementById('main'));
        option = {

            color: ['#3398DB'],
            tooltip : {
                trigger: 'axis',
                axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                    type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                }
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis : [
                {
                    type : 'category',
                    data : x,
                    axisTick: {
                        alignWithLabel: true
                    }
                }
            ],
            yAxis : [
                {
                    axisTick: {
                        alignWithLabel: true
                    }
                }
            ],
            series : [
                {
                    name:'直接访问',
                    type:'bar',
                    barWidth: '40%',
                    data:y
                }

            ],
            label: {
                    normal: {
                        show: true,
                        position: 'top',
                        formatter: '{c}'
                    }
                },
            itemStyle: {
                        normal: {

                            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                offset: 0,
                                color: 'rgba(17, 168,171, 1)'
                            }, {
                                offset: 1,
                                color: 'rgba(17, 168,171, 0.1)'
                            }]),
                            shadowColor: 'rgba(0, 0, 0, 0.1)',
                            shadowBlur: 10
                        }
                    }
        };
        myChart.setOption(option);
        // 到此 图表展示结束

        $('#cusTable').bootstrapTable('destroy');
                $(function () {
					$('#cusTable').bootstrapTable({
					    //是否显示行间隔色
                        striped: true,
                        //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
                        cache: false,
                        //是否显示分页（*）
                        pagination: true,
                         //是否启用排序
                        sortable: false,

                        //初始化加载第一页，默认第一页
                        //我设置了这一项，但是貌似没起作用，而且我这默认是0,- -
                        pageNumber:1,
                        //每页的记录行数（*）
                        pageSize: 5,
                        //可供选择的每页的行数（*）
                        pageList: [5,10, 25, 50, 100],

                        //分页方式：client客户端分页，server服务端分页（*）
                        sidePagination: "client",
                        //是否显示搜索
                        search: false,
                        //Enable the strict search.
                        strictSearch: true,
					    columns: [{
                                    field: 'key',
                                    title: '姓名'
                                }, {
                                    field: 'doc_count',
                                    title: '拜访次数'
                                }],
						data: data["buckets"]
					});
				});
                }); //此处 ajax的get方法结束
    }

// 公司趋势图
function LoadCompantyTrendGraph(req) {
        $.post("/echarts/api/company",req, function (data) {
            var x = data["x_series"];
            var y = data["y_series"];
        //此处开始图表展示
        var myChart = echarts.init(document.getElementById('main'));
        option = {
            color: ['#ff3d3d'],
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                x: 'left',
                padding: [10, 20, 0, 20],
                data: ['拜访次数'],
                selected: {
                    'VATS': true
                }
            },
            grid: {
                left: '0',
                right: '5%',
                bottom: '10%',
                top: '13%',
                containLabel: true
            },

            xAxis: {
                axisLabel :{
                    interval:0, //显示所有的x轴的数据
                    rotate: -45,
                    margin: 5
                } ,
                type: 'category',
                boundaryGap: false,
                splitLine: { //网格线
                    show: true,
                    lineStyle: {
                        color: ['#b1b1b1'],
                        type: 'dashed'
                    }
                },
                data:  x
            },
            yAxis: {
                splitLine: { //网格线
                    show: true,
                    lineStyle: {
                        color: ['#b1b1b1'],
                        type: 'dashed'
                    }
                }
            },
            series: [{
                name: 'VATS',
                type: 'line',
                data:  y,
                label: {
                    normal: {
                        show: true,
                        position: 'top' //值显示
                    }
                }
            }]
        };
        myChart.setOption(option)

        });//请求结束
    }

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

//index页, 公司趋势图
function LoadCompanyTrend(req) {
            $.post("/echarts/api/company",req,function (data) {
            var x = data["x_series"];
            var y = data["y_series"];
        //此处开始图表展示
        var myChart = echarts.init(document.getElementById('main'));
        option = {
            color: ['#ff3d3d'],
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                x: 'left',
                padding: [10, 20, 0, 20],
                data: ['拜访次数'],
                selected: {
                    'VATS': true
                }
            },
            grid: {
                left: '0',
                right: '5%',
                bottom: '10%',
                top: '13%',
                containLabel: true
            },

            xAxis: {
                axisLabel :{
                    interval:0, //显示所有的x轴的数据
                    rotate: -45,
                    margin: 5
                } ,
                type: 'category',
                boundaryGap: false,
                splitLine: { //网格线
                    show: true,
                    lineStyle: {
                        color: ['#b1b1b1'],
                        type: 'dashed'
                    }
                },
                data:  x
            },
            yAxis: {
                splitLine: { //网格线
                    show: true,
                    lineStyle: {
                        color: ['#b1b1b1'],
                        type: 'dashed'
                    }
                }
            },
            series: [{
                name: 'VATS',
                type: 'line',
                data:  y,
                label: {
                    normal: {
                        show: true,
                        position: 'top' //值显示
                    }
                }
            }]
        };
        myChart.setOption(option)

        });//请求结束
}

//index页 , 个人趋势图
function LoadPersonTrend(req) {
            $.post("/echarts/api/person",req ,function (data) {
            var x = data["x_series"];
            var y = data["y_series"];
        //此处开始图表展示
        var myChart = echarts.init(document.getElementById('main'));
        option = {
            color: ['#ff3d3d'],
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                x: 'left',
                padding: [10, 20, 0, 20],
                data: ['拜访次数'],
                selected: {
                    'VATS': true
                }
            },
            grid: {
                left: '0',
                right: '5%',
                bottom: '10%',
                top: '13%',
                containLabel: true
            },

            xAxis: {
                axisLabel :{
                    interval:0, //显示所有的x轴的数据
                    rotate: -45,
                    margin: 5
                } ,
                type: 'category',
                boundaryGap: false,
                splitLine: { //网格线
                    show: true,
                    lineStyle: {
                        color: ['#b1b1b1'],
                        type: 'dashed'
                    }
                },
                data:  x
            },
            yAxis: {
                splitLine: { //网格线
                    show: true,
                    lineStyle: {
                        color: ['#b1b1b1'],
                        type: 'dashed'
                    }
                }
            },
            series: [{
                name: 'VATS',
                type: 'line',
                data:  y,
                label: {
                    normal: {
                        show: true,
                        position: 'top' //值显示
                    }
                }
            }]
        };
        myChart.setOption(option)

        });//请求结束
}

//index页, 下拉菜单
//触发趋势图中的下拉菜单的事件
function show(){
            var objS = document.getElementById("mySelect");
            var grade = objS.options[objS.selectedIndex].value;
            //eval(grade);
        }

//index页, 查询按钮
function LoadGranph() {
            var form = $("#analyze").serialize();
            console.log(form);
            var objS = document.getElementById("mySelect");
            var load = objS.options[objS.selectedIndex].value;  //下拉菜单
            //var exec1 = load+"(\""+ query+ "\",\"" + month +"\")" ;
            var exec1 = load+"(\""+ form + "\")" ;
            //console.log(exec1);
            eval(exec1);
            //console.log(eval(exec1))
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
        //e.preventDefault();    //加上这句则导航的<a>标签会失效
        $('ul.nav > li').removeClass('active');
        $(this).addClass('active');
    });
}


//首页汇总表格数据中，点击按钮后显示的个人详细
function LoadPersonOnGpost(req) {
            $.post("/api/person/trend",req ,function (data) {
            var x = data["x_series"];
            var y = data["y_series"];
            var y_0 = data["y_0"];
            var y_1 = data["y_1"];
            var y_2 = data["y_2"];
        //此处开始图表展示
        var myChart = echarts.init(document.getElementById('main'));
        option = {
            color: ['#ff3d3d', '#00a0e9', '#f603ff', '#00b419'],
            tooltip: {
                trigger: 'item',
                position:["50%","50%"]
            },
            legend: {
                x: 'left',
                padding: [10, 20, 0, 20],
                data: ['汇总', '网点', '经销商', '团购'],
                selected: {
                    '汇总': true,
                    '网点': true,
                    '经销商': true,
                    '团购': true
                }
            },
            grid: {
                left: '0',
                right: '3%',
                bottom: '3%',
                top: '13%',
                containLabel: true
            },
            xAxis: {
                axisLabel :{
                            interval:0, //显示所有的x轴的数据
                            rotate: -45,
                            margin: 5
                } ,
                type: 'category',
                boundaryGap: false,
                splitLine: { //网格线
                    show: false,
                    lineStyle: {
                        color: ['#b1b1b1'],
                        type: 'dashed'
                    }
                },
                data: x
            },
            yAxis: {
                splitLine: { //网格线
                    show: false,
                    lineStyle: {
                        color: ['#b1b1b1'],
                        type: 'dashed'
                    }
                }
            },
            series: [{
                name: '汇总',
                type: 'line',
                data: y,
                label: {
                    normal: {
                        show: true,
                        position: 'top' //值显示
                    }
                }
            }, {
                name: '网点',
                type: 'line',
                data:  y_0,
                label: {
                    normal: {
                        show: false,
                        position: 'top'
                    }
                }
            }, {
                name: '经销商',
                type: 'line',
                data:  y_1,
                label: {
                    normal: {
                        show: true,
                        position: 'top'
                    }
                }
            }, {
                name: '团购',
                type: 'line',
                data:  y_2,
                label: {
                    normal: {
                        show: true,
                        position: 'top'
                    }
                }
            }]
        };
        //作图结束
        myChart.setOption(option)
        });//请求结束
}