// @Title  resource.go
// @Description  资源表单
// @Autor: rong	2022/03/03
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
    Name string `json:"name" binding:"max=63,unique=resources"`
    Description string `json:"description"`
    Action interface{} `json:"action"`
}

// ResourceQuery 请求资源分页表单
type ResourceQuery struct {
    Name string `json:"name"`
	PerPage int `form:"per_page" json:"per_page" query:"per_page"`
	Current int `form:"current" json:"current" query:"current"`
}

