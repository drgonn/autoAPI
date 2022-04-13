package dao

func (d *Dao) CountTenant(name string,ouid string,describe string,) (int, error) {
	tenant := model.Tenant{        Name: name,
        Ouid: ouid,
        Describe: describe,
}
	return tenant.Count(d.engine)
}

func (d *Dao) GetTenant(ouid string) (*model.Tenant, error) {
	tenant := model.Tenant{Ouid: ouid}
	return tenant.Get(d.engine)
}

func (d *Dao) GetTenantList(name string,ouid string,describe string, page, pageSize int) ([]*model.Tenant, error) {
	tenant := model.Tenant{        Name: name,
        Ouid: ouid,
        Describe: describe,
}
	pageOffset := app.GetPageOffset(page, pageSize)
	return tenant.List(d.engine, pageOffset, pageSize)
}

func (d *Dao) CreateTenant(name string,describe string,) (int64, error) {
	tenant := model.Tenant{
        Name: name,
        Describe: describe,
	}
	return tenant.Create(d.engine)
}

func (d *Dao) UpdateTenant(name string,describe string, ouid string) (int64, error) {
	tenant := model.Tenant{
	Ouid: ouid,
        Name: name,
        Describe: describe,
	}
	return tenant.Update(d.engine)
}

func (d *Dao) DeleteTenant(ouid string) (int64, error) {
	tenant := model.Tenant{Ouid: ouid}
	return tenant.Delete(d.engine)
}

