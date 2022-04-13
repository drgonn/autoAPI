package model

import (
  "database/sql"
"fmt"
"strings"
)
type Project struct {
    Id uint32 `json:"id"`
    Name string `json:"name"`
    Puid string `json:"puid"`
    Ouid string `json:"ouid"`
    Describe string `json:"describe"`
    UpdatedAt time.Time `json:"updated_at"`
    CreatedAt time.Time `json:"created_at"`
}
 
func (o Project) TableName() string {
	return "projects"
}
 
func (o Project) Count(db *sql.DB) (int, error) {
	var count int
	sqlStr := "select count(id) from projects "
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

func (o Project) List(db *sql.DB, pageOffset, pageSize int) ([]*Project, error) {
	var projects []*Project
	sqlStr := "select  `id`, `name`, `puid`, `ouid`, `describe`, `updated_at`, `created_at` from projects"
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
		var project Project
		err := rows.Scan(&project.Id, &project.Name, &project.Puid, &project.Ouid, &project.Describe, &project.UpdatedAt, &project.CreatedAt, )
		if err != nil {
			return nil, err
		}
		projects = append(projects, &project)
	}
	return projects, nil
}

func (o *Project) Get(db *sql.DB) (*Project, error) {
	sqlStr := "select  `id`, `name`, `puid`, `ouid`, `describe`, `updated_at`, `created_at` from projects where puid = ?"
	err := db.QueryRow(sqlStr, o.Puid).Scan(&o.Id, &o.Name, &o.Puid, &o.Ouid, &o.Describe, &o.UpdatedAt, &o.CreatedAt, )
	if err != nil {
		return nil, err
	}
	return o, nil
}

func (o Project) Create(db *sql.DB) (int64, error) {
	puid := uuid.NewV4().String()
	sqlStr := "insert into projects ( `name`, `ouid`, `describe`,`puid`) values ( ?, ?, ?, ?)"
	ret, err := db.Exec(sqlStr, o.Name, o.Ouid, o.Describe, puid)
	if err != nil {
		return -1, err
	}
	project_id, err := ret.LastInsertId()
	return project_id, err
}

func (o Project) Update(db *sql.DB) (int64, error) {
	sqlStr := "UPDATE projects SET  `name` = ?, `ouid` = ?, `describe` = ? where puid = ?"
	ret, err := db.Exec(sqlStr, o.Name, o.Ouid, o.Describe, o.Puid)
	if err != nil {
		return -1, err
	}
	n, err := ret.RowsAffected()
	if err != nil {
		return -1, err
	}
	return n, err
}

func (o Project) Delete(db *sql.DB) (int64, error) {
	sqlStr := "delete from projects where puid = ?"
	ret, err := db.Exec(sqlStr, o.Puid)
	if err != nil {
		return -1, err
	}
	n, err := ret.RowsAffected()
	if err != nil {
		return -1, err
	}
	return n, err
}
