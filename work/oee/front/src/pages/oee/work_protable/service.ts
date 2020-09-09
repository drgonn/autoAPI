import request from 'umi-request';
import { TableListParams , TablePutItem } from './data.d';

export async function queryWorkList(params?: TableListParams) {
  return request('/api/work/list', {
    params,
  });
}

export async function addWork(params: TableListParams) {
  return request('/api/work', {
    method: 'POST',
    data: {
      ...params,
    },
  });
}

export async function removeWork(params: { key: number[] }) {
  return request('/api/work', {
    method: 'DELETE',
    data: {
      ...params,
      method: 'delete',
    },
  });
}

export async function updateWork(params: TablePutItem) {
  return request(`/api/work/${params.id}`, {
    method: 'PUT',
    data: {
      ...params,
    },
  });
}
