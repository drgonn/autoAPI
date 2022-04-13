package service

type CountRoleRequest struct {
    Name string `json:"name" binding:"max=63"`
}

type RoleListRequest struct {
    Name string `json:"name" binding:"max=63"`
}

type CreateRoleRequest struct {
	Id       int64  `json:"id"`
    Name string `json:"name" binding:"required,max=63,unique=roles"`
    Description string `json:"description"`
    Permission interface{} `json:"permission"`
}

type UpdateRoleRequest struct {
	 Id uint `form:"id binding:"required"`
    Name string `json:"name" binding:"max=63"`
    Description string `json:"description"`
    Permission interface{} `json:"permission"`
}

type GetRoleRequest struct {
	 Id uint `form:"id binding:"required"`
}

type DeleteRoleRequest struct {
	 Id uint `form:"id binding:"required"`
}

func (svc *Service) CountRole(param *CountRoleRequest) (int, error) {
	return svc.dao.CountRole(param.Name,)
}

func (svc *Service) GetRoleList(param *RoleListRequest, pager *app.Pager) ([]*model.Role, error) {
	return svc.dao.GetRoleList(param.Name, pager.Page, pager.PageSize)
}

func (svc *Service) CreateRole(param *CreateRoleRequest) (int64, error) {
	return svc.dao.CreateRole(param.Name,param.Description,param.Permission,)
}

func (svc *Service) UpdateRole(param *UpdateRoleRequest) (int64, error) {
	return svc.dao.UpdateRole(param.Name,param.Description,param.Permission, param.Id)
}

func (svc *Service) DeleteRole(param *DeleteRoleRequest) (int64, error) {
	return svc.dao.DeleteRole(param.Id)
}

func (svc *Service) GetRole(param *GetRoleRequest) (*model.Role, error) {
	return svc.dao.GetRole(param.Id)
}

