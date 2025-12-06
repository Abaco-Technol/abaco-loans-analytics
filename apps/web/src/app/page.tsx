import styles from './page.module.css'

type Metric = {
  title: string
  value: string
  delta: string
  detail: string
  tone?: 'positive' | 'neutral' | 'negative'
}

type Stage = {
  name: string
  volume: string
  conversion: number
  lift: string
  tone?: 'positive' | 'neutral' | 'negative'
}

type RiskItem = {
  name: string
  exposure: string
  trend: string
  level: 'guarded' | 'stable' | 'watch'
}

type Initiative = {
  name: string
  owner: string
  status: string
  tone?: 'positive' | 'neutral'
}

type FundingLine = {
  source: string
  share: number
  cost: string
}

type Control = {
  name: string
  owner: string
  status: string
  health: 'onTrack' | 'attention' | 'delayed'
  note: string
}

type CollectionsTrack = {
  bucket: string
  recovery: string
  action: string
}

const metrics: Metric[] = [
  {
    title: 'Active portfolio',
    value: '$48.6M',
    delta: '+8.3% QoQ',
    detail: 'Low default exposure with disciplined origination',
    tone: 'positive',
  },
  {
    title: 'Net yield',
    value: '12.4%',
    delta: '+40 bps MoM',
    detail: 'After cost of funds and servicing efficiency',
    tone: 'positive',
  },
  {
    title: 'Collections efficiency',
    value: '96.1%',
    delta: '+1.2 pts',
    detail: 'Direct debit penetration and early-cure initiatives',
    tone: 'positive',
  },
  {
    title: 'Acquisition CAC / LTV',
    value: '1 : 5.8',
    delta: 'Guardrail < 1 : 4',
    detail: 'Paid media optimized for risk-adjusted approvals',
    tone: 'neutral',
  },
  {
    title: 'First-pay default',
    value: '0.7%',
    delta: '-0.2 pts',
    detail: 'Champion underwriting and bureau refresh cadence',
    tone: 'positive',
  },
]

const stages: Stage[] = [
  { name: 'Applications', volume: '12,420', conversion: 100, lift: '+6.2%', tone: 'positive' },
  { name: 'Pre-approved', volume: '8,310', conversion: 67, lift: '+3.5%', tone: 'positive' },
  { name: 'Funded', volume: '5,120', conversion: 41, lift: '+2.1%', tone: 'positive' },
  { name: 'On-book M1+', volume: '4,910', conversion: 39, lift: '-0.4%', tone: 'negative' },
]

const riskHeat: RiskItem[] = [
  {
    name: 'SME working capital',
    exposure: '$22.4M',
    trend: 'Stable risk, monitor FX',
    level: 'stable',
  },
  {
    name: 'Salary advance',
    exposure: '$11.8M',
    trend: 'Improving vintage curve',
    level: 'guarded',
  },
  { name: 'Auto loans', exposure: '$9.6M', trend: 'Watchlist dealers reduced 28%', level: 'watch' },
]

const initiatives: Initiative[] = [
  { name: 'AI underwriting refresh', owner: 'Risk', status: 'Deploying', tone: 'positive' },
  { name: 'Collections digital playbook', owner: 'CX', status: 'Live', tone: 'positive' },
  { name: 'Treasury laddering', owner: 'Finance', status: 'In-flight', tone: 'neutral' },
]

const funding: FundingLine[] = [
  { source: 'ABS investors', share: 44, cost: 'SOFR + 410 bps' },
  { source: 'Bank revolver', share: 32, cost: 'SOFR + 350 bps' },
  { source: 'Equity & retained', share: 24, cost: 'Blended 10.2%' },
]

const controls: Control[] = [
  {
    name: 'Credit policy v4.2',
    owner: 'Risk',
    status: 'Audited',
    health: 'onTrack',
    note: 'Aligned to IFRS9 overlays',
  },
  {
    name: 'Data lineage & PII',
    owner: 'Data',
    status: 'Compliant',
    health: 'onTrack',
    note: 'SOC2 and GDPR mappings updated',
  },
  {
    name: 'Collections QA',
    owner: 'CX',
    status: 'Reviewing',
    health: 'attention',
    note: 'Voice analytics sampling at 92%',
  },
  {
    name: 'Liquidity buffers',
    owner: 'Finance',
    status: 'Actioned',
    health: 'delayed',
    note: 'Target +0.5x set for quarter close',
  },
]

