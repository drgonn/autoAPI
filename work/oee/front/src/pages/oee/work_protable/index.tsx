import { DownOutlined, PlusOutlined } from '@ant-design/icons';
import { Button, Divider, Dropdown, Menu, message, Input } from 'antd';
import React, { useState, useRef } from 'react';
import { PageHeaderWrapper } from '@ant-design/pro-layout';
import ProTable, { ProColumns, ActionType } from '@ant-design/pro-table';

import { TableListItem } from './data.d';
import { queryWorkList } from './service';

const TableList: React.FC<{}> = () => {
  const actionRef = useRef<ActionType>();
  const columns: ProColumns<TableListItem>[] = [
    {
      title: '股名',
      dataIndex: 'device_name',
      valueType: 'text',
    },
    {
      title: '开始时间',
      dataIndex: 'start_time',
      valueType: 'dateTime',
    },
    {
      title: '结束时间',
      dataIndex: 'end_time',
      valueType: 'dateTime',
    },
    {
      title: '运行时间（秒）',
      dataIndex: 'seconds',
      valueType: 'digit',
    },
    {
      title: '工作类型',
      dataIndex: 'type',
      valueType: 'digit',
    },
  ];

  return (
    <PageHeaderWrapper>
      <ProTable<TableListItem>
        actionRef={actionRef}
        toolBarRender={(action, { selectedRows }) => [
        ]}
        request={(params, sorter, filter) => queryWorkList({ ...params, sorter, filter })}
        columns={columns}
      />
    </PageHeaderWrapper>
  );
};

export default TableList;
