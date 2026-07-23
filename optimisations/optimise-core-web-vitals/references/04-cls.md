# CLS fix

Target: ≤ 0.1 p75. Unexpected layout shift during load.

## 1. Find culprit

Lighthouse/GTmetrix layout shift panel or Playwright CLS script (`08-verify.md`).

Common: images without reserved space, fonts, ads, late-injected chrome, iframe/embeds.

## 2. Images — reserve box

**Bad:** `width` + `height` attrs but `className="w-full h-auto"` — box not reserved before decode.

**Good:**

```tsx
<div style={{ aspectRatio: `${width} / ${height}` }} className="relative w-full">
  <img src={src} alt={alt} width={width} height={height} className="size-full object-contain" />
</div>
```

Next: `fill` inside aspect-ratio wrapper; never bare `h-auto` on body images.

## 3. Fonts

- `font-display: swap` or optional
- Reserve line box: `min-h` on headings if swap shifts layout
- Preload critical `@font-face` files

## 4. Dynamic chrome — loading shells

Async layout chrome (footer, sidebar) racing main content → shift.

**Fix:**

- Viewport shell while route suspends: `min-h-dvh` on `loading.tsx` fallback
- Mirror final layout dimensions in skeleton (max-width, padding, grid)
- Chrome **after** main content in DOM stream order

```tsx
<div className="flex min-h-screen flex-col">
  <div className="flex-1 flex-col">{children}</div>
  {/* footer here, not sibling above empty flex-1 */}
</div>
```

## 5. Embeds / third-party

- `aspect-video` (or known ratio) wrapper for iframes
- Reserve ad slot height before script loads
- Defer non-critical widgets below fold

## 6. Animations

Non-composited animations (width/height/top) → CLS. Prefer `transform` + `opacity`.

## 7. Eden fleet appendix

Footer stream-order, `SanityFooter`, TrustPilot min-height → `appendix-eden-footer.md`.
