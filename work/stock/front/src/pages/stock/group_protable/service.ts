import request from 'umi-request';
import { TableListParams , TablePutItem } from './data.d';

export async function queryGroupList(params?: TableListParams) {
  return request('/api/group/list', {
    params,
  });
}

export async function addGroup(params: TableListParams) {
  return request('/api/group', {
    method: 'POST',
    data: {
      ...params,
    },
  });
}

export async function removeGroup(params: { key: number[] }) {
  return request('/api/group', {
    method: 'DELETE',
    data: {
      ...params,
      method: 'delete',
    },
  });
}

export async function updateGroup(params: TablePutItem) {
  return request(`/api/group/${params.id}`, {
    method: 'PUT',
    data: {
      ...params,
    },
  });
}
