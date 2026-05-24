# Design System Quick Reference

## Full CSS Variable Set

```css
:root {
  --accent-blue: #4f6df5;    --accent-blue-dark: #3b55d4;
  --accent-purple: #7c3aed;  --accent-purple-dark: #6d28d9;
  --accent-green: #10b981;   --accent-green-dark: #059669;
  --accent-orange: #f59e0b;  --accent-orange-dark: #d97706;
  --accent-red: #ef4444;     --accent-red-dark: #dc2626;
  --accent-pink: #db2777;    --accent-pink-dark: #be185d;

  --heading: #1a202c;
  --text: #2d3748;
  --text-muted: #718096;
  --bg: #ffffff;
}
```

## Component Snippets

### Slide Container
```html
<section class="slide">
  <span class="tag tag-1">Module Label</span>
  <h2>Title <span class="gradient">Accent</span></h2>
  <p class="text-muted">Subtitle</p>
  <!-- content -->
</section>
```

### Card Grid
```html
<div class="card-grid cols-3">
  <div class="card" style="border-left:3px solid var(--accent-blue)">
    <h4>Title</h4>
    <p>Content</p>
  </div>
  <!-- more cards -->
</div>
```

### Bar Chart (pure HTML/CSS)
```html
<div class="bar-chart bar-chart-4col">
  <span class="bar-name">Label</span>
  <span class="bar-year">2025</span>
  <div class="bar-track">
    <div class="bar-fill" style="width:75%; background:linear-gradient(90deg,#4f6df5,#3b55d4);"></div>
  </div>
  <span class="bar-val">Value</span>
</div>
```

### Highlight Box
```html
<div class="highlight-box">
  <strong>Key takeaway goes here</strong>
</div>
```

### Flow Diagram
```html
<div class="flow">
  <div class="flow-step">Step 1</div>
  <div class="flow-arrow">&rarr;</div>
  <div class="flow-step">Step 2</div>
  <div class="flow-arrow">&rarr;</div>
  <div class="flow-step">Step 3</div>
</div>
```

### Gradient Text
```html
<span style="background:linear-gradient(135deg,var(--accent-purple),var(--accent-blue));
  -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;">
  Accent Text
</span>
```

### Badge
```html
<span class="badge badge-blue">Tool Name</span>
<span class="badge badge-purple">Category</span>
```

### VS Comparison
```html
<div style="display:grid; grid-template-columns:1fr auto 1fr; gap:1em; align-items:center;">
  <div class="card" style="border-top:3px solid var(--accent-red);">
    <h4>Before</h4><p>Old way</p>
  </div>
  <span class="vs-text" style="font-size:1.5em; font-weight:700;">→</span>
  <div class="card" style="border-top:3px solid var(--accent-green);">
    <h4>After</h4><p>New way</p>
  </div>
</div>
```

### Phone Mockup
```html
<div style="width:280px; border:2px solid #e2e8f0; border-radius:24px; padding:8px; background:#f8fafc;">
  <div style="background:#1a202c; border-radius:16px; padding:12px; color:white; font-size:0.8em;">
    <!-- Status bar -->
    <div style="display:flex; justify-content:space-between; font-size:0.7em; opacity:0.6;">
      <span>9:41</span><span>LTE 📶 🔋</span>
    </div>
    <!-- Chat content -->
    <div style="margin-top:12px;">
      <div style="background:#2d3748; border-radius:12px; padding:8px 12px; margin:4px 0;">
        Message bubble
      </div>
    </div>
  </div>
</div>
```

### Terminal Mockup
```html
<div style="background:#1a1a2e; border-radius:8px; padding:16px; font-family:monospace; font-size:0.8em; color:#a0aec0;">
  <div style="margin-bottom:8px;">
    <span style="color:#68d391;">$</span> command here
  </div>
  <div>
    <span style="color:#63b3ed;">output</span> with
    <span style="color:#f6ad55;">colored</span> text
  </div>
</div>
```

## Navigation Script (slides.js)

Minimal scroll-snap navigation with keyboard support:
- IntersectionObserver tracks visible slide
- Arrow keys / Space / Home / End for navigation
- Progress bar auto-updates
- ~77 lines, zero dependencies

## Chart.js Patterns

### Line Chart with Annotation
```js
new Chart(ctx, {
  type: 'line',
  data: { datasets: [{ label: 'Trend', data: [...], borderColor: '#4f6df5' }] },
  options: {
    plugins: {
      annotation: {
        annotations: {
          line1: { type: 'line', yMin: 85, yMax: 85, borderColor: '#ef4444',
            borderDash: [6,6], label: { content: 'Baseline', display: true } }
        }
      }
    }
  }
});
```

### Cost/Scale Chart (Log Scale)
```js
options: { scales: { y: { type: 'logarithmic' } } }
```

## SVG Animation: Particle Flow
```svg
<circle r="3" fill="#4f6df5">
  <animateMotion dur="2s" repeatCount="indefinite" path="M0,0 L100,50"/>
  <animate attributeName="opacity" values=".9;.15;.9" dur="2s" repeatCount="indefinite"/>
</circle>
```
Vary `dur` per particle (2s-3.1s) for organic feel. Use bidirectional paths.
