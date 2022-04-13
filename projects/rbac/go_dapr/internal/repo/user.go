// @Title  user.go
// @Description  用户初始化
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

type UserRepo struct {
	db database.IDaprMysqlClient
}

type IUserRepo interface {
	Create(form forms.UserCreateForm) error
	Update(id int, form forms.UserUpdateForm) error
	Delete(id int) error
	Get(ids []uint) (*User, error)
	List(query forms.UserQuery) (int, []User, error)
}

var UserRepoProviderSet = wire.NewSet(NewUserRepo, wire.Bind(new(IUserRepo), new(*UserRepo)))

func NewUserRepo(db database.IDaprMysqlClient) *UserRepo {
	return &UserRepo{
		db: db,
	}
}

// User 用户结构
type User struct {
    Id uint `json:"id"`
    Uid string `json:"uid"`
    Permission interface{} `json:"permission"`
    UpdatedAt *time.Time `json:"updated_at"`
    CreatedAt *time.Time `json:"created_at"`
}

// @title: Create
// @description: 插入用户表一条数据
// @author: rong 2022/03/03
// @param: from froms.UserCreateForm 用户创建表单
// @return err error 错误或者无错误就是成功
func (r *UserRepo) Create(form forms.UserCreateForm) error {
    data, err := json.Marshal(form.Permission)
    if err != nil {
    	return err
    }
    var permission string = string(data)
    if permission == "null" {
    	permission = "{}"
    }

	sqlStr := fmt.Sprintf("INSERT INTO `users` ( `uid`, `permission`) VALUES ('%s' ,'%s' )", form.Uid ,permission )
	logger.Debug("sql string: ", sqlStr)

	if _, err := r.db.Exec(sqlStr); err != nil {
		logger.Error(err)
		return err
	}
	return nil
}
// @title: UpdateUser
// @description: 插入用户表一条数据
// @author: rong 2022/03/03
// @param: from froms.UserUpdateForm 用户更新表单
// @return err error 错误或者无错误就是成功
func (r *UserRepo) Update(id int, form forms.UserUpdateForm) error {
	var build strings.Builder

	build.WriteString("UPDATE `users` SET ")

	var sqlvals []string
    if 0 < len(form.Uid) {
        sqlvals = append(sqlvals, fmt.Sprintf(" `uid` = '%s' ", form.Uid))
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
// @description: 获取用户表一条数据
// @author: rong 2022/03/03
// @param: id int 要查询的用户Id
// @return *User 用户详情结构体
//         err error 错误或者无错误就是成功
func (r *UserRepo) Get(id int) (*User, error) {
	var resp []User
	sqlStr := fmt.Sprintf("SELECT * FROM `users` WHERE id = %d", id)

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
// @description: 获取用户列表
// @author: rong 2022/02/14 11:48
// @param: id int 用户ID
// @return int 列表数据总条数
//          []User 用户详细信息切片
//          err error 错误或者无错误就是成功
func (r *UserRepo) List(query forms.UserQuery) (int, []User, error) {
	var resp []User
	where := ""
	countSql := fmt.Sprintf("SELECT count(id) AS count FROM users%s", where)
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
	sqlstr := fmt.Sprintf("SELECT * FROM `users` %s LIMIT %d, %d", where, offset, query.PerPage)
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

// @title: DeleteUser
// @description: 批量删除用户
// @param: id int 用户ID切片
// @return err error 错误或者无错误就是成功
func (r *UserRepo) Delete(ids []uint) error {
	idsStrList := ArrayUint2Str(ids)
	idsStr := strings.Join(idsStrList, ",")
	sqlstr := fmt.Sprintf("DELETE FROM `users` WHERE `id` IN (%s)", idsStr)

	_, err := r.db.Exec(sqlstr)
	if err != nil {
		return err
	}
	return nil
}

