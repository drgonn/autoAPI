package service

type CountResourceRequest struct {
    Name string `json:"name" binding:"max=63"`
}

type ResourceListRequest struct {
    Name string `json:"name" binding:"max=63"`
}

type CreateResourceRequest struct {
	Id       int64  `json:"id"`
    Name string `json:"name" binding:"required,max=63,unique=resources"`
    Description string `json:"description"`
    Action interface{} `json:"action"`
}

type UpdateResourceRequest struct {
	 Id uint `form:"id binding:"required"`
    Description string `json:"description"`
    Action interface{} `json:"action"`
}

type GetResourceRequest struct {
	 Id uint `form:"id binding:"required"`
}

type DeleteResourceRequest struct {
	 Id uint `form:"id binding:"required"`
}

func (svc *Service) CountResource(param *CountResourceRequest) (int, error) {
	return svc.dao.CountResource(param.Name,)
}

func (svc *Service) GetResourceList(param *ResourceListRequest, pager *app.Pager) ([]*model.Resource, error) {
	return svc.dao.GetResourceList(param.Name, pager.Page, pager.PageSize)
}

func (svc *Service) CreateResource(param *CreateResourceRequest) (int64, error) {
	return svc.dao.CreateResource(param.Name,param.Description,param.Action,)
}

func (svc *Service) UpdateResource(param *UpdateResourceRequest) (int64, error) {
	return svc.dao.UpdateResource(param.Description,param.Action, param.Id)
}

func (svc *Service) DeleteResource(param *DeleteResourceRequest) (int64, error) {
	return svc.dao.DeleteResource(param.Id)
}

func (svc *Service) GetResource(param *GetResourceRequest) (*model.Resource, error) {
	return svc.dao.GetResource(param.Id)
}

