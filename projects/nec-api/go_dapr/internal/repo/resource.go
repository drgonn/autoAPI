// @Title  resource.go
// @Description  资源初始化
// @Autor: rong	2022/03/04
// @Update:
package repo

import (
	"encoding/json"
	"errors"
	"fmt"
	"strings"
	"time"

	"nec-api/internal/database"
	"nec-api/internal/forms"
	
	"dev.azure.com/netkit/unknown/gokit.git/logger"
	"github.com/google/wire"
)

// ResourceRepo 资源Repo
type ResourceRepo struct {
	db database.IDaprMysqlClient
}

// IResourceRepo 资源Repo公开接口
type IResourceRepo interface {
	Create(form forms.ResourceCreateForm) error
	Update(id int, form forms.ResourceUpdateForm) error
	Get(id int) (*Resource, error)
	List(query forms.ResourceQuery) (int, []Resource, error)
	Delete(ids []uint) error
}

// ResourceRepoProviderSet 资源IRepo公开接口与Repo绑定关系
var ResourceRepoProviderSet = wire.NewSet(NewResourceRepo, wire.Bind(new(IResourceRepo), new(*ResourceRepo)))

func NewResourceRepo(db database.IDaprMysqlClient) *ResourceRepo {
	return &ResourceRepo{
		db: db,
	}
}

// Resource 资源结构
type Resource struct {
	Id uint `json:"id"`
	Name string `json:"name"`
	Description string `json:"description"`
	Action interface{} `json:"action"`
	Updatedat *time.Time `json:"updatedat"`
	Createdat *time.Time `json:"createdat"`
}

// @title: Create
// @description: 插入资源表一条数据
// @author: rong 2022/03/04
// @param: from froms.ResourceCreateForm 资源创建表单
// @return err error 错误或者无错误就是成功
func (r *ResourceRepo) Create(form forms.ResourceCreateForm) error {
    // form.Action为json数据，先将它进行序列化转为string再插入sql语句中
	data, err := json.Marshal(form.Action)
	if err != nil {
		return err
	}

    // 判断提交的action是否为空，为空时默认为{}
	var action string = string(data)
	if action == "null" {
		action = "{}"
	}

    // 将form内数据插入Resource表中 
	sqlStr := fmt.Sprintf("INSERT INTO `resources` ( `name`, `description`, `action`) VALUES ('%s' ,'%s' ,'%s' )", form.Name, form.Description, action)
	logger.Debug("sql string: ", sqlStr)
	if _, err := r.db.Exec(sqlStr); err != nil {
		logger.Error(err)
		return err
	}
	return nil
}

// @title: Update
// @description: 修改资源表一条数据
// @author: rong 2022/03/04
// @param: id int 资源ID
//         from froms.ResourceUpdateForm 资源修改表单
// @return err error 错误或者无错误就是成功
func (r *ResourceRepo) Update(id int, form forms.ResourceUpdateForm) error {
    // 声明build用来组合sql sting
	var build strings.Builder
	build.WriteString("UPDATE `resources` SET ")

    // 声明sqlvals用来添加要更新的key = value
	var sqlvals []string

    // form.Action为json数据，先将它进行序列化转为string再插入sql语句中
	data, err := json.Marshal(form.Action)
	if err != nil {
		return err
	}

    // 判断提交的action是否为空，为空时默认为{}
	var action string = string(data)
	if action == "null" {
		action = "{}"
	}

    // 如果description字段不为空，拼入sql语句中进行更新
	if 0 < len(form.Description) {
        sqlvals = append(sqlvals, fmt.Sprintf(" `description` = '%s' ", form.Description))
	}

    // 将转为string的json字段action拼入sql语句中进行更新
	sqlvals = append(sqlvals, fmt.Sprintf(" `action` = '%s' ", action))

    // 判断是否有需要修改的数据，如果没有，返回更新参数错误
    if len(sqlvals) == 0 {
    	return errors.New(ErrorNoUpdateArgs)
	}

    // 将sqlvals用逗号合并，然后build合成sql对数据库进更新
    build.WriteString(strings.Join(sqlvals, ","))
    build.WriteString(fmt.Sprintf(" WHERE `id` =  %d", id))
    logger.Debug("sql string: ", build.String())
	if _, err := r.db.Exec(build.String()); err != nil {
		logger.Error(err)
		return err
	}
	return nil
}

