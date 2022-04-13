// @Title  role.go
// @Description  角色初始化
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

// RoleRepo 角色Repo
type RoleRepo struct {
	db database.IDaprMysqlClient
}

// IRoleRepo 角色Repo公开接口
type IRoleRepo interface {
	Create(form forms.RoleCreateForm) error
	Update(id int, form forms.RoleUpdateForm) error
	Get(id int) (*Role, error)
	List(query forms.RoleQuery) (int, []Role, error)
	Delete(ids []uint) error
}

// RoleRepoProviderSet 角色IRepo公开接口与Repo绑定关系
var RoleRepoProviderSet = wire.NewSet(NewRoleRepo, wire.Bind(new(IRoleRepo), new(*RoleRepo)))

func NewRoleRepo(db database.IDaprMysqlClient) *RoleRepo {
	return &RoleRepo{
		db: db,
	}
}

// Role 角色结构
type Role struct {
	Id uint `json:"id"`
	Name string `json:"name"`
	Description string `json:"description"`
	Permission interface{} `json:"permission"`
	Updatedat *time.Time `json:"updatedat"`
	Createdat *time.Time `json:"createdat"`
}

// @title: Create
// @description: 插入角色表一条数据
// @author: rong 2022/03/04
// @param: from froms.RoleCreateForm 角色创建表单
// @return err error 错误或者无错误就是成功
func (r *RoleRepo) Create(form forms.RoleCreateForm) error {
    // form.Permission为json数据，先将它进行序列化转为string再插入sql语句中
	data, err := json.Marshal(form.Permission)
	if err != nil {
		return err
	}

    // 判断提交的permission是否为空，为空时默认为{}
	var permission string = string(data)
	if permission == "null" {
		permission = "{}"
	}

    // 将form内数据插入Role表中 
	sqlStr := fmt.Sprintf("INSERT INTO `roles` ( `name`, `description`, `permission`) VALUES ('%s' ,'%s' ,'%s' )", form.Name, form.Description, permission)
	logger.Debug("sql string: ", sqlStr)
	if _, err := r.db.Exec(sqlStr); err != nil {
		logger.Error(err)
		return err
	}
	return nil
}

// @title: Update
// @description: 修改角色表一条数据
// @author: rong 2022/03/04
// @param: id int 角色ID
//         from froms.RoleUpdateForm 角色修改表单
// @return err error 错误或者无错误就是成功
func (r *RoleRepo) Update(id int, form forms.RoleUpdateForm) error {
    // 声明build用来组合sql sting
	var build strings.Builder
	build.WriteString("UPDATE `roles` SET ")

    // 声明sqlvals用来添加要更新的key = value
	var sqlvals []string

    // form.Permission为json数据，先将它进行序列化转为string再插入sql语句中
	data, err := json.Marshal(form.Permission)
	if err != nil {
		return err
	}

    // 判断提交的permission是否为空，为空时默认为{}
	var permission string = string(data)
	if permission == "null" {
		permission = "{}"
	}

    // 如果name字段不为空，拼入sql语句中进行更新
	if 0 < len(form.Name) {
        sqlvals = append(sqlvals, fmt.Sprintf(" `name` = '%s' ", form.Name))
	}

    // 如果description字段不为空，拼入sql语句中进行更新
	if 0 < len(form.Description) {
        sqlvals = append(sqlvals, fmt.Sprintf(" `description` = '%s' ", form.Description))
	}

    // 将转为string的json字段permission拼入sql语句中进行更新
	sqlvals = append(sqlvals, fmt.Sprintf(" `permission` = '%s' ", permission))

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
// @description: 获取角色表一条数据
// @author: rong 2022/03/04
// @param: id int 要查询的角色Id
// @return *Role 角色详情结构体
//         err error 错误或者无错误就是成功
func (r *RoleRepo) Get(id int) (*Role, error) {
    // 声明resp用来存查询获得的数据
	var resp []Role

    // 使用角色Id查询数据
	sqlStr := fmt.Sprintf("SELECT * FROM `roles` WHERE id = %d", id)
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

    // 将格式为json的字段permission解析后更新Role的Permission字段
	var permission map[string]interface{}
	err = json.Unmarshal([]byte(resp[0].Permission.(string)), &permission)
	if err != nil {
		return nil, err
	}
	resp[0].Permission = permission

    return &resp[0], nil
}

// @title: List
// @description: 获取角色列表
// @author: rong 2022/03/04
// @param: query forms.RoleQuery 请求角色分页表单
// @return int 列表数据总条数
//          []Role 角色详细信息切片
//          err error 错误或者无错误就是成功
func (r *RoleRepo) List(query forms.RoleQuery) (count int, roles []Role, err error) {
    // 声明resp用来存查询获得的数据
	var resp []Role
	where := ""

    // 如果有提交name，对其进行模糊查找
	if len(query.Name) > 0 {
	    where = fmt.Sprintf(" WHERE NAME LIKE '%%%s%%'", query.Name)
	}

    // 查询总数据条数并解析出值count
	countSql := fmt.Sprintf("SELECT count(id) AS count FROM roles%s", where)
	out, err := r.db.Query(countSql)
	if err != nil {
		logger.Error(err)
		return 0, nil, err
	}
	count, err = UnmarshalCount(out.Data)
	if count <= 0 {
		return 0, roles, nil
	}

    // 判断要获取的数据起始序号，如果它大于总数据条数，说明没有符合的数据分段，直接返回空切片
	offset := (query.Current - 1) * query.PerPage
	if offset >= count {
	    return count, roles, nil
	}

    // 查询分页数据并解析到Role切片当中
	sqlstr := fmt.Sprintf("SELECT * FROM `roles` %s LIMIT %d, %d", where, offset, query.PerPage)
	out, err = r.db.Query(sqlstr)
	if err != nil {
		return 0, nil, err
	}
	err = json.Unmarshal(out.Data, &resp)
	if err != nil {
		return 0, nil, err
	}

    // 循环Role切片resp，将json字段解析为json数据更新到新的Role切片roles当中，并返回该新切片
	for _, role := range resp {
		var permission map[string]interface{}
		if err := json.Unmarshal([]byte(role.Permission.(string)), &permission); err != nil {
			logger.Error(err)
		} else {
			role.Permission = permission
		}
		roles = append(roles, role)
	}

	return count, roles, nil
}

// @title: Delete
// @description: 批量删除角色
// @author: rong 2022/03/04
// @param: ids []uint 角色ID切片
// @return err error 错误或者无错误就是成功
func (r *RoleRepo) Delete(ids []uint) error {
    // 将数字切片ids []uint转化为[]string,里面的数字都变为string类型
	idsStrList := ArrayUint2Str(ids)

    // 用逗号合并id切片为一条字符串偏于sql中执行
	idsStr := strings.Join(idsStrList, ",")

    // sql执行删除操作,删掉包含在id列表里面的行
	sqlstr := fmt.Sprintf("DELETE FROM `roles` WHERE `id` IN (%s)", idsStr)
	_, err := r.db.Exec(sqlstr)
	if err != nil {
		return err
	}
	return nil
}

