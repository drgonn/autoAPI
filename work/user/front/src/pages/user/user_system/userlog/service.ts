import request from '@/utils/request';
import { getToken } from '@/utils/authority';
import { TableListParams , TablePutItem } from './data.d';

export async function queryUserlogList(params?: TableListParams) {
  return request(`/user/userlog/list`, {
    params,
  });
}

export async function addUserlog(params: TableListParams) {
  return request(`/user/userlog`, {
    method: 'POST',
    data: {
      ...params,
    },
  });
}

export async function removeUserlog(params: { key: number[] }) {
  return request(`/user/userlog`, {
    method: 'DELETE',
    data: {
      ...params,
      method: 'delete',
    },
  });
}

export async function updateUserlog(params: TablePutItem) {
  return request(`/user/userlog/${params.id}`, {
    method: 'PUT',
    data: {
      ...params,
    },
  });
}
