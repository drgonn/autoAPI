import request from '@/utils/request';
import { TableListParams , TablePutItem } from './data';

export async function queryUserList(params?: TableListParams) {
  return request(`/user/list`, {
    params,
  });
}

export async function addUser(params: TableListParams) {
  return request(`/user/user`, {
    method: 'POST',
    data: {
      ...params,
    },
  });
}

export async function removeUser(params: { key: number[] }) {
  return request(`/user/user`, {
    method: 'DELETE',
    data: {
      ...params,
      method: 'delete',
    },
  });
}

export async function updateUser(params: TablePutItem) {
  return request(`/user/user/${params.id}`, {
    method: 'PUT',
    data: {
      ...params,
    },
  });
}
