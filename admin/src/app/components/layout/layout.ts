import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterOutlet, RouterModule } from '@angular/router';

// Angular Material Components
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatListModule } from '@angular/material/list';
import { MatMenuModule } from '@angular/material/menu';
import { MatDividerModule } from '@angular/material/divider';

// Services
import { AuthService, User } from '../../services/auth';

@Component({
  selector: 'app-layout',
  standalone: true,
  imports: [
    CommonModule,
    RouterOutlet,
    RouterModule,
    MatSidenavModule,
    MatToolbarModule,
    MatButtonModule,
    MatIconModule,
    MatListModule,
    MatMenuModule,
    MatDividerModule
  ],
  templateUrl: './layout.html',
  styleUrl: './layout.scss'
})
export class LayoutComponent implements OnInit {
  sidebarVisible: boolean = true;
  currentUser: User | null = null;
  
  menuItems = [
    {
      label: 'Dashboard',
      icon: 'dashboard',
      route: '/dashboard'
    },
    {
      label: 'Actividades',
      icon: 'event',
      route: '/dashboard/activities'
    },
    {
      label: 'Reservas',
      icon: 'calendar_today',
      route: '/dashboard/reservations'
    },
    {
      label: 'Usuarios',
      icon: 'people',
      route: '/dashboard/users'
    }
  ];

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit() {
    this.loadCurrentUser();
  }

  async loadCurrentUser() {
    this.currentUser = this.authService.currentUserValue;
    if (!this.currentUser) {
      this.router.navigate(['/login']);
    }
  }

  getCurrentPageTitle(): string {
    const url = this.router.url;
    if (url.includes('/activities')) return 'Actividades';
    if (url.includes('/reservations')) return 'Reservas';
    if (url.includes('/users')) return 'Usuarios';
    if (url.includes('/notifications')) return 'Notificaciones';
    return 'Dashboard';
  }

  showProfile() {
    // TODO: Implementar vista de perfil
    console.log('Mostrar perfil');
  }

  showSettings() {
    // TODO: Implementar configuración
    console.log('Mostrar configuración');
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
