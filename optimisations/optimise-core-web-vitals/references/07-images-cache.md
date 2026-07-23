# Images + cache

LCP bytes + CLS reservation + CDN cache.

## 1. Size — serve right pixels

Display width ≠ source width → waste LCP duration.

**Sanity CDN** ([image URLs](https://www.sanity.io/docs/apis-and-sdks/image-urls)):

```text
?w=800&fit=max&auto=format&q=75
```

| Param | Use |
|-------|-----|
| `w` / `h` | Integer px — match `sizes` breakpoint |
| `fit=max` | Never upscale small assets |
| `auto=format` | WebP/AVIF per Accept |
| `q` | 75 default; lower for thumbs |

Next fleet: `unoptimized={true}` on `next/image` — **must** size at CDN URL builder, not full-res Sanity URL.

## 2. `sizes` + srcset

```tsx
<Image
  src={sanityImageUrl(asset, { width: 800 })}
  sizes="(max-width: 768px) 100vw, 672px"
  width={800}
  height={450}
  unoptimized
/>
```

Wrong `sizes` → browser picks oversized file.

## 3. CLS — reserve space

Explicit `width` + `height` on every image. Aspect-ratio wrapper when `fill` or fluid width.

No `h-auto` on content images without reserved box. See `04-cls.md`.

## 4. LCP image

- No `loading="lazy"` on LCP candidate
- `fetchpriority="high"` when supported
- Preload if discovered late: `<link rel="preload" as="image" href="…">`

## 5. Cache headers

**Page HTML:** `no-cache` — always revalidate entry document.

**Fingerprinted assets:** `public, max-age=31536000, immutable`.

**CDN images:** Sanity/Vercel CDN default long cache; bust via new URL (`w`, hash), not query spam.

Verify:

```bash
curl -sI "<image-url>" | rg -i cache-control
```

## 6. Static vs CMS

- `@public` import for static — hashed by bundler
- CMS → URL builder with `w` + `auto=format`; never raw multi-MB asset ref in `src`
