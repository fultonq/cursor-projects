export interface IsolationHeaders {
  tenantId: string;
  region: 'AMER' | 'EMEA' | 'APAC';
  correlationId?: string;
}
