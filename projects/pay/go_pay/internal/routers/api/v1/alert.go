package v1
type Alert struct{}
func NewAlert() Alert{return Alert{}}

func (p Alert) Create(c *gin.Context) {
param := service.CreateAlertRequest{}
response := app.NewResponse(c)
valid, errs := app.BindAndValid(c, &param)
if !valid {
    global.Logger.Errorf("app.BindAndValid errs: %v", errs)
    errRsp := errcode.InvalidParams.WithDetails(errs.Errors()...)
    response.ToErrorResponse(errRsp)
    return
}
    svc := service.New(c.Request.Context())
alert_id, err := svc.CreateAlert(&param)
if err != nil {
global.Logger.Errorf("svc.CreateAlert err: %v", err)
if alert_id == 0 {
	response.ToErrorResponse(errcode.ErrorCreateAlertNameExisted)
} else {
	response.ToErrorResponse(errcode.ErrorCreateAlertFail)
}
return
}
param.Id = alert_id
response.ToResponse(param)
return
}
func (t Alert) Get(c *gin.Context) {
	param := service.GetAlertRequest{Webhook: c.Param("webhook")}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}
	svc := service.New(c.Request.Context())
	alert, err := svc.GetAlert(&param)
	if err != nil {
		global.Logger.Errorf("svc.GetAlert err: %v", err)
		response.ToErrorResponse(errcode.ErrorGetAlertFail)
		return
	}
	response.ToResponse(alert)
	return
}

func (t Alert) List(c *gin.Context) {
	param := service.AlertListRequest{}
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
	totalRows, err := svc.CountAlert(&service.CountAlertRequest{
        Name: param.Name,
        Webhook: param.Webhook,
        Emails: param.Emails,
        Flow: param.Flow,
        All: param.All,
        Enable: param.Enable,
        Description: param.Description,
        Event: param.Event,
	})
	if err != nil {
		global.Logger.Errorf("svc.CountAlert err: %v", err)
		response.ToErrorResponse(errcode.ErrorCountAlertFail)
	}
	alerts, err := svc.GetAlertList(&param, &pager)
	if err != nil {
		global.Logger.Errorf("svc.GetAlertList err: %v", err)
		response.ToErrorResponse(errcode.ErrorGetAlertListFail)
		return
	}
	response.ToResponseList(alerts, totalRows)
	return
}

func (t Alert) Update(c *gin.Context) {
	param := service.UpdateAlertRequest{Webhook: c.Param("webhook")}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}

	svc := service.New(c.Request.Context())
	n, err := svc.UpdateAlert(&param)
	if err != nil || n < 1 {
		global.Logger.Errorf("svc.UpdateAlert err: %v", err)
		response.ToErrorResponse(errcode.ErrorUpdateAlertFail)
		return
	}

	response.ToResponse(gin.H{})
	return
}

func (t Alert) Delete(c *gin.Context) {
	param := service.DeleteAlertRequest{Webhook: c.Param("webhook")}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}

	svc := service.New(c.Request.Context())
	n, err := svc.DeleteAlert(&param)
	if err != nil || n < 1{
		global.Logger.Errorf("svc.DeleteAlert err: %v", err)
		response.ToErrorResponse(errcode.ErrorDeleteAlertFail)
		return
	}

	response.ToResponse(gin.H{})
	return
}
