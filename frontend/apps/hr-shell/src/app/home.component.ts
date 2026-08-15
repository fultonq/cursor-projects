import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  standalone: true,
  selector: 'hr-home',
  imports: [RouterLink],
  template: `
    <h1 class="hr-h1">Good morning, Priya</h1>
    <p class="hr-sub">People Partner · London · EMEA shard · 14 Aug 2026</p>
    <div class="hr-kpis">
      <article class="hr-card hr-kpi"><span>Headcount</span><strong>25,412</strong></article>
      <article class="hr-card hr-kpi"><span>Open requisitions</span><strong>186</strong></article>
      <article class="hr-card hr-kpi"><span>Payroll runs in progress</span><strong>3</strong></article>
      <article class="hr-card hr-kpi"><span>Compliance alerts</span><strong>7</strong></article>
    </div>
    <div class="hr-grid-2">
      <div class="hr-tiles">
        <a class="hr-card hr-tile" routerLink="/admin">
          <span class="hr-chip">Admin Portal</span>
          <h2>Workforce operations</h2>
          <p class="hr-sub">Directory, org chart, payroll, recruitment, IAM.</p>
        </a>
        <a class="hr-card hr-tile" routerLink="/ess">
          <span class="hr-chip">Self-service</span>
          <h2>Employee workspace</h2>
          <p class="hr-sub">Profile, time off, payslips, benefits.</p>
        </a>
      </div>
      <article class="hr-card">
        <h3>Regional pulse</h3>
        <table class="hr-table">
          <thead><tr><th>Region</th><th>Headcount</th><th>Shard</th></tr></thead>
          <tbody>
            <tr><td>AMER</td><td>9,840</td><td>pg-amer</td></tr>
            <tr><td>EMEA</td><td>10,205</td><td>pg-emea</td></tr>
            <tr><td>APAC</td><td>5,367</td><td>pg-apac</td></tr>
          </tbody>
        </table>
      </article>
    </div>
  `,
})
export class HomeComponent {}
