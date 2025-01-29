import { Component } from '@angular/core';
import { CurrencyService } from '../../services/currency.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; // Obsługa [(ngModel)]

@Component({
  selector: 'app-currency-list',
  templateUrl: './currency-list.component.html',
  styleUrls: ['./currency-list.component.css'],
  standalone: true, // Standalone component
  imports: [CommonModule, FormsModule], // Import wymaganych modułów
})
export class CurrencyListComponent {
  currencies: any[] = [];
  loading = false;

  selectedYear: number | undefined;
  selectedQuarter: number | undefined;
  selectedMonth: number | undefined;
  selectedDay: number | undefined;
  startDate: string | undefined;
  endDate: string | undefined;

  constructor(private currencyService: CurrencyService) {}

  // Metoda do pobierania danych z API NBP i zapisywania ich do bazy
  fetchAndSaveCurrencies(): void {
    if (this.startDate && this.endDate) {
      this.loading = true;
      this.currencyService.fetchAndSaveCurrencies(this.startDate, this.endDate).subscribe({
        next: () => {
          alert('Dane zostały pobrane i zapisane do bazy danych!');
          this.loading = false;
        },
        error: (error) => {
          alert('Wystąpił błąd podczas pobierania danych z API NBP: ' + error.message);
          this.loading = false;
        },
      });
    } else {
      alert('Proszę podać zakres dat!');
    }
  }


  // Metoda do filtrowania danych zapisanych w bazie
  getCurrencies(): void {
    this.loading = true;

    if (this.selectedDay) {
      this.currencyService.getCurrenciesByDay(this.selectedYear!, this.selectedMonth!, this.selectedDay).subscribe({
        next: (data) => (this.currencies = data),
        error: () => (this.loading = false),
        complete: () => (this.loading = false),
      });
    } else if (this.selectedMonth) {
        this.currencyService.getCurrenciesByMonth(this.selectedYear!, this.selectedMonth).subscribe({
          next: (data) => (this.currencies = data),
          error: () => (this.loading = false),
          complete: () => (this.loading = false),
        });
      } else if (this.selectedQuarter) {
        this.currencyService.getCurrenciesByQuarter(this.selectedYear!, this.selectedQuarter).subscribe({
          next: (data) => (this.currencies = data),
          error: () => (this.loading = false),
          complete: () => (this.loading = false),
        });
      } else if (this.selectedYear) {
        this.currencyService.getCurrenciesByYear(this.selectedYear).subscribe({
          next: (data) => (this.currencies = data),
          error: () => (this.loading = false),
          complete: () => (this.loading = false),
        });

    } else {
      alert('Proszę wybrać odpowiednie kryteria filtrowania.');
      this.loading = false;
    }
  }
  showCurrencies(): void {
    if (this.startDate && this.endDate) {
      this.currencyService.getCurrenciesByDateRange(this.startDate, this.endDate).subscribe({
        next: (data) => (this.currencies = data),
        error: () => (this.loading = false),
        complete: () => (this.loading = false),
      });
    }
  }
}
