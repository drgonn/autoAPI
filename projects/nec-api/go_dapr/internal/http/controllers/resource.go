// @Title  resource.go
// @Description  资源控制器定义以及初始化
// @Author	rong	2022/03/04
// @Update
package controllers

import (
	"net/http"
	"strconv"

	"nec-api/internal/forms"
	"nec-api/internal/repo"
	"nec-api/internal/response"
	
	"github.com/gin-gonic/gin"
	"github.com/google/wire"
)

// ResourceController 资源控制器
type ResourceController struct {
	repo repo.IResourceRepo
}

// IResourceController 资源控制器接口
type IResourceController interface{}

var ResourceControllerProviderSet = wire.NewSet(NewResourceController, wire.Bind(new(IResourceController), new(*ResourceController)))

// @title	NewResourceController
// @description	初始化资源控制器
// @author	rong	2022/03/04
// @param	repo interface 资源接口类
// @return  *ResourceController interface 资源类
func NewResourceController(repo repo.IResourceRepo) *ResourceController {
	return &ResourceController{
		repo: repo,
	}
}

// @title	Create
// @description	创建资源
// @author	rong	2022/03/04
// @param	form forms.ResourceCreateForm 创建资源表单参数
// @return  无
func (ctl *ResourceController) Create(c *gin.Context) {
	// 验证并绑定post提交的json数据到forms.ResourceCreateForm结构体实例form当中，验证错误则返回参数信息错误
	var form forms.ResourceCreateForm
	err := c.ShouldBindJSON(&form)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponseMessage(response.ParamBindError, err.Error()))
		return
	}

    //将post提交的数据绑定的结构体传递到repo当中，对数据库进行新增操作
	err = ctl.repo.Create(form)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponseMessage(response.CreateError, err.Error()))
		return
	}

    //接口返回创建成功json信息
	c.JSON(http.StatusOK, response.ResponseSuccess())
}

// @title	Update
// @description	修改资源
// @author	rong	2022/03/04
// @param	form forms.ResourceUpdateForm 修改资源表单参数
//          id int 要修改的资源ID
// @return  无
func (ctl *ResourceController) Update(c *gin.Context) {
	var err error

    // 获取url当中的参数，参数为空或类型不对返回非法请求错误
	idStr := c.Param("id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponse(response.InvalidRequest))
		return
	}

    // 验证并绑定put提交的json数据到forms.ResourceUpdateForm结构体实例form当中，验证错误则返回参数信息错误
	var form forms.ResourceUpdateForm
	err = c.ShouldBindJSON(&form)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponseMessage(response.ParamBindError, err.Error()))
		return
	}

    // 将put提交的数据绑定的结构体传递到repo当中，对数据库进行修改操作
	err = ctl.repo.Update(id, form)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponseMessage(response.UpdateError, err.Error()))
		return
	}

    // 接口返回修改成功json信息
	c.JSON(http.StatusOK, response.ResponseSuccess())
}

// @title	Get
// @description	获取某个资源
// @author	rong	2022/03/04
// @param	id int 要修改的资源ID
// @return  无
func (ctl *ResourceController) Get(c *gin.Context) {
	var err error

    // 获取url当中的参数，参数为空或类型不对返回非法请求错误
	idStr := c.Param("id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponse(response.InvalidRequest))
		return
    }


    // 将url当中获取的id传给repo，作为唯一标识去数据库查找一条数据，并返回资源的详情结构体
	resource, err := ctl.repo.Get(id)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponseMessage(response.GetError, err.Error()))
		return
	}

    // 接口返回成功json信息和资源详情
	c.JSON(http.StatusOK, response.NewResponseData(response.Success, resource))
}

// @title	List
// @description	获取资源列表
// @author	rong	2022/03/04
// @param	query forms.Resource 分页请求参数表单
// @return  无
func (ctl *ResourceController) List(c *gin.Context) {
	// 验证并绑定url当中的查询参数到forms.ResourceQuery结构体实例query当中，验证错误则返回参数信息错误
	var query forms.ResourceQuery
	err := c.ShouldBindQuery(&query)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponseMessage(response.ParamBindError, err.Error()))
		return
	}

    // 每页数据条数未提交默认为20条
	if query.PerPage < 1 {
		query.PerPage = 20
	}

    // 当前页未提交默认为第一页
	if query.Current < 1 {
		query.Current = 1
	}

    // 将分页查询数据提交到repo中到数据库找到对应的数据列表和总数据条数
	total, resources, err := ctl.repo.List(query)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponseMessage(response.GetError, err.Error()))
		return
	}

    // 将取得的分页数据数组，数据总条数，当页数据条数，请求分页数据插入到标准json输出结构体中
	size := len(resources)
	res := response.NewResponseData(response.Success, resources)
	res.Total = &total
	res.Current = query.Current
	res.PerPage = query.PerPage
	res.Size = &size

    //接口返回成功信息和资源分页列表
	c.JSON(http.StatusOK, res)
}
// @title	Delete
// @description	批量删除资源
// @author	rong	2022/03/04
// @param	form forms.DeleteIds 要删除的资源ID列表表单
// @return  无
func (ctl *ResourceController) Delete(c *gin.Context) {
	// 验证并绑定提交的json数据到DeleteIds结构体实例当中，为一个名为ids的需要删除的Id列表，验证错误则返回参数信息错误
	var form forms.DeleteIds
	err := c.ShouldBindJSON(&form)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponseMessage(response.ParamBindError, err.Error()))
		return
	}

    //将要删除的id切片传给repo去进行批量删除
	err = ctl.repo.Delete(form.Ids)
	if err != nil {
		c.JSON(http.StatusOK, response.NewResponseMessage(response.DeleteError, err.Error()))
		return
	}

    //接口返回删除成功信息
	c.JSON(http.StatusOK, response.ResponseSuccess())
}
