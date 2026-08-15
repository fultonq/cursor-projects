import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

@Component({
  standalone: true,
  selector: 'hr-admin-entry',
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <div class="hr-app">
      <aside class="hr-side">
        <p class="hr-brand" style="padding: 0 0.75rem 0.75rem">Admin Portal</p>
        <a routerLink="./" routerLinkActive="on" [routerLinkActiveOptions]="{ exact: true }">Overview</a>
        <a routerLink="directory" routerLinkActive="on">Directory</a>
        <a routerLink="org" routerLinkActive="on">Org chart</a>
        <a routerLink="recruitment" routerLinkActive="on">Recruitment</a>
        <a routerLink="payroll" routerLinkActive="on">Payroll</a>
        <a routerLink="access" routerLinkActive="on">Access</a>
      </aside>
      <section class="hr-main">
        <router-outlet />
      </section>
    </div>
  `,
})
export class RemoteEntryComponent {}