const collections: CollectionsTrack[] = [
  { bucket: 'Early cure (0-30)', recovery: '96.1%', action: 'SMS + direct debit' },
  { bucket: 'M1 (31-60)', recovery: '84.7%', action: 'Call cadence + NPS save' },
  { bucket: 'M2 (61-90)', recovery: '61.4%', action: 'Settlement offers' },
]

const deltaClass = (tone?: 'positive' | 'neutral' | 'negative') => {
  if (tone === 'negative') return styles.deltaNegative
  if (tone === 'positive') return styles.deltaPositive
  return styles.deltaNeutral
}

export default function Home() {
  return (
    <div className={styles.page}>
      <header className={styles.hero}>
        <div className={styles.heroText}>
          <p className={styles.tag}>ABACO — Loan Intelligence</p>
          <h1 className={styles.heading}>Precision growth with auditable, real-time insights.</h1>
          <p className={styles.subtitle}>
            Operational control, embedded risk discipline, and revenue clarity for digital lending
            teams across credit, product, finance, and collections.
          </p>
          <div className={styles.pills}>
            <span>Predictive risk</span>
            <span>Unit economics</span>
            <span>Collections</span>
            <span>Funding</span>
          </div>
          <div className={styles.heroActions}>
            <button className={styles.primaryCta}>Schedule a demo</button>
            <button className={styles.secondaryCta}>Download one-pager</button>
          </div>
        </div>
        <div className={styles.heroCard}>
          <div className={styles.heroRow}>
            <div>
              <p className={styles.label}>Run-rate revenue</p>
              <p className={styles.primaryValue}>$6.8M</p>
            </div>
            <div className={styles.pillPositive}>+14.6% QoQ</div>
          </div>
          <p className={styles.helper}>Risk-adjusted yield net of impairments and servicing.</p>
          <div className={styles.divider} />
          <div className={styles.heroGrid}>
            <div>
              <p className={styles.label}>Cost of risk</p>
              <p className={styles.secondaryValue}>2.9%</p>
            </div>
            <div>
              <p className={styles.label}>NPL 90</p>
              <p className={styles.secondaryValue}>1.3%</p>
            </div>
            <div>
              <p className={styles.label}>Capital buffer</p>
              <p className={styles.secondaryValue}>11.4%</p>
            </div>
          </div>
        </div>
      </header>

      <section className={styles.metrics}>
        {metrics.map((metric) => (
          <article key={metric.title} className={styles.card}>
            <div className={styles.cardHeader}>
              <p className={styles.label}>{metric.title}</p>
              <span className={deltaClass(metric.tone)}>{metric.delta}</span>
            </div>
            <p className={styles.cardValue}>{metric.value}</p>
            <p className={styles.helper}>{metric.detail}</p>
          </article>
        ))}
      </section>

      <section className={styles.grid}>
        <article className={styles.panel}>
          <header className={styles.panelHeader}>
            <div>
              <p className={styles.label}>Acquisition to book</p>
              <h2>Risk-calibrated funnel</h2>
            </div>
            <span className={styles.pillNeutral}>SLA monitored</span>
          </header>
          <div className={styles.stageList}>
            {stages.map((stage) => (
              <div key={stage.name} className={styles.stageRow}>
                <div>
                  <p className={styles.stageName}>{stage.name}</p>
                  <p className={styles.helper}>{stage.volume} customers</p>
                </div>
                <div className={styles.stageMeta}>
                  <div className={styles.stageBar}>
                    <span style={{ width: `${stage.conversion}%` }} />
                  </div>
                  <div className={styles.stageNumbers}>
                    <span>{stage.conversion}%</span>
                    <span className={deltaClass(stage.tone)}>{stage.lift}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </article>

        <article className={styles.panel}>
          <header className={styles.panelHeader}>
            <div>
              <p className={styles.label}>Risk radar</p>
              <h2>Exposure and actions</h2>
            </div>
            <span className={styles.pillPositive}>Audit ready</span>
          </header>
          <div className={styles.riskList}>
            {riskHeat.map((item) => (
              <div key={item.name} className={styles.riskItem}>
                <div>
                  <p className={styles.stageName}>{item.name}</p>
                  <p className={styles.helper}>{item.exposure}</p>
                </div>
                <div className={styles.riskMeta}>
                  <span className={`${styles.level} ${styles[item.level]}`}>{item.level}</span>
                  <span className={styles.trend}>{item.trend}</span>
                </div>
              </div>
            ))}
          </div>
          <div className={styles.divider} />
          <div className={styles.initiatives}>
            {initiatives.map((initiative) => (
              <div key={initiative.name} className={styles.initiative}>
                <div>
                  <p className={styles.stageName}>{initiative.name}</p>
                  <p className={styles.helper}>{initiative.owner} lead</p>
                </div>
                <span
                  className={
                    initiative.tone === 'positive' ? styles.pillPositive : styles.pillNeutral
                  }
                >
                  {initiative.status}
                </span>
              </div>
            ))}
          </div>
        </article>
      </section>

      <section className={styles.grid}>
        <article className={styles.panel}>
          <header className={styles.panelHeader}>
            <div>
              <p className={styles.label}>Liquidity and capital</p>
              <h2>Funding runway</h2>
            </div>
            <span className={styles.pillNeutral}>Stress-tested</span>
          </header>
          <div className={styles.fundingList}>
            {funding.map((line) => (
              <div key={line.source} className={styles.fundingRow}>
                <div className={styles.fundingHeader}>
                  <p className={styles.stageName}>{line.source}</p>
                  <p className={styles.helper}>{line.cost}</p>
                </div>
                <div className={styles.stageBar}>
                  <span style={{ width: `${line.share}%` }} />
                </div>
                <div className={styles.stageNumbers}>
                  <span>{line.share}% mix</span>
                  <span className={styles.helper}>Hedge aligned</span>
                </div>
              </div>
            ))}
          </div>
        </article>

        <article className={styles.panel}>
          <header className={styles.panelHeader}>
            <div>
              <p className={styles.label}>Controls and assurance</p>
              <h2>Audit-ready control tower</h2>
            </div>
            <span className={styles.pillPositive}>Realtime</span>
          </header>
          <div className={styles.controls}>
            {controls.map((control) => (
              <div key={control.name} className={styles.controlRow}>
                <div>
                  <p className={styles.stageName}>{control.name}</p>
                  <p className={styles.helper}>{control.note}</p>
                </div>
                <div className={styles.controlMeta}>
                  <span className={styles.stageName}>{control.owner}</span>
                  <span className={`${styles.status} ${styles[control.health]}`}>
                    {control.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </article>
      </section>

      <section className={styles.panel}>
        <header className={styles.panelHeader}>
          <div>
            <p className={styles.label}>Collections precision</p>
            <h2>Resolution playbook</h2>
          </div>
          <span className={styles.pillNeutral}>Champion / Challenger</span>
        </header>
        <div className={styles.collections}>
          {collections.map((line) => {
            // Parse recovery rate and determine tone
            const recoveryValue = parseFloat(line.recovery.replace('%', ''));
            let recoveryTone: 'positive' | 'neutral' | 'negative';
            if (recoveryValue >= 80) {
              recoveryTone = 'positive';
            } else if (recoveryValue >= 50) {
              recoveryTone = 'neutral';
            } else {
              recoveryTone = 'negative';
            }
            return (
              <div key={line.bucket} className={styles.collectionRow}>
                <div>
                  <p className={styles.stageName}>{line.bucket}</p>
                  <p className={styles.helper}>{line.action}</p>
                </div>
                <span className={styles[`delta${recoveryTone.charAt(0).toUpperCase() + recoveryTone.slice(1)}`]}>
                  {line.recovery}
                </span>
              </div>
            );
          })}
        </div>
      </section>
    </div>
  )
}
