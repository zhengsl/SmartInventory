# 1. 基本信息管理类接口
## 1.1. 省份信息查询
|||
| ---- | ---- |
| URL | http://{address}/smartinventory/decision/base/province |
| Method | GET |
| 参数 | name=xx, yy, … // 省份名称的数组，可以是简称也可以是全称，或者<br/>name=all // 查询所有省份数据 |
| 返回值 | [{}, {}, …] // 省份的名称和id列表，包含简称和全称，顺序和输入参数的顺序一致 |
| 异常情况 | 如果没有符合条件的结果返回空列表 |  
| 性能需求 | 从接收到请求到返回数据不超过100毫秒 |
## 1.2. 查询指定省份下的城市数据
|||
| ---- | ---- |
| URL | http://{address}/smartinventory/decision/base/province_city |
| Method | GET |
| 参数 | name=xx // 省份的名称，可以是简称也可以是全称，或者<br/>id=123456 // 省份的ID |
| 返回值 | [{}, {}, …] // 城市的名称和id列表 |
| 异常情况 | 如果没有符合条件的结果返回空列表 |  
| 性能需求 | 从接收到请求到返回数据不超过100毫秒 |
## 1.3. 查询指定城市的数据
|||
| ---- | ---- |
| URL | http://{address}/smartinventory/decision/base/city |
| Method | GET |
| 参数 | name=xx, yy, … // 城市名称的数组，或者<br/>name=all // 查询所有城市的数据 |
| 返回值 | [{}, {}, …] // 城市的名称和id列表 |
| 异常情况 | 如果没有符合条件的结果返回空列表 | 
| 性能需求 | 从接收到请求到返回数据不超过100毫秒 |
## 1.4. 查询两个城市间顺丰快递的价格标准和时效
|||
| ---- | ---- |
| URL | http://{address}/smartinventory/decision/base/express/sf |
| Method | GET |
| 参数 | from=xx // 发货城市的名称或ID & <br/>to=yy // 收货城市的名称或ID |
| 返回值 | {<br/>&nbsp;&nbsp;"basePrice": int // 标重价格<br/>&nbsp;&nbsp;"addedPrice": int // 单位续重价格<br/>&nbsp;&nbsp;"timeIndex": 1/2/3 // 时效性指数<br/>} |
| 异常情况 || 
| 性能需求 | 从接收到请求到返回数据不超过100毫秒 |
## 1.5. 查询基础数据集信息
|||
| ---- | ---- |
| URL | http://{address}/smartinventory/decision/base/metadata |
| Method | GET |
| 参数 | id=[] // 基础数据集的id数据，或者<br/>id=all // 查询所有基础数据集信息 |
| 返回值 | [{}, {}, {}, …] // 基础数据集元数据信息 |
| 异常情况 || 
| 性能需求 | 从接收到请求到返回数据不超过100毫秒 |
# 2. 统计类接口
## 2.1. 指定省在指定日期下的销量
|||
| ---- | ---- |
| URL | http://{address}/smartinventory/decision/stats/sales/province |
| Method | POST |
| 参数 | {<br/>&nbsp;&nbsp;"provinces": [], // 省份的名称列表，可以是简称，也可以是全称<br/>&nbsp;&nbsp;"years": [], // 年份列表，数字类型<br/>&nbsp;&nbsp;"months": [], // 月份列表，数字类型<br/>&nbsp;&nbsp;"days": [], // 日期列表，可以是完整的"年-月-日"，也可以是日期数字<br/>&nbsp;&nbsp;"filter": {} // 对数据的附加约束作为过滤条件<br/>} |
| 返回值 | {<br/>&nbsp;&nbsp;"provinces": [{}, {}, …], // 省份的名称和id列表，包含简称和全称<br/>&nbsp;&nbsp;"yearMonthDay": [], // 年月日列表，字符串类型<br/>&nbsp;&nbsp;"sales": [[], [], …] // 销售量，二维数组，第一级索引是省份，第二级索引是年/月份<br/>} |
| 异常情况 |
| 性能需求 | 从接收到请求到返回数据不超过100毫秒 |
## 2.2. 指定城市在指定日期下的销量
|||
| ---- | ---- |
| URL | http://{address}/smartinventory/decision/stats/sales/city
| Method | POST |
| 参数 | {<br/>&nbsp;&nbsp;"cities": [], // 城市的名称列表，可以是简称，也可以是全称<br/>&nbsp;&nbsp;"years": [], // 年份列表，数字类型<br/>&nbsp;&nbsp;"months": [], // 月份列表，数字类型<br/>&nbsp;&nbsp;"days": [], // 日期列表，可以是完整的"年-月-日"，也可以是日期数字<br/>&nbsp;&nbsp;"filter": {} // 对数据的附加约束作为过滤条件<br/>} |
| 返回值 | {<br/>&nbsp;&nbsp;"cities": [{}, {}, …], // 城市的名称和id列表<br/>&nbsp;&nbsp;"yearMonthDay": [], // 年月日列表，字符串类型<br/>&nbsp;&nbsp;"sales": [[], [], …] // 销售量，二维数组，第一级索引是省份，第二级索引是年/月份<br/>} |
| 异常情况 ||  
| 性能需求 | 从接收到请求到返回数据不超过100毫秒 |
## 2.3. 指定省在指定日期下的接收包裹的数量
|||
| ---- | ---- |
| URL | http://{address}/smartinventory/decision/stats/packages/province |
| Method | POST |
| 参数 | {<br/>&nbsp;&nbsp;"provinces": [], // 省份的名称列表，可以是简称，也可以是全称<br/>&nbsp;&nbsp;"years": [], // 年份列表，数字类型<br/>&nbsp;&nbsp;"months": [], // 月份列表，数字类型<br/>&nbsp;&nbsp;"days": [], // 日期列表，可以是完整的"年-月-日"，也可以是日期数字<br/>&nbsp;&nbsp;"filter": {} // 对数据的附加约束作为过滤条件<br/>} |
| 返回值 | {<br/>&nbsp;&nbsp;"provinces": [{}, {}, …], // 省份的名称和id列表，包含简称和全称<br/>&nbsp;&nbsp;"yearMonthDay": [], // 年月日列表，字符串类型<br/>&nbsp;&nbsp;"packages": [[], [], …] // 包裹数量，二维数组，第一级索引是省份，第二级索引是年/月份<br/>} |
| 异常情况  ||
| 性能需求 | 从接收请求到返回数据不超过100毫秒 |
## 2.4. 指定城市在指定日期下的接收包裹的数量
|||
| ---- | ---- |
| URL | http://{address}/smartinventory/decision/stats/packages/city |
| Method | POST |
| 参数 | {<br/>&nbsp;&nbsp;"cities": [], // 城市的名称列表，可以是简称，也可以是全称<br/>&nbsp;&nbsp;"years": [], // 年份列表，数字类型<br/>&nbsp;&nbsp;"months": [], // 月份列表，数字类型<br/>&nbsp;&nbsp;"days": [], // 日期列表，可以是完整的"年-月-日"，也可以是日期数字<br/>&nbsp;&nbsp;"filter": {} // 对数据的附加约束作为过滤条件<br/>}
| 返回值 | {<br/>&nbsp;&nbsp;"cities": [{}, {}, …], // 城市的名称和id列表<br/>&nbsp;&nbsp;"yearMonthDay": [], // 年月日列表，字符串类型<br/>&nbsp;&nbsp;"packages": [[], [], …] // 包裹数量，二维数组，第一级索引是省份，第二级索引是年/月份<br/>} |
| 异常情况 ||
| 性能需求 | 从接收请求到返回数据不超过100毫秒
## 2.5. 指定省在指定日期下的快递成本
|||
| ---- | ---- |
| URL | http://{address}/smartinventory/decision/stats/express/province |
| Method | POST |
| 参数 | {<br/>&nbsp;&nbsp;"provinces": [], // 省份的名称列表，可以是简称，也可以是全称<br/>&nbsp;&nbsp;"years": [], // 年份列表，数字类型<br/>&nbsp;&nbsp;"months": [], // 月份列表，数字类型<br/>&nbsp;&nbsp;"days": [] // 日期列表，可以是完整的"年-月-日"，也可以是日期数字<br/>} |
| 返回值 | {<br/>&nbsp;&nbsp;"provinces": [{}, {}, …], // 省份的名称和id列表，包含简称和全称<br/>&nbsp;&nbsp;"yearMonthDay": [], // 年月日列表，字符串类型<br/>&nbsp;&nbsp;"expressFee": [[], [], …] // 快递费用成本，二维数组，第一级索引是省份，第二级索引是年/月份<br/>} |
| 异常情况 ||
| 性能需求 | 从接收请求到返回数据不超过100毫秒 |
## 2.6. 指定城市在指定日期下的快递成本
|||
| ---- | ---- |
| URL | http://{address}/smartinventory/decision/stats/express/city |
| Method | POST |
| 参数 | {<br/>&nbsp;&nbsp;"cities": [], // 城市的名称列表，可以是简称，也可以是全称<br/>&nbsp;&nbsp;"years": [], // 年份列表，数字类型<br/>&nbsp;&nbsp;"months": [], // 月份列表，数字类型<br/>&nbsp;&nbsp;"days": [] // 日期列表，可以是完整的"年-月-日"，也可以是日期数字<br/>} |
| 返回值 | {<br/>&nbsp;&nbsp;"cities": [{}, {}, …], // 城市的名称和id列表<br/>&nbsp;&nbsp;"yearMonthDay": [], // 年月份列表，字符串类型<br/>&nbsp;&nbsp;"expressFee": [[], [], …] // 快递费用成本，二维数组，第一级索引是省份，第二级索引是年/月份<br/>} |
| 异常情况 ||
|性能需求 | 从接收到请求到返回数据不超过100毫秒 |
# 3. 规划类接口
## 3.1. 在指定仓库位置的前提下的最优物流方案
|||
| ---- | ---- |
| URL | http://{address}/smartinventory/decision/plan/warehouse/static |
| Method | POST |
| 参数 | {<br/>&nbsp;&nbsp;"warehouses": [], // 仓库所在城市的id列表<br/>&nbsp;&nbsp;"cities": [], // 目的城市的id列表<br/>&nbsp;&nbsp;"baseData": "" // 用于规划的基础数据集id<br/>} |
| 返回值 | {<br/>&nbsp;&nbsp;"solution": {"xxx": {"cities": [], "cost": 123, "time": 2}, "yyy": {"cities": [], "cost": 123, "time": 2}, …} // 不同仓库所覆盖的城市，快递成本预估，以及时效性参数<br/>} |
| 异常情况 ||
| 性能需求 | 从接收到请求到返回数据不超过1000毫秒 |
## 3.2. 寻找仓库布局方案
|||
| ---- | ---- |
| URL |http://{{address}}/smartinventory/decision/plan/warehouse/dynamic |
| Method |POST |
| 参数 | {<br/>&nbsp;&nbsp;"warehouses": [], // 仓库所在城市的id列表<br/>&nbsp;&nbsp;"cities": [], // 目的城市的id列表<br/>&nbsp;&nbsp;"baseData": "", // 用于规划的基础数据集id<br/>&nbsp;&nbsp;"warehouseCount": 10 // 目标仓库数量<br/>} |
| 返回值 | {<br/>&nbsp;&nbsp;"solution": {<br/>&nbsp;&nbsp;"xxx": {"cities": [], "cost": 123, "time": 2}, "yyy": {"cities": [], "cost": 123, "time": 2}, …<br/>&nbsp;&nbsp;} // 不同仓库所覆盖的城市，快递成本预估，以及时效性参数<br/>} |
| 异常情况 ||  
| 性能需求 | 从接收到请求到返回数据不超过10秒 |
# 4. 预测类接口
## 4.1. 指定省销量预测
|||
| ---- | ---- |
| URL | http://{{address}}/smartinventory/decision/forecast/sales/province |
| Method | POST |
| 参数 | {<br/>&nbsp;&nbsp;"provinces": [], // 省份的id列表<br/>&nbsp;&nbsp;"start": "yyyy-mm-dd", // 开始预测日期<br/>&nbsp;&nbsp;"mode": "" // 预测模式<br/>&nbsp;&nbsp;"algorithm": "" // 预测算法<br/>} | 
| 返回值 | {<br/>&nbsp;&nbsp;"provinces": [{}, {}, …], // 省份的名称和id列表，包含简称和全称<br/>&nbsp;&nbsp;"yearMonthDay": [], // 年月日列表，字符串类型<br/>&nbsp;&nbsp;"sales": [[], [], …] // 销售量，二维数组，第一级索引是省份，第二级索引是年/月份<br/>} |
| 异常情况 ||
| 性能需求 | 从接收到请求到返回数据不超过1000毫秒 |
## 4.2. 指定城市销量预测
|||
| ---- | ---- |
| URL | http://{{address}}/smartinventory/decision/forecast/sales/city |
| Method | POST |
| 参数 | {<br/>&nbsp;&nbsp;"cities": [], // 城市的id列表<br/>&nbsp;&nbsp;"start": "yyyy-mm-dd", // 开始预测日期<br/>&nbsp;&nbsp;"mode": "" // 预测模式<br/>&nbsp;&nbsp;"algorithm": "" // 预测算法<br/>} |
| 返回值 | {<br/>&nbsp;&nbsp;"cities": [{}, {}, …], // 城市的名称和id列表<br/>&nbsp;&nbsp;"yearMonthDay": [], // 年月日列表，字符串类型<br/>&nbsp;&nbsp;"sales": [[], [], …] // 销售量，二维数组，第一级索引是省份，第二级索引是年/月份<br/>} |
| 异常情况 ||
| 性能需求 | 从接收到请求到返回数据不超过1000毫秒 |