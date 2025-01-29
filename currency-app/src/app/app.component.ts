import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CurrencyFilterComponent } from './components/currency-filter/currency-filter.component';
import { CurrencyListComponent } from './components/currency-list/currency-list.component';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, CurrencyFilterComponent, CurrencyListComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
  standalone: true
})
export class AppComponent {
  title = 'currency-app';
}
/*@Component({
  selector: 'app-root',
  template: `<router-outlet></router-outlet>`,
  standalone: true,
  imports: [RouterOutlet]
})
export class AppComponent {}
*/
