package dao

func (d *Dao) CountProject(name string,puid string,ouid string,describe string,) (int, error) {
	project := model.Project{        Name: name,
        Puid: puid,
        Ouid: ouid,
        Describe: describe,
}
	return project.Count(d.engine)
}

func (d *Dao) GetProject(puid string) (*model.Project, error) {
	project := model.Project{Puid: puid}
	return project.Get(d.engine)
}

func (d *Dao) GetProjectList(name string,puid string,ouid string,describe string, page, pageSize int) ([]*model.Project, error) {
	project := model.Project{        Name: name,
        Puid: puid,
        Ouid: ouid,
        Describe: describe,
}
	pageOffset := app.GetPageOffset(page, pageSize)
	return project.List(d.engine, pageOffset, pageSize)
}

func (d *Dao) CreateProject(name string,ouid string,describe string,) (int64, error) {
	project := model.Project{
        Name: name,
        Ouid: ouid,
        Describe: describe,
	}
	return project.Create(d.engine)
}

func (d *Dao) UpdateProject(name string,ouid string,describe string, puid string) (int64, error) {
	project := model.Project{
	Puid: puid,
        Name: name,
        Ouid: ouid,
        Describe: describe,
	}
	return project.Update(d.engine)
}

func (d *Dao) DeleteProject(puid string) (int64, error) {
	project := model.Project{Puid: puid}
	return project.Delete(d.engine)
}

