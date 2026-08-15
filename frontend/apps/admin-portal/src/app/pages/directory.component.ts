import { Component } from '@angular/core';

@Component({
  standalone: true,
  selector: 'hr-admin-directory',
  template: `
    <div class="hr-row" style="justify-content: space-between">
      <div>
        <h1 class="hr-h1">Employee directory</h1>
        <p class="hr-sub">25,412 records · virtualized · region EMEA</p>
      </div>
      <div class="hr-row">
        <button class="hr-btn ghost" type="button">Export</button>
        <button class="hr-btn" type="button">Add employee</button>
      </div>
    </div>
    <div class="hr-row" style="margin-bottom: 0.8rem">
      <input class="hr-field" style="max-width: 280px; margin: 0" placeholder="Name, employee ID, email" readonly />
      <span class="hr-chip">EMEA</span>
      <span class="hr-chip">London HQ</span>
      <span class="hr-chip">Product Engineering</span>
      <span class="hr-chip">Active</span>
    </div>
    <article class="hr-card">
      <table class="hr-table">
        <thead>
          <tr><th>Employee</th><th>ID</th><th>Title</th><th>Org</th><th>Location</th><th>Status</th></tr>
        </thead>
        <tbody>
          @for (row of rows; track row.id) {
            <tr>
              <td>{{ row.name }}</td>
              <td>{{ row.id }}</td>
              <td>{{ row.title }}</td>
              <td>{{ row.org }}</td>
              <td>{{ row.location }}</td>
              <td><span class="hr-pill ok">Active</span></td>
            </tr>
          }
        </tbody>
      </table>
      <p class="hr-sub" style="margin: 0.75rem 0 0">Showing 1–8 of 10,205 in EMEA · cursor page (no offset)</p>
    </article>
  `,
})
export class DirectoryComponent {
  readonly rows = [
    { name: 'Priya Nair', id: 'EMP-104829', title: 'People Partner', org: 'People', location: 'London' },
    { name: 'Jonas Weber', id: 'EMP-100214', title: 'VP Engineering', org: 'Product Engineering', location: 'Berlin' },
    { name: 'Marcus Holm', id: 'EMP-188204', title: 'Staff Engineer', org: 'Platform', location: 'Stockholm' },
    { name: 'Amelia Chen', id: 'EMP-100001', title: 'Chief Executive Officer', org: 'Office of the CEO', location: 'London' },
    { name: 'Leila Haddad', id: 'EMP-176330', title: 'Staff Engineer', org: 'Platform', location: 'Paris' },
    { name: 'Sofia Alvarez', id: 'EMP-155902', title: 'Payroll Analyst', org: 'Compensation', location: 'Madrid' },
    { name: 'Kenji Sato', id: 'EMP-142118', title: 'Engineering Manager', org: 'Product Engineering', location: 'London' },
    { name: 'Nora Ibrahim', id: 'EMP-198441', title: 'Recruiter', org: 'Talent', location: 'Dubai' },
  ];
}
