package dao

func (d *Dao) CountCaptime(iccid string,status string,) (int, error) {
	captime := model.Captime{        Iccid: iccid,
        Status: status,
}
	return captime.Count(d.engine)
}

func (d *Dao) GetCaptime(id uint32) (*model.Captime, error) {
	captime := model.Captime{Id: id}
	return captime.Get(d.engine)
}

func (d *Dao) GetCaptimeList(iccid string,status string, page, pageSize int) ([]*model.Captime, error) {
	captime := model.Captime{        Iccid: iccid,
        Status: status,
}
	pageOffset := app.GetPageOffset(page, pageSize)
	return captime.List(d.engine, pageOffset, pageSize)
}

func (d *Dao) CreateCaptime(iccid string,status string,) (int64, error) {
	captime := model.Captime{
        Iccid: iccid,
        Status: status,
	}
	return captime.Create(d.engine)
}

func (d *Dao) UpdateCaptime(iccid string,status string, id uint32) (int64, error) {
	captime := model.Captime{
	Id: id,
        Iccid: iccid,
        Status: status,
	}
	return captime.Update(d.engine)
}

func (d *Dao) DeleteCaptime(id uint32) (int64, error) {
	captime := model.Captime{Id: id}
	return captime.Delete(d.engine)
}

