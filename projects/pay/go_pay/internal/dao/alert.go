package dao

func (d *Dao) CountAlert(name string,webhook string,emails ,flow float,all bool,enable bool,description string,event int,) (int, error) {
	alert := model.Alert{        Name: name,
        Webhook: webhook,
        Emails: emails,
        Flow: flow,
        All: all,
        Enable: enable,
        Description: description,
        Event: event,
}
	return alert.Count(d.engine)
}

func (d *Dao) GetAlert(webhook string) (*model.Alert, error) {
	alert := model.Alert{Webhook: webhook}
	return alert.Get(d.engine)
}

func (d *Dao) GetAlertList(name string,webhook string,emails ,flow float,all bool,enable bool,description string,event int, page, pageSize int) ([]*model.Alert, error) {
	alert := model.Alert{        Name: name,
        Webhook: webhook,
        Emails: emails,
        Flow: flow,
        All: all,
        Enable: enable,
        Description: description,
        Event: event,
}
	pageOffset := app.GetPageOffset(page, pageSize)
	return alert.List(d.engine, pageOffset, pageSize)
}

func (d *Dao) CreateAlert(name string,webhook string,emails ,flow float,all bool,enable bool,description string,event int,) (int64, error) {
	alert := model.Alert{
        Name: name,
        Webhook: webhook,
        Emails: emails,
        Flow: flow,
        All: all,
        Enable: enable,
        Description: description,
        Event: event,
	}
	return alert.Create(d.engine)
}

func (d *Dao) UpdateAlert(name string,webhook string,emails ,flow float,all bool,enable bool,description string,event int, webhook string) (int64, error) {
	alert := model.Alert{
	Webhook: webhook,
        Name: name,
        Webhook: webhook,
        Emails: emails,
        Flow: flow,
        All: all,
        Enable: enable,
        Description: description,
        Event: event,
	}
	return alert.Update(d.engine)
}

func (d *Dao) DeleteAlert(webhook string) (int64, error) {
	alert := model.Alert{Webhook: webhook}
	return alert.Delete(d.engine)
}

