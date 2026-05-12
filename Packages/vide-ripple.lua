--!nocheck
--!nolint
local REQUIRED_MODULE = require(script.Parent._Index["littensy_vide-ripple@0.10.2"]["vide-ripple"])
export type Animatable = REQUIRED_MODULE.Animatable 
export type Easing = REQUIRED_MODULE.Easing 
export type Motion<T = any> = REQUIRED_MODULE.Motion<T >
export type MotionOptions<T = any> = REQUIRED_MODULE.MotionOptions<T >
export type Spring<T = any> = REQUIRED_MODULE.Spring<T >
export type SpringOptions<T = any> = REQUIRED_MODULE.SpringOptions<T >
export type Tween<T = any> = REQUIRED_MODULE.Tween<T >
export type TweenOptions<T = any> = REQUIRED_MODULE.TweenOptions<T >
return REQUIRED_MODULE
