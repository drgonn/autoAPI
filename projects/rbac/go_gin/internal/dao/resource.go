package dao

func (d *Dao) CountResource(name string,) (int, error) {
	resource := model.Resource{        Name: name,
}
	return resource.Count(d.engine)
}

func (d *Dao) GetResource(id uint) (*model.Resource, error) {
	resource := model.Resource{Id: id}
	return resource.Get(d.engine)
}

func (d *Dao) GetResourceList(name string, page, pageSize int) ([]*model.Resource, error) {
	resource := model.Resource{        Name: name,
}
	pageOffset := app.GetPageOffset(page, pageSize)
	return resource.List(d.engine, pageOffset, pageSize)
}

func (d *Dao) CreateResource(name string,description string,action interface{},) (int64, error) {
	resource := model.Resource{
        Name: name,
        Description: description,
        Action: action,
	}
	return resource.Create(d.engine)
}

func (d *Dao) UpdateResource(description string,action interface{}, id uint) (int64, error) {
	resource := model.Resource{
	Id: id,
        Description: description,
        Action: action,
	}
	return resource.Update(d.engine)
}

func (d *Dao) DeleteResource(id uint) (int64, error) {
	resource := model.Resource{Id: id}
	return resource.Delete(d.engine)
}

