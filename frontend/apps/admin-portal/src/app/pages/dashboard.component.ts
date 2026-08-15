import { Component } from '@angular/core';

@Component({
  standalone: true,
  selector: 'hr-admin-dashboard',
  template: `
    <h1 class="hr-h1">Workforce operations</h1>
    <p class="hr-sub">14 Aug 2026 · tenant AETHER-GLOBAL · mock data</p>
    <div class="hr-kpis">
      <article class="hr-card hr-kpi"><span>Active employees</span><strong>25,412</strong></article>
      <article class="hr-card hr-kpi"><span>New hires (30d)</span><strong>214</strong></article>
      <article class="hr-card hr-kpi"><span>Attrition</span><strong>0.8%</strong></article>
      <article class="hr-card hr-kpi"><span>Time-to-fill</span><strong>31d</strong></article>
    </div>
    <div class="hr-grid-2">
      <article class="hr-card">
        <h3>Region shards</h3>
        <table class="hr-table">
          <thead><tr><th>Region</th><th>Headcount</th><th>Database</th></tr></thead>
          <tbody>
            <tr><td>AMER</td><td>9,840</td><td>hr_amer :5432</td></tr>
            <tr><td>EMEA</td><td>10,205</td><td>hr_emea :5433</td></tr>
            <tr><td>APAC</td><td>5,367</td><td>hr_apac :5434</td></tr>
          </tbody>
        </table>
      </article>
      <article class="hr-card">
        <h3>Attention required</h3>
        <table class="hr-table">
          <tbody>
            <tr><td>EMEA payroll calendar locked</td><td><span class="hr-pill warn">Cutoff</span></td></tr>
            <tr><td>APAC tax table stale (SG)</td><td><span class="hr-pill bad">Tax</span></td></tr>
            <tr><td>SAML cert expires in 18 days</td><td><span class="hr-pill warn">IAM</span></td></tr>
            <tr><td>GDPR DSAR queue · 4 open</td><td><span class="hr-pill">Audit</span></td></tr>
          </tbody>
        </table>
      </article>
    </div>
  `,
})
export class DashboardComponent {}
