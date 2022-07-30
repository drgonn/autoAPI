# 摄像头模块功能设计说明书
# 修订记录
# 三、HTTP接口说明
## 3.1 创建应用接口

接口地址：/api/hikv/app

YAPI测试地址：

请求方式：POST

**请求参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| name | 名称 | String | 是 |  |
| describe | 描述 | String | 是 |  |

**返回参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| status | 状态 | Boolean | 是 |  |
| code | 状态码 | Integer | 是 |  |
| message | 错误信息 | String | 否 |  |
| data | 详细信息 | Object | 是 |  |
| id | 主键ID | Uint | 是 |  |
| name | 名称 | String | 是 |  |
| aid | 唯一索引id | String | 是 |  |
| describe | 描述 | String | 是 |  |
| updated_at | 更新时间 | Datetime | 是 |  |
| created_at | 创建时间 | Datetime | 是 |  |

## 3.2 修改应用接口

接口地址：/api/hikv/app/{aid}

YAPI测试地址：

请求方式：PUT

**路径参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| aid | 唯一索引id | String | 是 |  |

**请求参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| name | 名称 | String | 否 |  |
| describe | 描述 | String | 否 |  |

**返回参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| status | 状态 | Boolean | 是 |  |
| code | 状态码 | Integer | 是 |  |
| message | 错误信息 | String | 否 |  |

## 3.3 获取单个应用接口

接口地址：/api/hikv/app/{aid}

YAPI测试地址：

请求方式：GET

**路径参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| aid | 唯一索引id | String | 是 |  |

**返回参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| status | 状态 | Boolean | 是 |  |
| code | 状态码 | Integer | 是 |  |
| message | 错误信息 | String | 否 |  |
| data | 详细信息 | Object | 是 |  |
| id | 主键ID | Uint | 是 |  |
| name | 名称 | String | 是 |  |
| aid | 唯一索引id | String | 是 |  |
| describe | 描述 | String | 是 |  |
| updated_at | 更新时间 | Datetime | 是 |  |
| created_at | 创建时间 | Datetime | 是 |  |

## 3.4 删除应用接口

接口地址：/api/hikv/app/{aid}

YAPI测试地址：

请求方式：DELETE

**路径参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| aid | 唯一索引id | String | 是 |  |

**返回参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| status | 状态 | Boolean | 是 |  |
| code | 状态码 | Integer | 是 |  |
| message | 错误信息 | String | 否 |  |

## 3.5 分页获取应用接口

接口地址：/api/hikv/apps

YAPI测试地址：

请求方式：GET

**请求参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| per_page | 分页条数 | Integer | 否 |  |
| current | 当前页数 | Integer | 否 |  |
| name | 名称 | String | 否 |  |
| aid | 唯一索引id | String | 否 |  |

**返回参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| per_page | 分页条数 | Integer | 是 |  |
| current | 当前页数 | Integer | 是 |  |
| size | 当前页数据条数 | Integer | 是 |  |
| total | 数据总数 | Integer | 是 |  |
| list | 分页信息 | List | 是 |  |
| id | 主键ID | Uint | 是 |  |
| name | 名称 | String | 是 |  |
| aid | 唯一索引id | String | 是 |  |
| describe | 描述 | String | 是 |  |
| updated_at | 更新时间 | Datetime | 是 |  |
| created_at | 创建时间 | Datetime | 是 |  |

## 3.6 创建摄像头接口

接口地址：/api/hikv/hikv

YAPI测试地址：

请求方式：POST

**请求参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| name | 名称 | String | 是 |  |
| describe | 描述 | String | 否 |  |
| serial | 摄像头序列号，就是摄像头生产出来的号码 | String | 是 |  |
| app_key | 摄像头所属账号的appKey | String | 是 |  |
| app_secret | 摄像头所属账号的appSecret | String | 是 |  |
| validate_code | 摄像头绑定验证码 | String | 是 |  |

**返回参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| status | 状态 | Boolean | 是 |  |
| code | 状态码 | Integer | 是 |  |
| message | 错误信息 | String | 否 |  |
| data | 详细信息 | Object | 是 |  |
| id | 主键ID | Integer | 是 |  |
| name | 名称 | String | 是 |  |
| describe | 描述 | String | 是 |  |
| serial | 摄像头序列号，就是摄像头生产出来的号码 | String | 是 |  |
| app_key | 摄像头所属账号的appKey | String | 是 |  |
| app_secret | 摄像头所属账号的appSecret | String | 是 |  |
| validate_code | 摄像头绑定验证码 | String | 是 |  |
| updated_at | 更新时间 | Datetime | 是 |  |
| created_at | 创建时间 | Datetime | 是 |  |

