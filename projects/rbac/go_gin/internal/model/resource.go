package model

import (
  "database/sql"
"fmt"
"strings"
)
type Resource struct {
    Id uint `json:"id"`
    Name string `json:"name"`
    Description string `json:"description"`
    Action interface{} `json:"action"`
    Updatedat *time.Time `json:"updatedat"`
    Createdat *time.Time `json:"createdat"`
}
 
func (o Resource) TableName() string {
	return "resources"
}
 
func (o Resource) Count(db *sql.DB) (int, error) {
	var count int
	sqlStr := "select count(id) from resources "
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

func (o Resource) List(db *sql.DB, pageOffset, pageSize int) ([]*Resource, error) {
	var resources []*Resource
	sqlStr := "select  `id`, `name`, `description`, `action`, `updatedat`, `createdat` from resources"
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
		var resource Resource
		err := rows.Scan(&resource.Id, &resource.Name, &resource.Description, &resource.Action, &resource.Updatedat, &resource.Createdat, )
		if err != nil {
			return nil, err
		}
		resources = append(resources, &resource)
	}
	return resources, nil
}

func (o *Resource) Get(db *sql.DB) (*Resource, error) {
	sqlStr := "select  `id`, `name`, `description`, `action`, `updatedat`, `createdat` from resources where id = ?"
	err := db.QueryRow(sqlStr, o.Id).Scan(&o.Id, &o.Name, &o.Description, &o.Action, &o.Updatedat, &o.Createdat, )
	if err != nil {
		return nil, err
	}
	return o, nil
}

func (o Resource) Create(db *sql.DB) (int64, error) {
var id int
sqlStr := "select id from resources where name=? "
err := db.QueryRow(sqlStr, o.Name).Scan(&id)
if id != 0 {
	err := fmt.Errorf("参数%s重复", o.Name)
	return 0, err
}
	sqlStr := "insert into resources ( `name`, `description`, `action`) values ( ?, ?, ?)"
	ret, err := db.Exec(sqlStr, o.Name, o.Description, o.Action)
	if err != nil {
		return -1, err
	}
	resource_id, err := ret.LastInsertId()
	return resource_id, err
}

func (o Resource) Update(db *sql.DB) (int64, error) {
var id int
sqlStr := "select id from resources where name=? "
err := db.QueryRow(sqlStr, o.Name).Scan(&id)
if id != 0 {
	err := fmt.Errorf("参数%s重复", o.Name)
	return 0, err
}
	sqlStr := "UPDATE resources SET  `description` = ?, `action` = ? where id = ?"
	ret, err := db.Exec(sqlStr, o.Description, o.Action, o.Id)
	if err != nil {
		return -1, err
	}
	n, err := ret.RowsAffected()
	if err != nil {
		return -1, err
	}
	return n, err
}

func (o Resource) Delete(db *sql.DB) (int64, error) {
	sqlStr := "delete from resources where id = ?"
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
