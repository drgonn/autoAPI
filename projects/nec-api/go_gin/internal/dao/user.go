package dao

func (d *Dao) CountUser() (int, error) {
	user := model.User{}
	return user.Count(d.engine)
}

func (d *Dao) GetUser(uid string) (*model.User, error) {
	user := model.User{Uid: uid}
	return user.Get(d.engine)
}

func (d *Dao) GetUserList( page, pageSize int) ([]*model.User, error) {
	user := model.User{}
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

func (d *Dao) UpdateUser(permission interface{}, uid string) (int64, error) {
	user := model.User{
	Uid: uid,
        Permission: permission,
	}
	return user.Update(d.engine)
}

func (d *Dao) DeleteUser(uid string) (int64, error) {
	user := model.User{Uid: uid}
	return user.Delete(d.engine)
}

