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
                right: '14%',
                bottom: '15%',
                containLabel: true
            },
            xAxis : [
                {
                    name: '开始工作',
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
                    name: '人 数',
                    axisTick: {
                        alignWithLabel: true
                    }
                }
            ],
            series : [
                {
                    name:'人数',
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
                right: '10%',
                bottom: '3%',
                containLabel: true
            },
            xAxis : [
                {
                    name: '拜访次数',
                    type : 'category',
                    data : x,
                    axisTick: {
                        alignWithLabel: true
                    }
                }
            ],
            yAxis : [
                {
                    name: '人 数',
                    axisTick: {
                        alignWithLabel: true
                    }
                }
            ],
            series : [
                {
                    name:'人数',
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
                name: '日 期',
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
                name: '拜访次数',
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
                name:  '日 期',
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
                name: "拜访次数",
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
                bottom: '-4%',
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


// 引入到首页

function class_by_tpye() {
    res = [];
    $.post("/apis/index/ccount" ,function (data) {
        var myChart = echarts.init(document.getElementById('main'));
        option = {
            title: {
                text: '分类汇总',
                subtext: '客户类型',
                x: 'center'
            },
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            series: [
                {
                    name: '客户类型',
                    type: 'pie',
                    radius: '30%',
                    center: ['50%', '35%'],
                    data: data,
                    itemStyle: {
                        emphasis: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        };
        myChart.setOption(option)
    });  // post successfully
}  //第一个函数完成


//首页分类2
function indexCountAll() {
    $.post("/apis/index/countall", function (data) {
        data = JSON.parse(data);
        //console.log();
        var myChart = echarts.init(document.getElementById('all'));

var builderJson = {
  "all": data.all,
  "charts": data.company
};

var downloadJson = data.class_customer;

var canvas = document.createElement('canvas');
var ctx = canvas.getContext('2d');
canvas.width = canvas.height = 100;
ctx.textAlign = 'center';
ctx.textBaseline = 'middle';
ctx.globalAlpha = 0.08;
ctx.font = '20px Microsoft Yahei';
ctx.translate(50, 50);
ctx.rotate(-Math.PI / 4);


option = {
    backgroundColor: {
        type: 'pattern',
        image: canvas,
        repeat: 'repeat'
    },
    tooltip: {},
    title: [{
        text: '各公司拜访记录汇总',
        subtext: '总计 ' + builderJson.all,
        x: '30%',
        textAlign: 'center'
    }, {
        text: '客户拜访数据汇总',
        subtext: '总计 ' + Object.keys(downloadJson).reduce(function (all, key) {
            return all + downloadJson[key];
        }, 0),
        x: '75%',
        textAlign: 'center'
    }],
    grid: [{
        top: 50,
        width: '50%',
        bottom: '55%',
        left: 10,
        containLabel: true
    }, {
        top: '55%',
        width: '50%',
        bottom: 0,
        left: 10,
        containLabel: true
    }],
    xAxis: [{
        type: 'value',
        max: builderJson.all / 2,
        splitLine: {
            show: false
        }
    }],
    yAxis: [{
        type: 'category',
        data: Object.keys(builderJson.charts),
        axisLabel: {
            interval: 0,
            rotate: 30
        },
        splitLine: {
            show: true
        }
    }],
    series: [{
        type: 'bar',
        stack: 'chart',
        z: 3,
        label: {
            normal: {
                position: 'right',
                show: true
            }
        },
        data: Object.keys(builderJson.charts).map(function (key) {
            return builderJson.charts[key];
        })
    }, {
        type: 'bar',
        stack: 'chart',
        silent: true,
        itemStyle: {
            normal: {
                color: '#eee'
            }
        },
        data: Object.keys(builderJson.charts).map(function (key) {
            return builderJson.all - builderJson.charts[key];
        })
    }, {
        type: 'pie',
        radius: [0, '30%'],
        center: ['75%', '25%'],
        data: Object.keys(downloadJson).map(function (key) {
            return {
                name: key,
                value: downloadJson[key]
            }
        })
    }]
};
    myChart.setOption(option)
    }); //请求
}