package dao

func (d *Dao) CountConfig() (int, error) {
	config := model.Config{}
	return config.Count(d.engine)
}

func (d *Dao) GetConfig(id uint) (*model.Config, error) {
	config := model.Config{Id: id}
	return config.Get(d.engine)
}

func (d *Dao) GetConfigList( page, pageSize int) ([]*model.Config, error) {
	config := model.Config{}
	pageOffset := app.GetPageOffset(page, pageSize)
	return config.List(d.engine, pageOffset, pageSize)
}

func (d *Dao) CreateConfig(pure_number bool,case_sensitive bool,special_characters bool,auto_expire uint64,) (int64, error) {
	config := model.Config{
        PureNumber: pure_number,
        CaseSensitive: case_sensitive,
        SpecialCharacters: special_characters,
        AutoExpire: auto_expire,
	}
	return config.Create(d.engine)
}

func (d *Dao) UpdateConfig(pure_number bool,case_sensitive bool,special_characters bool,auto_expire uint64, id uint) (int64, error) {
	config := model.Config{
	Id: id,
        PureNumber: pure_number,
        CaseSensitive: case_sensitive,
        SpecialCharacters: special_characters,
        AutoExpire: auto_expire,
	}
	return config.Update(d.engine)
}

func (d *Dao) DeleteConfig(id uint) (int64, error) {
	config := model.Config{Id: id}
	return config.Delete(d.engine)
}

