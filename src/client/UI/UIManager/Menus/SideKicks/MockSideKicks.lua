--!strict

export type SideKickRarity = "Common" | "Uncommon" | "Rare" | "Epic" | "Legendary" | "Mythic"

export type SideKickType = "Passive" | "Active"

export type MockSideKick = {
	SideKickId: string,
	Name: string,
	Description: string,
	Rarity: SideKickRarity,
	Type: SideKickType,
	ImageId: string,
	TransparentImageId: string,
	ModelPath: string,
	Skill: string?,
	BasePower: number,
	VirtualMachine: string,
}

local MockSideKicks: { MockSideKick } = {
	{
		SideKickId = "WeakCyberFemale",
		Name = "Weak Cyber Female",
		Description = "Enhanced with prototype velocity augments stolen from corporate labs, the Swift Runner blurs through space stations like a ghost. Its cybernetic legs pulse with unstable energy, leaving afterimages in the void. Speed is survival, and this runner never slows down.",
		Rarity = "Uncommon",
		Type = "Passive",
		ImageId = "rbxassetid://15382026898",
		TransparentImageId = "rbxassetid://15382071216",
		ModelPath = "Assets.SideKicks.Models.WeakCyberFemale",
		Skill = nil,
		BasePower = 1.4,
		VirtualMachine = "VM_1",
	},

	{
		SideKickId = "WeakCyberMale",
		Name = "Weak Cyber Male",
		Description = "A low-tier cybernetic runner drifting through the neon voids of Bloxdash. His outdated implants glitch under pressure, sparks flying as he struggles to keep up in the cold expanse of space. Weak… but still dashin'.",
		Rarity = "Common",
		Type = "Passive",
		ImageId = "rbxassetid://15382026368",
		TransparentImageId = "rbxassetid://15382070768",
		ModelPath = "Assets.SideKicks.Models.WeakCyberMale",
		Skill = nil,
		BasePower = 1.2,
		VirtualMachine = "VM_1",
	},

	{
		SideKickId = "FemaleJunker",
		Name = "Female Junker",
		Description = "Forged in the black matter cores of dying stars, the Shadow Dragon exists between dimensions. Its wings ripple with dark energy that bends light itself, and its roar echoes through the quantum foam. A creature of pure entropy, it freezes time in its wake.",
		Rarity = "Rare",
		Type = "Passive",
		ImageId = "rbxassetid://15382029512",
		TransparentImageId = "rbxassetid://15382073434",
		ModelPath = "Assets.SideKicks.Models.FemaleJunker",
		Skill = nil,
		BasePower = 1.6,
		VirtualMachine = "VM_1",
	},

	{
		SideKickId = "MaleJunker",
		Name = "Male Junker",
		Description = "IntegrityHash recomputation test.",
		Rarity = "Epic",
		Type = "Passive",
		ImageId = "rbxassetid://15382028307",
		TransparentImageId = "rbxassetid://15382072529",
		ModelPath = "Assets.SideKicks.Models.MaleJunker",
		Skill = nil,
		BasePower = 1.8,
		VirtualMachine = "VM_1",
	},

	{
		SideKickId = "FemaleHacker",
		Name = "Female Hacker",
		Description = "One of the most elusive and skilled hackers in the cyber underworld",
		Rarity = "Legendary",
		Type = "Active",
		ImageId = "rbxassetid://15382030133",
		TransparentImageId = "rbxassetid://15382074352",
		ModelPath = "Assets.SideKicks.Models.FemaleHacker",
		Skill = "SpeedHack",
		BasePower = 2.0,
		VirtualMachine = "VM_1",
	},

	{
		SideKickId = "Psionic",
		Name = "Psionic",
		Description = "A cyber-enhanced mind-walker who bends reality with pure neural force. Legend says he possesses a skill called Neural Jammer, capable of flooding enemy neural implants with psionic interference.",
		Rarity = "Mythic",
		Type = "Active",
		ImageId = "rbxassetid://15382027182",
		TransparentImageId = "rbxassetid://15382071693",
		ModelPath = "Assets.SideKicks.Models.Psionic",
		Skill = "NeuralJammer",
		BasePower = 2.2,
		VirtualMachine = "VM_1",
	},
}

return MockSideKicks
