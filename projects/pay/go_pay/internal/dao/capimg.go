package dao

func (d *Dao) CountCapimg() (int, error) {
	capimg := model.Capimg{}
	return capimg.Count(d.engine)
}

func (d *Dao) GetCapimg(id uint32) (*model.Capimg, error) {
	capimg := model.Capimg{Id: id}
	return capimg.Get(d.engine)
}

func (d *Dao) GetCapimgList( page, pageSize int) ([]*model.Capimg, error) {
	capimg := model.Capimg{}
	pageOffset := app.GetPageOffset(page, pageSize)
	return capimg.List(d.engine, pageOffset, pageSize)
}

func (d *Dao) CreateCapimg() (int64, error) {
	capimg := model.Capimg{
	}
	return capimg.Create(d.engine)
}

func (d *Dao) UpdateCapimg(hikv_url string, id uint32) (int64, error) {
	capimg := model.Capimg{
	Id: id,
        HikvUrl: hikv_url,
	}
	return capimg.Update(d.engine)
}

func (d *Dao) DeleteCapimg(id uint32) (int64, error) {
	capimg := model.Capimg{Id: id}
	return capimg.Delete(d.engine)
}

