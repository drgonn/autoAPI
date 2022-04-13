package v1
type AlertLog struct{}
func NewAlertLog() AlertLog{return AlertLog{}}

func (p AlertLog) Create(c *gin.Context) {
param := service.CreateAlertLogRequest{}
response := app.NewResponse(c)
valid, errs := app.BindAndValid(c, &param)
if !valid {
    global.Logger.Errorf("app.BindAndValid errs: %v", errs)
    errRsp := errcode.InvalidParams.WithDetails(errs.Errors()...)
    response.ToErrorResponse(errRsp)
    return
}
    svc := service.New(c.Request.Context())
alert_log_id, err := svc.CreateAlertLog(&param)
if err != nil {
global.Logger.Errorf("svc.CreateAlertLog err: %v", err)
if alert_log_id == 0 {
	response.ToErrorResponse(errcode.ErrorCreateAlertLogNameExisted)
} else {
	response.ToErrorResponse(errcode.ErrorCreateAlertLogFail)
}
return
}
param.Id = alert_log_id
response.ToResponse(param)
return
}
func (t AlertLog) Get(c *gin.Context) {
	param := service.GetAlertLogRequest{Status: c.Param("status")}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}
	svc := service.New(c.Request.Context())
	alert_log, err := svc.GetAlertLog(&param)
	if err != nil {
		global.Logger.Errorf("svc.GetAlertLog err: %v", err)
		response.ToErrorResponse(errcode.ErrorGetAlertLogFail)
		return
	}
	response.ToResponse(alert_log)
	return
}

func (t AlertLog) List(c *gin.Context) {
	param := service.AlertLogListRequest{}
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
	totalRows, err := svc.CountAlertLog(&service.CountAlertLogRequest{
        Iccid: param.Iccid,
        Status: param.Status,
	})
	if err != nil {
		global.Logger.Errorf("svc.CountAlertLog err: %v", err)
		response.ToErrorResponse(errcode.ErrorCountAlertLogFail)
	}
	alert_logs, err := svc.GetAlertLogList(&param, &pager)
	if err != nil {
		global.Logger.Errorf("svc.GetAlertLogList err: %v", err)
		response.ToErrorResponse(errcode.ErrorGetAlertLogListFail)
		return
	}
	response.ToResponseList(alert_logs, totalRows)
	return
}

func (t AlertLog) Update(c *gin.Context) {
	param := service.UpdateAlertLogRequest{Status: c.Param("status")}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}

	svc := service.New(c.Request.Context())
	n, err := svc.UpdateAlertLog(&param)
	if err != nil || n < 1 {
		global.Logger.Errorf("svc.UpdateAlertLog err: %v", err)
		response.ToErrorResponse(errcode.ErrorUpdateAlertLogFail)
		return
	}

	response.ToResponse(gin.H{})
	return
}

func (t AlertLog) Delete(c *gin.Context) {
	param := service.DeleteAlertLogRequest{Status: c.Param("status")}
	response := app.NewResponse(c)
	valid, errs := app.BindAndValid(c, &param)
	if !valid {
		global.Logger.Errorf("app.BindAndValid errs: %v", errs)
		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))
		return
	}

	svc := service.New(c.Request.Context())
	n, err := svc.DeleteAlertLog(&param)
	if err != nil || n < 1{
		global.Logger.Errorf("svc.DeleteAlertLog err: %v", err)
		response.ToErrorResponse(errcode.ErrorDeleteAlertLogFail)
		return
	}

	response.ToResponse(gin.H{})
	return
}
