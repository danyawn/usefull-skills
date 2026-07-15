---
name: dashboard-ux
description: Build or refine operational, finance, admin, and analytics dashboards that are concise, decision-first, self-explanatory, terminology-faithful, and easy to scan. Use for dashboard pages, KPI summaries, data tables, reporting views, and dashboard redesigns—especially when the UI is too wordy, card-heavy, dependent on instructional prose, inconsistent with the product vocabulary, generic, overly spacious, or visually decorative.
---

# Dashboard UX

Build an interface for an operator to make a decision or take an action—not a landing page about the dashboard. Let the interface explain itself through hierarchy, familiar patterns, precise labels, visible state, and immediate feedback. Treat explanatory prose as a signal to improve the interaction first.

## Workflow

1. Identify the operator, the decision they need to make, the primary action, and the selected scope (period, unit, status, or role). Ask only if the answer changes the information hierarchy.
2. Extract the product vocabulary before writing copy. Search existing user-facing navigation, routes, forms, tables, domain documentation, types, enums, tests, and fixtures for established entity names, statuses, and actions.
3. Inventory every proposed title, label, status, metric, instruction, and alert. Assign each fact one canonical location and delete repetitions before designing containers.
4. Sketch the page zones before styling: context/actions, headline signals, analysis, and detail. Prefer a table or drill-down for detail over adding every datum to the first viewport.
5. Implement with the project’s existing component system. For React apps, use the available component, React-performance, and browser-testing skills when relevant.
6. Test the real page at desktop and narrow widths with populated, empty, loading, and error states. Fix the highest-impact scanning, overflow, terminology, and accessibility failures before polishing.

## Self-Explanatory Interaction Rules

- Before adding helper copy, improve the label, control choice, placement, grouping, hierarchy, default value, affordance, or feedback. Redesign the interaction when removing an instructional paragraph makes the task unclear.
- Make the current scope, selected state, available action, disabled state, validation result, and action outcome visible at the point of use. Do not explain elsewhere what the interface can show directly.
- Use explicit action labels and familiar controls. Avoid unfamiliar icon-only actions, ambiguous nouns as buttons, and custom interaction patterns that require instructions.
- Show requirements and validation beside the affected control. Explain destructive, irreversible, exceptional, or legally significant consequences briefly at the decision point.
- Put advanced or rarely needed domain explanation behind progressive disclosure. Do not use tooltips to rescue unclear primary controls or hide information required to complete the task.
- Preserve accessibility while reducing copy. Self-explanatory means understandable through visible structure and semantics, not unlabeled minimalism.

## Content Rules

- Treat product terminology as an interface contract. Reuse the exact established user-facing noun, status, action, capitalization, abbreviation, and language across headings, metrics, filters, tables, and dialogs.
- Never invent an umbrella term, synonym, translation, abbreviation, or relational label merely to make copy shorter. Do not turn database relations, variable names, or implementation concepts into user-facing vocabulary.
- Resolve terminology in this order: explicit user wording or product glossary; domain documentation; repeated user-facing product copy; domain types and enums. If trustworthy sources conflict or no established term exists, ask or flag the proposed term instead of guessing.
- Use backend identifiers only to locate meaning. Convert them through established product copy; never display raw enum values, schema names, or inferred relationship names by default.
- Default to a page title only. Omit a subtitle unless it changes a decision, explains an abnormal state, or supplies information not already visible in filters, breadcrumbs, or data.
- Never add generic explanatory copy when the current scope and page purpose are already clear from navigation, filters, headings, or displayed data.
- Never expose implementation notes, data-source notes, or permission plumbing as ordinary UI copy. Show a short domain label only when the operator needs it; otherwise omit the field entirely. Keep terms such as `backend`, `hidden`, `internal`, implementation IDs, and storage details in code or internal documentation unless an authorized operator needs an explicit, user-facing explanation.
- Keep labels as short noun phrases and actions as short verbs. Prefer a number, state, or comparison over a prose sentence.
- Put explanation in an on-demand tooltip, disclosure, helper text next to a complex control, or empty/error state—not in the dashboard header.
- Show each fact once. Do not repeat the page title, selected scope, status, blocker, metric, or instruction in a header, card, alert, and table. Choose the location that best supports the next decision.
- Give each region a strict copy budget: one heading, optional status, and at most one short supporting sentence only when it changes the action or explains an irreversible consequence. Remove eyebrow labels such as step names or category captions when the heading already communicates the section.
- Replace prose with structure. Express blockers, readiness, ownership, and next actions in one compact table or list rather than an alert followed by repeated explanation and status rows.
- Use step labels only for a genuine ordered workflow in which later steps are unavailable or unsafe before earlier steps complete. Do not use `Step 1`, `Phase`, `Summary`, or similar labels as decoration.
- Do not narrate obvious design decisions in the final response. State what changed and any remaining decision in a few bullets unless the user asks for a rationale.

