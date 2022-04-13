// @Title  role.go
// @Description  角色控制器定义以及初始化
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

//RoleController 角色控制器
type RoleController struct {
	repo repo.IRoleRepo
}

// 角色控制器接口
type IRoleController interface{}

var RoleControllerProviderSet = wire.NewSet(NewRoleController, wire.Bind(new(IRoleController), new(*RoleController)))

// @title	NewRoleController
// @description	初始化角色控制器
// @author	rong	2022/03/03
// @param	repo interface 角色接口类
// @return  *RoleController interface 角色类
func NewRoleController(repo repo.IRoleRepo) *RoleController {
	return &RoleController{
		repo: repo,
	}
}

// @title	Create
// @description	创建角色
// @author	rong	2022/03/03
// @param	form forms.RoleCreateForm 创建角色表单参数
// @return  json 创建成功信息
func (ctl *RoleController) Create(c *gin.Context) {
	var form forms.RoleCreateForm
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
// @description	修改角色
// @author	rong	2022/03/03
// @param	form forms.RoleUpdateForm 修改角色表单参数
//          id int 要修改的角色ID
// @return  json 修改成功信息
func (ctl *RoleController) Update(c *gin.Context) {
	idStr := c.Param("id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponse(response.InvalidRequest))
		return

	var form forms.RoleUpdateForm
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
// @description	获取某个角色
// @author	rong	2022/03/03
// @param	id int 要修改的角色ID
// @return  json 成功信息和角色详情
func (ctl *RoleController) Get(c *gin.Context) {
	idStr := c.Param("id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponse(response.InvalidRequest))
		return
}

	role, err := ctl.repo.Get(id)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponseMessage(response.GetError, err.Error()))
		return
	}

	c.JSON(http.StatusOK, response.NewResponseData(response.Success, role))
}

// @title	List
// @description	获取角色列表
// @author	rong	2022/03/03
// @param	query forms.Role 分页请求参数表单
// @return  json 成功信息和角色分页列表
func (ctl *RoleController) List(c *gin.Context) {
	var query forms.RoleQuery
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
 
	total, roles, err := ctl.repo.List(query)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponseMessage(response.GetError, err.Error()))
		return
	}

	size := len(roles)

	res := response.NewResponseData(response.Success, roles)
	res.Total = &total
	res.Current = query.Current
	res.PerPage = query.PerPage
	res.Size = &size
	c.JSON(http.StatusOK, res)
}
// @title	Delete
// @description	删除角色
// @author	rong	2022/03/03
// @param	form forms.DeleteIds 要删除的角色ID列表表单
// @return  json 删除成功信息
func (ctl *RoleController) Delete(c *gin.Context) {
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
