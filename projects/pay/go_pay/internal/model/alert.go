package model

import (
  "database/sql"
"fmt"
"strings"
)
type Alert struct {
    Id uint32 `json:"id"`
    Name string `json:"name"`
    Webhook string `json:"webhook"`
    Emails  `json:"emails"`
    Flow float `json:"flow"`
    All bool `json:"all"`
    Enable bool `json:"enable"`
    Description string `json:"description"`
    Event int `json:"event"`
    UpdatedAt time.Time `json:"updated_at"`
    CreatedAt time.Time `json:"created_at"`
}
 
func (o Alert) TableName() string {
	return "alerts"
}
 
func (o Alert) Count(db *sql.DB) (int, error) {
	var count int
	sqlStr := "select count(id) from alerts "
	var where bool
    if o.Name != "" {
    if where {
        sqlStr += fmt.Sprintf("and name = \"%s\" ",o.Name)
    } else {
        sqlStr += fmt.Sprintf("where name = \"%s\" ",o.Name)
        where = true 
        }
    }
    if o.Webhook != "" {
    if where {
        sqlStr += fmt.Sprintf("and webhook = \"%s\" ",o.Webhook)
    } else {
        sqlStr += fmt.Sprintf("where webhook = \"%s\" ",o.Webhook)
        where = true 
        }
    }
    if o.Emails != "" {
    if where {
        sqlStr += fmt.Sprintf("and emails = \"%s\" ",o.Emails)
    } else {
        sqlStr += fmt.Sprintf("where emails = \"%s\" ",o.Emails)
        where = true 
        }
    }
    if o.Flow != "" {
    if where {
        sqlStr += fmt.Sprintf("and flow = \"%s\" ",o.Flow)
    } else {
        sqlStr += fmt.Sprintf("where flow = \"%s\" ",o.Flow)
        where = true 
        }
    }
    if o.All != "" {
    if where {
        sqlStr += fmt.Sprintf("and all = \"%s\" ",o.All)
    } else {
        sqlStr += fmt.Sprintf("where all = \"%s\" ",o.All)
        where = true 
        }
    }
    if o.Enable != "" {
    if where {
        sqlStr += fmt.Sprintf("and enable = \"%s\" ",o.Enable)
    } else {
        sqlStr += fmt.Sprintf("where enable = \"%s\" ",o.Enable)
        where = true 
        }
    }
    if o.Description != "" {
    if where {
        sqlStr += fmt.Sprintf("and description = \"%s\" ",o.Description)
    } else {
        sqlStr += fmt.Sprintf("where description = \"%s\" ",o.Description)
        where = true 
        }
    }
    if o.Event != "" {
    if where {
        sqlStr += fmt.Sprintf("and event = \"%s\" ",o.Event)
    } else {
        sqlStr += fmt.Sprintf("where event = \"%s\" ",o.Event)
        where = true 
        }
    }
	err := db.QueryRow(sqlStr).Scan(&count)
	if err != nil {
		return 0, err
	}
	return count, nil
}

