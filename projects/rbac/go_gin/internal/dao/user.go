package dao

func (d *Dao) CountUser(uid string,) (int, error) {
	user := model.User{        Uid: uid,
}
	return user.Count(d.engine)
}

func (d *Dao) GetUser(id uint) (*model.User, error) {
	user := model.User{Id: id}
	return user.Get(d.engine)
}

func (d *Dao) GetUserList(uid string, page, pageSize int) ([]*model.User, error) {
	user := model.User{        Uid: uid,
}
	pageOffset := app.GetPageOffset(page, pageSize)
	return user.List(d.engine, pageOffset, pageSize)
}

func (d *Dao) CreateUser(uid string,permission interface{},) (int64, error) {
	user := model.User{
        Uid: uid,
        Permission: permission,
	}
	return user.Create(d.engine)
}

func (d *Dao) UpdateUser(uid string,permission interface{}, id uint) (int64, error) {
	user := model.User{
	Id: id,
        Uid: uid,
        Permission: permission,
	}
	return user.Update(d.engine)
}

func (d *Dao) DeleteUser(id uint) (int64, error) {
	user := model.User{Id: id}
	return user.Delete(d.engine)
}

