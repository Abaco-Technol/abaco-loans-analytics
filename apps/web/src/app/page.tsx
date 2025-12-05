import Link from 'next/link'
import { z } from 'zod'

import { AnalyticsDashboard } from '@/components/analytics/AnalyticsDashboard'

import {
  controls as fallbackControls,
  metrics as fallbackMetrics,
  products as fallbackProducts,
  steps as fallbackSteps,
} from './data'
import styles from './page.module.css'
import { logLandingPageDiagnostic } from '../lib/landingPageDiagnostics'
import { isSupabaseConfigured, supabase } from '../lib/supabaseClient'
import {
  landingPageDataSchema,
  type LandingPageData,
  type Metric,
  type Product,
} from '../types/landingPage'

const navLinks: ReadonlyArray<{ label: string; href: string }> = [
  { label: 'KPIs', href: '#kpis' },
  { label: 'Products', href: '#products' },
  { label: 'Dashboards', href: '#dashboards' },
  { label: 'Compliance', href: '#compliance' },
  { label: 'Playbook', href: '#demo' },
]

const scorecards: ReadonlyArray<Metric> = [
  {
    label: 'Application-to-cash velocity',
    value: '< 48 hours',
  },
  {
    label: 'Loss-forecast confidence',
    value: '97%',
  },
  {
    label: 'Straight-through processing',
    value: '70%',
  },
]

const dashboards: ReadonlyArray<Product> = [
  {
    title: 'Liquidity & funding cockpit',
    detail: 'Covenant monitoring, cash runway, and facility utilization in one governed console.',
  },
  {
    title: 'Collections intelligence',
    detail: 'Roll rate, cure, and recovery tracking with interventions ranked by ROI.',
  },
  {
    title: 'Product P&L lenses',
    detail: 'Unit economics by channel, geography, and risk appetite with drilldowns on variance.',
  },
]

const landingPageSchema = z.object({
  metrics: landingPageDataSchema.shape.metrics,
  products: landingPageDataSchema.shape.products,
  controls: landingPageDataSchema.shape.controls,
  steps: landingPageDataSchema.shape.steps,
})

const fallbackData: LandingPageData = {
  metrics: fallbackMetrics.map((item) => ({ ...item })),
  products: fallbackProducts.map((item) => ({ ...item })),
  controls: [...fallbackControls],
  steps: fallbackSteps.map((item) => ({ ...item })),
}

const cloneFallbackData = (data: LandingPageData): LandingPageData =>
  JSON.parse(JSON.stringify(data))

async function getData(): Promise<LandingPageData> {
  if (!supabase || !isSupabaseConfigured) {
    logLandingPageDiagnostic({
      status: 'missing-config',
      supabaseConfigured: false,
      payload: fallbackData,
    })
    return cloneFallbackData(fallbackData)
  }

  const { data, error } = await supabase.from('landing_page_data').select('*').single()

  if (error || !data) {
    logLandingPageDiagnostic({
      status: 'fetch-error',
      supabaseConfigured: true,
      payload: fallbackData,
      error: error ?? 'no data returned',
    })
    return cloneFallbackData(fallbackData)
  }

  const parsed = landingPageSchema.safeParse(data)

  if (!parsed.success) {
    logLandingPageDiagnostic({
      status: 'invalid-shape',
      supabaseConfigured: true,
      payload: fallbackData,
      error: parsed.error.flatten(),
    })
    return cloneFallbackData(fallbackData)
  }

  logLandingPageDiagnostic({
    status: 'ok',
    supabaseConfigured: true,
    payload: parsed.data,
  })

  return parsed.data
}

