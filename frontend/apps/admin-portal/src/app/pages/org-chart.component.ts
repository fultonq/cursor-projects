import { Component } from '@angular/core';

@Component({
  standalone: true,
  selector: 'hr-admin-org',
  template: `
    <h1 class="hr-h1">Organization · Product Engineering</h1>
    <p class="hr-sub">As-of 14 Aug 2026 · EMEA forest · cross-region managers are correlation IDs</p>
    <div class="hr-org">
      <article class="hr-card hr-person">
        <div class="hr-avatar" style="margin: 0 auto 0.4rem">AC</div>
        <strong>Amelia Chen</strong>
        <p class="hr-sub">Chief Executive Officer</p>
      </article>
      <div class="hr-org-row">
        <article class="hr-card hr-person">
          <div class="hr-avatar" style="margin: 0 auto 0.4rem">JW</div>
          <strong>Jonas Weber</strong>
          <p class="hr-sub">VP Engineering · 186</p>
        </article>
        <article class="hr-card hr-person">
          <div class="hr-avatar" style="margin: 0 auto 0.4rem">PN</div>
          <strong>Priya Nair</strong>
          <p class="hr-sub">People Partner · 24</p>
        </article>
        <article class="hr-card hr-person">
          <div class="hr-avatar" style="margin: 0 auto 0.4rem">SA</div>
          <strong>Sofia Alvarez</strong>
          <p class="hr-sub">Payroll Ops · 12</p>
        </article>
      </div>
      <div class="hr-org-row">
        <article class="hr-card hr-person">
          <div class="hr-avatar" style="margin: 0 auto 0.4rem">MH</div>
          <strong>Marcus Holm</strong>
          <p class="hr-sub">Staff Engineer</p>
        </article>
        <article class="hr-card hr-person">
          <div class="hr-avatar" style="margin: 0 auto 0.4rem">LH</div>
          <strong>Leila Haddad</strong>
          <p class="hr-sub">Staff Engineer</p>
        </article>
        <article class="hr-card hr-person">
          <div class="hr-avatar" style="margin: 0 auto 0.4rem">KS</div>
          <strong>Kenji Sato</strong>
          <p class="hr-sub">Engineering Manager · 14</p>
        </article>
      </div>
    </div>
  `,
})
export class OrgChartComponent {}
