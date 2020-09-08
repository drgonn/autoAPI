import request from 'umi-request';
import { TableListParams  } from './data.d';

export async function queryWorkList(params?: TableListParams) {
  return request('/api/work/list', {
    params,
  });
}

