import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-currency-filter',
  templateUrl: './currency-filter.component.html',
  styleUrls: ['./currency-filter.component.css'],
  standalone: true,
})
export class CurrencyFilterComponent {
  @Output() filterChange = new EventEmitter<{ year: number, quarter: number, month: number, day: number }>();

  onFilterChange() {
    // Emitowanie zdarzenia z obiektem zawierającym year, quarter, month, day
    this.filterChange.emit({ year: 2025, quarter: 1, month: 1, day: 1 });
  }
}
