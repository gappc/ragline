export interface Query {
  query: string;
  filter?: unknown[];
  top_k?: number[];
}

export interface QueryBody {
  queries: Query[];
}

export interface DocumentSource {
  file: string;
  pages: number[];
}
