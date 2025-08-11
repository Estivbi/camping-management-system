import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatDialogModule, MatDialog } from '@angular/material/dialog';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatCardModule } from '@angular/material/card';
import { MatSnackBarModule, MatSnackBar } from '@angular/material/snack-bar';
import { Api, Activity } from '../../services/api';

@Component({
  selector: 'app-activities',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    MatFormFieldModule,
    MatInputModule,
    MatDialogModule,
    MatCheckboxModule,
    MatCardModule,
    MatSnackBarModule
  ],
  templateUrl: './activities.html',
  styleUrl: './activities.scss'
})
export class ActivitiesComponent implements OnInit {
  activities: Activity[] = [];
  activityForm: FormGroup;
  displayedColumns: string[] = ['name', 'description', 'capacity', 'price', 'duration', 'is_active', 'actions'];
  isEditing = false;
  editingId?: number;

  constructor(
    private api: Api,
    private fb: FormBuilder,
    private snackBar: MatSnackBar
  ) {
    this.activityForm = this.fb.group({
      name: ['', Validators.required],
      description: ['', Validators.required],
      capacity: [1, [Validators.required, Validators.min(1)]],
      price: [0, [Validators.required, Validators.min(0)]],
      duration: [60, [Validators.required, Validators.min(1)]],
      is_active: [true]
    });
  }

  ngOnInit(): void {
    this.loadActivities();
  }

  loadActivities(): void {
    this.api.getActividades().subscribe({
      next: (activities) => {
        this.activities = activities;
      },
      error: (error) => {
        console.error('Error cargando actividades:', error);
        this.snackBar.open('Error cargando actividades', 'Cerrar', { duration: 3000 });
      }
    });
  }

  onSubmit(): void {
    if (this.activityForm.valid) {
      const activityData = this.activityForm.value;

      if (this.isEditing && this.editingId) {
        this.api.updateActividad(this.editingId, activityData).subscribe({
          next: () => {
            this.snackBar.open('Actividad actualizada exitosamente', 'Cerrar', { duration: 3000 });
            this.resetForm();
            this.loadActivities();
          },
          error: (error) => {
            console.error('Error actualizando actividad:', error);
            this.snackBar.open('Error actualizando actividad', 'Cerrar', { duration: 3000 });
          }
        });
      } else {
        this.api.createActividad(activityData).subscribe({
          next: () => {
            this.snackBar.open('Actividad creada exitosamente', 'Cerrar', { duration: 3000 });
            this.resetForm();
            this.loadActivities();
          },
          error: (error) => {
            console.error('Error creando actividad:', error);
            this.snackBar.open('Error creando actividad', 'Cerrar', { duration: 3000 });
          }
        });
      }
    }
  }

  editActivity(activity: Activity): void {
    this.isEditing = true;
    this.editingId = activity.id;
    this.activityForm.patchValue(activity);
  }

  deleteActivity(id: number): void {
    if (confirm('¿Estás seguro de que deseas eliminar esta actividad?')) {
      this.api.deleteActividad(id).subscribe({
        next: () => {
          this.snackBar.open('Actividad eliminada exitosamente', 'Cerrar', { duration: 3000 });
          this.loadActivities();
        },
        error: (error) => {
          console.error('Error eliminando actividad:', error);
          this.snackBar.open('Error eliminando actividad', 'Cerrar', { duration: 3000 });
        }
      });
    }
  }

  resetForm(): void {
    this.activityForm.reset({
      name: '',
      description: '',
      capacity: 1,
      price: 0,
      duration: 60,
      is_active: true
    });
    this.isEditing = false;
    this.editingId = undefined;
  }
}
