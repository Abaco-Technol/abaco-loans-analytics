import styles from './page.module.css'

const kpis = [
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

const liquidityTracks = [
  { label: 'Cash', value: 48 },
  { label: 'Credit lines', value: 72 },
  { label: 'ABS capacity', value: 64 },
  { label: 'Equity buffer', value: 36 },
]

const pipeline = [
  { name: 'SME growth loans', stage: 'Credit memo', volume: '$18.4M', risk: 'Prime' },
  { name: 'BNPL merchant rollout', stage: 'Pricing', volume: '$9.7M', risk: 'Core' },
  { name: 'Renewable assets', stage: 'Due diligence', volume: '$6.2M', risk: 'Emerging' },
]

const alerts = [
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

const funding = [
  { label: 'Origination growth', value: 86, accent: 'primary' },
  { label: 'Portfolio health', value: 92, accent: 'success' },
  { label: 'Revenue capture', value: 78, accent: 'accent' },
  { label: 'Customer NPS', value: 71, accent: 'muted' },
]

export default function Home() {
  return (
    <div className={styles.page}>
      <div className={styles.shell}>
        <header className={styles.header}>
          <div>
            <p className={styles.eyebrow}>Abaco Loans Analytics</p>
            <h1>Financial intelligence engineered for growth.</h1>
            <p className={styles.lede}>
              Precision dashboards for revenue, risk, and liquidity. Built for boardroom velocity, investor readiness,
              and customer-centric execution.
            </p>
          </div>
          <div className={styles.statusBadges}>
            <span className={styles.pill}>Audit trail active</span>
            <span className={`${styles.pill} ${styles.pillStrong}`}>Real-time telemetry</span>
          </div>
        </header>

        <section className={`${styles.grid} ${styles.kpiGrid}`}>
          {kpis.map((kpi) => (
            <div key={kpi.label} className={`${styles.card} ${styles.kpi} ${styles[kpi.tone]}`}>
              <p className={styles.label}>{kpi.label}</p>
              <div className={styles.kpiValue}>{kpi.value}</div>
              <p className={styles.meta}>{kpi.detail}</p>
            </div>
          ))}
        </section>

        <section className={`${styles.grid} ${styles.split}`}>
          <div className={`${styles.card} ${styles.chart}`}>
            <div className={styles.cardHead}>
              <div>
                <p className={styles.label}>Funding trajectory</p>
                <h2>Capital efficiency with transparent guardrails</h2>
              </div>
              <span className={styles.pill}>Traceable</span>
            </div>
            <div className={styles.bars}>
              {funding.map((item) => (
                <div key={item.label} className={styles.barRow}>
                  <div className={styles.barMeta}>
                    <p className={styles.label}>{item.label}</p>
                    <p className={styles.meta}>{item.value}% goal attainment</p>
                  </div>
                  <div className={styles.barTrack}>
                    <span className={`${styles.fill} ${styles[item.accent]}`} style={{ width: `${item.value}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className={`${styles.card} ${styles.table}`}>
            <div className={styles.cardHead}>
              <div>
                <p className={styles.label}>Revenue pipeline</p>
                <h2>Commercial momentum</h2>
              </div>
              <span className={styles.pill}>All stages</span>
            </div>
            <div className={styles.tableHead}>
              <span>Initiative</span>
              <span>Stage</span>
              <span>Volume</span>
              <span>Risk band</span>
            </div>
            {pipeline.map((deal) => (
              <div key={deal.name} className={styles.tableRow}>
                <span>{deal.name}</span>
                <span>{deal.stage}</span>
                <span>{deal.volume}</span>
                <span className={styles.badge}>{deal.risk}</span>
              </div>
            ))}
          </div>
        </section>

        <section className={`${styles.grid} ${styles.split}`}>
          <div className={`${styles.card} ${styles.liquidity}`}>
            <div className={styles.cardHead}>
              <div>
                <p className={styles.label}>Liquidity stack</p>
                <h2>Coverage and diversification</h2>
              </div>
              <span className={styles.pill}>Updated hourly</span>
            </div>
            <div className={styles.liquidityGrid}>
              {liquidityTracks.map((track) => (
                <div key={track.label} className={styles.liquidityCard}>
                  <div className={styles.liquidityTop}>
                    <p className={styles.label}>{track.label}</p>
                    <p className={styles.strong}>{track.value}%</p>
                  </div>
                  <div className={styles.spark}>
                    <span className={styles.sparkFill} style={{ width: `${track.value}%` }} />
                  </div>
                  <p className={styles.meta}>Guardrail: 30% minimum per stream</p>
                </div>
              ))}
            </div>
          </div>

          <div className={`${styles.card} ${styles.alerts}`}>
            <div className={styles.cardHead}>
              <div>
                <p className={styles.label}>Controls & compliance</p>
                <h2>Signals with accountability</h2>
              </div>
              <span className={styles.pill}>Auditable</span>
            </div>
            <div className={styles.alertList}>
              {alerts.map((item) => (
                <div key={item.title} className={styles.alert}>
                  <p className={styles.alertTitle}>{item.title}</p>
                  <p className={styles.meta}>{item.description}</p>
                </div>
              ))}
            </div>
            <div className={styles.footer}>
              <p className={styles.label}>Next actions</p>
              <div className={styles.footerActions}>
                <span className={`${styles.pill} ${styles.pillStrong}`}>Send investment memo</span>
                <span className={styles.pill}>Export audit pack</span>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  )
}
