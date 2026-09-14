# Design Document: The Lenny Growth Assistant

## Executive Summary

The Lenny Growth Assistant requires a **distinctive, polished UI** that differentiates it from generic AI chatbots. The design combines the editorial quality of a premium research product with the functionality of a modern product workspace. The visual language should feel professional, intelligent, and purposeful—appropriate for product and growth professionals conducting serious research.

**Core Design Principle**: *This is a knowledge assistant for professionals, not a consumer chatbot.*

---

## Table of Contents

1. [Design Philosophy](#design-philosophy)
2. [Visual Identity](#visual-identity)
3. [Typography](#typography)
4. [Color System](#color-system)
5. [Spacing & Layout](#spacing--layout)
6. [Component Design](#component-design)
7. [Information Architecture](#information-architecture)
8. [Conversational Experience](#conversational-experience)
9. [Source Citation Design](#source-citation-design)
10. [Artifact Viewer](#artifact-viewer)
11. [States & Feedback](#states--feedback)
12. [Responsive Design](#responsive-design)
13. [Accessibility](#accessibility)
14. [Design System](#design-system)
15. [Differentiation from Generic Chatbots](#differentiation-from-generic-chatbots)

---

## Design Philosophy

### Core Principles

1. **Editorial Quality Over Playfulness**
   - Professional, not cutesy
   - Confidence through clarity
   - Typography-first design

2. **Information Density Without Clutter**
   - Surface relevant context
   - Hide complexity behind progressive disclosure
   - Every pixel serves a purpose

3. **Trust Through Transparency**
   - Always show sources
   - Make AI reasoning visible
   - Clear model/provider indicators

4. **Calm Technology**
   - Subtle animations
   - Quiet colors
   - Focus-friendly environment

5. **Memorable but Not Trendy**
   - Distinctive without gimmicks
   - Timeless over trendy
   - Professional over casual

---

## Visual Identity

### Brand Positioning

**The Lenny Growth Assistant** positions at the intersection of:
- **Premium Editorial**: Think *The Economist*, *Stratechery*
- **Product Workspace**: Think *Linear*, *Notion*
- **Research Tool**: Think *Perplexity*, *You.com* (but more refined)

### Visual Inspiration (Conceptual)

**DO:**
- Editorial layouts with strong typography
- Minimalist product tools with excellent hierarchy
- Professional research interfaces with clear source attribution

**DON'T:**
- Consumer chatbots (ChatGPT, Character.ai)
- Overly colorful/playful interfaces
- Generic Bootstrap/Material UI templates
- Excessive glassmorphism or gradients

### Key Visual Elements

1. **Strong Typography Hierarchy**
   - Clear headline/body distinction
   - Strategic font weight variation
   - Generous line height for readability

2. **Subtle Depth**
   - Soft shadows (not drop shadows)
   - Layered elevation
   - Borders for definition

3. **Purposeful Color**
   - Monochromatic base (grays/blacks)
   - Single accent color for key actions
   - Color used sparingly for meaning

4. **Whitespace as a Feature**
   - Breathing room around content
   - Distinct content blocks
   - Never cramped

---

## Typography

### Font Stack

**Primary**: System fonts for performance and native feel

```css
font-family: 
  -apple-system, 
  BlinkMacSystemFont, 
  'SF Pro Display',
  'Segoe UI', 
  'Roboto', 
  'Helvetica Neue', 
  Arial, 
  sans-serif;
```

**Why System Fonts**:
- ✅ Native feel on each platform
- ✅ Excellent readability
- ✅ Zero load time
- ✅ Professional appearance

**Alternative** (if custom font desired):
- **Inter**: Modern, highly readable, designed for screens
- **Söhne**: Similar to system fonts but distinctive
- **Roobert**: Clean, professional, slightly warmer

### Type Scale

```css
/* Display - Product name, major headings */
--text-display: 32px / 40px (line-height)
--font-weight: 600

/* Headline - Section headers */
--text-headline: 20px / 28px
--font-weight: 600

/* Body - Main content, messages */
--text-body: 15px / 24px
--font-weight: 400

/* Body Emphasis - Important body text */
--text-body-emphasis: 15px / 24px
--font-weight: 500

/* Small - Metadata, timestamps */
--text-small: 13px / 20px
--font-weight: 400

/* Tiny - Labels, captions */
--text-tiny: 11px / 16px
--font-weight: 500
--letter-spacing: 0.02em
--text-transform: uppercase
```

### Typography Rules

1. **Never use decorative fonts** for body text
2. **Line length**: Max 65 characters (approximately 680px)
3. **Line height**: 1.6 for body, 1.25 for headings
4. **Font weight**: Regular (400) for body, Medium (500) for emphasis, Semibold (600) for headings
5. **Letter spacing**: Slight tracking (+0.02em) for uppercase labels only

---

## Color System

### Base Colors (Monochrome Foundation)

```css
/* Background Layers */
--color-bg-primary: #FFFFFF       /* Main canvas */
--color-bg-secondary: #F8F9FA     /* Sidebar, secondary surfaces */
--color-bg-tertiary: #F1F3F5      /* Hover states, subtle backgrounds */

/* Text Colors */
--color-text-primary: #1A1D1F     /* Main content */
--color-text-secondary: #6C7380   /* Metadata, supporting text */
--color-text-tertiary: #9FA4AD    /* Disabled, least important */

/* Border Colors */
--color-border-primary: #E5E7EB   /* Main dividers */
--color-border-secondary: #F1F3F5 /* Subtle separators */
--color-border-focus: #3B82F6     /* Focus states */

/* Surface Colors */
--color-surface-base: #FFFFFF     /* Cards, panels */
--color-surface-hover: #F8F9FA    /* Hover surfaces */
--color-surface-active: #F1F3F5   /* Active/pressed surfaces */
```

### Accent Colors (Purposeful Highlights)

```css
/* Primary Accent - Key actions */
--color-primary: #2563EB          /* Vibrant blue */
--color-primary-hover: #1D4ED8
--color-primary-active: #1E40AF

/* Semantic Colors */
--color-success: #059669          /* Success states */
--color-warning: #D97706          /* Warnings */
--color-error: #DC2626            /* Errors */
--color-info: #0891B2             /* Informational */
```

### Source Citation Accent

```css
--color-source-bg: #FEF3C7        /* Soft amber background */
--color-source-border: #F59E0B    /* Amber border */
--color-source-text: #92400E      /* Dark amber text */
```

**Why Amber**: 
- Connotes research/highlighting
- Distinct from primary blue
- Professional, not distracting

### AI Message Accent (Subtle)

```css
--color-ai-bg: #F0F9FF            /* Lightest blue */
--color-ai-border: #BFDBFE        /* Soft blue border */
```

### Dark Mode (Optional, Phase 2)

If time permits:

```css
--color-bg-primary: #0F1419
--color-bg-secondary: #1A1F2E
--color-text-primary: #E5E7EB
--color-text-secondary: #9FA4AD
--color-primary: #3B82F6
```

---

## Spacing & Layout

### Spacing Scale (Base-4)

```css
--space-1: 4px    /* Tight spacing */
--space-2: 8px    /* Close spacing */
--space-3: 12px   /* Default small gap */
--space-4: 16px   /* Standard spacing */
--space-5: 20px   /* Comfortable spacing */
--space-6: 24px   /* Medium gap */
--space-8: 32px   /* Large gap */
--space-10: 40px  /* Extra large gap */
--space-12: 48px  /* Section spacing */
--space-16: 64px  /* Major section spacing */
```

### Layout Grid

```
┌─────────────────────────────────────────────────────────────┐
│                        Header (64px)                         │
│  Logo/Title                              Model Indicator     │
├──────────────┬──────────────────────────────────────────────┤
│              │                                               │
│   Sidebar    │          Main Content Area                   │
│   (280px)    │          (Flexible)                          │
│              │                                               │
│  Sessions    │  ┌─────────────────────────────────────┐    │
│  List        │  │                                      │    │
│              │  │     Conversation Messages            │    │
│  + New Chat  │  │                                      │    │
│              │  │                                      │    │
│              │  └─────────────────────────────────────┘    │
│              │                                               │
│              │  [  Message Input Composer  ]  [Send]        │
│              │                                               │
└──────────────┴──────────────────────────────────────────────┘
```

**With Artifact Open**:

```
┌─────────────────────────────────────────────────────────────┐
│                        Header (64px)                         │
├──────────────┬─────────────────────┬───────────────────────┤
│              │                     │                        │
│   Sidebar    │   Conversation      │   Artifact Viewer     │
│   (280px)    │   (Flexible)        │   (500px)             │
│              │                     │                        │
│  Sessions    │   Messages          │   [Rendered HTML]     │
│  List        │                     │                        │
│              │                     │                        │
│  + New Chat  │   Composer          │                        │
│              │                     │                        │
└──────────────┴─────────────────────┴───────────────────────┘
```

### Container Widths

```css
--container-narrow: 680px    /* Reading width for messages */
--container-medium: 920px    /* Comfortable content width */
--container-wide: 1400px     /* Full app width */
```

---

## Component Design

### Button Styles

```css
/* Primary Button */
.button-primary {
  background: var(--color-primary);
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 500;
  font-size: 15px;
  border: none;
  cursor: pointer;
  transition: background 150ms ease;
}

.button-primary:hover {
  background: var(--color-primary-hover);
}

/* Secondary Button */
.button-secondary {
  background: transparent;
  color: var(--color-text-primary);
  border: 1px solid var(--color-border-primary);
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 500;
}

/* Ghost Button */
.button-ghost {
  background: transparent;
  color: var(--color-text-secondary);
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
}

.button-ghost:hover {
  background: var(--color-bg-tertiary);
}
```

### Input Fields

```css
.input {
  background: var(--color-bg-primary);
  border: 1.5px solid var(--color-border-primary);
  border-radius: 8px;
  padding: 12px 16px;
  font-size: 15px;
  color: var(--color-text-primary);
  transition: border-color 150ms ease;
}

.input:focus {
  outline: none;
  border-color: var(--color-border-focus);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.input::placeholder {
  color: var(--color-text-tertiary);
}
```

### Cards

```css
.card {
  background: var(--color-surface-base);
  border: 1px solid var(--color-border-primary);
  border-radius: 12px;
  padding: var(--space-6);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.card:hover {
  border-color: var(--color-border-focus);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 200ms ease;
}
```

---

## Information Architecture

### Top-Level Navigation

```
┌─────────────────────────────────────────────────┐
│  🔷 The Lenny Growth Assistant    [Model: ...]  │
└─────────────────────────────────────────────────┘
```

**Header Elements**:
- Left: Logo/Product Name
- Right: Model Indicator (provider + model name)
- Optional: Settings icon (if time permits)

### Sidebar Structure

```
┌──────────────────┐
│                  │
│  + New Chat      │ ← Primary CTA
│                  │
│  ───────────     │
│                  │
│  Today           │ ← Temporal grouping
│  • Session 1     │
│  • Session 2     │
│                  │
│  Yesterday       │
│  • Session 3     │
│                  │
│  Last 7 Days     │
│  • Session 4     │
│  • Session 5     │
│                  │
└──────────────────┘
```

**Session Item**:
```
┌─────────────────────────────┐
│ How to improve retention?   │ ← First message preview
│ 12 messages · 2h ago        │ ← Metadata
└─────────────────────────────┘
```

### Main Content Hierarchy

```
┌──────────────────────────────────────┐
│                                      │
│  [Empty State / Messages]            │
│                                      │
│                                      │
│                                      │
│                                      │
├──────────────────────────────────────┤
│  [Message Composer]                  │
│  Type your question...               │
│  ──────────────────────  [Send]      │
└──────────────────────────────────────┘
```

---

## Conversational Experience

### Empty State

**Goal**: Immediately communicate value and provide starting points

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│            🔷                                       │
│       The Lenny Growth Assistant                   │
│                                                     │
│   Your research assistant for product and growth   │
│   strategy, grounded in Lenny Rachitsky's podcast │
│   library.                                         │
│                                                     │
│   ─────────────────────────────────────────────    │
│                                                     │
│   Try asking:                                      │
│                                                     │
│   ┌───────────────────────────────────────────┐  │
│   │ How should a startup improve retention?   │  │
│   └───────────────────────────────────────────┘  │
│                                                     │
│   ┌───────────────────────────────────────────┐  │
│   │ What does product-market fit look like?   │  │
│   └───────────────────────────────────────────┘  │
│                                                     │
│   ┌───────────────────────────────────────────┐  │
│   │ Turn this into a Ship 30 essay            │  │
│   └───────────────────────────────────────────┘  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Design Details**:
- Centered vertically and horizontally
- Large product icon/logo
- Clear value proposition
- 3-4 example prompts as clickable cards
- Soft background (not stark white)

### Message Bubble Design

**User Message**:
```
┌────────────────────────────────────────────┐
│ How should a startup improve retention?    │
│                                 10:30 AM   │
└────────────────────────────────────────────┘
```

**Design**:
- Aligned right
- Background: `var(--color-bg-tertiary)`
- No avatar (single-user context)
- Timestamp subtle, right-aligned

**Assistant Message**:
```
┌─────────────────────────────────────────────────────────┐
│ 🔷                                                      │
│                                                         │
│ Based on Lenny's conversation with Casey Winters and   │
│ other growth leaders, here are key retention           │
│ strategies:                                            │
│                                                         │
│ 1. **Define your core action**: Identify what action   │
│    truly correlates with long-term retention...        │
│                                                         │
│ 2. **Optimize onboarding to that action**: The faster  │
│    users complete the core action, the more likely...  │
│                                                         │
│ [Continue reading...]                                  │
│                                                         │
│ ───────────────────────────────────────────────────    │
│                                                         │
│ Sources:                                               │
│                                                         │
│ ┌────────────────────────────────────────────────┐    │
│ │ 📄 Building Growth Engines                      │    │
│ │ With Casey Winters                              │    │
│ │                                                 │    │
│ │ "The key to retention is getting users to the  │    │
│ │  core value as quickly as possible..."         │    │
│ └────────────────────────────────────────────────┘    │
│                                                         │
│                              ollama · llama3.2  10:31  │
└─────────────────────────────────────────────────────────┘
```

**Design**:
- Aligned left
- Small icon/logo top-left
- Background: `var(--color-ai-bg)` (very subtle)
- Clear separation from user messages
- Model/provider indicator bottom-right (subtle)

### Message Composer

```
┌─────────────────────────────────────────────────────────┐
│  Type your question...                                  │
│                                                   [Send]│
└─────────────────────────────────────────────────────────┘
```

**Features**:
- Auto-expanding textarea
- Max height with scroll
- Send button always visible
- Keyboard shortcut: ⌘/Ctrl+Enter
- Focus state: blue border glow
- Disabled state when generating

**Enhanced Version** (if time):
```
┌─────────────────────────────────────────────────────────┐
│  Type your question...                                  │
│                                                         │
│  ──────────────────────────────────────────────────    │
│  [📎]  [✨ Ship 30]  [🎨 Artifact]           [Send]   │
└─────────────────────────────────────────────────────────┘
```

---

## Source Citation Design

### Source Card

```
┌──────────────────────────────────────────────────────┐
│ 📄 Building Growth Engines with Casey Winters        │
│                                                      │
│ "The key to retention is getting users to the core  │
│ value as quickly as possible. Everything else in    │
│ onboarding should serve that single goal."          │
│                                                      │
│ Episode 045 · March 2023                            │
└──────────────────────────────────────────────────────┘
```

**Design Details**:
- Background: `var(--color-source-bg)` (soft amber)
- Border: `var(--color-source-border)` (amber accent)
- Icon: Document or microphone emoji
- Episode title: Bold, 15px
- Guest name: Included in title if available
- Excerpt: Italicized quote, 14px
- Metadata: Small gray text, 12px

**Hover State**:
- Slight elevation (shadow)
- Cursor: pointer (if clickable)
- Border darkens slightly

**Compact Version** (multiple sources):
```
┌────────────────────────────────────────┐
│ 📄 Building Growth Engines             │
│    Casey Winters · Episode 045         │
└────────────────────────────────────────┘
```

### Source List

When multiple sources:

```
Sources (3):

┌────────────────────────┐  ┌────────────────────────┐
│ 📄 Episode 045         │  │ 📄 Episode 078         │
│ Casey Winters          │  │ Elena Verna            │
└────────────────────────┘  └────────────────────────┘

┌────────────────────────┐
│ 📄 Episode 102         │
│ Lenny's Newsletter     │
└────────────────────────┘
```

**Layout**: 
- Grid (2 columns on desktop, 1 on mobile)
- Gap: `var(--space-4)`

---

## Artifact Viewer

### Panel Layout

**Closed State**: Artifact viewer hidden

**Open State**: Artifact viewer slides in from right

```
┌─────────────────────────┬─────────────────────────────┐
│                         │  ┌──────────────────────┐  │
│   Conversation          │  │ Artifact Viewer       │  │
│                         │  │                       │  │
│   [Messages]            │  │ ╔═══════════════════╗ │  │
│                         │  │ ║  [Rendered HTML]  ║ │  │
│                         │  │ ║                   ║ │  │
│                         │  │ ║                   ║ │  │
│                         │  │ ║                   ║ │  │
│                         │  │ ╚═══════════════════╝ │  │
│                         │  │                       │  │
│                         │  │  [< Code]  [Preview]  │  │
│                         │  └──────────────────────┘  │
│   [Composer]            │                             │
└─────────────────────────┴─────────────────────────────┘
```

### Artifact Viewer Header

```
┌──────────────────────────────────────────────────────┐
│  Growth Strategy Dashboard          [Code] [Preview] │
│  HTML Artifact · Generated 10:35 AM          [✕]    │
└──────────────────────────────────────────────────────┘
```

**Elements**:
- Title: Artifact title (from metadata)
- Type indicator: "HTML Artifact" or "Markdown Document"
- Timestamp
- Toggle: Code view / Preview
- Close button (X)

### Artifact Content Area

**Preview Mode**:
```
┌──────────────────────────────────────────────────────┐
│ ╔════════════════════════════════════════════════╗  │
│ ║                                                ║  │
│ ║          [Sandboxed HTML Rendering]            ║  │
│ ║                                                ║  │
│ ║          (iframe with sandbox)                 ║  │
│ ║                                                ║  │
│ ║                                                ║  │
│ ╚════════════════════════════════════════════════╝  │
└──────────────────────────────────────────────────────┘
```

**Code Mode**:
```
┌──────────────────────────────────────────────────────┐
│  <!DOCTYPE html>                                     │
│  <html>                                              │
│  <head>                                              │
│    <title>Growth Strategy</title>                   │
│    <style>                                           │
│      body { font-family: sans-serif; }              │
│    </style>                                          │
│  </head>                                             │
│  ...                                                 │
│                                                      │
│  [Copy Code]                                         │
└──────────────────────────────────────────────────────┘
```

**Syntax Highlighting**: Use Prism.js or similar

### Artifact Trigger Indicator

When artifact is generated, show clear visual feedback in chat:

```
┌─────────────────────────────────────────────────────┐
│ 🔷 I've created a growth strategy dashboard for you │
│                                                     │
│ ┌────────────────────────────────────────────┐    │
│ │  🎨  Growth Strategy Dashboard             │    │
│ │      HTML Artifact                         │    │
│ │                                            │    │
│ │      [View Artifact →]                     │    │
│ └────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

**On Click**: Opens artifact viewer panel

---

## States & Feedback

### Loading States

**Message Loading**:
```
┌─────────────────────────────────────────┐
│ 🔷                                      │
│                                         │
│ ● ● ● (animated dots)                  │
│                                         │
│ Searching Lenny's transcripts...       │
└─────────────────────────────────────────┘
```

**Stages** (optional):
1. "Searching transcripts..."
2. "Generating response..."
3. "Citing sources..."

**Design**: 
- Subtle animation (pulsing dots)
- Progress indicator if deterministic
- Never static "Loading..."

### Error States

**LLM Unavailable**:
```
┌──────────────────────────────────────────────────────┐
│ ⚠️  Unable to connect to Ollama                     │
│                                                      │
│ Please ensure Ollama is running:                    │
│                                                      │
│ 1. Check that Ollama is installed                   │
│ 2. Run: ollama serve                                │
│ 3. Verify model is downloaded: ollama list          │
│                                                      │
│ [View Troubleshooting Guide]    [Retry]             │
└──────────────────────────────────────────────────────┘
```

**Design**:
- Amber warning color
- Clear, actionable instructions
- Link to troubleshooting docs
- Retry button

**Insufficient Evidence**:
```
┌─────────────────────────────────────────────────────┐
│ 🔷                                                  │
│                                                     │
│ I don't have enough information in Lenny's         │
│ transcripts to answer this confidently.            │
│                                                     │
│ The available content doesn't specifically address │
│ [topic]. Would you like to ask about a related     │
│ topic that's covered in the podcast library?       │
│                                                     │
│ You might ask about:                               │
│ • Product-market fit                               │
│ • User retention strategies                        │
│ • Growth loops                                     │
└─────────────────────────────────────────────────────┘
```

### Empty States

**No Sessions**:
```
┌──────────────────────────┐
│                          │
│     📚                   │
│                          │
│  No conversations yet    │
│                          │
│  Click "New Chat" to     │
│  start researching       │
│                          │
└──────────────────────────┘
```

**No Sources Found**:
```
┌─────────────────────────────────┐
│ 🔍 No sources found             │
│                                 │
│ This response doesn't cite any │
│ specific transcript excerpts.  │
└─────────────────────────────────┘
```

---

## Responsive Design

### Breakpoints

```css
/* Mobile */
@media (max-width: 640px) { ... }

/* Tablet */
@media (min-width: 641px) and (max-width: 1024px) { ... }

/* Desktop */
@media (min-width: 1025px) { ... }
```

### Mobile Layout (< 640px)

```
┌──────────────────────────┐
│ ☰  Lenny Assistant  [•] │ ← Header (hamburger menu)
├──────────────────────────┤
│                          │
│   Conversation           │
│                          │
│   [Messages]             │
│                          │
│                          │
│                          │
├──────────────────────────┤
│ [Message Composer]       │
└──────────────────────────┘
```

**Mobile Changes**:
- Sidebar becomes drawer (opens from left)
- Artifact viewer becomes full-screen modal
- Source cards stack vertically
- Reduced padding (16px → 12px)
- Smaller font sizes (15px → 14px for body)

### Tablet Layout (641px - 1024px)

```
┌────────┬──────────────────┐
│        │                  │
│ Sidebar│  Conversation    │
│ (240px)│                  │
│        │                  │
│        │                  │
│        │                  │
└────────┴──────────────────┘
```

**Tablet Changes**:
- Narrower sidebar (280px → 240px)
- Artifact viewer becomes modal (not side-by-side)
- Source cards: 1 column instead of 2

### Desktop Layout (> 1024px)

Full layout as designed in Layout Grid section above.

---

## Accessibility

### Keyboard Navigation

**Essential Shortcuts**:
- `Tab`: Navigate through interactive elements
- `Shift+Tab`: Navigate backwards
- `Enter`: Activate buttons, send message
- `Cmd/Ctrl+Enter`: Send message from composer
- `Escape`: Close modals/artifact viewer
- `/`: Focus message composer
- `Cmd/Ctrl+K`: New chat (optional)

**Focus Indicators**:
```css
*:focus-visible {
  outline: 2px solid var(--color-border-focus);
  outline-offset: 2px;
  border-radius: 4px;
}
```

### Screen Reader Support

**Semantic HTML**:
```html
<nav aria-label="Session history">
  <button aria-label="New chat">+ New Chat</button>
  <ul>
    <li>
      <a href="/session/123" aria-label="Chat from 2 hours ago: How to improve retention?">
        How to improve retention?
      </a>
    </li>
  </ul>
</nav>

<main aria-label="Conversation">
  <article role="article" aria-label="Assistant message">
    <div aria-label="Message content">...</div>
    <aside aria-label="Sources">...</aside>
  </article>
</main>

<form aria-label="Message composer">
  <label for="message-input" class="sr-only">Type your question</label>
  <textarea id="message-input" aria-label="Message input"></textarea>
  <button type="submit" aria-label="Send message">Send</button>
</form>
```

**ARIA Labels**:
- All buttons have descriptive labels
- Loading states announce progress
- Errors announce with `aria-live="assertive"`
- Success messages with `aria-live="polite"`

### Color Contrast

**WCAG AA Compliance** (minimum):
- Normal text: 4.5:1 ratio
- Large text (18px+): 3:1 ratio
- Interactive elements: 3:1 ratio

**Verified Contrasts**:
- `#1A1D1F` on `#FFFFFF`: 16.3:1 ✓
- `#6C7380` on `#FFFFFF`: 5.8:1 ✓
- `#2563EB` on `#FFFFFF`: 6.4:1 ✓

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Design System

### Component Library

Create reusable components:

```
components/
├── Button/
│   ├── Button.tsx
│   ├── Button.module.css
│   └── Button.stories.tsx (if using Storybook)
├── Input/
├── Card/
├── MessageBubble/
├── SourceCard/
├── SessionSidebar/
├── ArtifactViewer/
├── ModelIndicator/
└── ...
```

### Design Tokens (CSS Variables)

```css
:root {
  /* Colors */
  --color-bg-primary: #FFFFFF;
  --color-bg-secondary: #F8F9FA;
  /* ... all colors ... */
  
  /* Spacing */
  --space-1: 4px;
  --space-2: 8px;
  /* ... all spacing ... */
  
  /* Typography */
  --text-display: 32px;
  --text-headline: 20px;
  /* ... all text styles ... */
  
  /* Borders */
  --border-radius-sm: 6px;
  --border-radius-md: 8px;
  --border-radius-lg: 12px;
  
  /* Shadows */
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.04);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.12);
  
  /* Transitions */
  --transition-fast: 150ms ease;
  --transition-base: 200ms ease;
  --transition-slow: 300ms ease;
}
```

### TailwindCSS Configuration (Optional)

If using Tailwind, extend with design tokens:

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        'bg-primary': '#FFFFFF',
        'bg-secondary': '#F8F9FA',
        // ... map all design tokens
      },
      spacing: {
        // Map to base-4 scale
      }
    }
  }
}
```

---

## Differentiation from Generic Chatbots

### ❌ Generic ChatGPT Clone (What NOT to Build)

```
┌────────────────────────────────────────┐
│ ChatGPT                    [New Chat]  │ ← Generic branding
├──────┬─────────────────────────────────┤
│      │                                 │
│ Chat │  Generic rounded chat bubbles   │ ← Basic bubbles
│ 1    │  with no clear hierarchy        │
│ Chat │                                 │
│ 2    │  💬 User: Question              │ ← Emoji spam
│ Chat │  🤖 AI: Generic answer          │
│ 3    │                                 │
│      │  No sources, no context         │ ← Missing sources
│      │                                 │
│      │  [ Type a message... ]  [Send]  │
└──────┴─────────────────────────────────┘
```

**Problems**:
- Generic blue gradient background
- ChatGPT-style rounded bubbles
- No source attribution
- Random AI sparkle icons
- Plain white background
- No visual hierarchy
- Feels like a template

### ✅ The Lenny Growth Assistant (What to Build)

```
┌──────────────────────────────────────────────────────────┐
│ 🔷 The Lenny Growth Assistant      ollama · llama3.2:3b  │
├──────────────┬───────────────────────────────────────────┤
│              │                                           │
│ + New Chat   │  Clean, editorial layout                 │
│              │  with strong typography                  │
│ ──────────   │                                           │
│              │  ┌─────────────────────────────────────┐ │
│ Today        │  │ User message (right-aligned)        │ │
│ • Retention  │  └─────────────────────────────────────┘ │
│              │                                           │
│ Yesterday    │  ┌─────────────────────────────────────┐ │
│ • PMF Guide  │  │ 🔷 Assistant response with clear    │ │
│              │  │    hierarchy and source citations   │ │
│              │  │                                     │ │
│              │  │ ┌────────────────────────────────┐ │ │
│              │  │ │ 📄 Source: Episode with Casey  │ │ │
│              │  │ │    Winters (amber highlight)   │ │ │
│              │  │ └────────────────────────────────┘ │ │
│              │  └─────────────────────────────────────┘ │
│              │                                           │
│              │  [  Focused message composer  ]  [Send]  │
└──────────────┴───────────────────────────────────────────┘
```

**Distinctive Elements**:

1. **Professional Branding**
   - Custom logo/icon (🔷 as placeholder)
   - Distinctive product name
   - Clear model indicator

2. **Editorial Typography**
   - Strong hierarchy (display, headline, body)
   - Generous line height (1.6)
   - Professional font stack

3. **Source Attribution**
   - Amber-highlighted source cards
   - Episode titles and guests
   - Clear visual separation

4. **Purposeful Layout**
   - Organized sidebar with temporal grouping
   - Clean message design (not generic bubbles)
   - Whitespace as design element

5. **Thoughtful Details**
   - Session titles from first message
   - Message count and timestamp
   - Model/provider visibility
   - Calm, professional color palette

---

## Animation & Motion

### Animation Principles

1. **Purposeful, Not Decorative**
   - Animations guide attention
   - Provide feedback
   - Communicate state changes

2. **Fast and Subtle**
   - Duration: 150-300ms
   - Easing: Ease-out for entrances, ease-in for exits
   - No bouncing or elastic effects

3. **Reduced Motion Support**
   - Respect `prefers-reduced-motion`
   - Essential feedback only

### Key Animations

**Message Appearance**:
```css
.message-enter {
  opacity: 0;
  transform: translateY(8px);
}

.message-enter-active {
  opacity: 1;
  transform: translateY(0);
  transition: all 200ms ease-out;
}
```

**Artifact Viewer Slide-In**:
```css
.artifact-enter {
  transform: translateX(100%);
}

.artifact-enter-active {
  transform: translateX(0);
  transition: transform 300ms ease-out;
}
```

**Loading Dots**:
```css
@keyframes pulse {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 1; }
}

.loading-dot {
  animation: pulse 1.5s infinite;
}

.loading-dot:nth-child(2) {
  animation-delay: 0.2s;
}

.loading-dot:nth-child(3) {
  animation-delay: 0.4s;
}
```

---

## Implementation Notes

### Phase 5 Priorities

1. **Core Layout** (2 hours)
   - Header, sidebar, main area
   - Responsive grid
   - Basic navigation

2. **Message Components** (2 hours)
   - User/assistant message bubbles
   - Message composer
   - Loading states

3. **Source Display** (1 hour)
   - Source card component
   - Source list layout

4. **Design System** (1 hour)
   - CSS variables
   - Button/input components
   - Typography styles

5. **Empty/Error States** (30 min)
   - Empty conversation state
   - Error messages
   - Loading indicators

6. **Artifact Viewer** (Phase 7, 2 hours)
   - Panel layout
   - Sandboxed rendering
   - Code/preview toggle

### Testing Checklist

- [ ] Test on Chrome, Safari, Firefox
- [ ] Test responsive breakpoints (mobile, tablet, desktop)
- [ ] Test keyboard navigation
- [ ] Test focus indicators
- [ ] Test color contrast (WCAG AA)
- [ ] Test reduced motion preference
- [ ] Test long content (message overflow, sidebar overflow)
- [ ] Test empty states
- [ ] Test error states
- [ ] Test artifact rendering (various HTML samples)

---

## Inspiration References

**Editorial Design**:
- The Economist digital edition
- Stratechery blog
- Substack premium publications

**Product Workspaces**:
- Linear (clean, purposeful)
- Notion (organized, hierarchical)
- Figma (professional, focused)

**Research Tools**:
- Perplexity AI (source citations)
- You.com (source cards)
- Elicit (academic paper summaries)

**Note**: Do not copy these interfaces directly. Use as conceptual inspiration for professionalism and clarity.

---

**Document Version**: 1.0  
**Last Updated**: Phase 0 - Initial Planning  
**Status**: Ready for Implementation
