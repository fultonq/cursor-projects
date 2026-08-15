import { Route } from '@angular/router';
import { RemoteEntryComponent } from './entry.component';

export const remoteRoutes: Route[] = [
  {
    path: '',
    component: RemoteEntryComponent,
    children: [
      { path: '', loadComponent: () => import('../pages/workspace.component').then((m) => m.WorkspaceComponent) },
      { path: 'profile', loadComponent: () => import('../pages/profile.component').then((m) => m.ProfileComponent) },
      { path: 'time-off', loadComponent: () => import('../pages/time-off.component').then((m) => m.TimeOffComponent) },
      { path: 'payslips', loadComponent: () => import('../pages/payslip.component').then((m) => m.PayslipComponent) },
    ],
  },
];
