package v1
type Role struct{}
func NewRole() Role{return Role{}}

func (p Role) Create(c *gin.Context) {
param := service.CreateRoleRequest{}
response := app.NewResponse(c)
valid, errs := app.BindAndValid(c, &param)
if !valid {
    global.Logger.Errorf("app.BindAndValid errs: %v", errs)
    errRsp := errcode.InvalidParams.WithDetails(errs.Errors()...)
    response.ToErrorResponse(errRsp)
    return
}
    svc := service.New(c.Request.Context())
role_id, err := svc.CreateRole(&param)
if err != nil {
global.Logger.Errorf("svc.CreateRole err: %v", err)
if role_id == 0 {
	response.ToErrorResponse(errcode.ErrorCreateRoleNameExisted)
} else {
	response.ToErrorResponse(errcode.ErrorCreateRoleFail)
}
return
}
param.Id = role_id
response.ToResponse(param)
return
}
func (t Role) Get(c *gin.Context) {
	param := service.GetRoleRequest{Id: convert.StrTo(c.Param("id")).MustUInt32()}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}
	svc := service.New(c.Request.Context())
	role, err := svc.GetRole(&param)
	if err != nil {
		global.Logger.Errorf("svc.GetRole err: %v", err)
		response.ToErrorResponse(errcode.ErrorGetRoleFail)
		return
	}
	response.ToResponse(role)
	return
}

func (t Role) List(c *gin.Context) {
	param := service.RoleListRequest{}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		errRsp := errcode.InvalidParams.WithDetails(errs.Errors()...)
		response.ToErrorResponse(errRsp)
		return
	}

	svc := service.New(c)
	pager := app.Pager{
		Page:     app.GetPage(c),
		PageSize: app.GetPageSize(c),
	}
	totalRows, err := svc.CountRole(&service.CountRoleRequest{
        Name: param.Name,
	})
	if err != nil {
		global.Logger.Errorf("svc.CountRole err: %v", err)
		response.ToErrorResponse(errcode.ErrorCountRoleFail)
	}
	roles, err := svc.GetRoleList(&param, &pager)
	if err != nil {
		global.Logger.Errorf("svc.GetRoleList err: %v", err)
		response.ToErrorResponse(errcode.ErrorGetRoleListFail)
		return
	}
	response.ToResponseList(roles, totalRows)
	return
}

func (t Role) Update(c *gin.Context) {
	param := service.UpdateRoleRequest{Id: convert.StrTo(c.Param("id")).MustUInt32()}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}

	svc := service.New(c.Request.Context())
	n, err := svc.UpdateRole(&param)
	if err != nil || n < 1 {
		global.Logger.Errorf("svc.UpdateRole err: %v", err)
		response.ToErrorResponse(errcode.ErrorUpdateRoleFail)
		return
	}

	response.ToResponse(gin.H{})
	return
}

func (t Role) Delete(c *gin.Context) {
	param := service.DeleteRoleRequest{Id: convert.StrTo(c.Param("id")).MustUInt32()}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}

	svc := service.New(c.Request.Context())
	n, err := svc.DeleteRole(&param)
	if err != nil || n < 1{
		global.Logger.Errorf("svc.DeleteRole err: %v", err)
		response.ToErrorResponse(errcode.ErrorDeleteRoleFail)
		return
	}

	response.ToResponse(gin.H{})
	return
}
