--!strict

-- Compatibility aliases for current modules that still use `Types.Source`
-- and `Types.Reactive` without generic parameters.
export type Source = (() -> any) & ((any) -> ())
export type Reactive = any

-- Preferred typed aliases for new/refactored modules.
export type SourceOf<T> = (() -> T) & ((T) -> ())
export type ReactiveOf<T> = T | (() -> T)

export type VoidCallback = () -> ()
export type CleanupCallback = () -> ()

return {}
