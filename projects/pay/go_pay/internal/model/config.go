package model

import (
  "database/sql"
"fmt"
"strings"
)
type Config struct {
    Id uint `json:"id"`
    Length uint `json:"length"`
    PureNumber bool `json:"pure_number"`
    CaseSensitive bool `json:"case_sensitive"`
    SpecialCharacters bool `json:"special_characters"`
    AutoExpire uint64 `json:"auto_expire"`
}
 
func (o Config) TableName() string {
	return "configs"
}
 
func (o Config) Count(db *sql.DB) (int, error) {
	var count int
	sqlStr := "select count(id) from configs "
	var where bool
	err := db.QueryRow(sqlStr).Scan(&count)
	if err != nil {
		return 0, err
	}
	return count, nil
}

func (o Config) List(db *sql.DB, pageOffset, pageSize int) ([]*Config, error) {
	var configs []*Config
	sqlStr := "select  `id`, `length`, `pure_number`, `case_sensitive`, `special_characters`, `auto_expire` from configs"
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
		var config Config
		err := rows.Scan(&config.Id, &config.Length, &config.PureNumber, &config.CaseSensitive, &config.SpecialCharacters, &config.AutoExpire, )
		if err != nil {
			return nil, err
		}
		configs = append(configs, &config)
	}
	return configs, nil
}

func (o *Config) Get(db *sql.DB) (*Config, error) {
	sqlStr := "select  `id`, `length`, `pure_number`, `case_sensitive`, `special_characters`, `auto_expire` from configs where id = ?"
	err := db.QueryRow(sqlStr, o.Id).Scan(&o.Id, &o.Length, &o.PureNumber, &o.CaseSensitive, &o.SpecialCharacters, &o.AutoExpire, )
	if err != nil {
		return nil, err
	}
	return o, nil
}

func (o Config) Create(db *sql.DB) (int64, error) {
	sqlStr := "insert into configs ( `pure_number`, `case_sensitive`, `special_characters`, `auto_expire`) values ( ?, ?, ?, ?)"
	ret, err := db.Exec(sqlStr, o.PureNumber, o.CaseSensitive, o.SpecialCharacters, o.AutoExpire)
	if err != nil {
		return -1, err
	}
	config_id, err := ret.LastInsertId()
	return config_id, err
}

func (o Config) Update(db *sql.DB) (int64, error) {
	sqlStr := "UPDATE configs SET  `pure_number` = ?, `case_sensitive` = ?, `special_characters` = ?, `auto_expire` = ? where id = ?"
	ret, err := db.Exec(sqlStr, o.PureNumber, o.CaseSensitive, o.SpecialCharacters, o.AutoExpire, o.Id)
	if err != nil {
		return -1, err
	}
	n, err := ret.RowsAffected()
	if err != nil {
		return -1, err
	}
	return n, err
}

func (o Config) Delete(db *sql.DB) (int64, error) {
	sqlStr := "delete from configs where id = ?"
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
