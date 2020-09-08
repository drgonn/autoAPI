import request from 'umi-request';
import { TableListParams  } from './data.d';

export async function queryDayList(params?: TableListParams) {
  return request('/api/day/list', {
    params,
  });
}

