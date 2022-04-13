package model

import (
  "database/sql"
"fmt"
"strings"
)
type Tenant struct {
    Id uint32 `json:"id"`
    Name string `json:"name"`
    Ouid string `json:"ouid"`
    Describe string `json:"describe"`
    UpdatedAt time.Time `json:"updated_at"`
    CreatedAt time.Time `json:"created_at"`
}
 
func (o Tenant) TableName() string {
	return "tenants"
}
 
func (o Tenant) Count(db *sql.DB) (int, error) {
	var count int
	sqlStr := "select count(id) from tenants "
	var where bool
    if o.Name != "" {
    if where {
        sqlStr += fmt.Sprintf("and name = \"%s\" ",o.Name)
    } else {
        sqlStr += fmt.Sprintf("where name = \"%s\" ",o.Name)
        where = true 
        }
    }
    if o.Ouid != "" {
    if where {
        sqlStr += fmt.Sprintf("and ouid = \"%s\" ",o.Ouid)
    } else {
        sqlStr += fmt.Sprintf("where ouid = \"%s\" ",o.Ouid)
        where = true 
        }
    }
    if o.Describe != "" {
    if where {
        sqlStr += fmt.Sprintf("and describe = \"%s\" ",o.Describe)
    } else {
        sqlStr += fmt.Sprintf("where describe = \"%s\" ",o.Describe)
        where = true 
        }
    }
	err := db.QueryRow(sqlStr).Scan(&count)
	if err != nil {
		return 0, err
	}
	return count, nil
}

func (o Tenant) List(db *sql.DB, pageOffset, pageSize int) ([]*Tenant, error) {
	var tenants []*Tenant
	sqlStr := "select  `id`, `name`, `ouid`, `describe`, `updated_at`, `created_at` from tenants"
	var where bool
    if o.Name != "" {
    if where {
        sqlStr += fmt.Sprintf("and name = \"%s\" ",o.Name)
    } else {
        sqlStr += fmt.Sprintf("where name = \"%s\" ",o.Name)
        where = true 
        }
    }
    if o.Ouid != "" {
    if where {
        sqlStr += fmt.Sprintf("and ouid = \"%s\" ",o.Ouid)
    } else {
        sqlStr += fmt.Sprintf("where ouid = \"%s\" ",o.Ouid)
        where = true 
        }
    }
    if o.Describe != "" {
    if where {
        sqlStr += fmt.Sprintf("and describe = \"%s\" ",o.Describe)
    } else {
        sqlStr += fmt.Sprintf("where describe = \"%s\" ",o.Describe)
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
		var tenant Tenant
		err := rows.Scan(&tenant.Id, &tenant.Name, &tenant.Ouid, &tenant.Describe, &tenant.UpdatedAt, &tenant.CreatedAt, )
		if err != nil {
			return nil, err
		}
		tenants = append(tenants, &tenant)
	}
	return tenants, nil
}

func (o *Tenant) Get(db *sql.DB) (*Tenant, error) {
	sqlStr := "select  `id`, `name`, `ouid`, `describe`, `updated_at`, `created_at` from tenants where ouid = ?"
	err := db.QueryRow(sqlStr, o.Ouid).Scan(&o.Id, &o.Name, &o.Ouid, &o.Describe, &o.UpdatedAt, &o.CreatedAt, )
	if err != nil {
		return nil, err
	}
	return o, nil
}

func (o Tenant) Create(db *sql.DB) (int64, error) {
var id int
sqlStr := "select id from tenants where name=? "
err := db.QueryRow(sqlStr, o.Name).Scan(&id)
if id != 0 {
	err := fmt.Errorf("参数%s重复", o.Name)
	return 0, err
}
	ouid := uuid.NewV4().String()
	sqlStr := "insert into tenants ( `name`, `describe`,`ouid`) values ( ?, ?, ?)"
	ret, err := db.Exec(sqlStr, o.Name, o.Describe, ouid)
	if err != nil {
		return -1, err
	}
	tenant_id, err := ret.LastInsertId()
	return tenant_id, err
}

func (o Tenant) Update(db *sql.DB) (int64, error) {
var id int
sqlStr := "select id from tenants where name=? "
err := db.QueryRow(sqlStr, o.Name).Scan(&id)
if id != 0 {
	err := fmt.Errorf("参数%s重复", o.Name)
	return 0, err
}
	sqlStr := "UPDATE tenants SET  `name` = ?, `describe` = ? where ouid = ?"
	ret, err := db.Exec(sqlStr, o.Name, o.Describe, o.Ouid)
	if err != nil {
		return -1, err
	}
	n, err := ret.RowsAffected()
	if err != nil {
		return -1, err
	}
	return n, err
}

func (o Tenant) Delete(db *sql.DB) (int64, error) {
	sqlStr := "delete from tenants where ouid = ?"
	ret, err := db.Exec(sqlStr, o.Ouid)
	if err != nil {
		return -1, err
	}
	n, err := ret.RowsAffected()
	if err != nil {
		return -1, err
	}
	return n, err
}
