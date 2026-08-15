import { Route } from '@angular/router';

export const appRoutes: Route[] = [
  { path: 'login', loadComponent: () => import('./login.component').then((m) => m.LoginComponent) },
  { path: '', loadComponent: () => import('./home.component').then((m) => m.HomeComponent) },
  {
    path: 'admin',
    loadChildren: () => import('admin-portal/Routes').then((m) => m.remoteRoutes),
  },
  {
    path: 'ess',
    loadChildren: () => import('employee-self-service/Routes').then((m) => m.remoteRoutes),
  },
];
