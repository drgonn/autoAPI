package service

type CountUserRequest struct {
}

type UserListRequest struct {
}

type CreateUserRequest struct {
	Id       int64  `json:"id"`
    Uid string `json:"uid" binding:"max=63,unique=users"`
    Permission interface{} `json:"permission"`
}

type UpdateUserRequest struct {
	 Uid string `form:"uid binding:"required"`
    Permission interface{} `json:"permission"`
}

type GetUserRequest struct {
	 Uid string `form:"uid binding:"required"`
}

type DeleteUserRequest struct {
	 Uid string `form:"uid binding:"required"`
}

func (svc *Service) CountUser(param *CountUserRequest) (int, error) {
	return svc.dao.CountUser()
}

func (svc *Service) GetUserList(param *UserListRequest, pager *app.Pager) ([]*model.User, error) {
	return svc.dao.GetUserList( pager.Page, pager.PageSize)
}

func (svc *Service) CreateUser(param *CreateUserRequest) (int64, error) {
	return svc.dao.CreateUser(param.Uid,param.Permission,)
}

func (svc *Service) UpdateUser(param *UpdateUserRequest) (int64, error) {
	return svc.dao.UpdateUser(param.Permission, param.Uid)
}

func (svc *Service) DeleteUser(param *DeleteUserRequest) (int64, error) {
	return svc.dao.DeleteUser(param.Uid)
}

func (svc *Service) GetUser(param *GetUserRequest) (*model.User, error) {
	return svc.dao.GetUser(param.Uid)
}

