package service

type CountPconfigRequest struct {
    Name string `json:"name" binding:"max=63"`
    Puid string `json:"puid" binding:"max=255"`
    Value string `json:"value"`
}

type PconfigListRequest struct {
    Name string `json:"name" binding:"max=63"`
    Puid string `json:"puid" binding:"max=255"`
    Value string `json:"value"`
}

type CreatePconfigRequest struct {
	Id       int64  `json:"id"`
    Name string `json:"name" binding:"required,max=63"`
    Puid string `json:"puid" binding:"max=255"`
    Value string `json:"value"`
}

type UpdatePconfigRequest struct {
	 Id uint32 `form:"id binding:"required"`
    Name string `json:"name" binding:"max=63"`
    Puid string `json:"puid" binding:"max=255"`
    Value string `json:"value"`
}

type GetPconfigRequest struct {
	 Id uint32 `form:"id binding:"required"`
}

type DeletePconfigRequest struct {
	 Id uint32 `form:"id binding:"required"`
}

func (svc *Service) CountPconfig(param *CountPconfigRequest) (int, error) {
	return svc.dao.CountPconfig(param.Name,param.Puid,param.Value,)
}

func (svc *Service) GetPconfigList(param *PconfigListRequest, pager *app.Pager) ([]*model.Pconfig, error) {
	return svc.dao.GetPconfigList(param.Name,param.Puid,param.Value, pager.Page, pager.PageSize)
}

func (svc *Service) CreatePconfig(param *CreatePconfigRequest) (int64, error) {
	return svc.dao.CreatePconfig(param.Name,param.Puid,param.Value,)
}

func (svc *Service) UpdatePconfig(param *UpdatePconfigRequest) (int64, error) {
	return svc.dao.UpdatePconfig(param.Name,param.Puid,param.Value, param.Id)
}

func (svc *Service) DeletePconfig(param *DeletePconfigRequest) (int64, error) {
	return svc.dao.DeletePconfig(param.Id)
}

func (svc *Service) GetPconfig(param *GetPconfigRequest) (*model.Pconfig, error) {
	return svc.dao.GetPconfig(param.Id)
}

