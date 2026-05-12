--!strict

-- Backward-compatible non-generic aliases for old modules.
export type Source = (() -> any) & ((any) -> ())
export type Reactive = any | (() -> any)

-- Stronger generic aliases for new/refactored modules.
export type SourceOf<T> = (() -> T) & ((T) -> ())
export type ReactiveOf<T> = T | (() -> T)

return {}
