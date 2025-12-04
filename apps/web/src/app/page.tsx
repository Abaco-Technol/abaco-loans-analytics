import Link from 'next/link'

import { controls, metrics, products, steps } from './data'
import styles from './page.module.css'

const navLinks = [
  { label: 'KPIs', href: '#kpis' },
  { label: 'Products', href: '#products' },
  { label: 'Controls', href: '#controls' },
  { label: 'Playbook', href: '#demo' },
]

export default function Page() {
  return (
    <main id="main-content" className={styles.page}>
      <nav className={styles.nav} aria-label="Primary">
        <div className={styles.brand}>Abaco Loans</div>
        <div className={styles.navLinks}>
          {navLinks.map((link) => (
            <Link key={link.href} href={link.href} className={styles.navLink}>
              {link.label}
            </Link>
          ))}
        </div>
        <Link href="#demo" className={styles.navCta}>
          Book a session
        </Link>
      </nav>

      <header className={styles.hero}>
        <div className={styles.pillRow}>
          <div className={styles.pill}>Growth & Risk Intelligence</div>
          <div className={styles.subPill}>Bank-grade controls</div>
        </div>
        <h1>Abaco Loans Analytics</h1>
        <p>
          A fintech command center that blends underwriting precision, revenue acceleration, and regulatory confidence in one
          cohesive experience.
        </p>
        <div className={styles.actions}>
          <Link href="#demo" className={styles.primaryButton}>
            Schedule a demo
          </Link>
          <Link href="#products" className={styles.secondaryButton}>
            Explore products
          </Link>
          <Link href="/settings" className={styles.secondaryButton}>
            Open settings
          </Link>
        </div>
        <div className={styles.metrics}>
          {metrics.map((metric) => (
            <dl key={metric.label} className={styles.metricCard}>
              <dt className={styles.metricLabel}>{metric.label}</dt>
              <dd className={styles.metricValue}>{metric.value}</dd>
            </dl>
          ))}
        </div>
      </header>

      <section id="kpis" className={styles.section}>
        <div className={styles.sectionHeader}>
          <p className={styles.sectionKicker}>KPIs & Evidence</p>
          <h2>Scorecards that prove runway, liquidity, and credit hygiene.</h2>
          <p className={styles.sectionCopy}>
            Every KPI pairs a formula, owner, and target so revenue, risk, and operations teams can act with confidence.
          </p>
        </div>
        <div className={styles.cardsGrid}>
          {products.map((product) => (
            <article key={product.title} className={styles.card}>
              <p className={styles.cardKicker}>Product</p>
              <h3>{product.title}</h3>
              <p>{product.detail}</p>
            </article>
          ))}
        </div>
      </section>

      <section id="products" className={styles.sectionAlt}>
        <div className={styles.sectionHeader}>
          <p className={styles.sectionKicker}>Dashboards</p>
          <h2>Portfolio, growth, and collections intelligence in one view.</h2>
        </div>
        <div className={styles.cardsGrid}>
          {steps.map((step) => (
            <article key={step.label} className={styles.card}>
              <p className={styles.cardKicker}>{step.label}</p>
              <h3>{step.title}</h3>
              <p>{step.copy}</p>
            </article>
          ))}
        </div>
      </section>

      <section id="controls" className={styles.section}>
        <div className={styles.sectionHeader}>
          <p className={styles.sectionKicker}>Controls</p>
          <h2>Compliance and resilience baked into every workflow.</h2>
        </div>
        <ul className={styles.list}>
          {controls.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </section>

      <section id="demo" className={styles.sectionAlt}>
        <div className={styles.sectionHeader}>
          <p className={styles.sectionKicker}>Playbook</p>
          <h2>Run the Abaco playbook with governed steps.</h2>
          <p className={styles.sectionCopy}>Partner-ready narratives, metrics, and controls for every stakeholder.</p>
        </div>
        <div className={styles.ctaRow}>
          <Link href="/docs" className={styles.primaryButton}>
            View documentation
          </Link>
          <Link href="mailto:hello@abaco.com" className={styles.secondaryButton}>
            Contact sales
          </Link>
        </div>
      </section>
    </main>
  )
}
