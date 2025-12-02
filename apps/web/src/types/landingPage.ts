export interface Metric {
  value: string
  label: string
}

export interface Product {
  title: string
  detail: string
}

export interface Step {
  label: string
  title: string
  copy: string
}

export interface LandingPageData {
  metrics: Metric[]
  products: Product[]
  controls: string[]
  steps: Step[]
}

export const EMPTY_LANDING_PAGE_DATA: LandingPageData = Object.freeze({
  metrics: [],
  products: [],
  controls: [],
  steps: [],
})
