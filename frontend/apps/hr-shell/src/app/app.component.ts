import { Component } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';

@Component({
  standalone: true,
  selector: 'hr-root',
  imports: [RouterOutlet, RouterLink],
  template: `
    <header class="shell">
      <strong>HR Shell</strong>
      <nav>
        <a routerLink="/">Home</a>
        <a routerLink="/admin">Admin</a>
        <a routerLink="/ess">Self-service</a>
      </nav>
    </header>
    <main>
      <router-outlet />
    </main>
  `,
  styles: [
    `
      .shell {
        display: flex;
        gap: 1.5rem;
        align-items: center;
        padding: 0.75rem 1.25rem;
        border-bottom: 1px solid #e5e7eb;
      }
      nav { display: flex; gap: 1rem; }
      main { padding: 1.25rem; }
    `,
  ],
})
export class AppComponent {}
