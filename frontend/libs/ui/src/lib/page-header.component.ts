import { Component, input } from '@angular/core';

@Component({
  standalone: true,
  selector: 'hr-page-header',
  template: `<header><h1>{{ title() }}</h1></header>`,
  styles: ['h1 { font-size: 1.4rem; margin: 0 0 1rem; }'],
})
export class PageHeaderComponent {
  title = input.required<string>();
}
