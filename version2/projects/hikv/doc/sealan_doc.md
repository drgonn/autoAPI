# 摄像头模块功能设计说明书
# 修订记录
# 三、HTTP接口说明
## 3.1 创建应用接口

接口地址：/api/hikv/app

YAPI测试地址：

请求方式：POST

**请求参数说明**

| 参数       | 类型     | 必须 | 含义 | 说明 |
|----|----|----|----|--------|
| name     | String | 是  | 名称 |    |
| describe | String | 是  | 描述 |    |

**返回参数说明**

| 参数         | 类型       | 必须 | 含义     | 说明 |
|----|----|----|----|--------|
| status     | Boolean  | 是  | 状态     |    |
| code       | Integer  | 是  | 状态码    |    |
| message    | String   | 否  | 错误信息   |    |
| data       | Object   | 是  | 详细信息   |    |
| id         | Uint     | 是  | 主键ID   |    |
| name       | String   | 是  | 名称     |    |
| aid        | String   | 是  | 唯一索引id |    |
| describe   | String   | 是  | 描述     |    |
| updated_at | Datetime | 是  | 更新时间   |    |
| created_at | Datetime | 是  | 创建时间   |    |

## 3.2 修改应用接口

接口地址：/api/hikv/app/{aid}

YAPI测试地址：

请求方式：PUT

**路径参数说明**

| 参数  | 类型     | 必须 | 含义     | 说明 |
|----|----|----|----|--------|
| aid | String | 是  | 唯一索引id |    |

**请求参数说明**

| 参数       | 类型     | 必须 | 含义 | 说明 |
|----|----|----|----|--------|
| name     | String | 否  | 名称 |    |
| describe | String | 否  | 描述 |    |

**返回参数说明**

| 参数      | 类型      | 必须 | 含义   | 说明 |
|----|----|----|----|--------|
| status  | Boolean | 是  | 状态   |    |
| code    | Integer | 是  | 状态码  |    |
| message | String  | 否  | 错误信息 |    |

## 3.3 获取单个应用接口

接口地址：/api/hikv/app/{aid}

YAPI测试地址：

请求方式：GET

**路径参数说明**

| 参数  | 类型     | 必须 | 含义     | 说明 |
|----|----|----|----|--------|
| aid | String | 是  | 唯一索引id |    |

**返回参数说明**

| 参数         | 类型       | 必须 | 含义     | 说明 |
|----|----|----|----|--------|
| status     | Boolean  | 是  | 状态     |    |
| code       | Integer  | 是  | 状态码    |    |
| message    | String   | 否  | 错误信息   |    |
| data       | Object   | 是  | 详细信息   |    |
| id         | Uint     | 是  | 主键ID   |    |
| name       | String   | 是  | 名称     |    |
| aid        | String   | 是  | 唯一索引id |    |
| describe   | String   | 是  | 描述     |    |
| updated_at | Datetime | 是  | 更新时间   |    |
| created_at | Datetime | 是  | 创建时间   |    |

## 3.4 删除应用接口

接口地址：/api/hikv/app/{aid}

YAPI测试地址：

请求方式：DELETE

**路径参数说明**

| 参数  | 类型     | 必须 | 含义     | 说明 |
|----|----|----|----|--------|
| aid | String | 是  | 唯一索引id |    |

**返回参数说明**

| 参数      | 类型      | 必须 | 含义   | 说明 |
|----|----|----|----|--------|
| status  | Boolean | 是  | 状态   |    |
| code    | Integer | 是  | 状态码  |    |
| message | String  | 否  | 错误信息 |    |

## 3.5 分页获取应用接口

接口地址：/api/hikv/apps

YAPI测试地址：

请求方式：GET

**请求参数说明**

| 参数       | 类型      | 必须 | 含义     | 说明 |
|----|----|----|----|--------|
| per_page | Integer | 否  | 分页条数   |    |
| current  | Integer | 否  | 当前页数   |    |
| name     | String  | 否  | 名称     |    |
| aid      | String  | 否  | 唯一索引id |    |

**返回参数说明**

| 参数         | 类型       | 必须 | 含义      | 说明 |
|----|----|----|----|--------|
| per_page   | Integer  | 是  | 分页条数    |    |
| current    | Integer  | 是  | 当前页数    |    |
| size       | Integer  | 是  | 当前页数据条数 |    |
| total      | Integer  | 是  | 数据总数    |    |
| list       | List     | 是  | 分页信息    |    |
| id         | Uint     | 是  | 主键ID    |    |
| name       | String   | 是  | 名称      |    |
| aid        | String   | 是  | 唯一索引id  |    |
| describe   | String   | 是  | 描述      |    |
| updated_at | Datetime | 是  | 更新时间    |    |
| created_at | Datetime | 是  | 创建时间    |    |

