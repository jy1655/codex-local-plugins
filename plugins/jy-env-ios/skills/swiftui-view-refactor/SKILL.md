---
name: swiftui-view-refactor
description: Use when refactoring SwiftUI view files into stable, testable structure by splitting large views, tightening data flow, or clarifying Observation ownership.
---

# SwiftUI View Refactor

## Overview
Refactor the requested SwiftUI surface while preserving behavior, state ownership, and
project conventions. Use the patterns below when they address an observed problem;
they do not require an architectural migration or cosmetic reordering.

## Core Guidelines

### 1) View ordering (top → bottom)
- This ordering is a reference when a file needs organization; preserve coherent local ordering during a narrow change.
- Environment
- `private`/`public` `let`
- `@State` / other stored properties
- computed `var` (non-view)
- `init`
- `body`
- computed view builders / other view helpers
- helper / async functions

### 2) Choose state and model boundaries to fit the project
- Views should be lightweight state expressions and orchestration points, not containers for business logic.
- Favor `@State`, `@Environment`, `@Query`, `.task`, `.task(id:)`, and `onChange` before reaching for a view model.
- Inject services and shared models via `@Environment`; keep domain logic in services/models, not in the view body.
- Do not introduce a view model just to mirror local view state or wrap environment dependencies.
- If a screen mixes responsibilities, consider coherent subviews or the project's existing model pattern according to the actual boundary.

### 3) Extract subviews when a responsibility or state boundary benefits
- Consider extraction where independent responsibilities make a view hard to understand or maintain.
- Prefer extracting dedicated `View` types for non-trivial sections, especially when they have state, async work, branching, or deserve their own preview.
- Small computed `some View` helpers are reasonable when they improve local readability without obscuring ownership.
- Pass small, explicit inputs (data, bindings, callbacks) into extracted subviews instead of handing down the entire parent state.
- If an extracted subview becomes reusable or independently meaningful, move it to its own file.

Prefer:

```swift
var body: some View {
    List {
        HeaderSection(title: title, subtitle: subtitle)
        FilterSection(
            filterOptions: filterOptions,
            selectedFilter: $selectedFilter
        )
        ResultsSection(items: filteredItems)
        FooterSection()
    }
}

private struct HeaderSection: View {
    let title: String
    let subtitle: String

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(title).font(.title2)
            Text(subtitle).font(.subheadline)
        }
    }
}

private struct FilterSection: View {
    let filterOptions: [FilterOption]
    @Binding var selectedFilter: FilterOption

    var body: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack {
                ForEach(filterOptions, id: \.self) { option in
                    FilterChip(option: option, isSelected: option == selectedFilter)
                        .onTapGesture { selectedFilter = option }
                }
            }
        }
    }
}
```

Avoid:

```swift
var body: some View {
    List {
        header
        filters
        results
        footer
    }
}

private var header: some View {
    VStack(alignment: .leading, spacing: 6) {
        Text(title).font(.title2)
        Text(subtitle).font(.subheadline)
    }
}
```

### 3b) Extract actions and side effects out of `body`
- Do not keep non-trivial button actions inline in the view body.
- Do not bury business logic inside `.task`, `.onAppear`, `.onChange`, or `.refreshable`.
- Prefer calling small private methods from the view, and move real business logic into services/models.
- The body should read like UI, not like a view controller.

```swift
Button("Save", action: save)
    .disabled(isSaving)

.task(id: searchText) {
    await reload(for: searchText)
}

private func save() {
    Task { await saveAsync() }
}

private func reload(for searchText: String) async {
    guard !searchText.isEmpty else {
        results = []
        return
    }
    await searchService.search(searchText)
}
```

### 4) Keep a stable view tree (avoid top-level conditional view swapping)
- Avoid `body` or computed views that return completely different root branches via `if/else`.
- Prefer a single stable base view with conditions inside sections/modifiers (`overlay`, `opacity`, `disabled`, `toolbar`, etc.).
- Root-level branch swapping causes identity churn, broader invalidation, and extra recomputation.

Prefer:

```swift
var body: some View {
    List {
        documentsListContent
    }
    .toolbar {
        if canEdit {
            editToolbar
        }
    }
}
```

Avoid:

```swift
var documentsListView: some View {
    if canEdit {
        editableDocumentsList
    } else {
        readOnlyDocumentsList
    }
}
```

### 5) View model handling (only if already present or explicitly requested)
- Preserve an existing view model architecture unless the requested change calls for a different ownership model.
- Do not introduce a view model unless the request or existing code clearly calls for one.
- Preserve optionality when it represents a real loading or lifecycle state.
- Use `init` for dependencies known at construction time. Change delayed initialization only when the task or lifecycle evidence requires it.

Example (Observation-based):

```swift
@State private var viewModel: SomeViewModel

init(dependency: Dependency) {
    _viewModel = State(initialValue: SomeViewModel(dependency: dependency))
}
```

### 6) Observation usage
- For `@Observable` reference types on iOS 17+, store them as `@State` in the owning view.
- Pass observables down explicitly; avoid optional state unless the UI genuinely needs it.
- If the deployment target includes iOS 16 or earlier, use `@StateObject` at the owner and `@ObservedObject` when injecting legacy observable models.

## Scope and Verification

Select only transformations that solve the requested problem. Preserve model lifetime,
navigation, layout, and business behavior unless changing them is part of the request.
Verify the affected behavior with a relevant build, test, preview, or runtime check and
report its limits. Do not add another refactor or repeat a passed check without a new
change, failure, or unresolved concern.

## Notes

- Prefer small, explicit view types over large conditional blocks and large computed `some View` properties.
- Keep computed view builders below `body` and non-view computed vars above `init`.
- A good SwiftUI refactor should make the view read top-to-bottom as data flow plus layout, not as mixed layout and imperative logic.
- For MV-first guidance and rationale, see `references/mv-patterns.md`.
- In addition to the references above, use web search to consult current Apple Developer documentation when SwiftUI APIs, Observation behavior, or platform guidance may have changed.

## Large-view handling

Line count alone does not justify splitting a view. Extract a dedicated `View` type or
file when a coherent responsibility, ownership boundary, or reuse need makes it useful.
Keep a focused one-off edit local when extraction would only add indirection.
