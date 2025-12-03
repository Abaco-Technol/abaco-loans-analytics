export type KPI = {
  label: string
  value: string
  detail: string
  tone: 'positive' | 'neutral' | 'negative'
}

export type LiquidityTrack = { label: string; value: number }

export type PipelineDeal = { name: string; stage: string; volume: string; risk: string }

export type Alert = { title: string; description: string }

export type FundingItem = { label: string; value: number; accent: 'primary' | 'success' | 'accent' | 'muted' }

export const kpis: KPI[] = [
  {
    label: 'Net loan yield',
    value: '7.4% ARR',
    detail: '+32 bps MoM',
    tone: 'positive',
  },
  {
    label: 'Delinquency ratio',
    value: '1.1%',
    detail: '-18% QoQ',
    tone: 'positive',
  },
  {
    label: 'Cost of risk',
    value: '2.3%',
    detail: 'Stable, <2.5% guardrail',
    tone: 'neutral',
  },
  {
    label: 'Operating leverage',
    value: '3.7x',
    detail: 'Efficiency at record high',
    tone: 'positive',
  },
]

export const liquidityTracks: LiquidityTrack[] = [
  { label: 'Cash', value: 48 },
  { label: 'Credit lines', value: 72 },
  { label: 'ABS capacity', value: 64 },
  { label: 'Equity buffer', value: 36 },
]

export const pipeline: PipelineDeal[] = [
  { name: 'SME growth loans', stage: 'Credit memo', volume: '$18.4M', risk: 'Prime' },
  { name: 'BNPL merchant rollout', stage: 'Pricing', volume: '$9.7M', risk: 'Core' },
  { name: 'Renewable assets', stage: 'Due diligence', volume: '$6.2M', risk: 'Emerging' },
]

export const alerts: Alert[] = [
  {
    title: 'Early risk drift',
    description: 'Consumer scorecards show 0.4% uptick in PD on vintage T-4; collections playbook triggered.',
  },
  {
    title: 'Liquidity runway',
    description: '12.4 months coverage at current burn; extendable to 18.1 months via committed facilities.',
  },
  {
    title: 'Audit ready',
    description: 'SOX controls mapped to data lineage with automated evidence capture and reviewer sign-off.',
  },
]

export const funding: FundingItem[] = [
  { label: 'Origination growth', value: 86, accent: 'primary' },
  { label: 'Portfolio health', value: 92, accent: 'success' },
  { label: 'Revenue capture', value: 78, accent: 'accent' },
  { label: 'Customer NPS', value: 71, accent: 'muted' },
]
