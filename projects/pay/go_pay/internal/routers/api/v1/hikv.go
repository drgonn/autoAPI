package v1
type Hikv struct{}
func NewHikv() Hikv{return Hikv{}}

func (p Hikv) Create(c *gin.Context) {
param := service.CreateHikvRequest{}
response := app.NewResponse(c)
valid, errs := app.BindAndValid(c, &param)
if !valid {
    global.Logger.Errorf("app.BindAndValid errs: %v", errs)
    errRsp := errcode.InvalidParams.WithDetails(errs.Errors()...)
    response.ToErrorResponse(errRsp)
    return
}
    svc := service.New(c.Request.Context())
hikv_id, err := svc.CreateHikv(&param)
if err != nil {
global.Logger.Errorf("svc.CreateHikv err: %v", err)
if hikv_id == 0 {
	response.ToErrorResponse(errcode.ErrorCreateHikvNameExisted)
} else {
	response.ToErrorResponse(errcode.ErrorCreateHikvFail)
}
return
}
param.Id = hikv_id
response.ToResponse(param)
return
}
func (t Hikv) Get(c *gin.Context) {
	param := service.GetHikvRequest{Id: convert.StrTo(c.Param("id")).MustUInt32()}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}
	svc := service.New(c.Request.Context())
	hikv, err := svc.GetHikv(&param)
	if err != nil {
		global.Logger.Errorf("svc.GetHikv err: %v", err)
		response.ToErrorResponse(errcode.ErrorGetHikvFail)
		return
	}
	response.ToResponse(hikv)
	return
}

func (t Hikv) List(c *gin.Context) {
	param := service.HikvListRequest{}
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
	totalRows, err := svc.CountHikv(&service.CountHikvRequest{
	})
	if err != nil {
		global.Logger.Errorf("svc.CountHikv err: %v", err)
		response.ToErrorResponse(errcode.ErrorCountHikvFail)
	}
	hikvs, err := svc.GetHikvList(&param, &pager)
	if err != nil {
		global.Logger.Errorf("svc.GetHikvList err: %v", err)
		response.ToErrorResponse(errcode.ErrorGetHikvListFail)
		return
	}
	response.ToResponseList(hikvs, totalRows)
	return
}

func (t Hikv) Update(c *gin.Context) {
	param := service.UpdateHikvRequest{Id: convert.StrTo(c.Param("id")).MustUInt32()}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}

	svc := service.New(c.Request.Context())
	n, err := svc.UpdateHikv(&param)
	if err != nil || n < 1 {
		global.Logger.Errorf("svc.UpdateHikv err: %v", err)
		response.ToErrorResponse(errcode.ErrorUpdateHikvFail)
		return
	}

	response.ToResponse(gin.H{})
	return
}

func (t Hikv) Delete(c *gin.Context) {
	param := service.DeleteHikvRequest{Id: convert.StrTo(c.Param("id")).MustUInt32()}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}

	svc := service.New(c.Request.Context())
	n, err := svc.DeleteHikv(&param)
	if err != nil || n < 1{
		global.Logger.Errorf("svc.DeleteHikv err: %v", err)
		response.ToErrorResponse(errcode.ErrorDeleteHikvFail)
		return
	}

	response.ToResponse(gin.H{})
	return
}
