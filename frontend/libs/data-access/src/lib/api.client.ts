import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { IsolationHeaders } from './isolation.headers';

/** Gateway-only HTTP. Apps must not call services directly. */
@Injectable({ providedIn: 'root' })
export class ApiClient {
  private readonly http = inject(HttpClient);
  private readonly base = '/api/v1';

  get<T>(path: string, isolation: IsolationHeaders) {
    return this.http.get<T>(`${this.base}${path}`, { headers: this.headers(isolation) });
  }

  private headers(isolation: IsolationHeaders): HttpHeaders {
    return new HttpHeaders({
      'X-Tenant-Id': isolation.tenantId,
      'X-Region': isolation.region,
      'X-Correlation-Id': isolation.correlationId ?? crypto.randomUUID(),
    });
  }
}
