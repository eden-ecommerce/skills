# Wireframes — publisher panel

Load **before Execute**. Fill per panel. **Stop until user OK.**

## Fill rules

- Replace `{_type}` with chosen `publisherCamelCase` literal
- Hub box: list only fields in schema (drop unused repeaters)
- PDP box: name layout (`static grid`, `carousel`, `FAQ`, `comparison`, etc.)
- Carousel section: skip if panel not carousel-like
- Max width: note `PANEL_MAX_WIDTH_PX` from design spec when relevant

## 1. Stack data flow

```
┌──────────────┐   GET /v1/panel/schemas   ┌─────────────────┐
│ API          │ ─────────────────────────►│ panelsRegistry  │
│ publisher*.ts│                           │ + assetId cases │
└──────┬───────┘                           └────────┬────────┘
       │                                            │
       │ panels-regen.sh                            │ copy generated/*
       ▼                                            ▼
┌──────────────┐  form + blockOptions   ┌──────────────────────┐
│ Hub          │ ───────────────────────►│ next-next-eden       │
│ generated/   │                         │ Renderer → registry  │
│ panels/      │                         │ PDP PublisherRenderer│
└──────┬───────┘                         └──────────────────────┘
       │
       │ props-only
       ▼
┌──────────────┐      stories       ┌─────────────┐
│ packages/ui  │ ◄─────────────────│ Storybook   │
│ storefront/* │                   │ publisher-  │
└──────────────┘                   │ panels/     │
                                   └─────────────┘
```

## 2. Hub editor

```
┌─ Add/Edit panel ({_type}) ──────────────────────────┐
│ Heading [______________________________]            │
│ Image   [ pick asset ]  Alt [___________]           │
│ ── optional repeaters ──                            │
│   • FAQ rows / spec rows / slides / hotspots        │
│                          [Cancel]  [Save]*          │
│ * disabled until dirty + valid                      │
└─────────────────────────────────────────────────────┘
```

## 3. Storefront PDP slot

```
┌─ Product page ──────────────────────────────────────┐
│  [hero / buy box]                                   │
│ ┌─ publisher panel ({_type}) ─────────────────────┐ │
│ │  heading                                        │ │
│ │  ┌──────────────────────────────────────────┐  │ │
│ │  │ static grid | carousel | FAQ | comparison │  │ │
│ │  └──────────────────────────────────────────┘  │ │
│ └─────────────────────────────────────────────────┘ │
│  [more panels…]                                     │
└─────────────────────────────────────────────────────┘
```

## 4. Carousel nav (if applicable)

```
navVariant dots:   (●)(○)(○)   [ slide ]
navVariant tabs:   [A][B][C]   [ pane ]
navVariant thumbs: [t][t][t]   [ main ]
navVariant steps:  1 — 2 — 3   [ step body ]
```

## Output format

Post in chat:

1. Filled wireframes (§1–4 as applicable)
2. `_type`, UI reuse decision, layer checklist (`end-to-end-checklist.md` phases)

Wait for explicit user OK. No code until OK.
