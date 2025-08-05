import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

// Angular Material Components (solo los necesarios para el contenido)
import { MatIconModule } from '@angular/material/icon';

// PrimeNG Components
import { CardModule } from 'primeng/card';
import { ChartModule } from 'primeng/chart';

interface DashboardStats {
  activities: number;
  reservations: number;
  users: number;
  revenue: number;
}

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    MatIconModule,
    CardModule,
    ChartModule
  ],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss'
})
export class DashboardComponent implements OnInit {
  stats: DashboardStats = {
    activities: 0,
    reservations: 0,
    users: 0,
    revenue: 0
  };

  chartData: any;
  chartOptions: any;

  ngOnInit() {
    this.loadStats();
    this.initChart();
  }

  async loadStats() {
    // TODO: Cargar estadísticas reales desde el backend
    // Por ahora usamos datos de ejemplo
    this.stats = {
      activities: 12,
      reservations: 8,
      users: 45,
      revenue: 1250
    };
  }

  initChart() {
    this.chartData = {
      labels: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
      datasets: [
        {
          label: 'Reservas',
          data: [5, 8, 12, 15, 18, 22, 25],
          borderColor: '#667eea',
          backgroundColor: 'rgba(102, 126, 234, 0.1)',
          tension: 0.4
        },
        {
          label: 'Actividades',
          data: [3, 6, 9, 12, 15, 18, 20],
          borderColor: '#764ba2',
          backgroundColor: 'rgba(118, 75, 162, 0.1)',
          tension: 0.4
        }
      ]
    };

    this.chartOptions = {
      plugins: {
        legend: {
          labels: {
            color: '#495057'
          }
        }
      },
      scales: {
        x: {
          ticks: {
            color: '#6c757d'
          },
          grid: {
            color: '#e9ecef'
          }
        },
        y: {
          ticks: {
            color: '#6c757d'
          },
          grid: {
            color: '#e9ecef'
          }
        }
      }
    };
  }
}
