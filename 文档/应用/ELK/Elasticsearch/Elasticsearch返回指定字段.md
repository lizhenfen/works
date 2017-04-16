两个都可以只返回指定的字段， 
    共同点:  都可以返回指定的字段，过滤不需要的字段
    不同点:
         1. fields只可以用于叶节点，_sources没有限制
         2. fields可以节省带宽，cpu和IO, _sources只节省带宽
  
//fields
{
  //其它查询条件
  ……
  "fields": [
    "goods_sale_number",
    "id"
  ]
}

//_source
{
  //其它查询条件
  ……
  "_source": [
    "goods_sale_number",
    "id"
  ]
}


去重:  可以通过aggregations操作


bootstrap-table实例:  http://www.cnblogs.com/landeanfen/p/4976838.html