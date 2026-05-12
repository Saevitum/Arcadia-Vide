--!strict

local Merge = {}

local function hasNumericKey(value: any): boolean
	if type(value) ~= "table" then
		return false
	end

	for key in pairs(value) do
		if type(key) == "number" then
			return true
		end
	end

	return false
end

local function isMergeableMap(value: any): boolean
	return type(value) == "table" and not hasNumericKey(value)
end

local function copyValue(value: any): any
	if type(value) ~= "table" then
		return value
	end

	local result = {}

	for key, childValue in pairs(value) do
		result[key] = copyValue(childValue)
	end

	return result
end

local function mergeValue(base: any, override: any): any
	if override == nil then
		return copyValue(base)
	end

	if not isMergeableMap(base) or not isMergeableMap(override) then
		return copyValue(override)
	end

	local result = copyValue(base)

	for key, overrideValue in pairs(override) do
		local baseValue = result[key]

		if isMergeableMap(baseValue) and isMergeableMap(overrideValue) then
			result[key] = mergeValue(baseValue, overrideValue)
		else
			result[key] = copyValue(overrideValue)
		end
	end

	return result
end

function Merge.copy<T>(value: T): T
	return copyValue(value) :: T
end

function Merge.deep<T>(base: T, override: any?): T
	return mergeValue(base, override) :: T
end

function Merge.many<T>(base: T, ...: any): T
	local result: any = copyValue(base)

	for _, patch in ipairs({ ... }) do
		result = mergeValue(result, patch)
	end

	return result :: T
end

return Merge
