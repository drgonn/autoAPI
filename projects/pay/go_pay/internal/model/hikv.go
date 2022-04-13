package model

import (
  "database/sql"
"fmt"
"strings"
)
type Hikv struct {
    Id uint `json:"id"`
    Name string `json:"name"`
    AppKey string `json:"app_key"`
    AppSecret string `json:"app_secret"`
    HikvSerial string `json:"hikv_serial"`
    ValidateCode string `json:"validate_code"`
    CapMinute uint `json:"cap_minute"`
    UpdatedAt time.Time `json:"updated_at"`
    CreatedAt time.Time `json:"created_at"`
}
 
func (o Hikv) TableName() string {
	return "hikvs"
}
 
func (o Hikv) Count(db *sql.DB) (int, error) {
	var count int
	sqlStr := "select count(id) from hikvs "
	var where bool
	err := db.QueryRow(sqlStr).Scan(&count)
	if err != nil {
		return 0, err
	}
	return count, nil
}

func (o Hikv) List(db *sql.DB, pageOffset, pageSize int) ([]*Hikv, error) {
	var hikvs []*Hikv
	sqlStr := "select  `id`, `name`, `app_key`, `app_secret`, `hikv_serial`, `validate_code`, `cap_minute`, `updated_at`, `created_at` from hikvs"
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
		var hikv Hikv
		err := rows.Scan(&hikv.Id, &hikv.Name, &hikv.AppKey, &hikv.AppSecret, &hikv.HikvSerial, &hikv.ValidateCode, &hikv.CapMinute, &hikv.UpdatedAt, &hikv.CreatedAt, )
		if err != nil {
			return nil, err
		}
		hikvs = append(hikvs, &hikv)
	}
	return hikvs, nil
}

func (o *Hikv) Get(db *sql.DB) (*Hikv, error) {
	sqlStr := "select  `id`, `name`, `app_key`, `app_secret`, `hikv_serial`, `validate_code`, `cap_minute`, `updated_at`, `created_at` from hikvs where id = ?"
	err := db.QueryRow(sqlStr, o.Id).Scan(&o.Id, &o.Name, &o.AppKey, &o.AppSecret, &o.HikvSerial, &o.ValidateCode, &o.CapMinute, &o.UpdatedAt, &o.CreatedAt, )
	if err != nil {
		return nil, err
	}
	return o, nil
}

func (o Hikv) Create(db *sql.DB) (int64, error) {
	sqlStr := "insert into hikvs ( `name`, `app_key`, `app_secret`, `hikv_serial`, `validate_code`, `cap_minute`) values ( ?, ?, ?, ?, ?, ?)"
	ret, err := db.Exec(sqlStr, o.Name, o.AppKey, o.AppSecret, o.HikvSerial, o.ValidateCode, o.CapMinute)
	if err != nil {
		return -1, err
	}
	hikv_id, err := ret.LastInsertId()
	return hikv_id, err
}

func (o Hikv) Update(db *sql.DB) (int64, error) {
	sqlStr := "UPDATE hikvs SET  `name` = ?, `app_key` = ?, `app_secret` = ?, `hikv_serial` = ?, `validate_code` = ?, `cap_minute` = ? where id = ?"
	ret, err := db.Exec(sqlStr, o.Name, o.AppKey, o.AppSecret, o.HikvSerial, o.ValidateCode, o.CapMinute, o.Id)
	if err != nil {
		return -1, err
	}
	n, err := ret.RowsAffected()
	if err != nil {
		return -1, err
	}
	return n, err
}

func (o Hikv) Delete(db *sql.DB) (int64, error) {
	sqlStr := "delete from hikvs where id = ?"
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
