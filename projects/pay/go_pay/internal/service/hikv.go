package service

type CountHikvRequest struct {
}

type HikvListRequest struct {
}

type CreateHikvRequest struct {
	Id       int64  `json:"id"`
    Name string `json:"name" binding:"required,max=63"`
    AppKey string `json:"app_key" binding:"required,max=63"`
    AppSecret string `json:"app_secret" binding:"required,max=63"`
    HikvSerial string `json:"hikv_serial" binding:"required,max=63"`
    ValidateCode string `json:"validate_code" binding:"required,max=63"`
    CapMinute uint `json:"cap_minute"`
}

type UpdateHikvRequest struct {
	 Id uint `form:"id binding:"required"`
    Name string `json:"name" binding:"max=63"`
    AppKey string `json:"app_key" binding:"max=63"`
    AppSecret string `json:"app_secret" binding:"max=63"`
    HikvSerial string `json:"hikv_serial" binding:"max=63"`
    ValidateCode string `json:"validate_code" binding:"max=63"`
    CapMinute uint `json:"cap_minute"`
}

type GetHikvRequest struct {
	 Id uint `form:"id binding:"required"`
}

type DeleteHikvRequest struct {
	 Id uint `form:"id binding:"required"`
}

func (svc *Service) CountHikv(param *CountHikvRequest) (int, error) {
	return svc.dao.CountHikv()
}

func (svc *Service) GetHikvList(param *HikvListRequest, pager *app.Pager) ([]*model.Hikv, error) {
	return svc.dao.GetHikvList( pager.Page, pager.PageSize)
}

func (svc *Service) CreateHikv(param *CreateHikvRequest) (int64, error) {
	return svc.dao.CreateHikv(param.Name,param.AppKey,param.AppSecret,param.HikvSerial,param.ValidateCode,param.CapMinute,)
}

func (svc *Service) UpdateHikv(param *UpdateHikvRequest) (int64, error) {
	return svc.dao.UpdateHikv(param.Name,param.AppKey,param.AppSecret,param.HikvSerial,param.ValidateCode,param.CapMinute, param.Id)
}

func (svc *Service) DeleteHikv(param *DeleteHikvRequest) (int64, error) {
	return svc.dao.DeleteHikv(param.Id)
}

func (svc *Service) GetHikv(param *GetHikvRequest) (*model.Hikv, error) {
	return svc.dao.GetHikv(param.Id)
}

