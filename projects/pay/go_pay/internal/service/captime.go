package service

type CountCaptimeRequest struct {
    Iccid string `json:"iccid" binding:"max=127"`
    Status string `json:"status" binding:"max=63"`
}

type CaptimeListRequest struct {
    Iccid string `json:"iccid" binding:"max=127"`
    Status string `json:"status" binding:"max=63"`
}

type CreateCaptimeRequest struct {
	Id       int64  `json:"id"`
    Iccid string `json:"iccid" binding:"required,max=127"`
    Status string `json:"status" binding:"max=63"`
}

type UpdateCaptimeRequest struct {
	 Id uint32 `form:"id binding:"required"`
    Iccid string `json:"iccid" binding:"max=127"`
    Status string `json:"status" binding:"max=63"`
}

type GetCaptimeRequest struct {
	 Id uint32 `form:"id binding:"required"`
}

type DeleteCaptimeRequest struct {
	 Id uint32 `form:"id binding:"required"`
}

func (svc *Service) CountCaptime(param *CountCaptimeRequest) (int, error) {
	return svc.dao.CountCaptime(param.Iccid,param.Status,)
}

func (svc *Service) GetCaptimeList(param *CaptimeListRequest, pager *app.Pager) ([]*model.Captime, error) {
	return svc.dao.GetCaptimeList(param.Iccid,param.Status, pager.Page, pager.PageSize)
}

func (svc *Service) CreateCaptime(param *CreateCaptimeRequest) (int64, error) {
	return svc.dao.CreateCaptime(param.Iccid,param.Status,)
}

func (svc *Service) UpdateCaptime(param *UpdateCaptimeRequest) (int64, error) {
	return svc.dao.UpdateCaptime(param.Iccid,param.Status, param.Id)
}

func (svc *Service) DeleteCaptime(param *DeleteCaptimeRequest) (int64, error) {
	return svc.dao.DeleteCaptime(param.Id)
}

func (svc *Service) GetCaptime(param *GetCaptimeRequest) (*model.Captime, error) {
	return svc.dao.GetCaptime(param.Id)
}

