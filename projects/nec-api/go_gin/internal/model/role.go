package model

import (
  "database/sql"
"fmt"
"strings"
)
type Role struct {
	Id uint `json:"id"`
	Name string `json:"name"`
	Description string `json:"description"`
	Permission interface{} `json:"permission"`
	Updatedat *time.Time `json:"updatedat"`
	Createdat *time.Time `json:"createdat"`
}
 
func (o Role) TableName() string {
	return "roles"
}
 
func (o Role) Count(db *sql.DB) (int, error) {
	var count int
	sqlStr := "select count(id) from roles "
	var where bool
    if o.Name != "" {
    if where {
        sqlStr += fmt.Sprintf("and name = \"%s\" ",o.Name)
    } else {
        sqlStr += fmt.Sprintf("where name = \"%s\" ",o.Name)
        where = true 
        }
    }
	err := db.QueryRow(sqlStr).Scan(&count)
	if err != nil {
		return 0, err
	}
	return count, nil
}

func (o Role) List(db *sql.DB, pageOffset, pageSize int) ([]*Role, error) {
	var roles []*Role
	sqlStr := "select  `id`, `name`, `description`, `permission`, `updatedat`, `createdat` from roles"
	var where bool
    if o.Name != "" {
    if where {
        sqlStr += fmt.Sprintf("and name = \"%s\" ",o.Name)
    } else {
        sqlStr += fmt.Sprintf("where name = \"%s\" ",o.Name)
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
		var role Role
		err := rows.Scan(&role.Id, &role.Name, &role.Description, &role.Permission, &role.Updatedat, &role.Createdat, )
		if err != nil {
			return nil, err
		}
		roles = append(roles, &role)
	}
	return roles, nil
}

func (o *Role) Get(db *sql.DB) (*Role, error) {
	sqlStr := "select  `id`, `name`, `description`, `permission`, `updatedat`, `createdat` from roles where id = ?"
	err := db.QueryRow(sqlStr, o.Id).Scan(&o.Id, &o.Name, &o.Description, &o.Permission, &o.Updatedat, &o.Createdat, )
	if err != nil {
		return nil, err
	}
	return o, nil
}

func (o Role) Create(db *sql.DB) (int64, error) {
var id int
sqlStr := "select id from roles where name=? "
err := db.QueryRow(sqlStr, o.Name).Scan(&id)
if id != 0 {
	err := fmt.Errorf("参数%s重复", o.Name)
	return 0, err
}
	sqlStr := "insert into roles ( `name`, `description`, `permission`) values ( ?, ?, ?)"
	ret, err := db.Exec(sqlStr, o.Name, o.Description, o.Permission)
	if err != nil {
		return -1, err
	}
	role_id, err := ret.LastInsertId()
	return role_id, err
}

func (o Role) Update(db *sql.DB) (int64, error) {
var id int
sqlStr := "select id from roles where name=? "
err := db.QueryRow(sqlStr, o.Name).Scan(&id)
if id != 0 {
	err := fmt.Errorf("参数%s重复", o.Name)
	return 0, err
}
	sqlStr := "UPDATE roles SET  `name` = ?, `description` = ?, `permission` = ? where id = ?"
	ret, err := db.Exec(sqlStr, o.Name, o.Description, o.Permission, o.Id)
	if err != nil {
		return -1, err
	}
	n, err := ret.RowsAffected()
	if err != nil {
		return -1, err
	}
	return n, err
}

func (o Role) Delete(db *sql.DB) (int64, error) {
	sqlStr := "delete from roles where id = ?"
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
