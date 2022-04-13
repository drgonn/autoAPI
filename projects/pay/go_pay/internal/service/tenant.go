package service

type CountTenantRequest struct {
    Name string `json:"name" binding:"max=63"`
    Ouid string `json:"ouid" binding:"max=255"`
    Describe string `json:"describe"`
}

type TenantListRequest struct {
    Name string `json:"name" binding:"max=63"`
    Ouid string `json:"ouid" binding:"max=255"`
    Describe string `json:"describe"`
}

type CreateTenantRequest struct {
	Id       int64  `json:"id"`
    Name string `json:"name" binding:"required,max=63"`
    Describe string `json:"describe"`
}

type UpdateTenantRequest struct {
	 Ouid string `form:"ouid binding:"required"`
    Name string `json:"name" binding:"max=63"`
    Describe string `json:"describe"`
}

type GetTenantRequest struct {
	 Ouid string `form:"ouid binding:"required"`
}

type DeleteTenantRequest struct {
	 Ouid string `form:"ouid binding:"required"`
}

func (svc *Service) CountTenant(param *CountTenantRequest) (int, error) {
	return svc.dao.CountTenant(param.Name,param.Ouid,param.Describe,)
}

func (svc *Service) GetTenantList(param *TenantListRequest, pager *app.Pager) ([]*model.Tenant, error) {
	return svc.dao.GetTenantList(param.Name,param.Ouid,param.Describe, pager.Page, pager.PageSize)
}

func (svc *Service) CreateTenant(param *CreateTenantRequest) (int64, error) {
	return svc.dao.CreateTenant(param.Name,param.Describe,)
}

func (svc *Service) UpdateTenant(param *UpdateTenantRequest) (int64, error) {
	return svc.dao.UpdateTenant(param.Name,param.Describe, param.Ouid)
}

func (svc *Service) DeleteTenant(param *DeleteTenantRequest) (int64, error) {
	return svc.dao.DeleteTenant(param.Ouid)
}

func (svc *Service) GetTenant(param *GetTenantRequest) (*model.Tenant, error) {
	return svc.dao.GetTenant(param.Ouid)
}

