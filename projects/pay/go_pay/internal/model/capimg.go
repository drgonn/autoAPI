package model

import (
  "database/sql"
"fmt"
"strings"
)
type Capimg struct {
    Id uint32 `json:"id"`
    HikvUrl string `json:"hikv_url"`
    CreatedAt time.Time `json:"created_at"`
}
 
func (o Capimg) TableName() string {
	return "capimgs"
}
 
func (o Capimg) Count(db *sql.DB) (int, error) {
	var count int
	sqlStr := "select count(id) from capimgs "
	var where bool
	err := db.QueryRow(sqlStr).Scan(&count)
	if err != nil {
		return 0, err
	}
	return count, nil
}

func (o Capimg) List(db *sql.DB, pageOffset, pageSize int) ([]*Capimg, error) {
	var capimgs []*Capimg
	sqlStr := "select  `id`, `hikv_url`, `created_at` from capimgs"
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
		var capimg Capimg
		err := rows.Scan(&capimg.Id, &capimg.HikvUrl, &capimg.CreatedAt, )
		if err != nil {
			return nil, err
		}
		capimgs = append(capimgs, &capimg)
	}
	return capimgs, nil
}

func (o *Capimg) Get(db *sql.DB) (*Capimg, error) {
	sqlStr := "select  `id`, `hikv_url`, `created_at` from capimgs where id = ?"
	err := db.QueryRow(sqlStr, o.Id).Scan(&o.Id, &o.HikvUrl, &o.CreatedAt, )
	if err != nil {
		return nil, err
	}
	return o, nil
}

func (o Capimg) Create(db *sql.DB) (int64, error) {
	sqlStr := "insert into capimgs () values ()"
	ret, err := db.Exec(sqlStr,)
	if err != nil {
		return -1, err
	}
	capimg_id, err := ret.LastInsertId()
	return capimg_id, err
}

func (o Capimg) Update(db *sql.DB) (int64, error) {
	sqlStr := "UPDATE capimgs SET  `hikv_url` = ? where id = ?"
	ret, err := db.Exec(sqlStr, o.HikvUrl, o.Id)
	if err != nil {
		return -1, err
	}
	n, err := ret.RowsAffected()
	if err != nil {
		return -1, err
	}
	return n, err
}

func (o Capimg) Delete(db *sql.DB) (int64, error) {
	sqlStr := "delete from capimgs where id = ?"
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
