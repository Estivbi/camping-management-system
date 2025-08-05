import { Routes } from '@angular/router';
import { LoginComponent } from './components/login/login';
import { LayoutComponent } from './components/layout/layout';
import { DashboardComponent } from './components/dashboard/dashboard';
import { ActivitiesComponent } from './components/activities/activities';
import { ReservationsComponent } from './components/reservations/reservations';
import { UsersComponent } from './components/users/users';

export const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { 
    path: 'dashboard', 
    component: LayoutComponent,
    children: [
      { path: '', redirectTo: 'overview', pathMatch: 'full' },
      { path: 'overview', component: DashboardComponent },
      { path: 'activities', component: ActivitiesComponent },
      { path: 'reservations', component: ReservationsComponent },
      { path: 'users', component: UsersComponent }
    ]
  }
];
