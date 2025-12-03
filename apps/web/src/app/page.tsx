import type { PostgrestSingleResponse } from '@supabase/supabase-js'
import Link from 'next/link'
import {
  controls as fallbackControls,
  metrics as fallbackMetrics,
  products as fallbackProducts,
  steps as fallbackSteps,
} from './data'
import styles from './page.module.css'
import { AnalyticsDashboard } from '@/components/analytics/AnalyticsDashboard'
import { isSupabaseConfigured, supabase } from '../lib/supabaseClient'
import { logLandingPageDiagnostic } from '../lib/landingPageDiagnostics'
import { landingPageDataSchema, type LandingPageData } from '../types/landingPage'

const fallbackLandingData = landingPageDataSchema.parse({
  metrics: fallbackMetrics,
  products: fallbackProducts,
  controls: fallbackControls,
  steps: fallbackSteps,
})

const NAV_LINKS = [
  { label: 'KPIs', href: '#kpis' },
  { label: 'Products', href: '#products' },
  { label: 'Compliance', href: '#compliance' },
  { label: 'Playbook', href: '#playbook' },
  { label: 'Analytics', href: '#analytics' },
]

async function getLandingPageData(): Promise<LandingPageData> {
  if (!supabase || !isSupabaseConfigured) {
    logLandingPageDiagnostic({
      status: 'missing-config',
      supabaseConfigured: false,
      payload: fallbackLandingData,
    })
    return fallbackLandingData
  }

  const { data, error }: PostgrestSingleResponse<LandingPageData> = await supabase
    .from('landing_page_data')
    .select('*')
    .single()

  if (error || !data) {
    logLandingPageDiagnostic({
      status: 'fetch-error',
      supabaseConfigured: true,
      error,
      payload: fallbackLandingData,
    })
    return fallbackLandingData
  }

  const parsed = landingPageDataSchema.safeParse(data)

  if (!parsed.success) {
    logLandingPageDiagnostic({
      status: 'invalid-shape',
      supabaseConfigured: true,
      error: parsed.error.flatten(),
      payload: fallbackLandingData,
    })
    return fallbackLandingData
  }

  logLandingPageDiagnostic({
    status: 'ok',
    supabaseConfigured: true,
    payload: parsed.data,
  })

  return parsed.data
}

export default async function Home() {
  const landingData = await getLandingPageData()
  const { metrics, products, controls, steps } = landingData

  return (
    <main className={styles.page} id="main-content">
      <nav className={styles.nav} aria-label="Primary">
        <span className={styles.brand}>Abaco</span>
        <div className={styles.navLinks}>
          {NAV_LINKS.map((link) => (
            <Link key={link.href} className={styles.navLink} href={link.href}>
              {link.label}
            </Link>
          ))}
        </div>
        <Link className={styles.navCta} href="#playbook">
          Launch a pilot
        </Link>
      </nav>

      <header className={styles.hero}>
        <div className={styles.pillRow}>
          <span className={styles.pill}>Audit-ready lending intelligence</span>
          <span className={styles.pill}>Portfolio & growth dashboards</span>
        </div>
        <h1>
          Evidence-driven lending decisions with governed KPIs, transparent controls, and
          customer-first delivery.
        </h1>
        <p>
          Abaco aligns product, risk, finance, and operations on one source of truth—complete with
          lineage, SLAs, and auditability. Deploy fast with pre-built dashboards, runbooks, and
          secure data onboarding.
        </p>
        <div className={styles.ctaRow}>
          <Link className={styles.primaryButton} href="#analytics">
            View analytics cockpit
          </Link>
          <Link className={styles.secondaryButton} href="mailto:hello@abaco.loans">
            Talk with us
          </Link>
        </div>
      </header>

      <section id="kpis" className={styles.metrics} aria-labelledby="kpis-heading">
        <div className={styles.sectionHeader}>
          <p className={styles.eyebrow}>Performance signals</p>
          <h2 id="kpis-heading">KPIs with ownership, refresh cadence, and lineage</h2>
          <p className={styles.sectionCopy}>
            Every metric is tied to a data contract and runbook so teams can react with clarity and
            speed.
          </p>
        </div>
        <dl className={styles.metricsGrid}>
          {metrics.map((metric) => (
            <div key={metric.label} className={styles.metricCard}>
              <dt className={styles.metricLabel}>{metric.label}</dt>
              <dd className={styles.metricValue}>{metric.value}</dd>
            </div>
          ))}
        </dl>
      </section>

      <section id="products" className={styles.section} aria-labelledby="products-heading">
        <div className={styles.sectionHeader}>
          <p className={styles.eyebrow}>Customer-centric growth</p>
          <h2 id="products-heading">Build, fund, and protect every loan strategy</h2>
          <p className={styles.sectionCopy}>
            Abaco aligns acquisition, credit, collections, and treasury teams around shared KPIs
            with zero-friction visibility and auditable execution.
          </p>
        </div>
        <div className={styles.cardGrid}>
          {products.map((product) => (
            <div key={product.title} className={styles.card}>
              <div className={styles.cardHeader}>
                <h3>{product.title}</h3>
              </div>
              <p>{product.detail}</p>
            </div>
          ))}
        </div>
      </section>

      <section id="compliance" className={styles.section} aria-labelledby="compliance-heading">
        <div className={styles.sectionHeader}>
          <p className={styles.eyebrow}>Operational excellence</p>
          <h2 id="compliance-heading">Compliance-first, automation-ready</h2>
          <p className={styles.sectionCopy}>
            Deploy with confidence using built-in governance, continuous monitoring, and clear
            accountabilities for every decision.
          </p>
        </div>
        <div className={styles.compliance}>
          <ul className={styles.complianceList}>
            {controls.map((item) => (
              <li key={item} className={styles.checkItem}>
                <span className={styles.checkBullet} aria-hidden="true" />
                <span>{item}</span>
              </li>
            ))}
          </ul>
          <div className={styles.auditBox}>
            <p className={styles.auditTitle}>Audit-ready by design</p>
            <ul>
              <li>Unified evidence across decisions, payments, and servicing.</li>
              <li>Exportable traces for regulators, investors, and partners.</li>
              <li>Service-level alerts with automated escalations.</li>
            </ul>
            <Link href="#analytics" className={styles.primaryGhost}>
              View drill-downs
            </Link>
          </div>
        </div>
      </section>

      <section id="playbook" className={styles.section} aria-labelledby="playbook-heading">
        <div className={styles.sectionHeader}>
          <p className={styles.eyebrow}>Delivery playbook</p>
          <h2 id="playbook-heading">From data to decisions in weeks</h2>
          <p className={styles.sectionCopy}>
            Guided onboarding, industrialized documentation, and observability to keep every sprint
            on budget and on time.
          </p>
        </div>
        <div className={styles.timeline}>
          {steps.map((step) => (
            <div key={step.label} className={styles.timelineStep}>
              <span className={styles.stepBadge}>{step.label}</span>
              <div>
                <h3>{step.title}</h3>
                <p>{step.copy}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className={styles.section} id="analytics" aria-labelledby="analytics-heading">
        <div className={styles.sectionHeader}>
          <p className={styles.eyebrow}>Analytics cockpit</p>
          <h2 id="analytics-heading">Quality gates, drill-downs, and alert routing</h2>
          <p className={styles.sectionCopy}>
            Upload sample portfolios, explore delinquency and roll-rate drill-downs, and route
            alerts to owners with runbooks and SLAs.
          </p>
        </div>
        <AnalyticsDashboard />
      </section>
    </main>
  )
}
