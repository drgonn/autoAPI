import request from 'umi-request';
import { TableListParams  } from './data.d';

export async function queryStockList(params?: TableListParams) {
  return request('/api/stock/list', {
    params,
  });
}

