import { DownOutlined, PlusOutlined } from '@ant-design/icons';
import { Button, Divider, Dropdown, Menu, message, Input } from 'antd';
import React, { useState, useRef } from 'react';
import { PageHeaderWrapper } from '@ant-design/pro-layout';
import ProTable, { ProColumns, ActionType } from '@ant-design/pro-table';

import { TableListItem } from './data.d';
import { queryDayList } from './service';

const TableList: React.FC<{}> = () => {
  const actionRef = useRef<ActionType>();
  const columns: ProColumns<TableListItem>[] = [
    {
      title: '股名',
      dataIndex: 'stock_name',
      valueType: 'text',
    },
    {
      title: '交易日期',
      dataIndex: 'trade_date',
      valueType: 'date',
    },
    {
      title: '当日收盘价',
      dataIndex: 'close',
      valueType: 'digit',
    },
    {
      title: '换手率（%）',
      dataIndex: 'turnover_rate',
      valueType: 'digit',
    },
    {
      title: '换手率（自由流通股）',
      dataIndex: 'turnover_rate_f',
      valueType: 'digit',
    },
    {
      title: '量比',
      dataIndex: 'volume_ratio',
      valueType: 'digit',
    },
    {
      title: '市盈率（总市值/净利润，亏损的PE为空）',
      dataIndex: 'pe',
      valueType: 'digit',
    },
    {
      title: '市盈率（TTM，亏损的PE为空）',
      dataIndex: 'pe_ttm',
      valueType: 'digit',
    },
    {
      title: '市净率（总市值/净资产）',
      dataIndex: 'pb',
      valueType: 'digit',
    },
    {
      title: '市销率',
      dataIndex: 'ps',
      valueType: 'digit',
    },
    {
      title: '市销率（TTM）',
      dataIndex: 'ps_ttm',
      valueType: 'digit',
      sorter: true,
    },
    {
      title: '股息率（%）',
      dataIndex: 'dv_ratio',
      valueType: 'digit',
      sorter: true,
    },
    {
      title: '股息率（TTM）（%）',
      dataIndex: 'dv_ttm',
      valueType: 'digit',
      sorter: true,
    },
    {
      title: '总股本（万股）',
      dataIndex: 'total_share',
      valueType: 'digit',
      sorter: true,
    },
    {
      title: '流通股本（万股）',
      dataIndex: 'float_share',
      valueType: 'digit',
      sorter: true,
    },
    {
      title: '自由流通股本（万）',
      dataIndex: 'free_share',
      valueType: 'digit',
      sorter: true,
    },
    {
      title: '总市值（万元）',
      dataIndex: 'total_mv',
      valueType: 'digit',
      sorter: true,
    },
    {
      title: '流通市值（万元）',
      dataIndex: 'circ_mv',
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
        request={(params, sorter, filter) => queryDayList({ ...params, sorter, filter })}
        columns={columns}
      />
    </PageHeaderWrapper>
  );
};

export default TableList;
