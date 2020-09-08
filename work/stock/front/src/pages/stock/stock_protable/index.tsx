import { DownOutlined, PlusOutlined } from '@ant-design/icons';
import { Button, Divider, Dropdown, Menu, message, Input } from 'antd';
import React, { useState, useRef } from 'react';
import { PageHeaderWrapper } from '@ant-design/pro-layout';
import ProTable, { ProColumns, ActionType } from '@ant-design/pro-table';

import { TableListItem } from './data.d';
import { queryStockList } from './service';

const TableList: React.FC<{}> = () => {
  const actionRef = useRef<ActionType>();
  const columns: ProColumns<TableListItem>[] = [
    {
      title: '代号',
      dataIndex: 'ts_code',
      valueType: 'text',
    },
    {
      title: '六位代号',
      dataIndex: 'symbol',
      valueType: 'text',
    },
    {
      title: '名称',
      dataIndex: 'name',
      valueType: 'text',
    },
    {
      title: '地区',
      dataIndex: 'area',
      valueType: 'text',
    },
    {
      title: '行业',
      dataIndex: 'industry',
      valueType: 'text',
    },
    {
      title: '全名',
      dataIndex: 'fullname',
      valueType: 'text',
    },
    {
      title: '英文名',
      dataIndex: 'enname',
      valueType: 'text',
    },
    {
      title: '交易板块',
      dataIndex: 'market',
      valueType: 'text',
    },
    {
      title: '交易所代码',
      dataIndex: 'exchange',
      valueType: 'text',
    },
    {
      title: '交易货币',
      dataIndex: 'curr_type',
      valueType: 'text',
    },
    {
      title: '上市状态： L上市 D退市 P暂停上市',
      dataIndex: 'list_status',
      valueType: 'text',
    },
    {
      title: '上市日期',
      dataIndex: 'list_date',
      valueType: 'date',
      sorter: true,
    },
    {
      title: '退市日期',
      dataIndex: 'delist_date',
      valueType: 'date',
    },
    {
      title: '是否沪深港通标的',
      dataIndex: 'is_hs',
      valueType: 'text',
    },
    {
      title: '现价',
      dataIndex: 'price',
      valueType: 'digit',
      sorter: true,
    },
    {
      title: '流通市值（万元）',
      dataIndex: 'circ_mv',
      valueType: 'digit',
      sorter: true,
    },
    {
      title: '市盈率（总市值/净利润，亏损的PE为空）',
      dataIndex: 'pe',
      valueType: 'digit',
      sorter: true,
    },
  ];

  return (
    <PageHeaderWrapper>
      <ProTable<TableListItem>
        actionRef={actionRef}
        toolBarRender={(action, { selectedRows }) => [
        ]}
        request={(params, sorter, filter) => queryStockList({ ...params, sorter, filter })}
        columns={columns}
      />
    </PageHeaderWrapper>
  );
};

export default TableList;
