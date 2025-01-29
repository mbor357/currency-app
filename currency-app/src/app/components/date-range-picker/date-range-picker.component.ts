// date-range-picker.component.ts
import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-date-range-picker',
  templateUrl: './date-range-picker.component.html',
  styleUrls: ['./date-range-picker.component.css'],
  standalone: true,
})
export class DateRangePickerComponent {
  @Output() dateRangeSelected = new EventEmitter<{ startDate: string; endDate: string }>();

  onSelectDateRange(startDate: string, endDate: string) {
    this.dateRangeSelected.emit({ startDate, endDate });
  }
}
