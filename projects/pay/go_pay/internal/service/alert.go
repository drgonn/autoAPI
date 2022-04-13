package service

type CountAlertRequest struct {
    Name string `json:"name" binding:"max=63"`
    Webhook string `json:"webhook"`
    Emails  `json:"emails"`
    Flow float `json:"flow"`
    All bool `json:"all"`
    Enable bool `json:"enable"`
    Description string `json:"description"`
    Event int `json:"event"`
}

type AlertListRequest struct {
    Name string `json:"name" binding:"max=63"`
    Webhook string `json:"webhook"`
    Emails  `json:"emails"`
    Flow float `json:"flow"`
    All bool `json:"all"`
    Enable bool `json:"enable"`
    Description string `json:"description"`
    Event int `json:"event"`
}

type CreateAlertRequest struct {
	Id       int64  `json:"id"`
    Name string `json:"name" binding:"required,max=63"`
    Webhook string `json:"webhook"`
    Emails  `json:"emails"`
    Flow float `json:"flow"`
    All bool `json:"all"`
    Enable bool `json:"enable"`
    Description string `json:"description"`
    Event int `json:"event"`
}

type UpdateAlertRequest struct {
	 Webhook string `form:"webhook binding:"required"`
    Name string `json:"name" binding:"max=63"`
    Webhook string `json:"webhook"`
    Emails  `json:"emails"`
    Flow float `json:"flow"`
    All bool `json:"all"`
    Enable bool `json:"enable"`
    Description string `json:"description"`
    Event int `json:"event"`
}

type GetAlertRequest struct {
	 Webhook string `form:"webhook binding:"required"`
}

type DeleteAlertRequest struct {
	 Webhook string `form:"webhook binding:"required"`
}

func (svc *Service) CountAlert(param *CountAlertRequest) (int, error) {
	return svc.dao.CountAlert(param.Name,param.Webhook,param.Emails,param.Flow,param.All,param.Enable,param.Description,param.Event,)
}

func (svc *Service) GetAlertList(param *AlertListRequest, pager *app.Pager) ([]*model.Alert, error) {
	return svc.dao.GetAlertList(param.Name,param.Webhook,param.Emails,param.Flow,param.All,param.Enable,param.Description,param.Event, pager.Page, pager.PageSize)
}

func (svc *Service) CreateAlert(param *CreateAlertRequest) (int64, error) {
	return svc.dao.CreateAlert(param.Name,param.Webhook,param.Emails,param.Flow,param.All,param.Enable,param.Description,param.Event,)
}

func (svc *Service) UpdateAlert(param *UpdateAlertRequest) (int64, error) {
	return svc.dao.UpdateAlert(param.Name,param.Webhook,param.Emails,param.Flow,param.All,param.Enable,param.Description,param.Event, param.Webhook)
}

func (svc *Service) DeleteAlert(param *DeleteAlertRequest) (int64, error) {
	return svc.dao.DeleteAlert(param.Webhook)
}

func (svc *Service) GetAlert(param *GetAlertRequest) (*model.Alert, error) {
	return svc.dao.GetAlert(param.Webhook)
}

