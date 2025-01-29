import { Injectable } from '@angular/core';
import {HttpClient, HttpParams} from '@angular/common/http';
import { Observable } from 'rxjs';
import { Currency } from '../models/currency.model';

@Injectable({
  providedIn: 'root'
})
export class CurrencyService {

  private apiUrl = `http://localhost:8000/currencies`;
  constructor(private http: HttpClient) { }

  fetchAndSaveCurrencies(startDate: string, endDate: string): Observable<any> {
    const params = new HttpParams()
      .set('start_date', startDate)
      .set('end_date', endDate);

    console.log(`Request URL: ${this.apiUrl}/fetch`, params.toString()); // Logowanie URL i parametrów
    return this.http.post(`${this.apiUrl}/fetch`, null, { params });
  }

  getCurrenciesByDateRange(startDate: string, endDate: string): Observable<Currency[]> {
    return this.http.get<Currency[]>(`${this.apiUrl}?start=${startDate}&end=${endDate}`);
  }

  getCurrenciesByYear(year: number): Observable<Currency[]> {
    return this.http.get<Currency[]>(`${this.apiUrl}/year/${year}`);
  }

  getCurrenciesByQuarter(year: number, quarter: number): Observable<Currency[]> {
    return this.http.get<Currency[]>(`${this.apiUrl}/quarter/${year}/${quarter}`);
  }

  getCurrenciesByMonth(year: number, month: number): Observable<Currency[]> {
    return this.http.get<Currency[]>(`${this.apiUrl}/month/${year}/${month}`);
  }

  getCurrenciesByDay(year: number, month: number | undefined, day: number): Observable<Currency[]> {
    return this.http.get<Currency[]>(`${this.apiUrl}/day/${year}/${month}/${day}`);
  }
}