## 3.7 修改摄像头接口

接口地址：/api/hikv/hikv/{serial}

YAPI测试地址：

请求方式：PUT

**路径参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| serial | 摄像头序列号，就是摄像头生产出来的号码 | String | 是 |  |

**请求参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| name | 名称 | String | 否 |  |
| describe | 描述 | String | 否 |  |

**返回参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| status | 状态 | Boolean | 是 |  |
| code | 状态码 | Integer | 是 |  |
| message | 错误信息 | String | 否 |  |

## 3.8 获取单个摄像头接口

接口地址：/api/hikv/hikv/{serial}

YAPI测试地址：

请求方式：GET

**路径参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| serial | 摄像头序列号，就是摄像头生产出来的号码 | String | 是 |  |

**返回参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| status | 状态 | Boolean | 是 |  |
| code | 状态码 | Integer | 是 |  |
| message | 错误信息 | String | 否 |  |
| data | 详细信息 | Object | 是 |  |
| id | 主键ID | Integer | 是 |  |
| name | 名称 | String | 是 |  |
| describe | 描述 | String | 是 |  |
| serial | 摄像头序列号，就是摄像头生产出来的号码 | String | 是 |  |
| app_key | 摄像头所属账号的appKey | String | 是 |  |
| app_secret | 摄像头所属账号的appSecret | String | 是 |  |
| validate_code | 摄像头绑定验证码 | String | 是 |  |
| updated_at | 更新时间 | Datetime | 是 |  |
| created_at | 创建时间 | Datetime | 是 |  |

## 3.9 删除摄像头接口

接口地址：/api/hikv/hikv/{serial}

YAPI测试地址：

请求方式：DELETE

**路径参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| serial | 摄像头序列号，就是摄像头生产出来的号码 | String | 是 |  |

**返回参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| status | 状态 | Boolean | 是 |  |
| code | 状态码 | Integer | 是 |  |
| message | 错误信息 | String | 否 |  |

## 3.10 分页获取摄像头接口

接口地址：/api/hikv/hikvs

YAPI测试地址：

请求方式：GET

**请求参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| per_page | 分页条数 | Integer | 否 |  |
| current | 当前页数 | Integer | 否 |  |

**返回参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| per_page | 分页条数 | Integer | 是 |  |
| current | 当前页数 | Integer | 是 |  |
| size | 当前页数据条数 | Integer | 是 |  |
| total | 数据总数 | Integer | 是 |  |
| list | 分页信息 | List | 是 |  |
| id | 主键ID | Integer | 是 |  |
| name | 名称 | String | 是 |  |
| describe | 描述 | String | 是 |  |
| serial | 摄像头序列号，就是摄像头生产出来的号码 | String | 是 |  |
| app_key | 摄像头所属账号的appKey | String | 是 |  |
| app_secret | 摄像头所属账号的appSecret | String | 是 |  |
| validate_code | 摄像头绑定验证码 | String | 是 |  |
| updated_at | 更新时间 | Datetime | 是 |  |
| created_at | 创建时间 | Datetime | 是 |  |

## 3.11 创建定时任务表接口

接口地址：/api/hikv/captime

YAPI测试地址：

请求方式：POST

**请求参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| describe | 描述 | String | 否 |  |
| serial | 摄像头序列号 | String | 是 |  |
| cap_at | 定时拍照时间 | String | 是 |  |

**返回参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| status | 状态 | Boolean | 是 |  |
| code | 状态码 | Integer | 是 |  |
| message | 错误信息 | String | 否 |  |
| data | 详细信息 | Object | 是 |  |
| id | 主键ID | Integer | 是 |  |
| describe | 描述 | String | 是 |  |
| serial | 摄像头序列号 | String | 是 |  |
| cap_at | 定时拍照时间 | String | 是 |  |
| type | 任务类型 | Integer | 是 | 1=固定时间抓拍，2=按时间间隔抓拍。改类型不用提交修改，自动根据cap_at参数是否有冒号判断类型 |
| created_at | 创建时间 | Datetime | 是 |  |
| updated_at | 更新时间 | Datetime | 是 |  |

## 3.12 修改定时任务表接口

接口地址：/api/hikv/captime/{id}

YAPI测试地址：

请求方式：PUT