// @title: Get
// @description: 获取资源表一条数据
// @author: rong 2022/03/04
// @param: id int 要查询的资源Id
// @return *Resource 资源详情结构体
//         err error 错误或者无错误就是成功
func (r *ResourceRepo) Get(id int) (*Resource, error) {
    // 声明resp用来存查询获得的数据
	var resp []Resource

    // 使用资源Id查询数据
	sqlStr := fmt.Sprintf("SELECT * FROM `resources` WHERE id = %d", id)
    out, err := r.db.Query(sqlStr)
    if err != nil {
    	return nil, err
	}

    // 解析查询返回的数据
    err = json.Unmarshal(out.Data, &resp)
    if err != nil {
    	return nil, err
	}

    // 如果返回的数据少于1条，说明没有找到，返回没找到错误
    if len(resp) < 1 {
    	return nil, errors.New(ErrorNotFound)
	}

    // 将格式为json的字段action解析后更新Resource的Action字段
	var action map[string]interface{}
	err = json.Unmarshal([]byte(resp[0].Action.(string)), &action)
	if err != nil {
		return nil, err
	}
	resp[0].Action = action

    return &resp[0], nil
}

// @title: List
// @description: 获取资源列表
// @author: rong 2022/03/04
// @param: query forms.ResourceQuery 请求资源分页表单
// @return int 列表数据总条数
//          []Resource 资源详细信息切片
//          err error 错误或者无错误就是成功
func (r *ResourceRepo) List(query forms.ResourceQuery) (count int, resources []Resource, err error) {
    // 声明resp用来存查询获得的数据
	var resp []Resource
	where := ""

    // 如果有提交name，对其进行模糊查找
	if len(query.Name) > 0 {
	    where = fmt.Sprintf(" WHERE NAME LIKE '%%%s%%'", query.Name)
	}

    // 查询总数据条数并解析出值count
	countSql := fmt.Sprintf("SELECT count(id) AS count FROM resources%s", where)
	out, err := r.db.Query(countSql)
	if err != nil {
		logger.Error(err)
		return 0, nil, err
	}
	count, err = UnmarshalCount(out.Data)
	if count <= 0 {
		return 0, resources, nil
	}

    // 判断要获取的数据起始序号，如果它大于总数据条数，说明没有符合的数据分段，直接返回空切片
	offset := (query.Current - 1) * query.PerPage
	if offset >= count {
	    return count, resources, nil
	}

    // 查询分页数据并解析到Resource切片当中
	sqlstr := fmt.Sprintf("SELECT * FROM `resources` %s LIMIT %d, %d", where, offset, query.PerPage)
	out, err = r.db.Query(sqlstr)
	if err != nil {
		return 0, nil, err
	}
	err = json.Unmarshal(out.Data, &resp)
	if err != nil {
		return 0, nil, err
	}

    // 循环Resource切片resp，将json字段解析为json数据更新到新的Resource切片resources当中，并返回该新切片
	for _, resource := range resp {
		var action map[string]interface{}
		if err := json.Unmarshal([]byte(resource.Action.(string)), &action); err != nil {
			logger.Error(err)
		} else {
			resource.Action = action
		}
		resources = append(resources, resource)
	}

	return count, resources, nil
}

// @title: Delete
// @description: 批量删除资源
// @author: rong 2022/03/04
// @param: ids []uint 资源ID切片
// @return err error 错误或者无错误就是成功
func (r *ResourceRepo) Delete(ids []uint) error {
    // 将数字切片ids []uint转化为[]string,里面的数字都变为string类型
	idsStrList := ArrayUint2Str(ids)

    // 用逗号合并id切片为一条字符串偏于sql中执行
	idsStr := strings.Join(idsStrList, ",")

    // sql执行删除操作,删掉包含在id列表里面的行
	sqlstr := fmt.Sprintf("DELETE FROM `resources` WHERE `id` IN (%s)", idsStr)
	_, err := r.db.Exec(sqlstr)
	if err != nil {
		return err
	}
	return nil
}

