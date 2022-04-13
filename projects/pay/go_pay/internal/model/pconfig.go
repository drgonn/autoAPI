package model

import (
  "database/sql"
"fmt"
"strings"
)
type Pconfig struct {
    Id uint32 `json:"id"`
    Name string `json:"name"`
    Puid string `json:"puid"`
    Value string `json:"value"`
    UpdatedAt time.Time `json:"updated_at"`
    CreatedAt time.Time `json:"created_at"`
}
 
func (o Pconfig) TableName() string {
	return "pconfigs"
}
 
func (o Pconfig) Count(db *sql.DB) (int, error) {
	var count int
	sqlStr := "select count(id) from pconfigs "
	var where bool
    if o.Name != "" {
    if where {
        sqlStr += fmt.Sprintf("and name = \"%s\" ",o.Name)
    } else {
        sqlStr += fmt.Sprintf("where name = \"%s\" ",o.Name)
        where = true 
        }
    }
    if o.Puid != "" {
    if where {
        sqlStr += fmt.Sprintf("and puid = \"%s\" ",o.Puid)
    } else {
        sqlStr += fmt.Sprintf("where puid = \"%s\" ",o.Puid)
        where = true 
        }
    }
    if o.Value != "" {
    if where {
        sqlStr += fmt.Sprintf("and value = \"%s\" ",o.Value)
    } else {
        sqlStr += fmt.Sprintf("where value = \"%s\" ",o.Value)
        where = true 
        }
    }
	err := db.QueryRow(sqlStr).Scan(&count)
	if err != nil {
		return 0, err
	}
	return count, nil
}

func (o Pconfig) List(db *sql.DB, pageOffset, pageSize int) ([]*Pconfig, error) {
	var pconfigs []*Pconfig
	sqlStr := "select  `id`, `name`, `puid`, `value`, `updated_at`, `created_at` from pconfigs"
	var where bool
    if o.Name != "" {
    if where {
        sqlStr += fmt.Sprintf("and name = \"%s\" ",o.Name)
    } else {
        sqlStr += fmt.Sprintf("where name = \"%s\" ",o.Name)
        where = true 
        }
    }
    if o.Puid != "" {
    if where {
        sqlStr += fmt.Sprintf("and puid = \"%s\" ",o.Puid)
    } else {
        sqlStr += fmt.Sprintf("where puid = \"%s\" ",o.Puid)
        where = true 
        }
    }
    if o.Value != "" {
    if where {
        sqlStr += fmt.Sprintf("and value = \"%s\" ",o.Value)
    } else {
        sqlStr += fmt.Sprintf("where value = \"%s\" ",o.Value)
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
		var pconfig Pconfig
		err := rows.Scan(&pconfig.Id, &pconfig.Name, &pconfig.Puid, &pconfig.Value, &pconfig.UpdatedAt, &pconfig.CreatedAt, )
		if err != nil {
			return nil, err
		}
		pconfigs = append(pconfigs, &pconfig)
	}
	return pconfigs, nil
}

func (o *Pconfig) Get(db *sql.DB) (*Pconfig, error) {
	sqlStr := "select  `id`, `name`, `puid`, `value`, `updated_at`, `created_at` from pconfigs where id = ?"
	err := db.QueryRow(sqlStr, o.Id).Scan(&o.Id, &o.Name, &o.Puid, &o.Value, &o.UpdatedAt, &o.CreatedAt, )
	if err != nil {
		return nil, err
	}
	return o, nil
}

func (o Pconfig) Create(db *sql.DB) (int64, error) {
	sqlStr := "insert into pconfigs ( `name`, `puid`, `value`) values ( ?, ?, ?)"
	ret, err := db.Exec(sqlStr, o.Name, o.Puid, o.Value)
	if err != nil {
		return -1, err
	}
	pconfig_id, err := ret.LastInsertId()
	return pconfig_id, err
}

func (o Pconfig) Update(db *sql.DB) (int64, error) {
	sqlStr := "UPDATE pconfigs SET  `name` = ?, `puid` = ?, `value` = ? where id = ?"
	ret, err := db.Exec(sqlStr, o.Name, o.Puid, o.Value, o.Id)
	if err != nil {
		return -1, err
	}
	n, err := ret.RowsAffected()
	if err != nil {
		return -1, err
	}
	return n, err
}

func (o Pconfig) Delete(db *sql.DB) (int64, error) {
	sqlStr := "delete from pconfigs where id = ?"
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
