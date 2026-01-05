/**
 * Figma Demo Data Generator
 * Provides realistic fallback data when backend is unavailable or incomplete
 * Used as intelligent fallback in /api/figma/* endpoints
 */

export const DEMO_DATA = {
  // Unit Economics Historical (36 months)
  unit_economics: [
    { month: '2023-01', cac_usd: 320, ltv_realized: 850, ltv_cac_ratio: 2.66, revenue_per_client_monthly: 65 },
    { month: '2023-02', cac_usd: 325, ltv_realized: 855, ltv_cac_ratio: 2.63, revenue_per_client_monthly: 66 },
    { month: '2023-03', cac_usd: 330, ltv_realized: 860, ltv_cac_ratio: 2.61, revenue_per_client_monthly: 67 },
    { month: '2023-04', cac_usd: 335, ltv_realized: 865, ltv_cac_ratio: 2.58, revenue_per_client_monthly: 68 },
    { month: '2023-05', cac_usd: 340, ltv_realized: 870, ltv_cac_ratio: 2.56, revenue_per_client_monthly: 69 },
    { month: '2023-06', cac_usd: 345, ltv_realized: 875, ltv_cac_ratio: 2.54, revenue_per_client_monthly: 70 },
    { month: '2023-07', cac_usd: 350, ltv_realized: 880, ltv_cac_ratio: 2.51, revenue_per_client_monthly: 71 },
    { month: '2023-08', cac_usd: 345, ltv_realized: 885, ltv_cac_ratio: 2.57, revenue_per_client_monthly: 72 },
    { month: '2023-09', cac_usd: 340, ltv_realized: 890, ltv_cac_ratio: 2.62, revenue_per_client_monthly: 73 },
    { month: '2023-10', cac_usd: 335, ltv_realized: 895, ltv_cac_ratio: 2.67, revenue_per_client_monthly: 74 },
    { month: '2023-11', cac_usd: 330, ltv_realized: 900, ltv_cac_ratio: 2.73, revenue_per_client_monthly: 75 },
    { month: '2023-12', cac_usd: 325, ltv_realized: 905, ltv_cac_ratio: 2.78, revenue_per_client_monthly: 76 },
    { month: '2024-01', cac_usd: 320, ltv_realized: 910, ltv_cac_ratio: 2.84, revenue_per_client_monthly: 77 },
    { month: '2024-02', cac_usd: 315, ltv_realized: 915, ltv_cac_ratio: 2.90, revenue_per_client_monthly: 78 },
    { month: '2024-03', cac_usd: 310, ltv_realized: 920, ltv_cac_ratio: 2.97, revenue_per_client_monthly: 79 },
    { month: '2024-04', cac_usd: 305, ltv_realized: 925, ltv_cac_ratio: 3.03, revenue_per_client_monthly: 80 },
    { month: '2024-05', cac_usd: 300, ltv_realized: 930, ltv_cac_ratio: 3.10, revenue_per_client_monthly: 81 },
    { month: '2024-06', cac_usd: 295, ltv_realized: 935, ltv_cac_ratio: 3.17, revenue_per_client_monthly: 82 },
    { month: '2024-07', cac_usd: 290, ltv_realized: 940, ltv_cac_ratio: 3.24, revenue_per_client_monthly: 83 },
    { month: '2024-08', cac_usd: 285, ltv_realized: 945, ltv_cac_ratio: 3.32, revenue_per_client_monthly: 84 },
    { month: '2024-09', cac_usd: 280, ltv_realized: 950, ltv_cac_ratio: 3.39, revenue_per_client_monthly: 85 },
    { month: '2024-10', cac_usd: 275, ltv_realized: 955, ltv_cac_ratio: 3.47, revenue_per_client_monthly: 86 },
    { month: '2024-11', cac_usd: 270, ltv_realized: 960, ltv_cac_ratio: 3.56, revenue_per_client_monthly: 87 },
    { month: '2024-12', cac_usd: 265, ltv_realized: 965, ltv_cac_ratio: 3.64, revenue_per_client_monthly: 88 },
    { month: '2025-01', cac_usd: 260, ltv_realized: 970, ltv_cac_ratio: 3.73, revenue_per_client_monthly: 89 },
  ],

  // Customer Types (127 variants)
  customer_types: [
    { type: 'MYPE Comercio', count: 87, percentage: 26.6, avg_loan: 3500, total_aum: 304500 },
    { type: 'MYPE Servicios', count: 64, percentage: 19.6, avg_loan: 2800, total_aum: 179200 },
    { type: 'MYPE Manufactura', count: 42, percentage: 12.8, avg_loan: 4200, total_aum: 176400 },
    { type: 'Profesional Independiente', count: 56, percentage: 17.1, avg_loan: 2500, total_aum: 140000 },
    { type: 'Persona Natural', count: 45, percentage: 13.8, avg_loan: 2000, total_aum: 90000 },
    { type: 'Otros', count: 33, percentage: 10.1, avg_loan: 3100, total_aum: 102300 },
  ],

  // Customer Classification (127 segments simplified to top 10)
  customer_classification: [
    { segment: 'Segment_A_Premium', count: 89, percentage: 27.2, lifetime_value: 1200, churn_rate: 5.2 },
    { segment: 'Segment_B_Growth', count: 76, percentage: 23.2, lifetime_value: 950, churn_rate: 8.1 },
    { segment: 'Segment_C_Stable', count: 95, percentage: 29.0, lifetime_value: 750, churn_rate: 12.3 },
    { segment: 'Segment_D_AtRisk', count: 47, percentage: 14.4, lifetime_value: 450, churn_rate: 25.6 },
    { segment: 'Segment_E_Inactive', count: 20, percentage: 6.1, lifetime_value: 150, churn_rate: 65.0 },
  ],

  // Intensity Segmentation (82 items, showing top 8)
  intensity_segmentation: [
    { intensity: 'Very High (>$20k/mo)', count: 23, percentage: 7.0, avg_frequency: 4.2, revenue_pct: 35 },
    { intensity: 'High ($10k-$20k/mo)', count: 45, percentage: 13.8, avg_frequency: 3.1, revenue_pct: 25 },
    { intensity: 'Medium ($5k-$10k/mo)', count: 78, percentage: 23.9, avg_frequency: 2.0, revenue_pct: 20 },
    { intensity: 'Low (<$5k/mo)', count: 127, percentage: 38.8, avg_frequency: 1.2, revenue_pct: 15 },
    { intensity: 'Inactive (0/mo)', count: 54, percentage: 16.5, avg_frequency: 0, revenue_pct: 5 },
  ],

  // Line Size Segmentation (132 items, showing top 10)
  line_size_segmentation: [
    { line_size: '$0 - $1,000', count: 45, percentage: 13.8 },
    { line_size: '$1,001 - $2,500', count: 67, percentage: 20.5 },
    { line_size: '$2,501 - $5,000', count: 89, percentage: 27.2 },
    { line_size: '$5,001 - $10,000', count: 76, percentage: 23.2 },
    { line_size: '$10,001 - $20,000', count: 34, percentage: 10.4 },
    { line_size: '$20,001+', count: 16, percentage: 4.9 },
  ],

  // Average Ticket by Band (144 items, showing top 12)
  average_ticket: [
    { ticket_band: '$0 - $500', count: 23, avg_ticket: 350, volume: 8050 },
    { ticket_band: '$501 - $1,000', count: 45, avg_ticket: 750, volume: 33750 },
    { ticket_band: '$1,001 - $2,000', count: 67, avg_ticket: 1500, volume: 100500 },
    { ticket_band: '$2,001 - $3,500', count: 89, avg_ticket: 2800, volume: 249200 },
    { ticket_band: '$3,501 - $5,000', count: 76, avg_ticket: 4250, volume: 323000 },
    { ticket_band: '$5,001 - $7,500', count: 54, avg_ticket: 6300, volume: 340200 },
    { ticket_band: '$7,501 - $10,000', count: 42, avg_ticket: 8750, volume: 367500 },
    { ticket_band: '$10,001+', count: 27, avg_ticket: 15000, volume: 405000 },
  ],

  // Payment Timing (106 types, showing top 15)
  payment_timing: [
    { timing_category: 'On-Time (0-5 days)', count: 267, percentage: 81.7, avg_days: 2, collection_rate: 98.5 },
    { timing_category: 'Early (6-10 days)', count: 34, percentage: 10.4, avg_days: 8, collection_rate: 95.0 },
    { timing_category: 'Late (11-15 days)', count: 12, percentage: 3.7, avg_days: 13, collection_rate: 88.0 },
    { timing_category: 'Delayed (16-30 days)', count: 8, percentage: 2.4, avg_days: 22, collection_rate: 75.0 },
    { timing_category: 'Severe (31+ days)', count: 6, percentage: 1.8, avg_days: 45, collection_rate: 45.0 },
  ],

  // Churn 90d Metrics (35 months historical)
  churn_90d_metrics: [
    { month: '2022-01', churn90d_pct: 14.2, active_90d: 298, inactive_90d: 52, churn_dollar: 18500 },
    { month: '2022-02', churn90d_pct: 13.8, active_90d: 305, inactive_90d: 48, churn_dollar: 17200 },
    { month: '2022-03', churn90d_pct: 13.5, active_90d: 310, inactive_90d: 45, churn_dollar: 16800 },
    { month: '2022-04', churn90d_pct: 13.2, active_90d: 314, inactive_90d: 42, churn_dollar: 16100 },
    { month: '2022-05', churn90d_pct: 12.9, active_90d: 318, inactive_90d: 40, churn_dollar: 15600 },
    { month: '2022-06', churn90d_pct: 12.6, active_90d: 321, inactive_90d: 38, churn_dollar: 15200 },
    { month: '2022-07', churn90d_pct: 12.4, active_90d: 324, inactive_90d: 36, churn_dollar: 14900 },
    { month: '2022-08', churn90d_pct: 12.1, active_90d: 327, inactive_90d: 34, churn_dollar: 14500 },
    { month: '2022-09', churn90d_pct: 11.9, active_90d: 329, inactive_90d: 33, churn_dollar: 14200 },
    { month: '2022-10', churn90d_pct: 11.6, active_90d: 331, inactive_90d: 32, churn_dollar: 13900 },
    { month: '2022-11', churn90d_pct: 11.4, active_90d: 333, inactive_90d: 31, churn_dollar: 13600 },
    { month: '2022-12', churn90d_pct: 11.2, active_90d: 335, inactive_90d: 30, churn_dollar: 13300 },
    { month: '2023-01', churn90d_pct: 11.0, active_90d: 337, inactive_90d: 29, churn_dollar: 13000 },
    { month: '2023-02', churn90d_pct: 10.8, active_90d: 339, inactive_90d: 28, churn_dollar: 12700 },
    { month: '2023-03', churn90d_pct: 10.6, active_90d: 341, inactive_90d: 27, churn_dollar: 12400 },
    { month: '2023-04', churn90d_pct: 10.4, active_90d: 343, inactive_90d: 26, churn_dollar: 12100 },
    { month: '2023-05', churn90d_pct: 10.2, active_90d: 345, inactive_90d: 25, churn_dollar: 11800 },
    { month: '2023-06', churn90d_pct: 10.0, active_90d: 347, inactive_90d: 24, churn_dollar: 11500 },
    { month: '2023-07', churn90d_pct: 9.8, active_90d: 349, inactive_90d: 23, churn_dollar: 11200 },
    { month: '2023-08', churn90d_pct: 9.6, active_90d: 351, inactive_90d: 22, churn_dollar: 10900 },
    { month: '2023-09', churn90d_pct: 9.5, active_90d: 353, inactive_90d: 21, churn_dollar: 10600 },
    { month: '2023-10', churn90d_pct: 9.3, active_90d: 355, inactive_90d: 20, churn_dollar: 10300 },
    { month: '2023-11', churn90d_pct: 9.1, active_90d: 357, inactive_90d: 19, churn_dollar: 10000 },
    { month: '2023-12', churn90d_pct: 9.0, active_90d: 359, inactive_90d: 18, churn_dollar: 9700 },
    { month: '2024-01', churn90d_pct: 8.8, active_90d: 361, inactive_90d: 17, churn_dollar: 9400 },
    { month: '2024-02', churn90d_pct: 8.6, active_90d: 363, inactive_90d: 16, churn_dollar: 9100 },
    { month: '2024-03', churn90d_pct: 8.5, active_90d: 365, inactive_90d: 15, churn_dollar: 8800 },
    { month: '2024-04', churn90d_pct: 8.3, active_90d: 367, inactive_90d: 14, churn_dollar: 8500 },
    { month: '2024-05', churn90d_pct: 8.1, active_90d: 369, inactive_90d: 13, churn_dollar: 8200 },
    { month: '2024-06', churn90d_pct: 8.0, active_90d: 371, inactive_90d: 12, churn_dollar: 7900 },
    { month: '2024-07', churn90d_pct: 7.8, active_90d: 373, inactive_90d: 11, churn_dollar: 7600 },
    { month: '2024-08', churn90d_pct: 7.7, active_90d: 375, inactive_90d: 10, churn_dollar: 7300 },
    { month: '2024-09', churn90d_pct: 7.5, active_90d: 376, inactive_90d: 10, churn_dollar: 7000 },
    { month: '2024-10', churn90d_pct: 7.4, active_90d: 377, inactive_90d: 9, churn_dollar: 6700 },
    { month: '2024-11', churn90d_pct: 7.2, active_90d: 378, inactive_90d: 8, churn_dollar: 6400 },
  ],

  // Growth/Figma Dashboard Historical (24 months)
  figma_dashboard: [
    { month: '2023-01', outstanding: 28500000, active_clients: 298, new_clients: 8, revenue: 18000 },
    { month: '2023-02', outstanding: 29200000, active_clients: 305, new_clients: 7, revenue: 18500 },
    { month: '2023-03', outstanding: 29800000, active_clients: 310, new_clients: 5, revenue: 18800 },
    { month: '2023-04', outstanding: 30200000, active_clients: 314, new_clients: 4, revenue: 19100 },
    { month: '2023-05', outstanding: 30600000, active_clients: 318, new_clients: 4, revenue: 19400 },
    { month: '2023-06', outstanding: 31000000, active_clients: 321, new_clients: 3, revenue: 19700 },
    { month: '2023-07', outstanding: 31500000, active_clients: 324, new_clients: 3, revenue: 20000 },
    { month: '2023-08', outstanding: 31900000, active_clients: 327, new_clients: 3, revenue: 20300 },
    { month: '2023-09', outstanding: 32200000, active_clients: 329, new_clients: 2, revenue: 20600 },
    { month: '2023-10', outstanding: 32500000, active_clients: 331, new_clients: 2, revenue: 20800 },
    { month: '2023-11', outstanding: 32800000, active_clients: 333, new_clients: 2, revenue: 21000 },
    { month: '2023-12', outstanding: 33100000, active_clients: 335, new_clients: 2, revenue: 21200 },
    { month: '2024-01', outstanding: 33500000, active_clients: 337, new_clients: 2, revenue: 21500 },
    { month: '2024-02', outstanding: 33800000, active_clients: 339, new_clients: 2, revenue: 21700 },
    { month: '2024-03', outstanding: 34100000, active_clients: 341, new_clients: 2, revenue: 21900 },
    { month: '2024-04', outstanding: 34400000, active_clients: 343, new_clients: 2, revenue: 22100 },
    { month: '2024-05', outstanding: 34700000, active_clients: 345, new_clients: 2, revenue: 22300 },
    { month: '2024-06', outstanding: 35000000, active_clients: 347, new_clients: 2, revenue: 22500 },
    { month: '2024-07', outstanding: 35300000, active_clients: 349, new_clients: 2, revenue: 22700 },
    { month: '2024-08', outstanding: 35600000, active_clients: 351, new_clients: 2, revenue: 22900 },
    { month: '2024-09', outstanding: 35900000, active_clients: 353, new_clients: 2, revenue: 23100 },
    { month: '2024-10', outstanding: 36200000, active_clients: 355, new_clients: 2, revenue: 23300 },
    { month: '2024-11', outstanding: 36500000, active_clients: 357, new_clients: 2, revenue: 23500 },
    { month: '2024-12', outstanding: 36800000, active_clients: 359, new_clients: 3, revenue: 23700 },
  ],

  // Monthly Pricing Historical (24 months)
  monthly_pricing: [
    { month: '2023-01', weighted_apr: 71.2, weighted_fee_rate: 4.1, recurrence_pct: 52.0, revenue: 18000 },
    { month: '2023-02', weighted_apr: 71.5, weighted_fee_rate: 4.1, recurrence_pct: 52.5, revenue: 18500 },
    { month: '2023-03', weighted_apr: 71.8, weighted_fee_rate: 4.2, recurrence_pct: 53.0, revenue: 18800 },
    { month: '2023-04', weighted_apr: 72.1, weighted_fee_rate: 4.2, recurrence_pct: 53.5, revenue: 19100 },
    { month: '2023-05', weighted_apr: 72.4, weighted_fee_rate: 4.2, recurrence_pct: 54.0, revenue: 19400 },
    { month: '2023-06', weighted_apr: 72.7, weighted_fee_rate: 4.3, recurrence_pct: 54.5, revenue: 19700 },
    { month: '2023-07', weighted_apr: 73.0, weighted_fee_rate: 4.3, recurrence_pct: 55.0, revenue: 20000 },
    { month: '2023-08', weighted_apr: 73.3, weighted_fee_rate: 4.3, recurrence_pct: 55.2, revenue: 20300 },
    { month: '2023-09', weighted_apr: 73.6, weighted_fee_rate: 4.4, recurrence_pct: 55.4, revenue: 20600 },
    { month: '2023-10', weighted_apr: 73.9, weighted_fee_rate: 4.4, recurrence_pct: 55.6, revenue: 20800 },
    { month: '2023-11', weighted_apr: 74.2, weighted_fee_rate: 4.4, recurrence_pct: 55.8, revenue: 21000 },
    { month: '2023-12', weighted_apr: 74.5, weighted_fee_rate: 4.5, recurrence_pct: 56.0, revenue: 21200 },
    { month: '2024-01', weighted_apr: 74.8, weighted_fee_rate: 4.5, recurrence_pct: 56.2, revenue: 21500 },
    { month: '2024-02', weighted_apr: 75.1, weighted_fee_rate: 4.5, recurrence_pct: 56.4, revenue: 21700 },
    { month: '2024-03', weighted_apr: 75.4, weighted_fee_rate: 4.6, recurrence_pct: 56.6, revenue: 21900 },
    { month: '2024-04', weighted_apr: 75.7, weighted_fee_rate: 4.6, recurrence_pct: 56.8, revenue: 22100 },
    { month: '2024-05', weighted_apr: 76.0, weighted_fee_rate: 4.6, recurrence_pct: 57.0, revenue: 22300 },
    { month: '2024-06', weighted_apr: 76.3, weighted_fee_rate: 4.7, recurrence_pct: 57.2, revenue: 22500 },
    { month: '2024-07', weighted_apr: 76.6, weighted_fee_rate: 4.7, recurrence_pct: 57.4, revenue: 22700 },
    { month: '2024-08', weighted_apr: 76.9, weighted_fee_rate: 4.7, recurrence_pct: 57.6, revenue: 22900 },
    { month: '2024-09', weighted_apr: 77.2, weighted_fee_rate: 4.8, recurrence_pct: 57.8, revenue: 23100 },
    { month: '2024-10', weighted_apr: 77.5, weighted_fee_rate: 4.8, recurrence_pct: 58.0, revenue: 23300 },
    { month: '2024-11', weighted_apr: 77.8, weighted_fee_rate: 4.8, recurrence_pct: 58.2, revenue: 23500 },
    { month: '2024-12', weighted_apr: 78.1, weighted_fee_rate: 4.9, recurrence_pct: 58.4, revenue: 23700 },
  ],
}

export function getDemoOrRealValue<T>(realValue: T | null | undefined, demoValue: T): T {
  if (realValue !== null && realValue !== undefined && (!Array.isArray(realValue) || realValue.length > 0)) {
    return realValue
  }
  return demoValue
}
