package service

type CountProjectRequest struct {
    Name string `json:"name" binding:"max=63"`
    Puid string `json:"puid" binding:"max=255"`
    Ouid string `json:"ouid" binding:"max=255"`
    Describe string `json:"describe"`
}

type ProjectListRequest struct {
    Name string `json:"name" binding:"max=63"`
    Puid string `json:"puid" binding:"max=255"`
    Ouid string `json:"ouid" binding:"max=255"`
    Describe string `json:"describe"`
}

type CreateProjectRequest struct {
	Id       int64  `json:"id"`
    Name string `json:"name" binding:"required,max=63"`
    Ouid string `json:"ouid" binding:"max=255"`
    Describe string `json:"describe"`
}

type UpdateProjectRequest struct {
	 Puid string `form:"puid binding:"required"`
    Name string `json:"name" binding:"max=63"`
    Ouid string `json:"ouid" binding:"max=255"`
    Describe string `json:"describe"`
}

type GetProjectRequest struct {
	 Puid string `form:"puid binding:"required"`
}

type DeleteProjectRequest struct {
	 Puid string `form:"puid binding:"required"`
}

func (svc *Service) CountProject(param *CountProjectRequest) (int, error) {
	return svc.dao.CountProject(param.Name,param.Puid,param.Ouid,param.Describe,)
}

func (svc *Service) GetProjectList(param *ProjectListRequest, pager *app.Pager) ([]*model.Project, error) {
	return svc.dao.GetProjectList(param.Name,param.Puid,param.Ouid,param.Describe, pager.Page, pager.PageSize)
}

func (svc *Service) CreateProject(param *CreateProjectRequest) (int64, error) {
	return svc.dao.CreateProject(param.Name,param.Ouid,param.Describe,)
}

func (svc *Service) UpdateProject(param *UpdateProjectRequest) (int64, error) {
	return svc.dao.UpdateProject(param.Name,param.Ouid,param.Describe, param.Puid)
}

func (svc *Service) DeleteProject(param *DeleteProjectRequest) (int64, error) {
	return svc.dao.DeleteProject(param.Puid)
}

func (svc *Service) GetProject(param *GetProjectRequest) (*model.Project, error) {
	return svc.dao.GetProject(param.Puid)
}