## 3.6 创建摄像头接口

接口地址：/api/hikv/hikv

YAPI测试地址：

请求方式：POST

**请求参数说明**

| 参数            | 类型     | 必须 | 含义                  | 说明 |
|----|----|----|----|--------|
| name          | String | 是  | 名称                  |    |
| describe      | String | 否  | 描述                  |    |
| serial        | String | 是  | 摄像头序列号，就是摄像头生产出来的号码 |    |
| app_key       | String | 是  | 摄像头所属账号的appKey      |    |
| app_secret    | String | 是  | 摄像头所属账号的appSecret   |    |
| validate_code | String | 是  | 摄像头绑定验证码            |    |

**返回参数说明**

| 参数            | 类型       | 必须 | 含义                  | 说明 |
|----|----|----|----|--------|
| status        | Boolean  | 是  | 状态                  |    |
| code          | Integer  | 是  | 状态码                 |    |
| message       | String   | 否  | 错误信息                |    |
| data          | Object   | 是  | 详细信息                |    |
| id            | Integer  | 是  | 主键ID                |    |
| name          | String   | 是  | 名称                  |    |
| describe      | String   | 是  | 描述                  |    |
| serial        | String   | 是  | 摄像头序列号，就是摄像头生产出来的号码 |    |
| app_key       | String   | 是  | 摄像头所属账号的appKey      |    |
| app_secret    | String   | 是  | 摄像头所属账号的appSecret   |    |
| validate_code | String   | 是  | 摄像头绑定验证码            |    |
| updated_at    | Datetime | 是  | 更新时间                |    |
| created_at    | Datetime | 是  | 创建时间                |    |

## 3.7 修改摄像头接口

接口地址：/api/hikv/hikv/{serial}

YAPI测试地址：

请求方式：PUT

**路径参数说明**

| 参数     | 类型     | 必须 | 含义                  | 说明 |
|----|----|----|----|--------|
| serial | String | 是  | 摄像头序列号，就是摄像头生产出来的号码 |    |

**请求参数说明**

| 参数       | 类型     | 必须 | 含义 | 说明 |
|----|----|----|----|--------|
| name     | String | 否  | 名称 |    |
| describe | String | 否  | 描述 |    |

**返回参数说明**

| 参数      | 类型      | 必须 | 含义   | 说明 |
|----|----|----|----|--------|
| status  | Boolean | 是  | 状态   |    |
| code    | Integer | 是  | 状态码  |    |
| message | String  | 否  | 错误信息 |    |

## 3.8 获取单个摄像头接口

接口地址：/api/hikv/hikv/{serial}

YAPI测试地址：

请求方式：GET

**路径参数说明**

| 参数     | 类型     | 必须 | 含义                  | 说明 |
|----|----|----|----|--------|
| serial | String | 是  | 摄像头序列号，就是摄像头生产出来的号码 |    |

**返回参数说明**

| 参数            | 类型       | 必须 | 含义                  | 说明 |
|----|----|----|----|--------|
| status        | Boolean  | 是  | 状态                  |    |
| code          | Integer  | 是  | 状态码                 |    |
| message       | String   | 否  | 错误信息                |    |
| data          | Object   | 是  | 详细信息                |    |
| id            | Integer  | 是  | 主键ID                |    |
| name          | String   | 是  | 名称                  |    |
| describe      | String   | 是  | 描述                  |    |
| serial        | String   | 是  | 摄像头序列号，就是摄像头生产出来的号码 |    |
| app_key       | String   | 是  | 摄像头所属账号的appKey      |    |
| app_secret    | String   | 是  | 摄像头所属账号的appSecret   |    |
| validate_code | String   | 是  | 摄像头绑定验证码            |    |
| updated_at    | Datetime | 是  | 更新时间                |    |
| created_at    | Datetime | 是  | 创建时间                |    |

## 3.9 删除摄像头接口

接口地址：/api/hikv/hikv/{serial}

YAPI测试地址：

请求方式：DELETE

**路径参数说明**

| 参数     | 类型     | 必须 | 含义                  | 说明 |
|----|----|----|----|--------|
| serial | String | 是  | 摄像头序列号，就是摄像头生产出来的号码 |    |

**返回参数说明**

| 参数      | 类型      | 必须 | 含义   | 说明 |
|----|----|----|----|--------|
| status  | Boolean | 是  | 状态   |    |
| code    | Integer | 是  | 状态码  |    |
| message | String  | 否  | 错误信息 |    |

