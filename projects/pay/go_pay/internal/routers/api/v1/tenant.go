package v1
type Tenant struct{}
func NewTenant() Tenant{return Tenant{}}

func (p Tenant) Create(c *gin.Context) {
param := service.CreateTenantRequest{}
response := app.NewResponse(c)
valid, errs := app.BindAndValid(c, &param)
if !valid {
    global.Logger.Errorf("app.BindAndValid errs: %v", errs)
    errRsp := errcode.InvalidParams.WithDetails(errs.Errors()...)
    response.ToErrorResponse(errRsp)
    return
}
    svc := service.New(c.Request.Context())
tenant_id, err := svc.CreateTenant(&param)
if err != nil {
global.Logger.Errorf("svc.CreateTenant err: %v", err)
if tenant_id == 0 {
	response.ToErrorResponse(errcode.ErrorCreateTenantNameExisted)
} else {
	response.ToErrorResponse(errcode.ErrorCreateTenantFail)
}
return
}
param.Id = tenant_id
response.ToResponse(param)
return
}
func (t Tenant) Get(c *gin.Context) {
	param := service.GetTenantRequest{Ouid: c.Param("ouid")}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}
	svc := service.New(c.Request.Context())
	tenant, err := svc.GetTenant(&param)
	if err != nil {
		global.Logger.Errorf("svc.GetTenant err: %v", err)
		response.ToErrorResponse(errcode.ErrorGetTenantFail)
		return
	}
	response.ToResponse(tenant)
	return
}

func (t Tenant) List(c *gin.Context) {
	param := service.TenantListRequest{}
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
	totalRows, err := svc.CountTenant(&service.CountTenantRequest{
        Name: param.Name,
        Ouid: param.Ouid,
        Describe: param.Describe,
	})
	if err != nil {
		global.Logger.Errorf("svc.CountTenant err: %v", err)
		response.ToErrorResponse(errcode.ErrorCountTenantFail)
	}
	tenants, err := svc.GetTenantList(&param, &pager)
	if err != nil {
		global.Logger.Errorf("svc.GetTenantList err: %v", err)
		response.ToErrorResponse(errcode.ErrorGetTenantListFail)
		return
	}
	response.ToResponseList(tenants, totalRows)
	return
}

func (t Tenant) Update(c *gin.Context) {
	param := service.UpdateTenantRequest{Ouid: c.Param("ouid")}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}

	svc := service.New(c.Request.Context())
	n, err := svc.UpdateTenant(&param)
	if err != nil || n < 1 {
		global.Logger.Errorf("svc.UpdateTenant err: %v", err)
		response.ToErrorResponse(errcode.ErrorUpdateTenantFail)
		return
	}

	response.ToResponse(gin.H{})
	return
}

func (t Tenant) Delete(c *gin.Context) {
	param := service.DeleteTenantRequest{Ouid: c.Param("ouid")}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}

	svc := service.New(c.Request.Context())
	n, err := svc.DeleteTenant(&param)
	if err != nil || n < 1{
		global.Logger.Errorf("svc.DeleteTenant err: %v", err)
		response.ToErrorResponse(errcode.ErrorDeleteTenantFail)
		return
	}

	response.ToResponse(gin.H{})
	return
}
