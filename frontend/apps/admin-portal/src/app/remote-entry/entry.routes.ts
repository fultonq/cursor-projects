import { Route } from '@angular/router';
import { RemoteEntryComponent } from './entry.component';

export const remoteRoutes: Route[] = [
  {
    path: '',
    component: RemoteEntryComponent,
    children: [
      { path: '', loadComponent: () => import('../pages/dashboard.component').then((m) => m.DashboardComponent) },
      { path: 'directory', loadComponent: () => import('../pages/directory.component').then((m) => m.DirectoryComponent) },
      { path: 'org', loadComponent: () => import('../pages/org-chart.component').then((m) => m.OrgChartComponent) },
      { path: 'recruitment', loadComponent: () => import('../pages/recruitment.component').then((m) => m.RecruitmentComponent) },
      { path: 'payroll', loadComponent: () => import('../pages/payroll.component').then((m) => m.PayrollComponent) },
      { path: 'access', loadComponent: () => import('../pages/iam.component').then((m) => m.IamComponent) },
    ],
  },
];