## 3.10 分页获取摄像头接口

接口地址：/api/hikv/hikvs

YAPI测试地址：

请求方式：GET

**请求参数说明**

| 参数       | 类型      | 必须 | 含义   | 说明 |
|----|----|----|----|--------|
| per_page | Integer | 否  | 分页条数 |    |
| current  | Integer | 否  | 当前页数 |    |

**返回参数说明**

| 参数            | 类型       | 必须 | 含义                  | 说明 |
|----|----|----|----|--------|
| per_page      | Integer  | 是  | 分页条数                |    |
| current       | Integer  | 是  | 当前页数                |    |
| size          | Integer  | 是  | 当前页数据条数             |    |
| total         | Integer  | 是  | 数据总数                |    |
| list          | List     | 是  | 分页信息                |    |
| id            | Integer  | 是  | 主键ID                |    |
| name          | String   | 是  | 名称                  |    |
| describe      | String   | 是  | 描述                  |    |
| serial        | String   | 是  | 摄像头序列号，就是摄像头生产出来的号码 |    |
| app_key       | String   | 是  | 摄像头所属账号的appKey      |    |
| app_secret    | String   | 是  | 摄像头所属账号的appSecret   |    |
| validate_code | String   | 是  | 摄像头绑定验证码            |    |
| updated_at    | Datetime | 是  | 更新时间                |    |
| created_at    | Datetime | 是  | 创建时间                |    |

## 3.11 创建定时任务表接口

接口地址：/api/hikv/captime

YAPI测试地址：

请求方式：POST

**请求参数说明**

| 参数       | 类型     | 必须 | 含义     | 说明 |
|----|----|----|----|--------|
| describe | String | 否  | 描述     |    |
| serial   | String | 是  | 摄像头序列号 |    |
| cap_at   | String | 是  | 定时拍照时间 |    |

**返回参数说明**

| 参数         | 类型       | 必须 | 含义     | 说明                                                 |
|----|----|----|----|--------|
| status     | Boolean  | 是  | 状态     |                                                    |
| code       | Integer  | 是  | 状态码    |                                                    |
| message    | String   | 否  | 错误信息   |                                                    |
| data       | Object   | 是  | 详细信息   |                                                    |
| id         | Integer  | 是  | 主键ID   |                                                    |
| describe   | String   | 是  | 描述     |                                                    |
| serial     | String   | 是  | 摄像头序列号 |                                                    |
| cap_at     | String   | 是  | 定时拍照时间 |                                                    |
| type       | Integer  | 是  | 任务类型   | 1=固定时间抓拍，2=按时间间隔抓拍。改类型不用提交修改，自动根据cap_at参数是否有冒号判断类型 |
| created_at | Datetime | 是  | 创建时间   |                                                    |
| updated_at | Datetime | 是  | 更新时间   |                                                    |

## 3.12 修改定时任务表接口

接口地址：/api/hikv/captime/{id}

YAPI测试地址：

请求方式：PUT

**路径参数说明**

| 参数 | 类型      | 必须 | 含义   | 说明 |
|----|----|----|----|--------|
| id | Integer | 是  | 主键ID |    |

**请求参数说明**

| 参数       | 类型     | 必须 | 含义     | 说明 |
|----|----|----|----|--------|
| describe | String | 否  | 描述     |    |
| serial   | String | 否  | 摄像头序列号 |    |
| cap_at   | String | 否  | 定时拍照时间 |    |

**返回参数说明**

| 参数      | 类型      | 必须 | 含义   | 说明 |
|----|----|----|----|--------|
| status  | Boolean | 是  | 状态   |    |
| code    | Integer | 是  | 状态码  |    |
| message | String  | 否  | 错误信息 |    |

## 3.13 获取单个定时任务表接口

接口地址：/api/hikv/captime/{id}

YAPI测试地址：

请求方式：GET

**路径参数说明**

| 参数 | 类型      | 必须 | 含义   | 说明 |
|----|----|----|----|--------|
| id | Integer | 是  | 主键ID |    |

**返回参数说明**

| 参数         | 类型       | 必须 | 含义     | 说明                                                 |
|----|----|----|----|--------|
| status     | Boolean  | 是  | 状态     |                                                    |
| code       | Integer  | 是  | 状态码    |                                                    |
| message    | String   | 否  | 错误信息   |                                                    |
| data       | Object   | 是  | 详细信息   |                                                    |
| id         | Integer  | 是  | 主键ID   |                                                    |
| describe   | String   | 是  | 描述     |                                                    |
| serial     | String   | 是  | 摄像头序列号 |                                                    |
| cap_at     | String   | 是  | 定时拍照时间 |                                                    |
| type       | Integer  | 是  | 任务类型   | 1=固定时间抓拍，2=按时间间隔抓拍。改类型不用提交修改，自动根据cap_at参数是否有冒号判断类型 |
| created_at | Datetime | 是  | 创建时间   |                                                    |
| updated_at | Datetime | 是  | 更新时间   |                                                    |

