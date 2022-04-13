package v1
type Pconfig struct{}
func NewPconfig() Pconfig{return Pconfig{}}

func (p Pconfig) Create(c *gin.Context) {
param := service.CreatePconfigRequest{}
response := app.NewResponse(c)
valid, errs := app.BindAndValid(c, &param)
if !valid {
    global.Logger.Errorf("app.BindAndValid errs: %v", errs)
    errRsp := errcode.InvalidParams.WithDetails(errs.Errors()...)
    response.ToErrorResponse(errRsp)
    return
}
    svc := service.New(c.Request.Context())
pconfig_id, err := svc.CreatePconfig(&param)
if err != nil {
global.Logger.Errorf("svc.CreatePconfig err: %v", err)
if pconfig_id == 0 {
	response.ToErrorResponse(errcode.ErrorCreatePconfigNameExisted)
} else {
	response.ToErrorResponse(errcode.ErrorCreatePconfigFail)
}
return
}
param.Id = pconfig_id
response.ToResponse(param)
return
}
func (t Pconfig) Get(c *gin.Context) {
	param := service.GetPconfigRequest{Id: convert.StrTo(c.Param("id")).MustUInt32()}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}
	svc := service.New(c.Request.Context())
	pconfig, err := svc.GetPconfig(&param)
	if err != nil {
		global.Logger.Errorf("svc.GetPconfig err: %v", err)
		response.ToErrorResponse(errcode.ErrorGetPconfigFail)
		return
	}
	response.ToResponse(pconfig)
	return
}

func (t Pconfig) List(c *gin.Context) {
	param := service.PconfigListRequest{}
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
	totalRows, err := svc.CountPconfig(&service.CountPconfigRequest{
        Name: param.Name,
        Puid: param.Puid,
        Value: param.Value,
	})
	if err != nil {
		global.Logger.Errorf("svc.CountPconfig err: %v", err)
		response.ToErrorResponse(errcode.ErrorCountPconfigFail)
	}
	pconfigs, err := svc.GetPconfigList(&param, &pager)
	if err != nil {
		global.Logger.Errorf("svc.GetPconfigList err: %v", err)
		response.ToErrorResponse(errcode.ErrorGetPconfigListFail)
		return
	}
	response.ToResponseList(pconfigs, totalRows)
	return
}

func (t Pconfig) Update(c *gin.Context) {
	param := service.UpdatePconfigRequest{Id: convert.StrTo(c.Param("id")).MustUInt32()}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}

	svc := service.New(c.Request.Context())
	n, err := svc.UpdatePconfig(&param)
	if err != nil || n < 1 {
		global.Logger.Errorf("svc.UpdatePconfig err: %v", err)
		response.ToErrorResponse(errcode.ErrorUpdatePconfigFail)
		return
	}

	response.ToResponse(gin.H{})
	return
}

func (t Pconfig) Delete(c *gin.Context) {
	param := service.DeletePconfigRequest{Id: convert.StrTo(c.Param("id")).MustUInt32()}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}

	svc := service.New(c.Request.Context())
	n, err := svc.DeletePconfig(&param)
	if err != nil || n < 1{
		global.Logger.Errorf("svc.DeletePconfig err: %v", err)
		response.ToErrorResponse(errcode.ErrorDeletePconfigFail)
		return
	}

	response.ToResponse(gin.H{})
	return
}
