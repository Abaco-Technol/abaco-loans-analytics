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

  const formatPercent = (value: number): string =>
    Number.isFinite(value) ? `${value.toFixed(1)}%` : '–'

  const sanitizeMarkdownCell = (value: string): string =>
    value
      .replace(/[\r\n]+/g, ' ')
      .replace(/[|`]/g, (match) => `\\${match}`)

  const treemapSection = treemap
    .map((entry) => `| ${sanitizeMarkdownCell(entry.label)} | ${entry.value.toLocaleString()} | ${sanitizeMarkdownCell(entry.color)} |`)
    .join('\n')

  const rollRateSection = rollRates
    .map((rate) => `| ${sanitizeMarkdownCell(rate.from)} | ${sanitizeMarkdownCell(rate.to)} | ${formatPercent(rate.percent)} |`)
    .join('\n')

  const growthSection = growthProjection
    .map((point) => `| ${sanitizeMarkdownCell(point.label)} | ${formatPercent(point.yield)} | ${point.loanVolume.toLocaleString()} |`)
    .join('\n')

  const treemapTable = treemapSection || '| – | – | – |'
  const rollRateTable = rollRateSection || '| – | – | – |'
  const growthTable = growthSection || '| – | – | – |'

  return `# Portfolio Analytics Report\n\n` +
    `## KPIs\n` +
    `- Delinquency rate: ${formatPercent(kpis.delinquencyRate)}\n` +
    `- Portfolio yield: ${formatPercent(kpis.portfolioYield)}\n` +
    `- Average LTV: ${formatPercent(kpis.averageLTV)}\n` +
    `- Average DTI: ${formatPercent(kpis.averageDTI)}\n` +
    `- Active loans: ${kpis.loanCount}\n\n` +
    `## Segment Treemap\n` +
    `| Segment | Principal Balance | Color |\n` +
    `|---|---|---|\n` +
    `${treemapTable}\n\n` +
    `## Roll-rate Cascade\n` +
    `| From | To | Percent |\n` +
    `|---|---|---|\n` +
    `${rollRateTable}\n\n` +
    `## Growth Path\n` +
    `| Month | Yield | Loan Volume |\n` +
    `|---|---|---|\n` +
    `${growthTable}`
}
