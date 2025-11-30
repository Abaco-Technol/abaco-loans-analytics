'use client';

import Image from 'next/image';
import { useState } from 'react';

const endpoints = [
  {
    name: 'Image Generation',
    path: '/api/generate-image',
    method: 'POST',
    description:
      'POST /api/generate-image streams prompt text, style presets, and KPI metadata to create financial storyboards ready for stakeholder decks.',
  },
];

const kpis = [
  { label: 'Pipeline Throughput', value: '4.8M tx/month', trend: '+12% vs last cycle' },
  { label: 'Model SLAs Met', value: '99.6%', trend: 'Latency 180ms' },
  { label: 'Monetized Insights', value: '$3.2M ARR', trend: 'New deals signed this quarter' },
];

const dashboards = [
  {
    title: 'Commercial Intelligence Grid',
    detail:
      'Combines client segments, revenue velocity, and risk scoring so you prioritize conversations that move the needle.',
  },
  {
    title: 'Growth Motion Tracker',
    detail:
      'Visualizes cadence compliance, automation coverage, and the ROI of AI-assisted prospecting playbooks.',
  },
  {
    title: 'Audit-ready Health Feed',
    detail: 'Captures every notifier with lineage metadata so compliance reviews become checkpoints, not delays.',
  },
];

export default function HomePage() {
  const [prompt, setPrompt] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setImageUrl('');
    setError('');

    try {
      const response = await fetch('/api/generate-image', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${process.env.NEXT_PUBLIC_API_SECRET_KEY}`,
        },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.details || 'Failed to generate image');
      }

      const data = await response.json();
      setImageUrl(data.imageUrls?.[0] || '');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container">
      <header className="hero">
        <p className="eyebrow">Abaco Commercial Intelligence</p>
        <h1>Financial intelligence with traceable impact</h1>
        <p>
          Coordinated analytics, secure automation, and KPI-grade delivery ensure every insight is ready to convert into action.
        </p>
      </header>

      <section className="section-card">
        <div className="form-grid">
          <div>
            <h2>Image generation API</h2>
            <p className="lede">
              The image generation API is available at <code>POST /api/generate-image</code>. Use it to surface branded visuals
              that narrate quarterly results or campaign performance.
            </p>
          </div>
          <form className="input-row" onSubmit={handleSubmit}>
            <input
              type="text"
              value={prompt}
              onChange={(event) => setPrompt(event.target.value)}
              placeholder="Enter your prompt (e.g., modern fintech dashboard)"
              required
            />
            <button type="submit" disabled={loading}>
              {loading ? 'Generating...' : 'Generate image'}
            </button>
          </form>
        </div>

        {error && <p className="error">{error}</p>}
        {imageUrl && (
          <div className="result">
            <h3>Generated visual preview</h3>
            <Image
              src={imageUrl}
              alt="Generated asset"
              width={1200}
              height={720}
              className="result-img"
              unoptimized
              priority
            />
          </div>
        )}
      </section>

      <section className="section-grid">
        <article className="section-card">
          <h2>API surface</h2>
          <ul className="endpoint-list">
            {endpoints.map((endpoint) => (
              <li key={endpoint.path}>
                <span className="tag">{endpoint.method}</span>
                <code>{endpoint.path}</code>
                <p>{endpoint.description}</p>
              </li>
            ))}
          </ul>
        </article>

        <article className="section-card">
          <h2>Key Performance Indicators</h2>
          <div className="kpi-grid">
            {kpis.map((kpi) => (
              <div key={kpi.label} className="kpi">
                <p className="kpi-label">{kpi.label}</p>
                <p className="kpi-value">{kpi.value}</p>
                <p className="kpi-trend">{kpi.trend}</p>
              </div>
            ))}
          </div>
        </article>
      </section>

      <section className="section-card">
        <h2>Dashboards and audit trails</h2>
        <div className="dashboards">
          {dashboards.map((dash) => (
            <div className="dashboard-block" key={dash.title}>
              <h3>{dash.title}</h3>
              <p>{dash.detail}</p>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
