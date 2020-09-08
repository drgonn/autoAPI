import request from 'umi-request';
import { TableListParams  } from './data.d';

export async function queryDeviceList(params?: TableListParams) {
  return request('/api/device/list', {
    params,
  });
}

