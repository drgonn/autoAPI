// @Title  user.go
// @Description  用户控制器定义以及初始化
// @Author	rong	2022/03/03
// @Update
package controllers

import (
	"nec-api/internal/forms"
	"nec-api/internal/repo"
	"nec-api/internal/response"
	"net/http"
	"strconv"

	"github.com/google/wire"

	"github.com/gin-gonic/gin"
)

//UserController 用户控制器
type UserController struct {
	repo repo.IUserRepo
}

// 用户控制器接口
type IUserController interface{}

var UserControllerProviderSet = wire.NewSet(NewUserController, wire.Bind(new(IUserController), new(*UserController)))

// @title	NewUserController
// @description	初始化用户控制器
// @author	rong	2022/03/03
// @param	repo interface 用户接口类
// @return  *UserController interface 用户类
func NewUserController(repo repo.IUserRepo) *UserController {
	return &UserController{
		repo: repo,
	}
}

// @title	Create
// @description	创建用户
// @author	rong	2022/03/03
// @param	form forms.UserCreateForm 创建用户表单参数
// @return  json 创建成功信息
func (ctl *UserController) Create(c *gin.Context) {
	var form forms.UserCreateForm
	err := c.ShouldBindJSON(&form)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponseMessage(response.ParamBindError, err.Error()))
		return
	}

	err = ctl.repo.Create(form)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponseMessage(response.CreateError, err.Error()))
		return
	}

	c.JSON(http.StatusOK, response.ResponseSuccess())
}

// @title	Update
// @description	修改用户
// @author	rong	2022/03/03
// @param	form forms.UserUpdateForm 修改用户表单参数
//          id int 要修改的用户ID
// @return  json 修改成功信息
func (ctl *UserController) Update(c *gin.Context) {
	idStr := c.Param("id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponse(response.InvalidRequest))
		return

	var form forms.UserUpdateForm
	err = c.ShouldBindJSON(&form)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponseMessage(response.ParamBindError, err.Error()))
		return
	}

	err = ctl.repo.Update(id, form)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponseMessage(response.UpdateError, err.Error()))
		return
	}

	c.JSON(http.StatusOK, response.ResponseSuccess())
}

// @title	Get
// @description	获取某个用户
// @author	rong	2022/03/03
// @param	id int 要修改的用户ID
// @return  json 成功信息和用户详情
func (ctl *UserController) Get(c *gin.Context) {
	idStr := c.Param("id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponse(response.InvalidRequest))
		return
}

	user, err := ctl.repo.Get(id)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponseMessage(response.GetError, err.Error()))
		return
	}

	c.JSON(http.StatusOK, response.NewResponseData(response.Success, user))
}

// @title	List
// @description	获取用户列表
// @author	rong	2022/03/03
// @param	query forms.User 分页请求参数表单
// @return  json 成功信息和用户分页列表
func (ctl *UserController) List(c *gin.Context) {
	var query forms.UserQuery
	err := c.ShouldBindQuery(&query)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponseMessage(response.ParamBindError, err.Error()))
		return
	}

	if query.PerPage < 1 {
		query.PerPage = 20
	}
 
	if query.Current < 1 {
		query.Current = 1
	}
 
	total, users, err := ctl.repo.List(query)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponseMessage(response.GetError, err.Error()))
		return
	}

	size := len(users)

	res := response.NewResponseData(response.Success, users)
	res.Total = &total
	res.Current = query.Current
	res.PerPage = query.PerPage
	res.Size = &size
	c.JSON(http.StatusOK, res)
}
// @title	Delete
// @description	删除用户
// @author	rong	2022/03/03
// @param	form forms.DeleteIds 要删除的用户ID列表表单
// @return  json 删除成功信息
func (ctl *UserController) Delete(c *gin.Context) {
	var form forms.DeleteIds
	err := c.ShouldBindJSON(&form)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponseMessage(response.CreateError, err.Error()))
		return
	}

	err = c.ShouldBindJSON(&form)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponseMessage(response.ParamBindError, err.Error()))
		return
	}

	err = ctl.repo.Delete(form.Ids)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponseMessage(response.DeleteError, err.Error()))
		return
	}
	c.JSON(http.StatusOK, response.ResponseSuccess())
}
