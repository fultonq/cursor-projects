import { Component } from '@angular/core';

@Component({
  standalone: true,
  selector: 'hr-admin-payroll',
  template: `
    <h1 class="hr-h1">Payroll runs · August 2026</h1>
    <p class="hr-sub">No cross-region posting — each run stays on its shard.</p>
    <div class="hr-kpis">
      <article class="hr-card hr-kpi"><span>AMER · USD</span><strong>62%</strong><p class="hr-sub">In progress</p></article>
      <article class="hr-card hr-kpi"><span>EMEA · EUR</span><strong>Queued</strong><p class="hr-sub">Cutoff 20 Aug</p></article>
      <article class="hr-card hr-kpi"><span>APAC · SGD</span><strong>Validate</strong><p class="hr-sub">Tax table stale</p></article>
      <article class="hr-card hr-kpi"><span>Pay groups</span><strong>18</strong><p class="hr-sub">4 jurisdictions</p></article>
    </div>
    <div class="hr-grid-2">
      <article class="hr-card">
        <h3>Pay groups</h3>
        <table class="hr-table">
          <thead><tr><th>Group</th><th>Jurisdiction</th><th>CCY</th><th>Employees</th><th>Status</th></tr></thead>
          <tbody>
            <tr><td>UK Monthly</td><td>GB-ENG</td><td>GBP</td><td>4,120</td><td><span class="hr-pill">Ready</span></td></tr>
            <tr><td>DE Monthly</td><td>DE</td><td>EUR</td><td>2,880</td><td><span class="hr-pill">Ready</span></td></tr>
            <tr><td>FR Monthly</td><td>FR</td><td>EUR</td><td>1,640</td><td><span class="hr-pill warn">Review</span></td></tr>
            <tr><td>SG Monthly</td><td>SG</td><td>SGD</td><td>980</td><td><span class="hr-pill bad">Tax</span></td></tr>
          </tbody>
        </table>
      </article>
      <article class="hr-card">
        <h3>Run EMEA-2026-08</h3>
        <p>Load payees <span class="hr-pill ok">done</span></p>
        <p>Apply elements <span class="hr-pill ok">done</span></p>
        <p>Tax engine <span class="hr-pill warn">running</span></p>
        <p>Bank file <span class="hr-pill">queued</span></p>
      </article>
    </div>
  `,
})
export class PayrollComponent {}
