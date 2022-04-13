// @Title  resource.go
// @Description  资源初始化
// @Autor: rong	2022/03/03
// @Update:
package repo

import (
	"encoding/json"
	"errors"
	"fmt"
	"nauth/internal/database"
	"nauth/internal/forms"
	"strings"
	"time"

	"dev.azure.com/netkit/unknown/gokit.git/logger"
	"github.com/google/wire"
)

type ResourceRepo struct {
	db database.IDaprMysqlClient
}

type IResourceRepo interface {
	Create(form forms.ResourceCreateForm) error
	Update(id int, form forms.ResourceUpdateForm) error
	Delete(id int) error
	Get(ids []uint) (*Resource, error)
	List(query forms.UserQuery) (int, []Resource, error)
}

var ResourceRepoProviderSet = wire.NewSet(NewResourceRepo, wire.Bind(new(IResourceRepo), new(*ResourceRepo)))

func NewResourceRepo(db database.IDaprMysqlClient) *ResourceRepo {
	return &ResourceRepo{
		db: db,
	}
}

// Resource 资源结构
type Resource struct {
	Id          uint        `json:"id"`
	Name        string      `json:"name"`
	Description string      `json:"description"`
	Action      interface{} `json:"action"`
	Updatedat   *time.Time  `json:"updatedat"`
	Createdat   *time.Time  `json:"createdat"`
}

// @title: Create
// @description: 插入资源表一条数据
// @author: rong 2022/03/03
// @param: from froms.ResourceCreateForm 资源创建表单
// @return err error 错误或者无错误就是成功
func (r *ResourceRepo) Create(form forms.ResourceCreateForm) error {
	data, err := json.Marshal(form.Action)
	if err != nil {
		return err
	}
	var action string = string(data)
	if action == "null" {
		action = "{}"
	}

	sqlStr := fmt.Sprintf("INSERT INTO `resources` ( `name`, `description`, `action`) VALUES ('%s' ,'%s' ,'%s' )", form.Name, form.Description, action)
	logger.Debug("sql string: ", sqlStr)

	if _, err := r.db.Exec(sqlStr); err != nil {
		logger.Error(err)
		return err
	}
	return nil
}

// @title: UpdateResource
// @description: 插入资源表一条数据
// @author: rong 2022/03/03
// @param: from froms.ResourceUpdateForm 资源更新表单
// @return err error 错误或者无错误就是成功
func (r *ResourceRepo) Update(id int, form forms.ResourceUpdateForm) error {
	var build strings.Builder

	build.WriteString("UPDATE `resources` SET ")

	var sqlvals []string
	if 0 < len(form.Description) {
		sqlvals = append(sqlvals, fmt.Sprintf(" `description` = '%s' ", form.Description))
	}
	if 0 < len(form.Action) {
		sqlvals = append(sqlvals, fmt.Sprintf(" `action` = '%v' ", form.Action))
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
// @description: 获取资源表一条数据
// @author: rong 2022/03/03
// @param: id int 要查询的资源Id
// @return *Resource 资源详情结构体
//         err error 错误或者无错误就是成功
func (r *ResourceRepo) Get(id int) (*Resource, error) {
	var resp []Resource
	sqlStr := fmt.Sprintf("SELECT * FROM `resources` WHERE id = %d", id)

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
// @description: 获取资源列表
// @author: rong 2022/02/14 11:48
// @param: id int 资源ID
// @return int 列表数据总条数
//          []Resource 资源详细信息切片
//          err error 错误或者无错误就是成功
func (r *ResourceRepo) List(query forms.UserQuery) (int, []Resource, error) {
	var resp []Resource
	where := ""
	if len(query.Name) > 0 {
		where = fmt.Sprintf(" WHERE NAME LIKE '%%%s%%'", query.Name)
	}

	countSql := fmt.Sprintf("SELECT count(id) AS count FROM resources%s", where)
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
	sqlstr := fmt.Sprintf("SELECT * FROM `resources` %s LIMIT %d, %d", where, offset, query.PerPage)
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

// @title: DeleteResource
// @description: 批量删除资源
// @param: id int 资源ID切片
// @return err error 错误或者无错误就是成功
func (r *ResourceRepo) Delete(ids []uint) error {
	idsStrList := ArrayUint2Str(ids)
	idsStr := strings.Join(idsStrList, ",")
	sqlstr := fmt.Sprintf("DELETE FROM `resources` WHERE `id` IN (%s)", idsStr)

	_, err := r.db.Exec(sqlstr)
	if err != nil {
		return err
	}
	return nil
}
