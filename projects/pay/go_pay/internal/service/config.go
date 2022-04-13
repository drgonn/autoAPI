package service

type CountConfigRequest struct {
}

type ConfigListRequest struct {
}

type CreateConfigRequest struct {
	Id       int64  `json:"id"`
    PureNumber bool `json:"pure_number" binding:"required"`
    CaseSensitive bool `json:"case_sensitive" binding:"required"`
    SpecialCharacters bool `json:"special_characters" binding:"required"`
    AutoExpire uint64 `json:"auto_expire" binding:"required"`
}

type UpdateConfigRequest struct {
	 Id uint `form:"id binding:"required"`
    PureNumber bool `json:"pure_number"`
    CaseSensitive bool `json:"case_sensitive"`
    SpecialCharacters bool `json:"special_characters"`
    AutoExpire uint64 `json:"auto_expire"`
}

type GetConfigRequest struct {
	 Id uint `form:"id binding:"required"`
}

type DeleteConfigRequest struct {
	 Id uint `form:"id binding:"required"`
}

func (svc *Service) CountConfig(param *CountConfigRequest) (int, error) {
	return svc.dao.CountConfig()
}

func (svc *Service) GetConfigList(param *ConfigListRequest, pager *app.Pager) ([]*model.Config, error) {
	return svc.dao.GetConfigList( pager.Page, pager.PageSize)
}

func (svc *Service) CreateConfig(param *CreateConfigRequest) (int64, error) {
	return svc.dao.CreateConfig(param.PureNumber,param.CaseSensitive,param.SpecialCharacters,param.AutoExpire,)
}

func (svc *Service) UpdateConfig(param *UpdateConfigRequest) (int64, error) {
	return svc.dao.UpdateConfig(param.PureNumber,param.CaseSensitive,param.SpecialCharacters,param.AutoExpire, param.Id)
}

func (svc *Service) DeleteConfig(param *DeleteConfigRequest) (int64, error) {
	return svc.dao.DeleteConfig(param.Id)
}

func (svc *Service) GetConfig(param *GetConfigRequest) (*model.Config, error) {
	return svc.dao.GetConfig(param.Id)
}