func (o Alert) List(db *sql.DB, pageOffset, pageSize int) ([]*Alert, error) {
	var alerts []*Alert
	sqlStr := "select  `id`, `name`, `webhook`, `emails`, `flow`, `all`, `enable`, `description`, `event`, `updated_at`, `created_at` from alerts"
	var where bool
    if o.Name != "" {
    if where {
        sqlStr += fmt.Sprintf("and name = \"%s\" ",o.Name)
    } else {
        sqlStr += fmt.Sprintf("where name = \"%s\" ",o.Name)
        where = true 
        }
    }
    if o.Webhook != "" {
    if where {
        sqlStr += fmt.Sprintf("and webhook = \"%s\" ",o.Webhook)
    } else {
        sqlStr += fmt.Sprintf("where webhook = \"%s\" ",o.Webhook)
        where = true 
        }
    }
    if o.Emails != "" {
    if where {
        sqlStr += fmt.Sprintf("and emails = \"%s\" ",o.Emails)
    } else {
        sqlStr += fmt.Sprintf("where emails = \"%s\" ",o.Emails)
        where = true 
        }
    }
    if o.Flow != "" {
    if where {
        sqlStr += fmt.Sprintf("and flow = \"%s\" ",o.Flow)
    } else {
        sqlStr += fmt.Sprintf("where flow = \"%s\" ",o.Flow)
        where = true 
        }
    }
    if o.All != "" {
    if where {
        sqlStr += fmt.Sprintf("and all = \"%s\" ",o.All)
    } else {
        sqlStr += fmt.Sprintf("where all = \"%s\" ",o.All)
        where = true 
        }
    }
    if o.Enable != "" {
    if where {
        sqlStr += fmt.Sprintf("and enable = \"%s\" ",o.Enable)
    } else {
        sqlStr += fmt.Sprintf("where enable = \"%s\" ",o.Enable)
        where = true 
        }
    }
    if o.Description != "" {
    if where {
        sqlStr += fmt.Sprintf("and description = \"%s\" ",o.Description)
    } else {
        sqlStr += fmt.Sprintf("where description = \"%s\" ",o.Description)
        where = true 
        }
    }
    if o.Event != "" {
    if where {
        sqlStr += fmt.Sprintf("and event = \"%s\" ",o.Event)
    } else {
        sqlStr += fmt.Sprintf("where event = \"%s\" ",o.Event)
        where = true 
        }
    }
	if pageOffset >= 0 && pageSize > 0 {
		sqlStr += fmt.Sprintf(" limit %d offset %d", pageSize, pageOffset)
	}
	rows, err := db.Query(sqlStr)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	for rows.Next() {
		var alert Alert
		err := rows.Scan(&alert.Id, &alert.Name, &alert.Webhook, &alert.Emails, &alert.Flow, &alert.All, &alert.Enable, &alert.Description, &alert.Event, &alert.UpdatedAt, &alert.CreatedAt, )
		if err != nil {
			return nil, err
		}
		alerts = append(alerts, &alert)
	}
	return alerts, nil
}

func (o *Alert) Get(db *sql.DB) (*Alert, error) {
	sqlStr := "select  `id`, `name`, `webhook`, `emails`, `flow`, `all`, `enable`, `description`, `event`, `updated_at`, `created_at` from alerts where webhook = ?"
	err := db.QueryRow(sqlStr, o.Webhook).Scan(&o.Id, &o.Name, &o.Webhook, &o.Emails, &o.Flow, &o.All, &o.Enable, &o.Description, &o.Event, &o.UpdatedAt, &o.CreatedAt, )
	if err != nil {
		return nil, err
	}
	return o, nil
}

func (o Alert) Create(db *sql.DB) (int64, error) {
var id int
sqlStr := "select id from alerts where name=? "
err := db.QueryRow(sqlStr, o.Name).Scan(&id)
if id != 0 {
	err := fmt.Errorf("参数%s重复", o.Name)
	return 0, err
}
	webhook := uuid.NewV4().String()
	sqlStr := "insert into alerts ( `name`, `webhook`, `emails`, `flow`, `all`, `enable`, `description`, `event`,`webhook`) values ( ?, ?, ?, ?, ?, ?, ?, ?, ?)"
	ret, err := db.Exec(sqlStr, o.Name, o.Webhook, o.Emails, o.Flow, o.All, o.Enable, o.Description, o.Event, webhook)
	if err != nil {
		return -1, err
	}
	alert_id, err := ret.LastInsertId()
	return alert_id, err
}

func (o Alert) Update(db *sql.DB) (int64, error) {
var id int
sqlStr := "select id from alerts where name=? "
err := db.QueryRow(sqlStr, o.Name).Scan(&id)
if id != 0 {
	err := fmt.Errorf("参数%s重复", o.Name)
	return 0, err
}
	sqlStr := "UPDATE alerts SET  `name` = ?, `webhook` = ?, `emails` = ?, `flow` = ?, `all` = ?, `enable` = ?, `description` = ?, `event` = ? where webhook = ?"
	ret, err := db.Exec(sqlStr, o.Name, o.Webhook, o.Emails, o.Flow, o.All, o.Enable, o.Description, o.Event, o.Webhook)
	if err != nil {
		return -1, err
	}
	n, err := ret.RowsAffected()
	if err != nil {
		return -1, err
	}
	return n, err
}

func (o Alert) Delete(db *sql.DB) (int64, error) {
	sqlStr := "delete from alerts where webhook = ?"
	ret, err := db.Exec(sqlStr, o.Webhook)
	if err != nil {
		return -1, err
	}
	n, err := ret.RowsAffected()
	if err != nil {
		return -1, err
	}
	return n, err
}