export default async function Home() {
  const { metrics, products, controls, steps } = await getData()

  const structuredData = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: 'Abaco Loans Analytics',
    url: 'https://abaco-loans-analytics.com',
    description:
      'Abaco Loans Analytics unifies lending KPIs, governance, and revenue acceleration in one compliant, investor-ready experience.',
    areaServed: 'Global',
    brand: {
      '@type': 'Brand',
      name: 'Abaco Loans Analytics',
    },
    offers: {
      '@type': 'Offer',
      category: 'Financial technology',
      availability: 'https://schema.org/InStock',
    },
    hasOfferCatalog: {
      '@type': 'OfferCatalog',
      name: 'Growth & Risk Intelligence Suite',
      itemListElement: products.map((product) => ({
        '@type': 'Offer',
        itemOffered: {
          '@type': 'Service',
          name: product.title,
          description: product.detail,
        },
      })),
    },
    makesOffer: scorecards.map((score) => ({
      '@type': 'Offer',
      itemOffered: {
        '@type': 'Service',
        name: score.label,
        description: score.value,
      },
    })),
  }

  return (
    <div className={styles.page}>
      <nav className={styles.nav} aria-label="Primary">
        <span className={styles.brand}>Abaco</span>
        <div className={styles.navLinks}>
          {navLinks.map((link) => (
            <Link key={link.href} className={styles.navLink} href={link.href}>
              {link.label}
            </Link>
          ))}
        </div>
        <Link className={styles.navCta} href="#demo">
          Launch a pilot
        </Link>
      </nav>

      <main id="main-content" className={styles.main}>
        <section className={styles.hero} aria-labelledby="hero-heading">
          <div className={styles.pillRow}>
            <span className={styles.pill}>Governed growth platform</span>
            <span className={styles.subPill}>Audit-ready</span>
            <span className={styles.subPill}>Investor-grade</span>
          </div>
          <h1 id="hero-heading">
            Financial intelligence that turns lending KPIs into repeatable wins
          </h1>
          <p>
            Align credit, collections, and capital teams with dashboards, controls, and automated
            guardrails that keep every decision observable and auditable.
          </p>
          <div className={styles.actions}>
            <Link className={styles.primaryButton} href="#demo">
              Schedule a demo
            </Link>
            <Link className={styles.secondaryButton} href="#analytics">
              View analytics suite
            </Link>
          </div>
        </section>

        <section id="kpis" aria-labelledby="kpis-heading" className={styles.section}>
          <div className={styles.sectionHeader}>
            <p className={styles.eyebrow}>KPI cockpit</p>
            <h2 id="kpis-heading">Track the signals that run the lending business</h2>
            <p className={styles.sectionCopy}>
              A curated KPI stack across growth, risk, liquidity, and operations with controls built
              for auditors and investors.
            </p>
          </div>
          <div className={styles.metricsGrid}>
            {metrics.map((metric) => (
              <div key={metric.label} className={styles.metricCard}>
                <p className={styles.metricValue}>{metric.value}</p>
                <p className={styles.metricLabel}>{metric.label}</p>
              </div>
            ))}
          </div>
          <div className={styles.metricsGrid}>
            {scorecards.map((metric) => (
              <div key={metric.label} className={styles.metricCard}>
                <p className={styles.metricValue}>{metric.value}</p>
                <p className={styles.metricLabel}>{metric.label}</p>
              </div>
            ))}
          </div>
        </section>

        <section id="products" aria-labelledby="products-heading" className={styles.section}>
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

        <section id="dashboards" aria-labelledby="dashboards-heading" className={styles.section}>
          <div className={styles.sectionHeader}>
            <p className={styles.eyebrow}>Signals and dashboards</p>
            <h2 id="dashboards-heading">Commercial and financial intelligence on demand</h2>
            <p className={styles.sectionCopy}>
              Live dashboards that measure profitability, liquidity, and risk posture with built-in
              governance for every audience.
            </p>
          </div>
          <div className={styles.dashboardGrid}>
            {dashboards.map((dashboard) => (
              <div key={dashboard.title} className={styles.dashboardCard}>
                <div className={styles.dashboardHeader}>
                  <h3>{dashboard.title}</h3>
                </div>
                <p>{dashboard.detail}</p>
              </div>
            ))}
          </div>
          <div className={styles.linkRow}>
            <Link href="#demo" className={styles.primaryGhost}>
              Launch a pilot
            </Link>
            <Link href="#demo" className={styles.linkGhost}>
              Download governance pack
            </Link>
          </div>
        </section>

        <section id="compliance" aria-labelledby="compliance-heading" className={styles.section}>
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
              <Link href="#demo" className={styles.primaryGhost}>
                Launch a pilot
              </Link>
            </div>
          </div>
        </section>

        <section id="demo" aria-labelledby="playbook-heading" className={styles.section}>
          <div className={styles.sectionHeader}>
            <p className={styles.eyebrow}>Delivery playbook</p>
            <h2 id="playbook-heading">From data to decisions in weeks</h2>
            <p className={styles.sectionCopy}>
              Guided onboarding, industrialized documentation, and observability to keep every
              sprint on budget and on time.
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

        <section className={styles.section} id="analytics">
          <div className={styles.sectionHeader}>
            <p className={styles.eyebrow}>Analytics suite</p>
            <h2>Portfolio visibility with built-in governance</h2>
            <p className={styles.sectionCopy}>
              Dashboards, matrices, and drilldowns that instrument the lending lifecycle while
              maintaining controls.
            </p>
          </div>
          <AnalyticsDashboard />
        </section>
      </main>

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(structuredData),
        }}
      />
    </div>
  )
}
