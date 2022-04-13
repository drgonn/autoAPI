package service

type CountAlertLogRequest struct {
    Iccid string `json:"iccid" binding:"max=127"`
    Status int64 `json:"status"`
}

type AlertLogListRequest struct {
    Iccid string `json:"iccid" binding:"max=127"`
    Status int64 `json:"status"`
}

type CreateAlertLogRequest struct {
	Id       int64  `json:"id"`
    Iccid string `json:"iccid" binding:"required,max=127"`
}

type UpdateAlertLogRequest struct {
	 Status int64 `form:"status binding:"required"`
    Iccid string `json:"iccid" binding:"max=127"`
}

type GetAlertLogRequest struct {
	 Status int64 `form:"status binding:"required"`
}

type DeleteAlertLogRequest struct {
	 Status int64 `form:"status binding:"required"`
}

func (svc *Service) CountAlertLog(param *CountAlertLogRequest) (int, error) {
	return svc.dao.CountAlertLog(param.Iccid,param.Status,)
}

func (svc *Service) GetAlertLogList(param *AlertLogListRequest, pager *app.Pager) ([]*model.AlertLog, error) {
	return svc.dao.GetAlertLogList(param.Iccid,param.Status, pager.Page, pager.PageSize)
}

func (svc *Service) CreateAlertLog(param *CreateAlertLogRequest) (int64, error) {
	return svc.dao.CreateAlertLog(param.Iccid,)
}

func (svc *Service) UpdateAlertLog(param *UpdateAlertLogRequest) (int64, error) {
	return svc.dao.UpdateAlertLog(param.Iccid, param.Status)
}

func (svc *Service) DeleteAlertLog(param *DeleteAlertLogRequest) (int64, error) {
	return svc.dao.DeleteAlertLog(param.Status)
}

func (svc *Service) GetAlertLog(param *GetAlertLogRequest) (*model.AlertLog, error) {
	return svc.dao.GetAlertLog(param.Status)
}

