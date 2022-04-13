package dao

func (d *Dao) CountRole(name string,) (int, error) {
	role := model.Role{        Name: name,
}
	return role.Count(d.engine)
}

func (d *Dao) GetRole(id uint) (*model.Role, error) {
	role := model.Role{Id: id}
	return role.Get(d.engine)
}

func (d *Dao) GetRoleList(name string, page, pageSize int) ([]*model.Role, error) {
	role := model.Role{        Name: name,
}
	pageOffset := app.GetPageOffset(page, pageSize)
	return role.List(d.engine, pageOffset, pageSize)
}

func (d *Dao) CreateRole(name string,description string,permission interface{},) (int64, error) {
	role := model.Role{
        Name: name,
        Description: description,
        Permission: permission,
	}
	return role.Create(d.engine)
}

func (d *Dao) UpdateRole(name string,description string,permission interface{}, id uint) (int64, error) {
	role := model.Role{
	Id: id,
        Name: name,
        Description: description,
        Permission: permission,
	}
	return role.Update(d.engine)
}

func (d *Dao) DeleteRole(id uint) (int64, error) {
	role := model.Role{Id: id}
	return role.Delete(d.engine)
}

