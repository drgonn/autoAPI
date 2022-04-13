package dao

func (d *Dao) CountHikv() (int, error) {
	hikv := model.Hikv{}
	return hikv.Count(d.engine)
}

func (d *Dao) GetHikv(id uint) (*model.Hikv, error) {
	hikv := model.Hikv{Id: id}
	return hikv.Get(d.engine)
}

func (d *Dao) GetHikvList( page, pageSize int) ([]*model.Hikv, error) {
	hikv := model.Hikv{}
	pageOffset := app.GetPageOffset(page, pageSize)
	return hikv.List(d.engine, pageOffset, pageSize)
}

func (d *Dao) CreateHikv(name string,app_key string,app_secret string,hikv_serial string,validate_code string,cap_minute uint,) (int64, error) {
	hikv := model.Hikv{
        Name: name,
        AppKey: app_key,
        AppSecret: app_secret,
        HikvSerial: hikv_serial,
        ValidateCode: validate_code,
        CapMinute: cap_minute,
	}
	return hikv.Create(d.engine)
}

func (d *Dao) UpdateHikv(name string,app_key string,app_secret string,hikv_serial string,validate_code string,cap_minute uint, id uint) (int64, error) {
	hikv := model.Hikv{
	Id: id,
        Name: name,
        AppKey: app_key,
        AppSecret: app_secret,
        HikvSerial: hikv_serial,
        ValidateCode: validate_code,
        CapMinute: cap_minute,
	}
	return hikv.Update(d.engine)
}

func (d *Dao) DeleteHikv(id uint) (int64, error) {
	hikv := model.Hikv{Id: id}
	return hikv.Delete(d.engine)
}

