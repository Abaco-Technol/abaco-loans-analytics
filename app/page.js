export default function HomePage() {
  return (
    <main style={{ fontFamily: 'sans-serif', padding: '2rem', textAlign: 'center' }}>
      <div style={{ maxWidth: '600px', margin: 'auto' }}>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 'bold' }}>
          Abaco Loans Analytics
        </h1>
        <p style={{ marginTop: '1rem', fontSize: '1.1rem', color: '#888' }}>The image generation API is available and ready for use.</p>
        <code style={{ display: 'inline-block', background: '#eee', padding: '0.5rem 1rem', borderRadius: '0.25rem', marginTop: '1.5rem' }}>POST /api/generate-image</code>
      </div>
    </main>
  );
}