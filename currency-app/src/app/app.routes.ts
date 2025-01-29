import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CurrencyFilterComponent } from './components/currency-filter/currency-filter.component';
import { CurrencyListComponent } from './components/currency-list/currency-list.component';


/*
@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
export const routes: Routes = [
  { path: '', component: CurrencyListComponent }
];

export const routingModule = RouterModule.forRoot(routes);
*/

export const routes: Routes = [
  { path: '', component: CurrencyListComponent }
];
