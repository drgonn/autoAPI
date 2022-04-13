package model

import (
  "database/sql"
"fmt"
"strings"
)
type Captime struct {
    Id uint32 `json:"id"`
    Iccid string `json:"iccid"`
    Status string `json:"status"`
    CreatedAt time.Time `json:"created_at"`
}
 
func (o Captime) TableName() string {
	return "captimes"
}
 
func (o Captime) Count(db *sql.DB) (int, error) {
	var count int
	sqlStr := "select count(id) from captimes "
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

func (o Captime) List(db *sql.DB, pageOffset, pageSize int) ([]*Captime, error) {
	var captimes []*Captime
	sqlStr := "select  `id`, `iccid`, `status`, `created_at` from captimes"
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
		var captime Captime
		err := rows.Scan(&captime.Id, &captime.Iccid, &captime.Status, &captime.CreatedAt, )
		if err != nil {
			return nil, err
		}
		captimes = append(captimes, &captime)
	}
	return captimes, nil
}

func (o *Captime) Get(db *sql.DB) (*Captime, error) {
	sqlStr := "select  `id`, `iccid`, `status`, `created_at` from captimes where id = ?"
	err := db.QueryRow(sqlStr, o.Id).Scan(&o.Id, &o.Iccid, &o.Status, &o.CreatedAt, )
	if err != nil {
		return nil, err
	}
	return o, nil
}

func (o Captime) Create(db *sql.DB) (int64, error) {
	sqlStr := "insert into captimes ( `iccid`, `status`) values ( ?, ?)"
	ret, err := db.Exec(sqlStr, o.Iccid, o.Status)
	if err != nil {
		return -1, err
	}
	captime_id, err := ret.LastInsertId()
	return captime_id, err
}

func (o Captime) Update(db *sql.DB) (int64, error) {
	sqlStr := "UPDATE captimes SET  `iccid` = ?, `status` = ? where id = ?"
	ret, err := db.Exec(sqlStr, o.Iccid, o.Status, o.Id)
	if err != nil {
		return -1, err
	}
	n, err := ret.RowsAffected()
	if err != nil {
		return -1, err
	}
	return n, err
}

func (o Captime) Delete(db *sql.DB) (int64, error) {
	sqlStr := "delete from captimes where id = ?"
	ret, err := db.Exec(sqlStr, o.Id)
	if err != nil {
		return -1, err
	}
	n, err := ret.RowsAffected()
	if err != nil {
		return -1, err
	}
	return n, err
}
