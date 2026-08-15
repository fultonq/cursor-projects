import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  standalone: true,
  selector: 'hr-ess-workspace',
  imports: [RouterLink],
  template: `
    <h1 class="hr-h1">Your Friday snapshot</h1>
    <p class="hr-sub">Marcus Holm · Staff Engineer · Stockholm · EMEA</p>
    <div class="hr-kpis">
      <article class="hr-card hr-kpi"><span>Time off balance</span><strong>18.5d</strong></article>
      <article class="hr-card hr-kpi"><span>Next payday</span><strong>31 Aug</strong></article>
      <article class="hr-card hr-kpi"><span>Goals</span><strong>3 / 5</strong></article>
      <article class="hr-card hr-kpi"><span>Last net pay</span><strong>€4,820</strong></article>
    </div>
    <div class="hr-grid-2">
      <article class="hr-card">
        <h3>Upcoming</h3>
        <p>1:1 with Jonas · Mon 10:00</p>
        <p>Payroll cutoff · 20 Aug</p>
        <p>PTO window · 8–12 Sep (draft)</p>
      </article>
      <article class="hr-card">
        <h3>Quick actions</h3>
        <div class="hr-row">
          <a class="hr-btn" routerLink="time-off">Request time off</a>
          <a class="hr-btn ghost" routerLink="payslips">View payslip</a>
          <a class="hr-btn ghost" routerLink="profile">Update address</a>
        </div>
      </article>
    </div>
  `,
})
export class WorkspaceComponent {}
