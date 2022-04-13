package model

import (
  "database/sql"
"fmt"
"strings"
)
type User struct {
    Id uint `json:"id"`
    Uid string `json:"uid"`
    Permission interface{} `json:"permission"`
    UpdatedAt *time.Time `json:"updated_at"`
    CreatedAt *time.Time `json:"created_at"`
}
 
func (o User) TableName() string {
	return "users"
}
 
func (o User) Count(db *sql.DB) (int, error) {
	var count int
	sqlStr := "select count(id) from users "
	var where bool
    if o.Uid != "" {
    if where {
        sqlStr += fmt.Sprintf("and uid = \"%s\" ",o.Uid)
    } else {
        sqlStr += fmt.Sprintf("where uid = \"%s\" ",o.Uid)
        where = true 
        }
    }
	err := db.QueryRow(sqlStr).Scan(&count)
	if err != nil {
		return 0, err
	}
	return count, nil
}

func (o User) List(db *sql.DB, pageOffset, pageSize int) ([]*User, error) {
	var users []*User
	sqlStr := "select  `id`, `uid`, `permission`, `updated_at`, `created_at` from users"
	var where bool
    if o.Uid != "" {
    if where {
        sqlStr += fmt.Sprintf("and uid = \"%s\" ",o.Uid)
    } else {
        sqlStr += fmt.Sprintf("where uid = \"%s\" ",o.Uid)
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
		var user User
		err := rows.Scan(&user.Id, &user.Uid, &user.Permission, &user.UpdatedAt, &user.CreatedAt, )
		if err != nil {
			return nil, err
		}
		users = append(users, &user)
	}
	return users, nil
}

func (o *User) Get(db *sql.DB) (*User, error) {
	sqlStr := "select  `id`, `uid`, `permission`, `updated_at`, `created_at` from users where id = ?"
	err := db.QueryRow(sqlStr, o.Id).Scan(&o.Id, &o.Uid, &o.Permission, &o.UpdatedAt, &o.CreatedAt, )
	if err != nil {
		return nil, err
	}
	return o, nil
}

func (o User) Create(db *sql.DB) (int64, error) {
	sqlStr := "insert into users ( `uid`, `permission`) values ( ?, ?)"
	ret, err := db.Exec(sqlStr, o.Uid, o.Permission)
	if err != nil {
		return -1, err
	}
	user_id, err := ret.LastInsertId()
	return user_id, err
}

func (o User) Update(db *sql.DB) (int64, error) {
	sqlStr := "UPDATE users SET  `uid` = ?, `permission` = ? where id = ?"
	ret, err := db.Exec(sqlStr, o.Uid, o.Permission, o.Id)
	if err != nil {
		return -1, err
	}
	n, err := ret.RowsAffected()
	if err != nil {
		return -1, err
	}
	return n, err
}

func (o User) Delete(db *sql.DB) (int64, error) {
	sqlStr := "delete from users where id = ?"
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
