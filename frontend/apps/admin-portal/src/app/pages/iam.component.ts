import { Component } from '@angular/core';

@Component({
  standalone: true,
  selector: 'hr-admin-iam',
  template: `
    <h1 class="hr-h1">Identity & access</h1>
    <p class="hr-sub">Region claim is not a tenant. Residency is enforced by X-Region.</p>
    <div class="hr-kpis">
      <article class="hr-card hr-kpi"><span>OIDC</span><strong>Okta</strong><p class="hr-sub">Connected</p></article>
      <article class="hr-card hr-kpi"><span>SAML backup</span><strong>Entra ID</strong><p class="hr-sub">Standby</p></article>
      <article class="hr-card hr-kpi"><span>Job roles</span><strong>54</strong><p class="hr-sub">Permission sets</p></article>
      <article class="hr-card hr-kpi"><span>Principals</span><strong>25,412</strong><p class="hr-sub">Tenant-scoped</p></article>
    </div>
    <article class="hr-card">
      <table class="hr-table">
        <thead><tr><th>Role</th><th>Principals</th><th>Sample permissions</th><th>Region scope</th></tr></thead>
        <tbody>
          <tr><td>People Partner</td><td>86</td><td>directory:read, assignment:write</td><td>claimed</td></tr>
          <tr><td>Payroll Ops Lead</td><td>14</td><td>payroll:run, payslip:read</td><td>claimed</td></tr>
          <tr><td>Recruiter</td><td>41</td><td>requisition:read, offer:draft</td><td>claimed</td></tr>
          <tr><td>Engineering Manager</td><td>312</td><td>directory:read, offer:approve</td><td>claimed</td></tr>
          <tr><td>Compliance Officer</td><td>9</td><td>audit:read, dsar:export</td><td>multi-read*</td></tr>
        </tbody>
      </table>
      <p class="hr-sub">*Compliance reads Analytics projections, never source shards.</p>
    </article>
  `,
})
export class IamComponent {}
