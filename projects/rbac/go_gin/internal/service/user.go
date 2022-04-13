package service

type CountUserRequest struct {
    Uid string `json:"uid" binding:"max=63"`
}

type UserListRequest struct {
    Uid string `json:"uid" binding:"max=63"`
}

type CreateUserRequest struct {
	Id       int64  `json:"id"`
    Uid string `json:"uid" binding:"max=63"`
    Permission interface{} `json:"permission"`
}

type UpdateUserRequest struct {
	 Id uint `form:"id binding:"required"`
    Uid string `json:"uid" binding:"max=63"`
    Permission interface{} `json:"permission"`
}

type GetUserRequest struct {
	 Id uint `form:"id binding:"required"`
}

type DeleteUserRequest struct {
	 Id uint `form:"id binding:"required"`
}

func (svc *Service) CountUser(param *CountUserRequest) (int, error) {
	return svc.dao.CountUser(param.Uid,)
}

func (svc *Service) GetUserList(param *UserListRequest, pager *app.Pager) ([]*model.User, error) {
	return svc.dao.GetUserList(param.Uid, pager.Page, pager.PageSize)
}

func (svc *Service) CreateUser(param *CreateUserRequest) (int64, error) {
	return svc.dao.CreateUser(param.Uid,param.Permission,)
}

func (svc *Service) UpdateUser(param *UpdateUserRequest) (int64, error) {
	return svc.dao.UpdateUser(param.Uid,param.Permission, param.Id)
}

func (svc *Service) DeleteUser(param *DeleteUserRequest) (int64, error) {
	return svc.dao.DeleteUser(param.Id)
}

func (svc *Service) GetUser(param *GetUserRequest) (*model.User, error) {
	return svc.dao.GetUser(param.Id)
}

