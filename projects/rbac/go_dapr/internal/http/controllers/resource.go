// @Title  resource.go
// @Description  资源控制器定义以及初始化
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

//ResourceController 资源控制器
type ResourceController struct {
	repo repo.IResourceRepo
}

// 资源控制器接口
type IResourceController interface{}

var ResourceControllerProviderSet = wire.NewSet(NewResourceController, wire.Bind(new(IResourceController), new(*ResourceController)))

// @title	NewResourceController
// @description	初始化资源控制器
// @author	rong	2022/03/03
// @param	repo interface 资源接口类
// @return  *ResourceController interface 资源类
func NewResourceController(repo repo.IResourceRepo) *ResourceController {
	return &ResourceController{
		repo: repo,
	}
}

// @title	Create
// @description	创建资源
// @author	rong	2022/03/03
// @param	form forms.ResourceCreateForm 创建资源表单参数
// @return  json 创建成功信息
func (ctl *ResourceController) Create(c *gin.Context) {
	var form forms.ResourceCreateForm
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
// @description	修改资源
// @author	rong	2022/03/03
// @param	form forms.ResourceUpdateForm 修改资源表单参数
//          id int 要修改的资源ID
// @return  json 修改成功信息
func (ctl *ResourceController) Update(c *gin.Context) {
	idStr := c.Param("id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponse(response.InvalidRequest))
		return

	var form forms.ResourceUpdateForm
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
// @description	获取某个资源
// @author	rong	2022/03/03
// @param	id int 要修改的资源ID
// @return  json 成功信息和资源详情
func (ctl *ResourceController) Get(c *gin.Context) {
	idStr := c.Param("id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponse(response.InvalidRequest))
		return
}

	resource, err := ctl.repo.Get(id)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponseMessage(response.GetError, err.Error()))
		return
	}

	c.JSON(http.StatusOK, response.NewResponseData(response.Success, resource))
}

// @title	List
// @description	获取资源列表
// @author	rong	2022/03/03
// @param	query forms.Resource 分页请求参数表单
// @return  json 成功信息和资源分页列表
func (ctl *ResourceController) List(c *gin.Context) {
	var query forms.ResourceQuery
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
 
	total, resources, err := ctl.repo.List(query)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponseMessage(response.GetError, err.Error()))
		return
	}

	size := len(resources)

	res := response.NewResponseData(response.Success, resources)
	res.Total = &total
	res.Current = query.Current
	res.PerPage = query.PerPage
	res.Size = &size
	c.JSON(http.StatusOK, res)
}
// @title	Delete
// @description	删除资源
// @author	rong	2022/03/03
// @param	form forms.DeleteIds 要删除的资源ID列表表单
// @return  json 删除成功信息
func (ctl *ResourceController) Delete(c *gin.Context) {
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
