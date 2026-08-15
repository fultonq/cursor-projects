import { Component } from '@angular/core';

@Component({
  standalone: true,
  selector: 'hr-ess-payslip',
  template: `
    <h1 class="hr-h1">Payslip · July 2026</h1>
    <p class="hr-sub">Stored in the EMEA region shard (GDPR).</p>
    <div class="hr-grid-2">
      <article class="hr-card">
        <h3>Aether Dynamics EMEA AB</h3>
        <table class="hr-table">
          <tbody>
            <tr><td>Employee</td><td>Marcus Holm · EMP-188204</td></tr>
            <tr><td>Location</td><td>Stockholm</td></tr>
            <tr><td>Currency</td><td>EUR</td></tr>
            <tr><td>Gross</td><td>€6,450</td></tr>
            <tr><td>Tax</td><td>€1,210</td></tr>
            <tr><td>Pension</td><td>€290</td></tr>
            <tr><td>Insurance</td><td>€130</td></tr>
            <tr><td><strong>Net</strong></td><td><strong>€4,820</strong></td></tr>
          </tbody>
        </table>
        <div class="hr-row" style="margin-top: 0.8rem">
          <button class="hr-btn" type="button">Download PDF</button>
          <button class="hr-btn ghost" type="button">Send to email</button>
        </div>
      </article>
      <article class="hr-card">
        <h3>Periods</h3>
        <p>May 2026</p>
        <p>June 2026</p>
        <p><strong>July 2026</strong></p>
      </article>
    </div>
  `,
})
export class PayslipComponent {}
