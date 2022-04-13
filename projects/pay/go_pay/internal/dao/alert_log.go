package dao

func (d *Dao) CountAlertLog(iccid string,status int64,) (int, error) {
	alert_log := model.AlertLog{        Iccid: iccid,
        Status: status,
}
	return alert_log.Count(d.engine)
}

func (d *Dao) GetAlertLog(status int64) (*model.AlertLog, error) {
	alert_log := model.AlertLog{Status: status}
	return alert_log.Get(d.engine)
}

func (d *Dao) GetAlertLogList(iccid string,status int64, page, pageSize int) ([]*model.AlertLog, error) {
	alert_log := model.AlertLog{        Iccid: iccid,
        Status: status,
}
	pageOffset := app.GetPageOffset(page, pageSize)
	return alert_log.List(d.engine, pageOffset, pageSize)
}

func (d *Dao) CreateAlertLog(iccid string,) (int64, error) {
	alert_log := model.AlertLog{
        Iccid: iccid,
	}
	return alert_log.Create(d.engine)
}

func (d *Dao) UpdateAlertLog(iccid string, status int64) (int64, error) {
	alert_log := model.AlertLog{
	Status: status,
        Iccid: iccid,
	}
	return alert_log.Update(d.engine)
}

func (d *Dao) DeleteAlertLog(status int64) (int64, error) {
	alert_log := model.AlertLog{Status: status}
	return alert_log.Delete(d.engine)
}

