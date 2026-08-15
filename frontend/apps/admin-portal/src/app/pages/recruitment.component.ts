import { Component } from '@angular/core';

@Component({
  standalone: true,
  selector: 'hr-admin-recruitment',
  template: `
    <h1 class="hr-h1">Recruitment pipeline</h1>
    <p class="hr-sub">186 open requisitions · offer accept 71% · EMEA filter</p>
    <div class="hr-kanban">
      @for (col of columns; track col.name) {
        <div class="hr-col">
          <strong>{{ col.name }} · {{ col.cards.length }}</strong>
          @for (card of col.cards; track card.id) {
            <article class="hr-card" style="margin-top: 0.5rem; padding: 0.7rem">
              <div>{{ card.name }}</div>
              <p class="hr-sub" style="margin: 0.2rem 0 0">{{ card.role }} · {{ card.id }}</p>
            </article>
          }
        </div>
      }
    </div>
  `,
})
export class RecruitmentComponent {
  readonly columns = [
    { name: 'Sourcing', cards: [{ name: 'Owen Blake', role: 'HRBP', id: 'REQ-2090' }] },
    { name: 'Screen', cards: [{ name: 'Mia Rossi', role: 'Payroll Analyst', id: 'REQ-2077' }] },
    {
      name: 'Interview',
      cards: [
        { name: 'Leila Haddad', role: 'Staff Engineer', id: 'REQ-2041' },
        { name: 'Arjun Mehta', role: 'Staff Engineer', id: 'REQ-2041' },
      ],
    },
    { name: 'Offer', cards: [{ name: 'Hannah Cole', role: 'Recruiter', id: 'REQ-2112' }] },
    { name: 'Hired', cards: [{ name: 'Kenji Sato', role: 'Eng Manager', id: 'REQ-1988' }] },
  ];
}
