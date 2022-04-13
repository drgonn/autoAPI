// @Title  resource.go
// @Description  资源表单
// @Autor: rong	2022/03/04
// @Update:
package forms

// ResourceCreateForm 资源创建表单
type ResourceCreateForm struct {
    Name string `json:"name" binding:"required,max=63,unique=resources"`
    Description string `json:"description"`
    Action interface{} `json:"action"`
}

// ResourceUpdateForm 资源修改表单
type ResourceUpdateForm struct {
    Description string `json:"description"`
    Action interface{} `json:"action"`
}

// ResourceQuery 请求资源分页表单
type ResourceQuery struct {
    Name string `form:"name"`
	PerPage int `form:"per_page"`
	Current int `form:"current"`
}

