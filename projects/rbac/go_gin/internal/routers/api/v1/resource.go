package v1
type Resource struct{}
func NewResource() Resource{return Resource{}}

func (p Resource) Create(c *gin.Context) {
param := service.CreateResourceRequest{}
response := app.NewResponse(c)
valid, errs := app.BindAndValid(c, &param)
if !valid {
    global.Logger.Errorf("app.BindAndValid errs: %v", errs)
    errRsp := errcode.InvalidParams.WithDetails(errs.Errors()...)
    response.ToErrorResponse(errRsp)
    return
}
    svc := service.New(c.Request.Context())
resource_id, err := svc.CreateResource(&param)
if err != nil {
global.Logger.Errorf("svc.CreateResource err: %v", err)
if resource_id == 0 {
	response.ToErrorResponse(errcode.ErrorCreateResourceNameExisted)
} else {
	response.ToErrorResponse(errcode.ErrorCreateResourceFail)
}
return
}
param.Id = resource_id
response.ToResponse(param)
return
}
func (t Resource) Get(c *gin.Context) {
	param := service.GetResourceRequest{Id: convert.StrTo(c.Param("id")).MustUInt32()}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}
	svc := service.New(c.Request.Context())
	resource, err := svc.GetResource(&param)
	if err != nil {
		global.Logger.Errorf("svc.GetResource err: %v", err)
		response.ToErrorResponse(errcode.ErrorGetResourceFail)
		return
	}
	response.ToResponse(resource)
	return
}

func (t Resource) List(c *gin.Context) {
	param := service.ResourceListRequest{}
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
	totalRows, err := svc.CountResource(&service.CountResourceRequest{
        Name: param.Name,
	})
	if err != nil {
		global.Logger.Errorf("svc.CountResource err: %v", err)
		response.ToErrorResponse(errcode.ErrorCountResourceFail)
	}
	resources, err := svc.GetResourceList(&param, &pager)
	if err != nil {
		global.Logger.Errorf("svc.GetResourceList err: %v", err)
		response.ToErrorResponse(errcode.ErrorGetResourceListFail)
		return
	}
	response.ToResponseList(resources, totalRows)
	return
}

func (t Resource) Update(c *gin.Context) {
	param := service.UpdateResourceRequest{Id: convert.StrTo(c.Param("id")).MustUInt32()}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}

	svc := service.New(c.Request.Context())
	n, err := svc.UpdateResource(&param)
	if err != nil || n < 1 {
		global.Logger.Errorf("svc.UpdateResource err: %v", err)
		response.ToErrorResponse(errcode.ErrorUpdateResourceFail)
		return
	}

	response.ToResponse(gin.H{})
	return
}

func (t Resource) Delete(c *gin.Context) {
	param := service.DeleteResourceRequest{Id: convert.StrTo(c.Param("id")).MustUInt32()}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}

	svc := service.New(c.Request.Context())
	n, err := svc.DeleteResource(&param)
	if err != nil || n < 1{
		global.Logger.Errorf("svc.DeleteResource err: %v", err)
		response.ToErrorResponse(errcode.ErrorDeleteResourceFail)
		return
	}

	response.ToResponse(gin.H{})
	return
}
