# Truthly Engineering Standards — AGENT.md

This file is consumed by Claude during automated PR review. It contains Truthly's
engineering principles, architectural rules, code smell taxonomy, testing requirements,
and conventions. All review feedback should be grounded in these standards.

---

## 1. Scope: New Code vs. Legacy Code

- **New code** (new files, classes, functions) must comply fully with all principles
  from day one.
- **Modified code** within the PR scope should be improved toward compliance where
  reasonable. Modifications must not increase tech debt — no new code smells, no new
  lint/type failures, no coverage regression.
- **Untouched legacy code** outside the PR scope carries no obligation in that PR.
  Do not scope-creep a feature PR into a refactoring PR.
- **Exceptions** require: (a) written justification in the PR description, (b) reviewer
  approval, and (c) a follow-up Jira ticket labeled `tech-debt` within 2 sprints.

---

## 2. Architectural Principles

### 2.1 Adapter Pattern for APIs and Network Calls

All external communication (REST APIs, Firebase, RevenueCat, analytics SDKs, third-party
services) must go through an adapter (gateway/port). The adapter provides a clean interface;
implementation details are hidden behind it.

- **iOS:** Protocol + concrete class (e.g., `UserAuthService` protocol, `FirebaseAuthAdapter`).
- **Android:** TypeScript interface + implementation module in `/services/adapters/`.
- **Web:** Typed adapter modules in `/lib/adapters/`.

### 2.2 Business Logic Separated from UI Code

Views render state. They do not compute, fetch, or transform it. All business logic lives
in view models, services, hooks, or domain-layer modules. Views observe published state
and call methods on their view models.

**Rule of thumb:** If you delete every view file, the business logic should still compile
and all logic tests should still pass.

### 2.3 Component-Based View Architecture

Any UI element that appears in more than one place must be extracted into a shared component.

- **iOS:** `TruthlyUI` module or Swift package.
- **Android:** `/components/shared/` directory.
- **Web:** `/components/ui/` directory.

### 2.4 SOLID Principles

- **S — Single Responsibility:** Every module/class/function has exactly one reason to change.
- **O — Open/Closed:** Open for extension, closed for modification. Use protocols/interfaces.
- **L — Liskov Substitution:** Subtypes must be substitutable for base types without breaking.
- **I — Interface Segregation:** No client should depend on interfaces it does not use. Break
  large protocols into focused ones.
- **D — Dependency Inversion:** Depend on abstractions, not concrete implementations.
  Dependencies are injected, not hard-coded.

### 2.5 GRASP Principles

- **Information Expert:** Assign responsibility to the class that has the data.
- **Creator:** Create instances in the class that closely uses/contains them.
- **Controller:** Use-case controllers mediate between UI and domain.
- **Low Coupling:** Minimize dependencies between classes.
- **High Cohesion:** Each class has a focused, well-defined purpose.
- **Polymorphism:** Use protocols/interfaces instead of switch/case on type codes.
- **Indirection:** Use adapters, repositories, and service layers to reduce direct coupling.
- **Protected Variations:** Wrap predicted variation points in stable interfaces.
- **Pure Fabrication:** Create service classes when no domain class is a natural fit.

### 2.6 DRY — Don't Repeat Yourself

Every piece of knowledge should have a single, unambiguous, authoritative representation.
When the same logic, constant, configuration, or pattern appears in more than one place,
extract it.

### 2.7 No Magic Numbers

Literal numeric or string values with unexplained meaning must never appear inline. Extract
every magic number/string into a named constant that communicates intent. This includes:
API paths, error codes, timeout durations, retry counts, layout dimensions, color hex values,
and feature flag keys.

### 2.8 Mobile & API Resilience

- **API Versioning:** All endpoints versioned (e.g., `/v1/readings`). Old versions sunset
  with 90-day minimum window.
- **Graceful Degradation:** Clients check `minAppVersion` from API responses.
- **Local Database Migrations:** Explicit, versioned migration steps. Failed migrations must
  not crash the app.

---

## 3. Code Smells Taxonomy (Mäntylä & Lassenius)

Flag any of the following during review:

