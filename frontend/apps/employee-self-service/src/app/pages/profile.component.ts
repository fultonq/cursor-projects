import { Component } from '@angular/core';

@Component({
  standalone: true,
  selector: 'hr-ess-profile',
  template: `
    <h1 class="hr-h1">Profile</h1>
    <p class="hr-sub">Workforce master data is read-only here. Address changes raise a case.</p>
    <div class="hr-grid-2">
      <article class="hr-card">
        <h3>Employment</h3>
        <table class="hr-table">
          <tbody>
            <tr><td>Employee ID</td><td>EMP-188204</td></tr>
            <tr><td>Title</td><td>Staff Engineer</td></tr>
            <tr><td>Org</td><td>Platform</td></tr>
            <tr><td>Manager</td><td>Jonas Weber</td></tr>
            <tr><td>Location</td><td>Stockholm</td></tr>
            <tr><td>Region</td><td>EMEA</td></tr>
          </tbody>
        </table>
      </article>
      <article class="hr-card">
        <h3>Personal (in-region)</h3>
        <label>Legal name</label>
        <input class="hr-field" value="Marcus Holm" readonly />
        <label>Work email</label>
        <input class="hr-field" value="marcus.holm@aetherdynamics.com" readonly />
        <label>Home address</label>
        <input class="hr-field" value="Södermalm, Stockholm, SE" readonly />
        <button class="hr-btn" type="button">Request correction</button>
      </article>
    </div>
  `,
})
export class ProfileComponent {}
