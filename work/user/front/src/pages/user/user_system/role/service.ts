import request from '@/utils/request';
import { TableListParams , TablePutItem } from './data.d';

export async function queryRoleList(params?: TableListParams) {
  return request(`/user/role/list`, {
    params,
  });
}

export async function addRole(params: TableListParams) {
  return request(`/user/role`, {
    method: 'POST',
    data: {
      ...params,
    },
  });
}

export async function removeRole(params: { key: number[] }) {
  return request(`/user/role`, {
    method: 'DELETE',
    data: {
      ...params,
      method: 'delete',
    },
  });
}

export async function updateRole(params: TablePutItem) {
  return request(`/user/role/${params.id}`, {
    method: 'PUT',
    data: {
      ...params,
    },
  });
}
