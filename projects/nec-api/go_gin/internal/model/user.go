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
	Updatedat *time.Time `json:"updatedat"`
	Createdat *time.Time `json:"createdat"`
}
 
func (o User) TableName() string {
	return "users"
}
 
func (o User) Count(db *sql.DB) (int, error) {
	var count int
	sqlStr := "select count(id) from users "
	var where bool
	err := db.QueryRow(sqlStr).Scan(&count)
	if err != nil {
		return 0, err
	}
	return count, nil
}

func (o User) List(db *sql.DB, pageOffset, pageSize int) ([]*User, error) {
	var users []*User
	sqlStr := "select  `id`, `uid`, `permission`, `updatedat`, `createdat` from users"
	var where bool
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
		err := rows.Scan(&user.Id, &user.Uid, &user.Permission, &user.Updatedat, &user.Createdat, )
		if err != nil {
			return nil, err
		}
		users = append(users, &user)
	}
	return users, nil
}

func (o *User) Get(db *sql.DB) (*User, error) {
	sqlStr := "select  `id`, `uid`, `permission`, `updatedat`, `createdat` from users where uid = ?"
	err := db.QueryRow(sqlStr, o.Uid).Scan(&o.Id, &o.Uid, &o.Permission, &o.Updatedat, &o.Createdat, )
	if err != nil {
		return nil, err
	}
	return o, nil
}

func (o User) Create(db *sql.DB) (int64, error) {
var id int
sqlStr := "select id from users where uid=? "
err := db.QueryRow(sqlStr, o.Uid).Scan(&id)
if id != 0 {
	err := fmt.Errorf("参数%s重复", o.Uid)
	return 0, err
}
	uid := uuid.NewV4().String()
	sqlStr := "insert into users ( `uid`, `permission`,`uid`) values ( ?, ?, ?)"
	ret, err := db.Exec(sqlStr, o.Uid, o.Permission, uid)
	if err != nil {
		return -1, err
	}
	user_id, err := ret.LastInsertId()
	return user_id, err
}

func (o User) Update(db *sql.DB) (int64, error) {
var id int
sqlStr := "select id from users where uid=? "
err := db.QueryRow(sqlStr, o.Uid).Scan(&id)
if id != 0 {
	err := fmt.Errorf("参数%s重复", o.Uid)
	return 0, err
}
	sqlStr := "UPDATE users SET  `permission` = ? where uid = ?"
	ret, err := db.Exec(sqlStr, o.Permission, o.Uid)
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
	sqlStr := "delete from users where uid = ?"
	ret, err := db.Exec(sqlStr, o.Uid)
	if err != nil {
		return -1, err
	}
	n, err := ret.RowsAffected()
	if err != nil {
		return -1, err
	}
	return n, err
}
