import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

@Component({
  standalone: true,
  selector: 'hr-ess-entry',
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <div class="hr-app">
      <aside class="hr-side">
        <p class="hr-brand" style="padding: 0 0.75rem 0.75rem">Self-service</p>
        <a routerLink="./" routerLinkActive="on" [routerLinkActiveOptions]="{ exact: true }">Workspace</a>
        <a routerLink="profile" routerLinkActive="on">Profile</a>
        <a routerLink="time-off" routerLinkActive="on">Time off</a>
        <a routerLink="payslips" routerLinkActive="on">Payslips</a>
      </aside>
      <section class="hr-main">
        <router-outlet />
      </section>
    </div>
  `,
})
export class RemoteEntryComponent {}