**路径参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| id | 主键ID | Integer | 是 |  |

**请求参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| describe | 描述 | String | 否 |  |
| serial | 摄像头序列号 | String | 否 |  |
| cap_at | 定时拍照时间 | String | 否 |  |

**返回参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| status | 状态 | Boolean | 是 |  |
| code | 状态码 | Integer | 是 |  |
| message | 错误信息 | String | 否 |  |

## 3.13 获取单个定时任务表接口

接口地址：/api/hikv/captime/{id}

YAPI测试地址：

请求方式：GET

**路径参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| id | 主键ID | Integer | 是 |  |

**返回参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| status | 状态 | Boolean | 是 |  |
| code | 状态码 | Integer | 是 |  |
| message | 错误信息 | String | 否 |  |
| data | 详细信息 | Object | 是 |  |
| id | 主键ID | Integer | 是 |  |
| describe | 描述 | String | 是 |  |
| serial | 摄像头序列号 | String | 是 |  |
| cap_at | 定时拍照时间 | String | 是 |  |
| type | 任务类型 | Integer | 是 | 1=固定时间抓拍，2=按时间间隔抓拍。改类型不用提交修改，自动根据cap_at参数是否有冒号判断类型 |
| created_at | 创建时间 | Datetime | 是 |  |
| updated_at | 更新时间 | Datetime | 是 |  |

## 3.14 删除定时任务表接口

接口地址：/api/hikv/captime/{id}

YAPI测试地址：

请求方式：DELETE

**路径参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| id | 主键ID | Integer | 是 |  |

**返回参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| status | 状态 | Boolean | 是 |  |
| code | 状态码 | Integer | 是 |  |
| message | 错误信息 | String | 否 |  |

## 3.15 分页获取定时任务表接口

接口地址：/api/hikv/captimes

YAPI测试地址：

请求方式：GET

**请求参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| per_page | 分页条数 | Integer | 否 |  |
| current | 当前页数 | Integer | 否 |  |
| serial | 摄像头序列号 | String | 否 |  |
| type | 任务类型 | Integer | 否 | 1=固定时间抓拍，2=按时间间隔抓拍。改类型不用提交修改，自动根据cap_at参数是否有冒号判断类型 |

**返回参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| per_page | 分页条数 | Integer | 是 |  |
| current | 当前页数 | Integer | 是 |  |
| size | 当前页数据条数 | Integer | 是 |  |
| total | 数据总数 | Integer | 是 |  |
| list | 分页信息 | List | 是 |  |
| id | 主键ID | Integer | 是 |  |
| describe | 描述 | String | 是 |  |
| serial | 摄像头序列号 | String | 是 |  |
| cap_at | 定时拍照时间 | String | 是 |  |
| type | 任务类型 | Integer | 是 | 1=固定时间抓拍，2=按时间间隔抓拍。改类型不用提交修改，自动根据cap_at参数是否有冒号判断类型 |
| created_at | 创建时间 | Datetime | 是 |  |
| updated_at | 更新时间 | Datetime | 是 |  |

## 3.16 删除抓拍图片表接口

接口地址：/api/hikv/capimg/{id}

YAPI测试地址：

请求方式：DELETE

**路径参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| id | 主键ID | Integer | 是 |  |

**返回参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| status | 状态 | Boolean | 是 |  |
| code | 状态码 | Integer | 是 |  |
| message | 错误信息 | String | 否 |  |

## 3.17 分页获取抓拍图片表接口

接口地址：/api/hikv/capimgs

YAPI测试地址：

请求方式：GET

**请求参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| per_page | 分页条数 | Integer | 否 |  |
| current | 当前页数 | Integer | 否 |  |

**返回参数说明**

| 参数 | 含义 | 类型 | 必须 | 说明 |
|----|----|----|----|--------|
| per_page | 分页条数 | Integer | 是 |  |
| current | 当前页数 | Integer | 是 |  |
| size | 当前页数据条数 | Integer | 是 |  |
| total | 数据总数 | Integer | 是 |  |
| list | 分页信息 | List | 是 |  |
| id | 主键ID | Integer | 是 |  |
| url | 图片地址 | String | 是 |  |
| serial | 摄像头序列号 | String | 是 |  |
| created_at | 创建时间 | Datetime | 是 |  |
| updated_at | 更新时间 | Datetime | 是 |  |

# 四、影响分析

# 五、计划

# 六、质量目标

# 七、测试建议

# 八、其他信息

# 九、参考资料

