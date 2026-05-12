--!strict

local SharedTypes = require(script.Parent.Parent.SharedTypes)

export type Source<T> = SharedTypes.Source<T>

export type PulseDriverOptions = {
	phase: Source<number>,
	duration: number?,
	easingStyle: Enum.EasingStyle?,
	easingDirection: Enum.EasingDirection?,
}

return {}
