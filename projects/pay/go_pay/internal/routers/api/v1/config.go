package v1
type Config struct{}
func NewConfig() Config{return Config{}}

func (p Config) Create(c *gin.Context) {
param := service.CreateConfigRequest{}
response := app.NewResponse(c)
valid, errs := app.BindAndValid(c, &param)
if !valid {
    global.Logger.Errorf("app.BindAndValid errs: %v", errs)
    errRsp := errcode.InvalidParams.WithDetails(errs.Errors()...)
    response.ToErrorResponse(errRsp)
    return
}
    svc := service.New(c.Request.Context())
config_id, err := svc.CreateConfig(&param)
if err != nil {
global.Logger.Errorf("svc.CreateConfig err: %v", err)
if config_id == 0 {
	response.ToErrorResponse(errcode.ErrorCreateConfigNameExisted)
} else {
	response.ToErrorResponse(errcode.ErrorCreateConfigFail)
}
return
}
param.Id = config_id
response.ToResponse(param)
return
}
func (t Config) Get(c *gin.Context) {
	param := service.GetConfigRequest{Id: convert.StrTo(c.Param("id")).MustUInt32()}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}
	svc := service.New(c.Request.Context())
	config, err := svc.GetConfig(&param)
	if err != nil {
		global.Logger.Errorf("svc.GetConfig err: %v", err)
		response.ToErrorResponse(errcode.ErrorGetConfigFail)
		return
	}
	response.ToResponse(config)
	return
}

func (t Config) List(c *gin.Context) {
	param := service.ConfigListRequest{}
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
	totalRows, err := svc.CountConfig(&service.CountConfigRequest{
	})
	if err != nil {
		global.Logger.Errorf("svc.CountConfig err: %v", err)
		response.ToErrorResponse(errcode.ErrorCountConfigFail)
	}
	configs, err := svc.GetConfigList(&param, &pager)
	if err != nil {
		global.Logger.Errorf("svc.GetConfigList err: %v", err)
		response.ToErrorResponse(errcode.ErrorGetConfigListFail)
		return
	}
	response.ToResponseList(configs, totalRows)
	return
}

func (t Config) Update(c *gin.Context) {
	param := service.UpdateConfigRequest{Id: convert.StrTo(c.Param("id")).MustUInt32()}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}

	svc := service.New(c.Request.Context())
	n, err := svc.UpdateConfig(&param)
	if err != nil || n < 1 {
		global.Logger.Errorf("svc.UpdateConfig err: %v", err)
		response.ToErrorResponse(errcode.ErrorUpdateConfigFail)
		return
	}

	response.ToResponse(gin.H{})
	return
}

func (t Config) Delete(c *gin.Context) {
	param := service.DeleteConfigRequest{Id: convert.StrTo(c.Param("id")).MustUInt32()}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}

	svc := service.New(c.Request.Context())
	n, err := svc.DeleteConfig(&param)
	if err != nil || n < 1{
		global.Logger.Errorf("svc.DeleteConfig err: %v", err)
		response.ToErrorResponse(errcode.ErrorDeleteConfigFail)
		return
	}

	response.ToResponse(gin.H{})
	return
}
