
#### 3、 captime 定时任务表

| 序号 | 名称 | 描述 | 类型 | 键 | 为空 | 额外 | 默认值 |
| :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
| 1 | `id` | 主键ID | int(10) unsigned | PRI | NO | auto_increment |  |
| 2 | `describe` | 描述 | varchar(255) |  | YES |  | NULL |
| 1 | `serial` | 摄像头序列号，就是摄像头生产出来的号码，使用外键关联摄像头 | varchar(255) |  | NO |  |  |
| 2 | `cap_at` | 定时拍照时间，例如字符串"12:34" ,即在12点34分进行抓拍，字符串"16"表示没隔16分钟抓拍 | varchar(255) |  | NO |  | NULL |
| 7 | `type` | 任务类型，1=固定时间抓拍，2=按时间间隔抓拍。改类型不用提交修改，自动根据cap_at参数是否有冒号判断类型 | int(11) |  | NO |  | 0 |
| 4 | `created_at` | 创建时间 | datetime |  | YES |  | current_timestamp() |
| 5 | `updated_at` | 更新时间 | datetime |  | YES | on update current_timestamp() | NULL |

#### 4、 capimg 抓拍图片表

| 序号 | 名称 | 描述 | 类型 | 键 | 为空 | 额外 | 默认值 |
| :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
| 1 | `id` | 主键ID | int(10) unsigned | PRI | NO | auto_increment |  |
| 2 | `url` | 图片地址 | varchar(255) |  | YES |  | NULL |
| 1 | `serial` | 摄像头序列号，就是摄像头生产出来的号码，使用外键关联摄像头 | varchar(255) |  | NO |  |  |
| 4 | `created_at` | 创建时间 | datetime |  | YES |  | current_timestamp() |
| 5 | `updated_at` | 更新时间 | datetime |  | YES | on update current_timestamp() | NULL |
