export interface Metric {
  value: string;
  label: string;
}

export interface Product {
  title: string;
  detail: string;
}

export interface Step {
  label: string;
  title: string;
  copy: string;
}

// Placeholder data
export const metrics: Metric[] = [{ value: '11x', label: 'Coverage velocity' }];
export const products: Product[] = [{ title: 'Product 1', detail: 'Product detail' }];
export const controls: string[] = ['Control 1'];
export const steps: Step[] = [{ label: '1', title: 'Step 1', copy: 'Step copy' }];