## 3.14 删除定时任务表接口

接口地址：/api/hikv/captime/{id}

YAPI测试地址：

请求方式：DELETE

**路径参数说明**

| 参数 | 类型      | 必须 | 含义   | 说明 |
|----|----|----|----|--------|
| id | Integer | 是  | 主键ID |    |

**返回参数说明**

| 参数      | 类型      | 必须 | 含义   | 说明 |
|----|----|----|----|--------|
| status  | Boolean | 是  | 状态   |    |
| code    | Integer | 是  | 状态码  |    |
| message | String  | 否  | 错误信息 |    |

## 3.15 分页获取定时任务表接口

接口地址：/api/hikv/captimes

YAPI测试地址：

请求方式：GET

**请求参数说明**

| 参数       | 类型      | 必须 | 含义     | 说明                                                 |
|----|----|----|----|--------|
| per_page | Integer | 否  | 分页条数   |                                                    |
| current  | Integer | 否  | 当前页数   |                                                    |
| serial   | String  | 否  | 摄像头序列号 |                                                    |
| type     | Integer | 否  | 任务类型   | 1=固定时间抓拍，2=按时间间隔抓拍。改类型不用提交修改，自动根据cap_at参数是否有冒号判断类型 |

**返回参数说明**

| 参数         | 类型       | 必须 | 含义      | 说明                                                 |
|----|----|----|----|--------|
| per_page   | Integer  | 是  | 分页条数    |                                                    |
| current    | Integer  | 是  | 当前页数    |                                                    |
| size       | Integer  | 是  | 当前页数据条数 |                                                    |
| total      | Integer  | 是  | 数据总数    |                                                    |
| list       | List     | 是  | 分页信息    |                                                    |
| id         | Integer  | 是  | 主键ID    |                                                    |
| describe   | String   | 是  | 描述      |                                                    |
| serial     | String   | 是  | 摄像头序列号  |                                                    |
| cap_at     | String   | 是  | 定时拍照时间  |                                                    |
| type       | Integer  | 是  | 任务类型    | 1=固定时间抓拍，2=按时间间隔抓拍。改类型不用提交修改，自动根据cap_at参数是否有冒号判断类型 |
| created_at | Datetime | 是  | 创建时间    |                                                    |
| updated_at | Datetime | 是  | 更新时间    |                                                    |

## 3.16 删除抓拍图片表接口

接口地址：/api/hikv/capimg/{id}

YAPI测试地址：

请求方式：DELETE

**路径参数说明**

| 参数 | 类型      | 必须 | 含义   | 说明 |
|----|----|----|----|--------|
| id | Integer | 是  | 主键ID |    |

**返回参数说明**

| 参数      | 类型      | 必须 | 含义   | 说明 |
|----|----|----|----|--------|
| status  | Boolean | 是  | 状态   |    |
| code    | Integer | 是  | 状态码  |    |
| message | String  | 否  | 错误信息 |    |

## 3.17 分页获取抓拍图片表接口

接口地址：/api/hikv/capimgs

YAPI测试地址：

请求方式：GET

**请求参数说明**

| 参数       | 类型      | 必须 | 含义   | 说明 |
|----|----|----|----|--------|
| per_page | Integer | 否  | 分页条数 |    |
| current  | Integer | 否  | 当前页数 |    |

**返回参数说明**

| 参数         | 类型       | 必须 | 含义      | 说明 |
|----|----|----|----|--------|
| per_page   | Integer  | 是  | 分页条数    |    |
| current    | Integer  | 是  | 当前页数    |    |
| size       | Integer  | 是  | 当前页数据条数 |    |
| total      | Integer  | 是  | 数据总数    |    |
| list       | List     | 是  | 分页信息    |    |
| id         | Integer  | 是  | 主键ID    |    |
| url        | String   | 是  | 图片地址    |    |
| serial     | String   | 是  | 摄像头序列号  |    |
| created_at | Datetime | 是  | 创建时间    |    |
| updated_at | Datetime | 是  | 更新时间    |    |

# 四、影响分析

# 五、计划

# 六、质量目标

# 七、测试建议

# 八、其他信息

# 九、参考资料

