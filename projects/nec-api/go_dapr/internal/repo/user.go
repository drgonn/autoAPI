// @Title  user.go
// @Description  用户初始化
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

// UserRepo 用户Repo
type UserRepo struct {
	db database.IDaprMysqlClient
}

// IUserRepo 用户Repo公开接口
type IUserRepo interface {
	Create(form forms.UserCreateForm) error
	Update(id int, form forms.UserUpdateForm) error
	Get(id int) (*User, error)
	List(query forms.UserQuery) (int, []User, error)
	Delete(ids []uint) error
}

// UserRepoProviderSet 用户IRepo公开接口与Repo绑定关系
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
	Updatedat *time.Time `json:"updatedat"`
	Createdat *time.Time `json:"createdat"`
}

// @title: Create
// @description: 插入用户表一条数据
// @author: rong 2022/03/04
// @param: from froms.UserCreateForm 用户创建表单
// @return err error 错误或者无错误就是成功
func (r *UserRepo) Create(form forms.UserCreateForm) error {
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

    // 将form内数据插入User表中 
	sqlStr := fmt.Sprintf("INSERT INTO `users` ( `uid`, `permission`) VALUES ('%s' ,'%s' )", form.Uid, permission)
	logger.Debug("sql string: ", sqlStr)
	if _, err := r.db.Exec(sqlStr); err != nil {
		logger.Error(err)
		return err
	}
	return nil
}

// @title: Update
// @description: 修改用户表一条数据
// @author: rong 2022/03/04
// @param: id int 用户ID
//         from froms.UserUpdateForm 用户修改表单
// @return err error 错误或者无错误就是成功
func (r *UserRepo) Update(id int, form forms.UserUpdateForm) error {
    // 声明build用来组合sql sting
	var build strings.Builder
	build.WriteString("UPDATE `users` SET ")

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
// @description: 获取用户表一条数据
// @author: rong 2022/03/04
// @param: id int 要查询的用户Id
// @return *User 用户详情结构体
//         err error 错误或者无错误就是成功
func (r *UserRepo) Get(id int) (*User, error) {
    // 声明resp用来存查询获得的数据
	var resp []User

    // 使用用户Uid查询数据
	sqlStr := fmt.Sprintf("SELECT * FROM `users` WHERE id = %d", id)
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

    // 将格式为json的字段permission解析后更新User的Permission字段
	var permission map[string]interface{}
	err = json.Unmarshal([]byte(resp[0].Permission.(string)), &permission)
	if err != nil {
		return nil, err
	}
	resp[0].Permission = permission

    return &resp[0], nil
}

// @title: List
// @description: 获取用户列表
// @author: rong 2022/03/04
// @param: query forms.UserQuery 请求用户分页表单
// @return int 列表数据总条数
//          []User 用户详细信息切片
//          err error 错误或者无错误就是成功
func (r *UserRepo) List(query forms.UserQuery) (count int, users []User, err error) {
    // 声明resp用来存查询获得的数据
	var resp []User
	where := ""

    // 查询总数据条数并解析出值count
	countSql := fmt.Sprintf("SELECT count(id) AS count FROM users%s", where)
	out, err := r.db.Query(countSql)
	if err != nil {
		logger.Error(err)
		return 0, nil, err
	}
	count, err = UnmarshalCount(out.Data)
	if count <= 0 {
		return 0, users, nil
	}

    // 判断要获取的数据起始序号，如果它大于总数据条数，说明没有符合的数据分段，直接返回空切片
	offset := (query.Current - 1) * query.PerPage
	if offset >= count {
	    return count, users, nil
	}

    // 查询分页数据并解析到User切片当中
	sqlstr := fmt.Sprintf("SELECT * FROM `users` %s LIMIT %d, %d", where, offset, query.PerPage)
	out, err = r.db.Query(sqlstr)
	if err != nil {
		return 0, nil, err
	}
	err = json.Unmarshal(out.Data, &resp)
	if err != nil {
		return 0, nil, err
	}

    // 循环User切片resp，将json字段解析为json数据更新到新的User切片users当中，并返回该新切片
	for _, user := range resp {
		var permission map[string]interface{}
		if err := json.Unmarshal([]byte(user.Permission.(string)), &permission); err != nil {
			logger.Error(err)
		} else {
			user.Permission = permission
		}
		users = append(users, user)
	}

	return count, users, nil
}

// @title: Delete
// @description: 批量删除用户
// @author: rong 2022/03/04
// @param: ids []uint 用户ID切片
// @return err error 错误或者无错误就是成功
func (r *UserRepo) Delete(ids []uint) error {
    // 将数字切片ids []uint转化为[]string,里面的数字都变为string类型
	idsStrList := ArrayUint2Str(ids)

    // 用逗号合并id切片为一条字符串偏于sql中执行
	idsStr := strings.Join(idsStrList, ",")

    // sql执行删除操作,删掉包含在id列表里面的行
	sqlstr := fmt.Sprintf("DELETE FROM `users` WHERE `id` IN (%s)", idsStr)
	_, err := r.db.Exec(sqlstr)
	if err != nil {
		return err
	}
	return nil
}

