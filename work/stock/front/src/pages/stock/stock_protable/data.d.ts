export interface TableListItem {
  id?: number;
  ts_code: string;
  symbol: string;
  name: string;
  area: string;
  industry: string;
  fullname: string;
  enname: string;
  market: string;
  exchange: string;
  curr_type: string;
  list_status: string;
  list_date: Date;
  delist_date: Date;
  is_hs: string;
  price: number;
  circ_mv: number;
  pe: number;
}

export interface TableListPagination {
  total: number;
  pageSize: number;
  current: number;
}

export interface TableListData {
  list: TableListItem[];
  pagination: Partial<TableListPagination>;
}

export interface TableListParams {
  status?: string;
  name?: string;
  desc?: string;
  key?: number;
  pageSize?: number;
  currentPage?: number;
  filter?: { [key: string]: any[] };
  sorter?: { [key: string]: any };
}
