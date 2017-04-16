(function(){
    var myAjax = {}  //设置一个空对象
    window.myAjax = myAjax   //对浏览器向外暴漏一个接口
    //=======属性
    myAjax.version = "0.1.1";
    //=======方法==========
    myAjax.get = function () {

    };
    //=========私有方法=====
    myAjax._JSONToURLParamer = function (json) {
        var myArrParts = [];
        for(k in json){
            myArrParts.push(k +"=" + encodeURIComponent(json[k]))
        }
        return myArrParts.join("&");
    };

    myAjax._FormSerialize = function(){
        var formid = document.getElementById("formid");
        var formelments = formid.elements; //获取表单控件
        var arrFormLength = formelments.length;  //获取表单长度
        var jsonParts = {};
        var v ="";
        for(var i=0; i<arrFormLength; i++){
            var field = formelments[i];
            var k = field.name;
            switch (field.type){
                case "button":
                case "subbit":
                case "reset":
                    break;
                case "select-one":
                    var options = field.options;
                    var optionLength = options.length;
                    for(var j=0; j<optionLength; j++){
                        if(options[j].selected){
                            v = options[j].value;
                        }
                    }
                    break;
                case "radio":
                case "checkbox":
                    if(!field.checked){
                        break;
                    }
                case "text":
                     v = field.value;
                     jsonParts[k] = v;
                     break;
            }



        }

    }
})();/**
 * Created by Administrator on 2017/4/3.
 */
