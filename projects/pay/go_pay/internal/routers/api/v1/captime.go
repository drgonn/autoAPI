package v1
type Captime struct{}
func NewCaptime() Captime{return Captime{}}

func (p Captime) Create(c *gin.Context) {
param := service.CreateCaptimeRequest{}
response := app.NewResponse(c)
valid, errs := app.BindAndValid(c, &param)
if !valid {
    global.Logger.Errorf("app.BindAndValid errs: %v", errs)
    errRsp := errcode.InvalidParams.WithDetails(errs.Errors()...)
    response.ToErrorResponse(errRsp)
    return
}
    svc := service.New(c.Request.Context())
captime_id, err := svc.CreateCaptime(&param)
if err != nil {
global.Logger.Errorf("svc.CreateCaptime err: %v", err)
if captime_id == 0 {
	response.ToErrorResponse(errcode.ErrorCreateCaptimeNameExisted)
} else {
	response.ToErrorResponse(errcode.ErrorCreateCaptimeFail)
}
return
}
param.Id = captime_id
response.ToResponse(param)
return
}
func (t Captime) Get(c *gin.Context) {
	param := service.GetCaptimeRequest{Id: convert.StrTo(c.Param("id")).MustUInt32()}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}
	svc := service.New(c.Request.Context())
	captime, err := svc.GetCaptime(&param)
	if err != nil {
		global.Logger.Errorf("svc.GetCaptime err: %v", err)
		response.ToErrorResponse(errcode.ErrorGetCaptimeFail)
		return
	}
	response.ToResponse(captime)
	return
}

func (t Captime) List(c *gin.Context) {
	param := service.CaptimeListRequest{}
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
	totalRows, err := svc.CountCaptime(&service.CountCaptimeRequest{
        Iccid: param.Iccid,
        Status: param.Status,
	})
	if err != nil {
		global.Logger.Errorf("svc.CountCaptime err: %v", err)
		response.ToErrorResponse(errcode.ErrorCountCaptimeFail)
	}
	captimes, err := svc.GetCaptimeList(&param, &pager)
	if err != nil {
		global.Logger.Errorf("svc.GetCaptimeList err: %v", err)
		response.ToErrorResponse(errcode.ErrorGetCaptimeListFail)
		return
	}
	response.ToResponseList(captimes, totalRows)
	return
}

func (t Captime) Update(c *gin.Context) {
	param := service.UpdateCaptimeRequest{Id: convert.StrTo(c.Param("id")).MustUInt32()}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}

	svc := service.New(c.Request.Context())
	n, err := svc.UpdateCaptime(&param)
	if err != nil || n < 1 {
		global.Logger.Errorf("svc.UpdateCaptime err: %v", err)
		response.ToErrorResponse(errcode.ErrorUpdateCaptimeFail)
		return
	}

	response.ToResponse(gin.H{})
	return
}

func (t Captime) Delete(c *gin.Context) {
	param := service.DeleteCaptimeRequest{Id: convert.StrTo(c.Param("id")).MustUInt32()}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}

	svc := service.New(c.Request.Context())
	n, err := svc.DeleteCaptime(&param)
	if err != nil || n < 1{
		global.Logger.Errorf("svc.DeleteCaptime err: %v", err)
		response.ToErrorResponse(errcode.ErrorDeleteCaptimeFail)
		return
	}

	response.ToResponse(gin.H{})
	return
}
