package model

import (
  "database/sql"
"fmt"
"strings"
)
type AlertLog struct {
    Id uint32 `json:"id"`
    Iccid string `json:"iccid"`
    Status int64 `json:"status"`
    UpdatedAt time.Time `json:"updated_at"`
    CreatedAt time.Time `json:"created_at"`
}
 
func (o AlertLog) TableName() string {
	return "alert_logs"
}
 
func (o AlertLog) Count(db *sql.DB) (int, error) {
	var count int
	sqlStr := "select count(id) from alert_logs "
	var where bool
    if o.Iccid != "" {
    if where {
        sqlStr += fmt.Sprintf("and iccid = \"%s\" ",o.Iccid)
    } else {
        sqlStr += fmt.Sprintf("where iccid = \"%s\" ",o.Iccid)
        where = true 
        }
    }
    if o.Status != "" {
    if where {
        sqlStr += fmt.Sprintf("and status = \"%s\" ",o.Status)
    } else {
        sqlStr += fmt.Sprintf("where status = \"%s\" ",o.Status)
        where = true 
        }
    }
	err := db.QueryRow(sqlStr).Scan(&count)
	if err != nil {
		return 0, err
	}
	return count, nil
}

func (o AlertLog) List(db *sql.DB, pageOffset, pageSize int) ([]*AlertLog, error) {
	var alert_logs []*AlertLog
	sqlStr := "select  `id`, `iccid`, `status`, `updated_at`, `created_at` from alert_logs"
	var where bool
    if o.Iccid != "" {
    if where {
        sqlStr += fmt.Sprintf("and iccid = \"%s\" ",o.Iccid)
    } else {
        sqlStr += fmt.Sprintf("where iccid = \"%s\" ",o.Iccid)
        where = true 
        }
    }
    if o.Status != "" {
    if where {
        sqlStr += fmt.Sprintf("and status = \"%s\" ",o.Status)
    } else {
        sqlStr += fmt.Sprintf("where status = \"%s\" ",o.Status)
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
		var alert_log AlertLog
		err := rows.Scan(&alert_log.Id, &alert_log.Iccid, &alert_log.Status, &alert_log.UpdatedAt, &alert_log.CreatedAt, )
		if err != nil {
			return nil, err
		}
		alert_logs = append(alert_logs, &alert_log)
	}
	return alert_logs, nil
}

func (o *AlertLog) Get(db *sql.DB) (*AlertLog, error) {
	sqlStr := "select  `id`, `iccid`, `status`, `updated_at`, `created_at` from alert_logs where status = ?"
	err := db.QueryRow(sqlStr, o.Status).Scan(&o.Id, &o.Iccid, &o.Status, &o.UpdatedAt, &o.CreatedAt, )
	if err != nil {
		return nil, err
	}
	return o, nil
}

func (o AlertLog) Create(db *sql.DB) (int64, error) {
	status := uuid.NewV4().String()
	sqlStr := "insert into alert_logs ( `iccid`,`status`) values ( ?, ?)"
	ret, err := db.Exec(sqlStr, o.Iccid, status)
	if err != nil {
		return -1, err
	}
	alert_log_id, err := ret.LastInsertId()
	return alert_log_id, err
}

func (o AlertLog) Update(db *sql.DB) (int64, error) {
	sqlStr := "UPDATE alert_logs SET  `iccid` = ? where status = ?"
	ret, err := db.Exec(sqlStr, o.Iccid, o.Status)
	if err != nil {
		return -1, err
	}
	n, err := ret.RowsAffected()
	if err != nil {
		return -1, err
	}
	return n, err
}

func (o AlertLog) Delete(db *sql.DB) (int64, error) {
	sqlStr := "delete from alert_logs where status = ?"
	ret, err := db.Exec(sqlStr, o.Status)
	if err != nil {
		return -1, err
	}
	n, err := ret.RowsAffected()
	if err != nil {
		return -1, err
	}
	return n, err
}
