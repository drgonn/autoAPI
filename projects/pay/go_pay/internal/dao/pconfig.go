package dao

func (d *Dao) CountPconfig(name string,puid string,value string,) (int, error) {
	pconfig := model.Pconfig{        Name: name,
        Puid: puid,
        Value: value,
}
	return pconfig.Count(d.engine)
}

func (d *Dao) GetPconfig(id uint32) (*model.Pconfig, error) {
	pconfig := model.Pconfig{Id: id}
	return pconfig.Get(d.engine)
}

func (d *Dao) GetPconfigList(name string,puid string,value string, page, pageSize int) ([]*model.Pconfig, error) {
	pconfig := model.Pconfig{        Name: name,
        Puid: puid,
        Value: value,
}
	pageOffset := app.GetPageOffset(page, pageSize)
	return pconfig.List(d.engine, pageOffset, pageSize)
}

func (d *Dao) CreatePconfig(name string,puid string,value string,) (int64, error) {
	pconfig := model.Pconfig{
        Name: name,
        Puid: puid,
        Value: value,
	}
	return pconfig.Create(d.engine)
}

func (d *Dao) UpdatePconfig(name string,puid string,value string, id uint32) (int64, error) {
	pconfig := model.Pconfig{
	Id: id,
        Name: name,
        Puid: puid,
        Value: value,
	}
	return pconfig.Update(d.engine)
}

func (d *Dao) DeletePconfig(id uint32) (int64, error) {
	pconfig := model.Pconfig{Id: id}
	return pconfig.Delete(d.engine)
}

