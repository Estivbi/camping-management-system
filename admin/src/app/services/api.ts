import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Activity {
  id?: number;
  name: string;
  description: string;
  capacity: number;
  price: number;
  duration: number;
  is_active: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class Api {
  private baseUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) { }

  // Actividades
  getActividades(): Observable<Activity[]> {
    return this.http.get<Activity[]>(`${this.baseUrl}/api/activities`);
  }

  getActividad(id: number): Observable<Activity> {
    return this.http.get<Activity>(`${this.baseUrl}/api/activities/${id}`);
  }

  createActividad(activity: Omit<Activity, 'id'>): Observable<Activity> {
    return this.http.post<Activity>(`${this.baseUrl}/api/activities`, activity);
  }

  updateActividad(id: number, activity: Partial<Activity>): Observable<Activity> {
    return this.http.put<Activity>(`${this.baseUrl}/api/activities/${id}`, activity);
  }

  deleteActividad(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/api/activities/${id}`);
  }

  // Auth helpers
  private getAuthHeaders(): HttpHeaders {
    const token = localStorage.getItem('access_token');
    return new HttpHeaders({
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    });
  }
}
