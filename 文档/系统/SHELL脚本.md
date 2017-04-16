set -o noclobber  #当重定向到文件时, 若文件存在, 报错
set -x xx.sh      #debug的方式执行shell脚本

expr常用方法:
    expr length "$STR"  #计算出STR的字符串的长度
    expr substr "$STR" start length  #截取子字符串
    expr index "$STR" search_str     #search_str的索引位置
    expr 1 + 2       #数学计算, +号两边必须有空格
    
column: 表格输出结果
    -t: 自动对齐
    
readonly VAR   #设置只读变量

read -p "提示信息" VAR  #保存用户输入到VAR变量, 若无VAR,默认为REPLY

#数组
1. 通过一个索引一个值, 索引必须为数字,从0开始
    arr[0]='test'
2. 一次赋值多个, 索引按照输入顺序
    arr=(test1 test2 test3)
3. 一次赋值多个, 同时指定索引
    arr=([1]=test [3]=test3 [2]=test2)
4. 从指定索引开始赋值
    arr=([3]=test1 test2 test3)
    
${arr[*]} 和 ${arr[@]}的区别和相同:
相同:
    不使用"时， 表达的意思都是一样的
不同；
    "${arr[*]}": 表示一个整体
    "${arr[@]}": 表示每一个个体
    
$#: 传递的位置参数的个数
shift: 移除已经处理的参数; 无参数, 表示从前开始一个一个删除, 可以指定n ， 表示一下删除n个