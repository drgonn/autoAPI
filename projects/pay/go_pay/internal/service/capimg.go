package service

type CountCapimgRequest struct {
}

type CapimgListRequest struct {
}

type CreateCapimgRequest struct {
	Id       int64  `json:"id"`
}

type UpdateCapimgRequest struct {
	 Id uint32 `form:"id binding:"required"`
}

type GetCapimgRequest struct {
	 Id uint32 `form:"id binding:"required"`
}

type DeleteCapimgRequest struct {
	 Id uint32 `form:"id binding:"required"`
}

func (svc *Service) CountCapimg(param *CountCapimgRequest) (int, error) {
	return svc.dao.CountCapimg()
}

func (svc *Service) GetCapimgList(param *CapimgListRequest, pager *app.Pager) ([]*model.Capimg, error) {
	return svc.dao.GetCapimgList( pager.Page, pager.PageSize)
}

func (svc *Service) CreateCapimg(param *CreateCapimgRequest) (int64, error) {
	return svc.dao.CreateCapimg()
}

func (svc *Service) UpdateCapimg(param *UpdateCapimgRequest) (int64, error) {
	return svc.dao.UpdateCapimg(param.HikvUrl, param.Id)
}

func (svc *Service) DeleteCapimg(param *DeleteCapimgRequest) (int64, error) {
	return svc.dao.DeleteCapimg(param.Id)
}

func (svc *Service) GetCapimg(param *GetCapimgRequest) (*model.Capimg, error) {
	return svc.dao.GetCapimg(param.Id)
}

