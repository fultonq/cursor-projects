import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  standalone: true,
  selector: 'hr-login',
  imports: [RouterLink],
  template: `
    <section class="hr-login">
      <aside class="hr-login-hero">
        <p class="hr-brand">Aether HR</p>
        <h1>Global workforce, region-isolated.</h1>
        <p>25,412 principals · OIDC + SAML · AMER · EMEA · APAC</p>
        <div class="hr-row" style="margin-top: 1.5rem">
          <span class="hr-chip">AMER</span>
          <span class="hr-chip">EMEA</span>
          <span class="hr-chip">APAC</span>
        </div>
      </aside>
      <div class="hr-login-form">
        <div class="hr-card hr-login-card">
          <h2 class="hr-h1">Sign in to your workspace</h2>
          <p class="hr-sub">Continue with your company identity provider.</p>
          <label>Work email</label>
          <input class="hr-field" value="priya.nair@aetherdynamics.com" readonly />
          <label>Tenant ID</label>
          <input class="hr-field" value="AETHER-GLOBAL" readonly />
          <a class="hr-btn" routerLink="/" style="display: inline-block">Continue with company SSO</a>
          <p class="hr-sub" style="margin-top: 1rem">Use SAML IdP · Use recovery code</p>
        </div>
      </div>
    </section>
  `,
})
export class LoginComponent {}
