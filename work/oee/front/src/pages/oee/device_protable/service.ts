import request from 'umi-request';
import { TableListParams  } from './data.d';

export async function queryDeviceList(params?: TableListParams) {
  return request('/api/device/list', {
    params,
  });
}

export async function addDevice(params: TableListParams) {
  return request('/api/device', {
    method: 'POST',
    data: {
      ...params,
    },
  });
}

