import { DownOutlined, PlusOutlined } from '@ant-design/icons';
import { Button, Divider, Dropdown, Menu, message, Input, Form, Modal } from 'antd';
import React, { useState, useRef } from 'react';
import { PageHeaderWrapper } from '@ant-design/pro-layout';
import ProTable, { ProColumns, ActionType } from '@ant-design/pro-table';

import CreateForm from './components/CreateForm';
import { TableListItem } from './data.d';
import { queryDeviceList, updateDevice , addDevice , removeDevice  } from './service';

const handleAdd = async (fields: TableListItem) => {
  const hide = message.loading('正在添加');
  try {
    const res = await addDevice({ ...fields });
    if (res.success){
      hide();
      message.success('添加成功');
      return true;
    }else{
      message.error(res.errmsg)
      hide();
      return
    }
  } catch (error) {
    hide();
    message.error('添加失败请重试！');
    return false;
  }
};

const handleRemove = async (selectedRows: TableListItem[]) => {
  const hide = message.loading('正在删除');
  if (!selectedRows) return true;
  try {
    await removeDevice({
      ids: selectedRows.map((row) => row.id),
    });
    hide();
    message.success('删除成功，即将刷新');
    return true;
  } catch (error) {
    hide();
    message.error('删除失败，请重试');
    return false;
  }
};

const TableList: React.FC<{}> = () => {
  const [createModalVisible, handleModalVisible] = useState<boolean>(false);
  const [updateModalVisible, handleUpdateModalVisible] = useState<boolean>(false);
  const [stepFormValues, setStepFormValues] = useState({});
  const [id,setId]=useState(0)
  const [formvalues,setValues]=useState({})
  const [form] = Form.useForm()
  const actionRef = useRef<ActionType>();
  const columns: ProColumns<TableListItem>[] = [
    {
      title: '代号',
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
      title: '操作',
      dataIndex: 'option',
      valueType: 'option',
      render: (_, record) => (
        <>
          <a
            onClick={() => {
              handleUpdateModalVisible(true);
              setValues(record);
              setId(record.id);
            }}
          >
            修改
          </a>
          <Divider type="vertical" />
        </>
      ),
    },
  ];

  const handleUpdate = ()=>{
    const hide=message.loading('正在提交...')
    form
      .validateFields().then(async(values)=>{
      try{
        values.id = id
        const res=await updateDevice({...values})
        if(res.success){
          hide()
          message.success('创建成功！')
          handleUpdateModalVisible(false);
          actionRef.current.reload();
        }else{
          message.error(res.errmsg||'请求失败请重试！');
          hide();
          return;
        }
      }catch(error){
        message.error('请求失败请重试！');
        hide();
      }
    })
  }
  return (
    <PageHeaderWrapper>
      <ProTable<TableListItem>
        actionRef={actionRef}
        rowKey="id"
        rowSelection={{}}
        toolBarRender={(action, { selectedRows }) => [
          <Button type="primary" onClick={() => handleModalVisible(true)}>
            <PlusOutlined /> 新建
          </Button>,
          selectedRows && selectedRows.length > 0 && (
            <Dropdown
              overlay={
                <Menu
                  onClick={async (e) => {
                    if (e.key === 'remove') {
                      await handleRemove(selectedRows);
                      action.reload();
                    }
                  }}
                  selectedKeys={[]}
                >
                  <Menu.Item key="remove">批量删除</Menu.Item>
                  <Menu.Item key="approval">批量审批</Menu.Item>
                </Menu>
              }
            >
              <Button>
                批量操作 <DownOutlined />
              </Button>
            </Dropdown>
          ),
        ]}
        request={(params, sorter, filter) => queryDeviceList({ ...params, sorter, filter })}
        columns={columns}
      />
      <CreateForm onCancel={() => handleModalVisible(false)} modalVisible={createModalVisible}>
        <ProTable<TableListItem, TableListItem>
          onSubmit={async (value) => {
            const success = await handleAdd(value);
            if (success) {
              handleModalVisible(false);
              if (actionRef.current) {
                actionRef.current.reload();
              }
            }
          }}
          rowKey="key"
          type="form"
          columns={columns}
          rowSelection={{}}
        />
      </CreateForm>
      <Modal
        title="编辑设备"
        visible={updateModalVisible}
        onOk={handleUpdate}
        onCancel={()=>{handleUpdateModalVisible(false)}}
      >
        <Form form={form} initialValues={formvalues}>
          <Form.Item
            labelCol={{ span: 5 }}
            wrapperCol={{ span: 15 }}
            name='symbol'
            rules= {[{ required: false, message: '请输入名称!' }]}
            label="设备代号"
          >
            <Input placeholder="请输入代号" />
          </Form.Item>
          <Form.Item
            labelCol={{ span: 5 }}
            wrapperCol={{ span: 15 }}
            name='name'
            rules= {[{ required: false, message: '请输入名称!' }]}
            label="设备名称"
          >
            <Input placeholder="请输入名称" />
          </Form.Item>
          <Form.Item
            labelCol={{ span: 5 }}
            wrapperCol={{ span: 15 }}
            name='area'
            rules= {[{ required: false, message: '请输入名称!' }]}
            label="设备地区"
          >
            <Input placeholder="请输入地区" />
          </Form.Item>
        </Form>
      </Modal>
    </PageHeaderWrapper>
  );
};

export default TableList;
