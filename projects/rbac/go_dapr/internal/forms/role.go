// @Title  role.go
// @Description  角色表单
// @Autor: rong	2022/03/03
// @Update:
package forms

// RoleCreateForm 角色创建表单
type RoleCreateForm struct {
    Name string `json:"name" binding:"required,max=63,unique=roles"`
    Description string `json:"description"`
    Permission interface{} `json:"permission"`
}

// RoleUpdateForm 角色修改表单
type RoleUpdateForm struct {
    Name string `json:"name" binding:"max=63,unique=roles"`
    Description string `json:"description"`
    Permission interface{} `json:"permission"`
}

// RoleQuery 请求角色分页表单
type RoleQuery struct {
    Name string `json:"name"`
	PerPage int `form:"per_page" json:"per_page" query:"per_page"`
	Current int `form:"current" json:"current" query:"current"`
}