| Category | Smells | What to Watch For |
|---|---|---|
| **Bloaters** | Long Method, Large Class, Primitive Obsession, Long Parameter List, Data Clumps | Functions > 30 lines, classes > 300 lines, methods with 4+ parameters, groups of primitives that travel together (use a struct/type). |
| **OO Abusers** | Switch Statements, Temporary Field, Refused Bequest, Alternative Classes with Different Interfaces | Switch/case on type codes (use polymorphism), fields only used in some methods, subclasses ignoring parent behavior. |
| **Change Preventers** | Divergent Change, Shotgun Surgery, Parallel Inheritance Hierarchies | One class modified for many unrelated reasons, one change requiring edits across many files, duplicated class hierarchies. |
| **Dispensables** | Lazy Class, Data Class, Duplicate Code, Dead Code, Speculative Generality | Classes that don't justify their existence, unused code, abstractions built for hypothetical future needs. |
| **Couplers** | Feature Envy, Inappropriate Intimacy, Message Chains, Middle Man | Methods more interested in another class's data, tightly coupled pairs, long chains like `a.getB().getC().getD()`. |

---

## 4. Testing Requirements

### Coverage Thresholds (enforced in CI)

| Metric | iOS | Android | Web |
|---|---|---|---|
| Business Logic Coverage | 80% min | 80% min | 80% min |
| Overall Coverage | 60% min | 60% min | 60% min |
| New Code Coverage | 90% min | 90% min | 90% min |
| UI Test Flows | All critical paths | All critical paths | All critical paths |

### Platform Test Frameworks

- **iOS:** XCTest (unit), XCUITest (UI), swift-snapshot-testing (visual regression).
- **Android:** Jest (unit), React Native Testing Library (component), Detox (E2E).
- **Web:** Vitest or Jest (unit), React Testing Library (component), Playwright (E2E).

### Testing Rules

- All view models, services, adapters, and domain logic must have unit tests.
- New logic without tests is a **Blocking** finding.
- Tests must cover both flag-on and flag-off states for feature flags.
- Use protocol-based / mock-based dependency injection for testability.
- Assertions must be meaningful — test behavior, not implementation.

---

## 5. Feature Flags & A/B Testing

- All significant new features and risky changes must be behind feature flags (LaunchDarkly).
- Every flag needs: flag name, target removal date (2–4 weeks after rollout), cleanup owner.
- Flags fully rolled out for 30+ days are tech debt — flag with `flag-cleanup`.
- Tests must cover both flag-on and flag-off paths.

---

## 6. Security Baseline

- **No secrets in source code** — ever. Use environment variables or secrets managers.
- **Dependency scanning** must be enabled. Critical/high CVEs patched within 7 days.
- **Input validation** at system boundaries.
- **Error messages** must not expose internal details to end users.

---

## 7. Performance Budgets

| Metric | iOS | Android | Web |
|---|---|---|---|
| Cold Launch | < 2s | < 3s | < 3s (LCP) |
| Bundle Size | Flag > 5% increase | Flag > 5% increase | < 300 KB initial JS (gzip) |
| Memory | < 150 MB | < 200 MB | Monitor Core Web Vitals |
| API p95 | < 500 ms | < 500 ms | < 500 ms |

---

## 8. Accessibility Requirements

- All interactive elements must have meaningful accessibility labels.
- All images must have descriptive alt text or be marked decorative.
- Color contrast must meet WCAG 2.1 AA (4.5:1 normal text, 3:1 large text).
- Focus order must be logical.
- Functionality must not rely solely on color, gestures, or motion.
- **Web:** Lighthouse accessibility score must be >= 90.

---

## 9. Conventions

### Branching

- Gitflow-style: `main` (production), `develop` (integration), `feature/*`, `hotfix/*`, `release/*`.
- Feature branches from `develop`: `feature/TRUTH-XXX-short-description`.
- Keep feature branches short-lived (2–3 days).

### PR Requirements

- CI must pass (lint, compile, tests, coverage gate).
- At least one human reviewer approval.
- Claude automated review must be addressed (blocking findings resolved or justified).

### PR Self-Check (expected of every author)

- [ ] Every new class/module has a single, clear responsibility?
- [ ] All business logic outside of view code?
- [ ] External services accessed through adapter protocols/interfaces?
- [ ] Unit tests written for all new logic?
- [ ] No duplicated code that exists in shared components?
- [ ] Accessibility identifiers on new interactive elements?
- [ ] Code coverage at or above threshold?
- [ ] No magic numbers or unexplained literals?
