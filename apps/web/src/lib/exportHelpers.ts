import type { ProcessedAnalytics } from '@/types/analytics'

export function processedAnalyticsToCSV(analytics: ProcessedAnalytics): string {
  const rows = analytics.loans.map((loan) => ({
    ...loan,
    ltv: ((loan.loan_amount / Math.max(loan.appraised_value, 1)) * 100).toFixed(1),
  }))
  const headers = Object.keys(rows[0] ?? {})
  const csvRows = rows.map((row) => headers.map((key) => row[key as keyof typeof row]).join(','))
  return [headers.join(','), ...csvRows].join('\n')
}

export function processedAnalyticsToJSON(analytics: ProcessedAnalytics): string {
  return JSON.stringify({
    kpis: analytics.kpis,
    treemap: analytics.treemap,
    rollRates: analytics.rollRates,
    growthProjection: analytics.growthProjection,
  }, null, 2)
}

export function processedAnalyticsToMarkdown(analytics: ProcessedAnalytics): string {
  const { kpis, treemap, rollRates, growthProjection } = analytics

  const treemapSection = treemap
    .map((entry) => `| ${entry.label} | ${entry.value.toLocaleString()} | ${entry.color} |`)
    .join('\n')

  const rollRateSection = rollRates
    .map((rate) => `| ${rate.from} | ${rate.to} | ${rate.percent.toFixed(1)}% |`)
    .join('\n')

  const growthSection = growthProjection
    .map((point) => `| ${point.label} | ${point.yield}% | ${point.loanVolume.toLocaleString()} |`)
    .join('\n')

  return `# Portfolio Analytics Report\n\n` +
    `## KPIs\n` +
    `- Delinquency rate: ${kpis.delinquencyRate}%\n` +
    `- Portfolio yield: ${kpis.portfolioYield}%\n` +
    `- Average LTV: ${kpis.averageLTV}%\n` +
    `- Average DTI: ${kpis.averageDTI}%\n` +
    `- Active loans: ${kpis.loanCount}\n\n` +
    `## Segment Treemap\n` +
    `| Segment | Principal Balance | Color |\n` +
    `|---|---|---|\n` +
    `${treemapSection}\n\n` +
    `## Roll-rate Cascade\n` +
    `| From | To | Percent |\n` +
    `|---|---|---|\n` +
    `${rollRateSection || '| – | – | – |'}\n\n` +
    `## Growth Path\n` +
    `| Month | Yield | Loan Volume |\n` +
    `|---|---|---|\n` +
    `${growthSection}`
}
