import os
import sys
sys.path.append(os.path.abspath('.../tools'))

from tools import Tdb

def w_component_index(root,ojson):
	appname = ojson.get('app')
	databases = ojson.get('databases')
	routes = ojson.get('routes') or []
	databases_dir = {i['table'] : i for i in databases}

	for route in routes:
		path = route['path']
		components = route['components']
		for component in components:
			component_name = component['table']
			module = component['module']
			table = databases_dir[component_name]
			table_zh = table.get('zh')
			args = table.get('args')
			crud = table.get('crud')
			os.makedirs(os.path.join(root,f'src/pages/{path}/{component_name.lower()}_{module}'),exist_ok=True)
			initdir = os.path.join(root,f'src/pages/{path}/{component_name.lower()}_{module}/index.tsx')
			com_dir = os.path.join(root,f'src/pages/{path}/{component_name.lower()}_{module}')
			w = open(initdir,'w+')


			w.write(f"""import {{ DownOutlined, PlusOutlined }} from '@ant-design/icons';\n""")
			w.write(f"""import {{ Button, Divider, Dropdown, Menu, message, Input, Form, Modal }} from 'antd';\n""")
			w.write(f"""import React, {{ useState, useRef }} from 'react';\n""")
			w.write(f"""import {{ PageHeaderWrapper }} from '@ant-design/pro-layout';\n""")
			w.write(f"""import ProTable, {{ ProColumns, ActionType }} from '@ant-design/pro-table';\n""")
			w.write(f"""\n""")
			if "post" in crud:
				w.write(f"""import CreateForm from './components/CreateForm';\n""")
				if not os.path.exists(os.path.join(com_dir,'components')):
					os.system(f"cp -r {os.path.join(root,'src/pages/ListTableList/components')}  {com_dir}")

			w.write(f"""import {{ TableListItem }} from './data.d';\n""")
			w.write(f"""import {{ query{component_name}List""")
			if "put" in crud:
				w.write(f""", update{component_name} """)
			if "post" in crud:
				w.write(f""", add{component_name} """)
			if "delete" in crud:
				w.write(f""", remove{component_name} """)
			w.write(f""" }} from './service';\n""")
			w.write(f"""\n""")

			# 添加功能，创建功能
			if "post" in crud:
				w.write(f"""const handleAdd = async (fields: TableListItem) => {{\n""")
				w.write(f"""  const hide = message.loading('正在添加');\n""")
				w.write(f"""  try {{\n""")
				w.write(f"""    const res = await add{component_name}({{ ...fields }});\n""")
				w.write(f"""    if (res.success){{\n""")
				w.write(f"""      hide();\n""")
				w.write(f"""      message.success('添加成功');\n""")
				w.write(f"""      return true;\n""")
				w.write(f"""    }}else{{\n""")
				w.write(f"""      message.error(res.errmsg)\n""")
				w.write(f"""      hide();\n""")
				w.write(f"""      return\n""")
				w.write(f"""    }}\n""")

				w.write(f"""  }} catch (error) {{\n""")
				w.write(f"""    hide();\n""")
				w.write(f"""    message.error('添加失败请重试！');\n""")
				w.write(f"""    return false;\n""")
				w.write(f"""  }}\n""")
				w.write(f"""}};\n""")
				w.write(f"""\n""")



			# 删除功能
			if "delete" in crud:
				w.write(f"""const handleRemove = async (selectedRows: TableListItem[]) => {{\n""")
				w.write(f"""  const hide = message.loading('正在删除');\n""")
				w.write(f"""  if (!selectedRows) return true;\n""")
				w.write(f"""  try {{\n""")
				w.write(f"""    await remove{component_name}({{\n""")
				w.write(f"""      ids: selectedRows.map((row) => row.id),\n""")
				w.write(f"""    }});\n""")
				w.write(f"""    hide();\n""")
				w.write(f"""    message.success('删除成功，即将刷新');\n""")
				w.write(f"""    return true;\n""")
				w.write(f"""  }} catch (error) {{\n""")
				w.write(f"""    hide();\n""")
				w.write(f"""    message.error('删除失败，请重试');\n""")
				w.write(f"""    return false;\n""")
				w.write(f"""  }}\n""")
				w.write(f"""}};\n""")
				w.write(f"""\n""")


			w.write(f"""const TableList: React.FC<{{}}> = () => {{\n""")
			if "post" in crud:
				w.write(f"""  const [createModalVisible, handleModalVisible] = useState<boolean>(false);\n""")
			if "put" in crud:
				w.write(f"""  const [updateModalVisible, handleUpdateModalVisible] = useState<boolean>(false);\n""")
				w.write(f"""  const [stepFormValues, setStepFormValues] = useState({{}});\n""")
				w.write(f"""  const [id,setId]=useState(0)\n""")
				w.write(f"""  const [formvalues,setValues]=useState({{}})\n""")
				w.write(f"""  const [form] = Form.useForm()\n""")
			w.write(f"""  const actionRef = useRef<ActionType>();\n""")

			w.write(f"""  const columns: ProColumns<TableListItem>[] = [\n""")
			parents = table['parents']
			for parent in parents:  # 显示父表中的值
				parentname = parent.get('name')
				show = parent.get("show")
				if show is not None:
					for sho in show:
						s_name = sho['name']
						s_type = sho['type']
						s_mean = sho['mean']
						type = Tdb(s_type).protable_valuetype

						w.write(f"""    {{\n""")
						w.write(f"""      title: '{s_mean}',\n""")
						w.write(f"""      dataIndex: '{parentname.lower()}_{s_name}',\n""")
						w.write(f"""      valueType: '{type}',\n""")
						w.write(f"""    }},\n""")
			args = table['args']
			for arg in args:
				arg_name = arg['name']
				arg_mean = arg['mean']
				type = Tdb(arg['type']).protable_valuetype

				w.write(f"""    {{\n""")
				w.write(f"""      title: '{arg_mean}',\n""")
				w.write(f"""      dataIndex: '{arg_name}',\n""")
				w.write(f"""      valueType: '{type}',\n""")
				if arg.get('sorter'):
					w.write(f"""      sorter: true,\n""")
				w.write(f"""    }},\n""")



			if False:
				w.write(f"""    {{\n""")
				w.write(f"""      title: '规则名称',\n""")
				w.write(f"""      dataIndex: 'name',\n""")
				w.write(f"""      rules: [\n""")
				w.write(f"""        {{\n""")
				w.write(f"""          required: true,\n""")
				w.write(f"""          message: '规则名称为必填项',\n""")
				w.write(f"""        }},\n""")
				w.write(f"""      ],\n""")
				w.write(f"""    }},\n""")
				w.write(f"""    {{\n""")
				w.write(f"""      title: '服务调用次数',\n""")
				w.write(f"""      dataIndex: 'callNo',\n""")
				w.write(f"""      sorter: true,\n""")
				w.write(f"""      hideInForm: true,\n""")
				w.write(f"""      renderText: (val: string) => `${{val}} 万`,\n""")
				w.write(f"""    }},\n""")

				w.write(f"""    {{\n""")
				w.write(f"""      title: '状态',\n""")
				w.write(f"""      dataIndex: 'status',\n""")
				w.write(f"""      hideInForm: true,\n""")
				w.write(f"""      valueEnum: {{\n""")
				w.write(f"""        0: {{ text: '关闭', status: 'Default' }},\n""")
				w.write(f"""        1: {{ text: '运行中', status: 'Processing' }},\n""")
				w.write(f"""        2: {{ text: '已上线', status: 'Success' }},\n""")
				w.write(f"""        3: {{ text: '异常', status: 'Error' }},\n""")
				w.write(f"""      }},\n""")
				w.write(f"""    }},\n""")
				w.write(f"""    {{\n""")
				w.write(f"""      title: '上次调度时间',\n""")
				w.write(f"""      dataIndex: 'updatedAt',\n""")
				w.write(f"""      sorter: true,\n""")
				w.write(f"""      valueType: 'dateTime',\n""")
				w.write(f"""      hideInForm: true,\n""")
				w.write(f"""      renderFormItem: (item, {{ defaultRender, ...rest }}, form) => {{\n""")
				w.write(f"""        const status = form.getFieldValue('status');\n""")
				w.write(f"""        if (`${{status}}` === '0') {{\n""")
				w.write(f"""          return false;\n""")
				w.write(f"""        }}\n""")
				w.write(f"""        if (`${{status}}` === '3') {{\n""")
				w.write(f"""          return <Input {{...rest}} placeholder="请输入异常原因！" />;\n""")
				w.write(f"""        }}\n""")
				w.write(f"""        return defaultRender(item);\n""")
				w.write(f"""      }},\n""")
				w.write(f"""    }},\n""")
			if "put" in crud:
				w.write(f"""    {{\n""")
				w.write(f"""      title: '操作',\n""")
				w.write(f"""      dataIndex: 'option',\n""")
				w.write(f"""      valueType: 'option',\n""")
				w.write(f"""      render: (_, record) => (\n""")
				w.write(f"""        <>\n""")
				w.write(f"""          <a\n""")
				w.write(f"""            onClick={{() => {{\n""")
				w.write(f"""              handleUpdateModalVisible(true);\n""")
				w.write(f"""              setValues(record);\n""")
				w.write(f"""              setId(record.id);\n""")
				w.write(f"""            }}}}\n""")
				w.write(f"""          >\n""")
				w.write(f"""            修改\n""")
				w.write(f"""          </a>\n""")
				w.write(f"""          <Divider type="vertical" />\n""")
				w.write(f"""        </>\n""")
				w.write(f"""      ),\n""")
				w.write(f"""    }},\n""")
			w.write(f"""  ];\n""")
			w.write(f"""\n""")

			if "put" in crud:
				w.write(f"""  const handleUpdate = ()=>{{\n""")
				w.write(f"""    const hide=message.loading('正在提交...')\n""")
				w.write(f"""    form\n""")
				w.write(f"""      .validateFields().then(async(values)=>{{\n""")
				w.write(f"""      try{{\n""")
				w.write(f"""        values.id = id\n""")
				w.write(f"""        const res=await updateDevice({{...values}})\n""")
				w.write(f"""        if(res.success){{\n""")
				w.write(f"""          hide()\n""")
				w.write(f"""          message.success('创建成功！')\n""")
				w.write(f"""          handleUpdateModalVisible(false);\n""")
				w.write(f"""          actionRef.current.reload();\n""")
				w.write(f"""        }}else{{\n""")
				w.write(f"""          message.error(res.errmsg||'请求失败请重试！');\n""")
				w.write(f"""          hide();\n""")
				w.write(f"""          return;\n""")
				w.write(f"""        }}\n""")
				w.write(f"""      }}catch(error){{\n""")
				w.write(f"""        message.error('请求失败请重试！');\n""")
				w.write(f"""        hide();\n""")
				w.write(f"""      }}\n""")
				w.write(f"""    }})\n""")
				w.write(f"""  }}\n""")


			w.write(f"""  return (\n""")
			w.write(f"""    <PageHeaderWrapper>\n""")
			w.write(f"""      <ProTable<TableListItem>\n""")
			w.write(f"""        actionRef={{actionRef}}\n""")
			if False:
				w.write(f"""        headerTitle="查询表格"\n""")
			if "delete" in crud:
				w.write(f"""        rowKey="id"\n""")
				w.write(f"""        rowSelection={{{{}}}}\n""")

			w.write(f"""        toolBarRender={{(action, {{ selectedRows }}) => [\n""")
			if "post" in crud:
				w.write(f"""          <Button type="primary" onClick={{() => handleModalVisible(true)}}>\n""")
				w.write(f"""            <PlusOutlined /> 新建\n""")
				w.write(f"""          </Button>,\n""")
			if "delete" in crud:
				w.write(f"""          selectedRows && selectedRows.length > 0 && (\n""")
				w.write(f"""            <Dropdown\n""")
				w.write(f"""              overlay={{\n""")
				w.write(f"""                <Menu\n""")
				w.write(f"""                  onClick={{async (e) => {{\n""")
				w.write(f"""                    if (e.key === 'remove') {{\n""")
				w.write(f"""                      await handleRemove(selectedRows);\n""")
				w.write(f"""                      action.reload();\n""")
				w.write(f"""                    }}\n""")
				w.write(f"""                  }}}}\n""")
				w.write(f"""                  selectedKeys={{[]}}\n""")
				w.write(f"""                >\n""")
				w.write(f"""                  <Menu.Item key="remove">批量删除</Menu.Item>\n""")
				w.write(f"""                  <Menu.Item key="approval">批量审批</Menu.Item>\n""")
				w.write(f"""                </Menu>\n""")
				w.write(f"""              }}\n""")
				w.write(f"""            >\n""")
				w.write(f"""              <Button>\n""")
				w.write(f"""                批量操作 <DownOutlined />\n""")
				w.write(f"""              </Button>\n""")
				w.write(f"""            </Dropdown>\n""")
				w.write(f"""          ),\n""")
			w.write(f"""        ]}}\n""")
			if False:
				w.write(f"""        tableAlertRender={{({{ selectedRowKeys, selectedRows }}) => (\n""")
				w.write(f"""          <div>\n""")
				w.write(f"""            已选择 <a style={{{{ fontWeight: 600 }}}}>{{selectedRowKeys.length}}</a> 项&nbsp;&nbsp;\n""")
				w.write(f"""            <span>\n""")
				w.write(f"""              服务调用次数总计 {{selectedRows.reduce((pre, item) => pre + item.callNo, 0)}} 万\n""")
				w.write(f"""            </span>\n""")
				w.write(f"""          </div>\n""")
				w.write(f"""        )}}\n""")

			w.write(f"""        request={{(params, sorter, filter) => query{component_name}List({{ ...params, sorter, filter }})}}\n""")
			w.write(f"""        columns={{columns}}\n""")
			w.write(f"""      />\n""")

			if "post" in crud:
				w.write(f"""      <CreateForm onCancel={{() => handleModalVisible(false)}} modalVisible={{createModalVisible}}>\n""")
				w.write(f"""        <ProTable<TableListItem, TableListItem>\n""")
				w.write(f"""          onSubmit={{async (value) => {{\n""")
				w.write(f"""            const success = await handleAdd(value);\n""")
				w.write(f"""            if (success) {{\n""")
				w.write(f"""              handleModalVisible(false);\n""")
				w.write(f"""              if (actionRef.current) {{\n""")
				w.write(f"""                actionRef.current.reload();\n""")
				w.write(f"""              }}\n""")
				w.write(f"""            }}\n""")
				w.write(f"""          }}}}\n""")
				w.write(f"""          rowKey="key"\n""")
				w.write(f"""          type="form"\n""")
				w.write(f"""          columns={{columns}}\n""")
				w.write(f"""          rowSelection={{{{}}}}\n""")
				w.write(f"""        />\n""")
				w.write(f"""      </CreateForm>\n""")
			if "put" in crud:
				w.write(f"""      <Modal\n""")
				w.write(f"""        title="编辑{table_zh}"\n""")
				w.write(f"""        visible={{updateModalVisible}}\n""")
				w.write(f"""        onOk={{handleUpdate}}\n""")
				w.write(f"""        onCancel={{()=>{{handleUpdateModalVisible(false)}}}}\n""")
				w.write(f"""      >\n""")
				w.write(f"""        <Form form={{form}} initialValues={{formvalues}}>\n""")
				for arg in args:
					w.write(f"""          <Form.Item\n""")
					w.write(f"""            labelCol={{{{ span: 5 }}}}\n""")
					w.write(f"""            wrapperCol={{{{ span: 15 }}}}\n""")
					w.write(f"""            name='{arg.get('name')}'\n""")
					w.write(f"""            rules= {{[{{ required: false, message: '请输入名称!' }}]}}\n""")
					w.write(f"""            label="{table_zh}{arg.get('mean')}"\n""")
					w.write(f"""          >\n""")
					w.write(f"""            <Input placeholder="请输入{arg.get('mean')}" />\n""")
					w.write(f"""          </Form.Item>\n""")
				w.write(f"""        </Form>\n""")
				w.write(f"""      </Modal>\n""")

                


			w.write(f"""    </PageHeaderWrapper>\n""")
			w.write(f"""  );\n""")
			w.write(f"""}};\n""")
			w.write(f"""\n""")
			w.write(f"""export default TableList;\n""")
