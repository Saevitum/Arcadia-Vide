--!strict

export type Source<T> = (() -> T) & ((T) -> ())
export type Reactive<T> = T | (() -> T)

return {}
