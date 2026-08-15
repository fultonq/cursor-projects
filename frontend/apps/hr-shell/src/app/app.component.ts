import { Component, computed, inject } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { NavigationEnd, Router, RouterLink, RouterOutlet } from '@angular/router';
import { filter, map, startWith } from 'rxjs';

@Component({
  standalone: true,
  selector: 'hr-root',
  imports: [RouterOutlet, RouterLink],
  template: `
    @if (!isLogin()) {
      <header class="hr-top">
        <span class="hr-brand">Aether HR</span>
        <input class="hr-search" placeholder="Search people, jobs, tickets…" readonly />
        <span class="hr-chip">Aether Dynamics</span>
        <span class="hr-chip">EMEA</span>
        <nav class="hr-row">
          <a routerLink="/">Home</a>
          <a routerLink="/admin">Admin</a>
          <a routerLink="/ess">Self-service</a>
        </nav>
        <span class="hr-avatar">PN</span>
      </header>
    }
    <router-outlet />
  `,
})
export class AppComponent {
  private readonly router = inject(Router);
  private readonly url = toSignal(
    this.router.events.pipe(
      filter((event): event is NavigationEnd => event instanceof NavigationEnd),
      map(() => this.router.url),
      startWith(this.router.url)
    ),
    { initialValue: this.router.url }
  );
  readonly isLogin = computed(() => this.url().startsWith('/login'));
}
