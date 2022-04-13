// @Title  role.go
// @Description  角色初始化
// @Autor: rong	2022/03/03
// @Update:
package repo

import (
	"encoding/json"
	"errors"
	"fmt"
	"nauth/internal/database"
	"nauth/internal/forms"
	"time"

	"dev.azure.com/netkit/unknown/gokit.git/logger"
	"github.com/google/wire"
)

type RoleRepo struct {
	db database.IDaprMysqlClient
}

type IRoleRepo interface {
	Create(form forms.RoleCreateForm) error
	Update(id int, form forms.RoleUpdateForm) error
	Delete(id int) error
	Get(ids []uint) (*Role, error)
	List(query forms.UserQuery) (int, []Role, error)
}

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
// @author: rong 2022/03/03
// @param: from froms.RoleCreateForm 角色创建表单
// @return err error 错误或者无错误就是成功
func (r *RoleRepo) Create(form forms.RoleCreateForm) error {
    data, err := json.Marshal(form.Permission)
    if err != nil {
    	return err
    }
    var permission string = string(data)
    if permission == "null" {
    	permission = "{}"
    }

	sqlStr := fmt.Sprintf("INSERT INTO `roles` ( `name`, `description`, `permission`) VALUES ('%s' ,'%s' ,'%s' )", form.Name ,form.Description ,permission )
	logger.Debug("sql string: ", sqlStr)

	if _, err := r.db.Exec(sqlStr); err != nil {
		logger.Error(err)
		return err
	}
	return nil
}
// @title: UpdateRole
// @description: 插入角色表一条数据
// @author: rong 2022/03/03
// @param: from froms.RoleUpdateForm 角色更新表单
// @return err error 错误或者无错误就是成功
func (r *RoleRepo) Update(id int, form forms.RoleUpdateForm) error {
	var build strings.Builder

	build.WriteString("UPDATE `roles` SET ")

	var sqlvals []string
    if 0 < len(form.Name) {
        sqlvals = append(sqlvals, fmt.Sprintf(" `name` = '%s' ", form.Name))
    }
    if 0 < len(form.Description) {
        sqlvals = append(sqlvals, fmt.Sprintf(" `description` = '%s' ", form.Description))
    }
    if 0 < len(form.Permission) {
        sqlvals = append(sqlvals, fmt.Sprintf(" `permission` = '%v' ", form.Permission))
    }

    if len(sqlvals) == 0 {
    	return errors.New(ErrorNoUpdateArgs)
	}
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
// @author: rong 2022/03/03
// @param: id int 要查询的角色Id
// @return *Role 角色详情结构体
//         err error 错误或者无错误就是成功
func (r *RoleRepo) Get(id int) (*Role, error) {
	var resp []Role
	sqlStr := fmt.Sprintf("SELECT * FROM `roles` WHERE id = %d", id)

    out, err := r.db.Query(sqlStr)
    if err != nil {
    	return nil, err
	}
    err = json.Unmarshal(out.Data, &resp)
    if err != nil {
    	return nil, err
	}
    if len(resp) < 1 {
    	return nil, errors.New(ErrorNotFound)
	}
    return &resp[0], nil
}

// @title: List
// @description: 获取角色列表
// @author: rong 2022/02/14 11:48
// @param: id int 角色ID
// @return int 列表数据总条数
//          []Role 角色详细信息切片
//          err error 错误或者无错误就是成功
func (r *RoleRepo) List(query forms.UserQuery) (int, []Role, error) {
	var resp []Role
	where := ""
    if len(query.Name) > 0 {
        where = fmt.Sprintf(" WHERE NAME LIKE '%%%s%%'", query.Name)
    }

	countSql := fmt.Sprintf("SELECT count(id) AS count FROM roles%s", where)
	out, err := r.db.Query(countSql)
	if err != nil {
		logger.Error(err)
		return 0, nil, err
	}
	count := UnmarshalCount(out.Data)
	if count <= 0 {
		return 0, resp, nil
	}

	offset := (query.Current - 1) * query.PerPage
	sqlstr := fmt.Sprintf("SELECT * FROM `roles` %s LIMIT %d, %d", where, offset, query.PerPage)
	out, err = r.db.Query(sqlstr)

	if err != nil {
		return 0, nil, err
	}
	err = json.Unmarshal(out.Data, &resp)
	if err != nil {
		return 0, nil, err
	}

	return count, resp, nil
}

// @title: DeleteRole
// @description: 批量删除角色
// @param: id int 角色ID切片
// @return err error 错误或者无错误就是成功
func (r *RoleRepo) Delete(ids []uint) error {
	idsStrList := ArrayUint2Str(ids)
	idsStr := strings.Join(idsStrList, ",")
	sqlstr := fmt.Sprintf("DELETE FROM `roles` WHERE `id` IN (%s)", idsStr)

	_, err := r.db.Exec(sqlstr)
	if err != nil {
		return err
	}
	return nil
}

