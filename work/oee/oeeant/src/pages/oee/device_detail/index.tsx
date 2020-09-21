import React, {useEffect, useRef, useState} from 'react';
import {PageHeaderWrapper} from '@ant-design/pro-layout';
import {
  Chart,
  Interval,
  Axis,
  Tooltip,
  Coordinate,
  Legend,
  View,
  Annotation,
} from "bizcharts";
import { DataView } from '@antv/data-set';
import DataSet from "@antv/data-set";
import { queryWorktimeList, updateWorktime , addWorktime , removeWorktime  } from "../worktime/service"

import ProCard from '@ant-design/pro-card';
import {Card, Descriptions} from 'antd';
import ProTable from '@ant-design/pro-table';
import moment from 'moment';


const operationTabList = [

  {
    key: 'WorkTime',
    tab: '工作时间分析',
  },
  {
    key: 'DeviceDetail',
    tab: '驾动率',
  },

  {
    key: 'Status',
    tab: '故障率',
  },
];

const data = [
  { value: 251, type: '大事例一', name: '子事例一' },
  { value: 1048, type: '大事例一', name: '子事例二' },
  { value: 610, type: '大事例二', name: '子事例三' },
  { value: 434, type: '大事例二', name: '子事例四' },
  { value: 335, type: '大事例三', name: '子事例五' },
  { value: 250, type: '大事例三', name: '子事例六' },
];

const modify_worktime = (data) => {
  let chart_data = []
  for (let o of data) {
    let type1
    let name1
    switch (o.type) {
      case 1:
        type1 = "停止时间";
        name1 = "休息时间";
        break
      case 2:
        type1 = "负荷时间";
        name1 = "日常管理时间";
        break
      case 3:
        name1 = "停机时间";
        type1 = "负荷时间";
        break
      case 4:
        type1 = "负荷时间";
        name1 = "运转时间";
        break
      case 5:
        name1 = "计划停止时间";
        type1 = "负荷时间";
        break
      case 6:
        type1 = "负荷时间";
        name1 = "日常管理时间";
        break
    }
    chart_data.push({ type: type1, value: o.seconds, name:name1});
  }
  return chart_data;
}

const cadv = (data) => {
  // 通过 DataSet 计算百分比
  const chartdata = modify_worktime(data)
  const dv = new DataView();
  console.log(chartdata)
  dv.source(chartdata).transform({
    type: 'percent',
    field: 'value',
    dimension: 'type',
    as: 'percent',
  });
  console.log(dv)
  return dv
}
const cadv1 = (data) => {
  // 通过 DataSet 计算百分比
  const chartdata = modify_worktime(data)
  const dv1 = new DataView();
  console.log(chartdata)
  dv1.source(chartdata).transform({
    type: 'percent',
    field: 'value',
    dimension: 'name',
    as: 'percent',
  });
  return dv1
}

export default (e) => {
  const [detail, setDetail] = useState({});
  const [worktime, setworktime] = useState([]);
  const [statedv, setdv    ] = useState([]);
  const [statedv1, setdv1    ] = useState([]);
  const [tabkey, setTabkey] = useState('WorkTime');
  const [flowdata, setFlowdata] = useState([]);
  const [sorter, setSorter] = useState('');
  const actionRef = useRef();
  const { id } = e.location.query;
  const month = new Date().getMonth() + 1;
  const monthtitle = `${month} 月流量套餐使用详情表`;
  const onOperationTabChange = (key) => {
    setTabkey(key);
  };
  useEffect(() => {
    async function fetchData() {
      const wtime = await queryWorktimeList({device_id:id,pageSize:70});
      setworktime(wtime.data);
      setdv(cadv(wtime.data).rows)
      setdv1(cadv1(wtime.data).rows)


      // setDetail(data);
      // const list = [];
      // const flowlist = await queryFlowdata({ iccid: data.iccid, month });
      // if (flowlist.length) {
      //   flowlist.reverse().map((item) => {
      //     list.push({
      //       x: moment(item.date).format('MM-DD'),
      //       y: item.dataUsage,
      //     });
      //   });
      // }
      // setFlowdata(list);
    }
    fetchData();
  }, []);

  console.log(statedv1)
  // console.log(statedv.slice(1))
  // console.log(statedv.slice(1).pop())
  // console.log(statedv.length>0 && statedv.slice(1).pop().value)


  const contentList = {
    DeviceDetail: (
      <Descriptions bordered>
        <Descriptions.Item label="编号"> {worktime.length} </Descriptions.Item>
        <Descriptions.Item label="总流量"> ddd M </Descriptions.Item>
        <Descriptions.Item label="剩余量"> dd M </Descriptions.Item>
        <Descriptions.Item label="本月总量">sdd M </Descriptions.Item>
      </Descriptions>
    ),
    WorkTime: (
    <ProCard style={{ marginTop: 3 }}  ghost>
      <ProCard bordered layout="center">
        <Descriptions bordered>
          <Descriptions.Item label="停止时间" span={3}> {statedv.length>0 && statedv[1].value}s </Descriptions.Item>
          <Descriptions.Item label="休息时间" span={3}> {statedv.length>0 && statedv[1].value}s </Descriptions.Item>
          <Descriptions.Item label="负荷时间" span={3}> {statedv.length>0 && statedv[0].value}s </Descriptions.Item>
          <Descriptions.Item label="运转时间" span={1}>{statedv1.length>0 && statedv1[2].value}s</Descriptions.Item>
          <Descriptions.Item label="日常管理" span={1}>{statedv1.length>0 && statedv1[1].value}s</Descriptions.Item>
          <Descriptions.Item label="停机时间" span={1}>{statedv1.length>0 && statedv1[0].value}s</Descriptions.Item>
        </Descriptions>
      </ProCard>
      <ProCard colSpan="40%" bordered>
        <Chart
          height={400}
          data={statedv}
          autoFit
          scale={{
            percent: {
              formatter: (val) => {
                val = `${(val * 100).toFixed(2)}%`;
                return val;
              },
            }
          }}
        >
          <Coordinate type="theta" radius={0.5} />
          <Axis visible={false} />
          <Legend visible={false} />
          <Tooltip showTitle={false} />
          <Interval
            position="percent"
            adjust="stack"
            color="type"
            element-highlight
            style={{
              lineWidth: 1,
              stroke: '#fff',
            }}
            label={['type', {
              offset: -15,
            }]}
          />
          <View data={statedv1}>
            <Coordinate type="theta" radius={0.75} innerRadius={0.5 / 0.75} />
            <Interval
              position="percent"
              adjust="stack"
              color={['name', ['#BAE7FF', '#7FC9FE', '#71E3E3', '#ABF5F5', '#8EE0A1', '#BAF5C4']]}
              element-highlight
              style={{
                lineWidth: 1,
                stroke: '#fff',
              }}
              label="name"
            />
          </View>
        </Chart>
      </ProCard>
    </ProCard>



    ),
  };

  return (
    <PageHeaderWrapper>
      <Card
        tabList={operationTabList}
        onTabChange={(key) => {
          onOperationTabChange(key);
        }}
      >
        {contentList[tabkey]}
      </Card>
    </PageHeaderWrapper>
  );
};
