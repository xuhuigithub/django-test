重点
---

> 如何是用django的restframework 制作REST API

> REST API之所以有REST是要重复使用的Application Programming Interface

> REST API 最基本的验证，将验证参数添加到混淆类中，让VIewSet继承混淆类，以达到添加验证的目的


## 如何取得后端数据

> 构建后端数据模型（models），  
> 先Serialize(序列化,serializers)，  
> 再ViewSet(展示,views) 

## 过滤器

> search field like this http://127.0.0.1:10800/api/tasks/?search=11011 find and return task where order=11011

> 你还可以这样搜索http://127.0.0.1:10800/api/tasks/?order=11011

> 你还可已自定义过滤器