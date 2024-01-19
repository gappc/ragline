export interface Query {
  query: string;
  filter?: unknown[];
  top_k?: number[];
}

export interface QueryBody {
  queries: Query[];
}
