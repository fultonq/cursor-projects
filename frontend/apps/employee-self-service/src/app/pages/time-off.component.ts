import { Component } from '@angular/core';

@Component({
  standalone: true,
  selector: 'hr-ess-time-off',
  template: `
    <h1 class="hr-h1">Time off</h1>
    <p class="hr-sub">Balances are EMEA-local. Approver: Jonas Weber</p>
    <div class="hr-grid-2">
      <article class="hr-card">
        <h3>August 2026</h3>
        <div class="hr-org-row" style="justify-content: flex-start">
          @for (d of days; track d) {
            <span class="hr-chip" [class.warn]="d === 8 || d === 9">{{ d }}</span>
          }
        </div>
        <p class="hr-sub">Teal/amber chips mark requested days (8–12 Sep draft shown as 8–9 preview).</p>
      </article>
      <article class="hr-card">
        <h3>New request</h3>
        <label>Type</label>
        <input class="hr-field" value="Vacation" readonly />
        <label>Dates</label>
        <input class="hr-field" value="8 Sep 2026 – 12 Sep 2026" readonly />
        <p>Balance after request: <strong>13.5 days</strong></p>
        <button class="hr-btn" type="button">Submit request</button>
      </article>
    </div>
    <article class="hr-card" style="margin-top: 0.85rem">
      <h3>History</h3>
      <table class="hr-table">
        <tbody>
          <tr><td>12–16 May 2026</td><td>Vacation</td><td><span class="hr-pill ok">Approved</span></td></tr>
          <tr><td>3 Mar 2026</td><td>Sick</td><td><span class="hr-pill ok">Approved</span></td></tr>
        </tbody>
      </table>
    </article>
  `,
})
export class TimeOffComponent {
  readonly days = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14];
}
