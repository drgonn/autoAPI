// @Title  user.go
// @Description  用户表单
// @Autor: rong	2022/03/03
// @Update:
package forms

// UserCreateForm 用户创建表单
type UserCreateForm struct {
    Uid string `json:"uid" binding:"max=63"`
    Permission interface{} `json:"permission"`
}

// UserUpdateForm 用户修改表单
type UserUpdateForm struct {
    Uid string `json:"uid" binding:"max=63"`
    Permission interface{} `json:"permission"`
}

// UserQuery 请求用户分页表单
type UserQuery struct {
    Uid string `json:"uid"`
	PerPage int `form:"per_page" json:"per_page" query:"per_page"`
	Current int `form:"current" json:"current" query:"current"`
}

