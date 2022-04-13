package v1
type Capimg struct{}
func NewCapimg() Capimg{return Capimg{}}

func (p Capimg) Create(c *gin.Context) {
param := service.CreateCapimgRequest{}
response := app.NewResponse(c)
valid, errs := app.BindAndValid(c, &param)
if !valid {
    global.Logger.Errorf("app.BindAndValid errs: %v", errs)
    errRsp := errcode.InvalidParams.WithDetails(errs.Errors()...)
    response.ToErrorResponse(errRsp)
    return
}
    svc := service.New(c.Request.Context())
capimg_id, err := svc.CreateCapimg(&param)
if err != nil {
global.Logger.Errorf("svc.CreateCapimg err: %v", err)
if capimg_id == 0 {
	response.ToErrorResponse(errcode.ErrorCreateCapimgNameExisted)
} else {
	response.ToErrorResponse(errcode.ErrorCreateCapimgFail)
}
return
}
param.Id = capimg_id
response.ToResponse(param)
return
}
func (t Capimg) Get(c *gin.Context) {
	param := service.GetCapimgRequest{Id: convert.StrTo(c.Param("id")).MustUInt32()}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}
	svc := service.New(c.Request.Context())
	capimg, err := svc.GetCapimg(&param)
	if err != nil {
		global.Logger.Errorf("svc.GetCapimg err: %v", err)
		response.ToErrorResponse(errcode.ErrorGetCapimgFail)
		return
	}
	response.ToResponse(capimg)
	return
}

func (t Capimg) List(c *gin.Context) {
	param := service.CapimgListRequest{}
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
	totalRows, err := svc.CountCapimg(&service.CountCapimgRequest{
	})
	if err != nil {
		global.Logger.Errorf("svc.CountCapimg err: %v", err)
		response.ToErrorResponse(errcode.ErrorCountCapimgFail)
	}
	capimgs, err := svc.GetCapimgList(&param, &pager)
	if err != nil {
		global.Logger.Errorf("svc.GetCapimgList err: %v", err)
		response.ToErrorResponse(errcode.ErrorGetCapimgListFail)
		return
	}
	response.ToResponseList(capimgs, totalRows)
	return
}

func (t Capimg) Update(c *gin.Context) {
	param := service.UpdateCapimgRequest{Id: convert.StrTo(c.Param("id")).MustUInt32()}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}

	svc := service.New(c.Request.Context())
	n, err := svc.UpdateCapimg(&param)
	if err != nil || n < 1 {
		global.Logger.Errorf("svc.UpdateCapimg err: %v", err)
		response.ToErrorResponse(errcode.ErrorUpdateCapimgFail)
		return
	}

	response.ToResponse(gin.H{})
	return
}

func (t Capimg) Delete(c *gin.Context) {
	param := service.DeleteCapimgRequest{Id: convert.StrTo(c.Param("id")).MustUInt32()}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}

	svc := service.New(c.Request.Context())
	n, err := svc.DeleteCapimg(&param)
	if err != nil || n < 1{
		global.Logger.Errorf("svc.DeleteCapimg err: %v", err)
		response.ToErrorResponse(errcode.ErrorDeleteCapimgFail)
		return
	}

	response.ToResponse(gin.H{})
	return
}
