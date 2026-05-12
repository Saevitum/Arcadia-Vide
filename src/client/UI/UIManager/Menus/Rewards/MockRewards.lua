--!strict

export type RewardState = "Claimed" | "Available" | "Locked"

export type RewardTemplate = {
	Title: string,
	ImageId: string,
	Description: string,
	Money: number?,
	SideKick: string?,
}

export type RewardView = RewardTemplate & {
	Tier: number,
	State: RewardState,
	TimeRemaining: string?,
}

local REWARD_TEMPLATES: { RewardTemplate } = {
	{
		Title = "Small Money",
		ImageId = "rbxassetid://84274182811067",
		Money = 100,
		Description = "Your first reward. Thank you for playing!",
	},

	{
		Title = "Small Blue Gem",
		ImageId = "rbxassetid://89372741992780",
		SideKick = "Psionic",
		Description = "A rare SideKick reward from the current cycle.",
	},

	{
		Title = "Money Pouch",
		ImageId = "rbxassetid://84274182811067",
		Money = 250,
		Description = "A small pouch of credits to boost your progress.",
	},

	{
		Title = "Cash Bundle",
		ImageId = "rbxassetid://84274182811067",
		Money = 400,
		Description = "A compact cash bundle earned by staying active.",
	},

	{
		Title = "Money Stack",
		ImageId = "rbxassetid://84274182811067",
		Money = 600,
		Description = "A bigger stack of money for your reward cycle.",
	},

	{
		Title = "Large Money Bag",
		ImageId = "rbxassetid://84274182811067",
		Money = 1000,
		Description = "A large money bag. Claim it before moving to the next reward.",
	},

	{
		Title = "Cash Briefcase",
		ImageId = "rbxassetid://84274182811067",
		Money = 1200,
		Description = "A secured briefcase filled with extra credits.",
	},

	{
		Title = "Money Chest",
		ImageId = "rbxassetid://84274182811067",
		Money = 1400,
		Description = "A chest of money unlocked later in the cycle.",
	},

	{
		Title = "Money Vault",
		ImageId = "rbxassetid://84274182811067",
		Money = 1600,
		Description = "A vault reward for players who keep progressing.",
	},

	{
		Title = "Big G Money",
		ImageId = "rbxassetid://84274182811067",
		Money = 1800,
		Description = "A high-value money reward from the current cycle.",
	},

	{
		Title = "Money Reserve",
		ImageId = "rbxassetid://84274182811067",
		Money = 2000,
		Description = "A reserve payout saved for dedicated players.",
	},

	{
		Title = "Elon Musk",
		ImageId = "rbxassetid://84274182811067",
		Money = 2500,
		Description = "The final reward of this cycle. Complete the cycle to upgrade future rewards.",
	},
}

local MOCK_TIMERS = {
	"15:17",
	"35:17",
	"55:17",
	"01:15:17",
	"01:35:17",
	"01:55:17",
}

local MockRewards: { RewardView } = {}

for index, template in REWARD_TEMPLATES do
	local state: RewardState
	local timeRemaining: string? = nil

	if index <= 5 then
		state = "Claimed"
	elseif index == 6 then
		state = "Available"
	else
		state = "Locked"
		timeRemaining = MOCK_TIMERS[index - 6] or "LOCKED"
	end

	table.insert(MockRewards, {
		Tier = index - 1,
		Title = template.Title,
		ImageId = template.ImageId,
		Description = template.Description,
		Money = template.Money,
		SideKick = template.SideKick,
		State = state,
		TimeRemaining = timeRemaining,
	})
end

return MockRewards