## Layout and Density Rules

- Treat desktop operational dashboards as desktop-first. Use the available width purposefully; do not stretch a mobile layout into a sparse desktop page.
- Keep the header compact: title, current scope, and primary action should normally fit in one horizontal band. Do not create a tall hero area.
- Place global filters together near the top. Place local filters immediately beside or above the widget they affect. Make active filters and data freshness visible.
- Use hierarchy before containers: spacing, alignment, typography, and grouping should explain the page before adding cards.
- Preserve design consistency across the product. Reuse the same spacing scale, typography roles, surface treatment, icon style, control states, table behavior, and semantic color meanings instead of inventing a new visual treatment per section.
- Use a card only when it groups a self-contained KPI, control, or independently actionable unit. Avoid cards inside cards and do not give every label/value pair its own card.
- Prefer flat sections with whitespace or a divider for page structure. Do not wrap an entire workflow step in a large full-width card and then place alerts, tables, or bordered lists inside it.
- Use one primary heading per region. Avoid stacks such as eyebrow + title + subtitle + metadata unless every layer is necessary and non-redundant.
- Show at most four headline KPI groups in the first row unless the task explicitly needs more. Keep secondary metrics in an analysis section or table.
- Prefer compact, readable tables for exact values; bar charts for comparisons; line charts for trends; KPI blocks for a single headline. Do not create charts merely to fill space.
- Make each chart answer one operator question and communicate one primary message. Split or simplify a chart that combines unrelated concepts.
- Keep charts visually quiet. Use light, minimal gridlines and remove decorative backgrounds, shadows, 3D effects, textures, and markers that do not improve reading.
- In numeric tables, right-align numeric values and minimize columns. When data is wider than the viewport, use a keyboard-focusable horizontal scroll container instead of converting the table into stacked cards by default.
- Use one restrained neutral surface system. Reserve color for semantic status, selection, and data encoding. Avoid gradients, glassmorphism, decorative blur, and heavy shadows by default.

## Create and Edit Interactions

- Use a popup dialog only for a focused, low-risk action that keeps the operator in the current context: a confirmation, a single setting, or quick creation with at most five simple required inputs.
- Use a dedicated create/edit page when the form has many fields, multiple sections, dependent fields, attachments, preview, detailed validation, related records, or a meaningful risk of losing work. Do not force a long form into a modal or side panel.
- Default complex creation to a dedicated page. Use the same page pattern for complex edits so navigation, validation, and unsaved-change protection remain predictable.
- Keep the page title and current object identity clear. Place the primary save action and cancel/back action in a persistent, easy-to-reach header or footer when the form scrolls.
- Use a confirmation dialog for destructive actions. Do not make a destructive action the primary visual action.

## Required States and Accessibility

- Provide loading, empty, error, and permission-denied states where data can vary.
- Ensure keyboard access, visible focus, semantic headings, labels for icon-only controls, and sufficient contrast.
- Do not hide critical labels, values, takeaways, or navigation behind hover or focus. Keep the main summary visible and provide a data-table alternative for complex charts when needed.
- Keep text readable at normal zoom.
- Verify numeric, date, currency, and percentage formatting for the product locale and domain.

## Final Review

Before handoff, answer these questions:

1. Can an operator identify the current scope and the most important state in five seconds?
2. Can a first-time operator identify the primary action and its expected result without reading an instructional paragraph? If not, redesign the interaction.
3. Does every sentence, card, chart, and color communicate a decision, status, or action?
4. Is any fact shown more than once? Keep the strongest instance and remove the rest.
5. Is a generic subtitle, decorative section label, nested card, or excess whitespace removable without losing meaning? Remove it.
6. Can two adjacent alerts, lists, or status blocks become one compact decision surface? Merge them.
7. Does every user-facing term exist in the product vocabulary, and is it used consistently? Replace or flag anything inferred, translated, or invented.
8. Can a keyboard and screen-reader user reach and understand the controls and key data?
9. Does the detailed view remain usable when values, labels, filters, or table rows grow?

If a web-interface audit skill is available, run it after implementation as a review pass; do not let it replace product context or visual judgment.
