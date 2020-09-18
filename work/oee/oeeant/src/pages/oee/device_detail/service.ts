import request from 'umi-request';
import { TableListParams , TablePutItem } from './data.d';

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

export async function removeDevice(params: { key: number[] }) {
  return request('/api/device', {
    method: 'DELETE',
    data: {
      ...params,
      method: 'delete',
    },
  });
}

export async function updateDevice(params: TablePutItem) {
  return request(`/api/device/${params.id}`, {
    method: 'PUT',
    data: {
      ...params,
    },
  });
}
