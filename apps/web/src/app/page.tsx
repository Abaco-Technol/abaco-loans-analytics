import type { Metadata } from 'next'

import styles from './page.module.css'
import { alerts, funding, kpis, liquidityTracks, pipeline } from './dashboardData'

export const metadata: Metadata = {
  title: 'Abaco Loans Analytics Dashboard',
  description: 'Financial intelligence dashboard highlighting revenue, risk, liquidity, and compliance insights.',
}

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
