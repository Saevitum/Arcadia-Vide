# Vide Lessons For This Project

This file is a project-specific shortcut reference for future UIManager work. Read this before changing or creating Vide UI so the codebase does not need to be rescanned every time.

## Core Vide Pattern

- Most UI files start with `--!strict`.
- Vide is required from `ReplicatedStorage.Packages.vide`.
- Set `Vide.strict = true` in modules that create UI.
- Common imports:
  - `local create = Vide.create`
  - `local source = Vide.source`
  - `local action = Vide.action`
  - `local cleanup = Vide.cleanup`
  - `local effect = Vide.effect`
- UI is returned by calling `create("InstanceClass")({ ...props, children... })`.
- Reactive values are usually functions/sources, so properties can be assigned functions:
  - `Visible = function() return selected() ~= nil end`
  - `Text = function() return tostring(value()) end`
  - `BackgroundColor3 = function() ... end`
- A `Source<T>` is typed in `UITypes.lua` as `(() -> T) & ((T) -> ())`.
- Local UI-only state belongs inside the menu component with `source(...)` unless it must be shared through the store.

## UIManager Structure

- Shared UI building blocks live in `src/client/UI/UIManager/Components`.
- Shared animation/effect helpers live in `src/client/UI/UIManager/Effects`.
- Shared prop/type definitions live in `src/client/UI/UIManager/UITypes.lua`.
- Menu exports are collected in `src/client/UI/UIManager/Menus/init.lua`.
- Button exports are collected in `src/client/UI/UIManager/Buttons/init.lua`.
- Prefer existing components before making menu-local UI:
  - `Components.Panel`
  - `Components.ActionButton`
  - `Components.ScrollArea`
  - `Components.Text`
  - `Components.Image`
  - `Components.Slider`
  - `Components.ToggleButton`
  - `Components.ToggleSwitch`

## Menu File Structure

Use the SideKicks menu as the model for complex menus:

- Keep `init.lua` or `init.luau` as the composition root.
- Keep root menu files focused on:
  - creating local state
  - returning `Panel`
  - laying out the main content shell
  - wiring child components together
- Move single-responsibility UI pieces into child modules.
- Good examples:
  - `SideKicks/init.luau`
  - `SideKicks/SideKickButtons.lua`
  - `SideKicks/SideKickCard.lua`
  - `SideKicks/SideKickInfo.lua`
- Do not let a root menu file accumulate all rows, controls, helper components, and style constants.

## SettingsMenu Structure

`SettingsMenu` is now a folder ModuleScript:

- `SettingsMenu/init.lua`
  - Owns local state.
  - Creates the `Panel`.
  - Mounts `TabStrip`, `VolumeSettingsPage`, `UserSettingsPage`, and `GameSettingsPage`.
- `SettingsMenu/TabStrip.lua`
  - Creates the top tab button row.
  - Uses `ActionButton` through `TabButton`.
- `SettingsMenu/TabButton.lua`
  - Creates one tab button.
  - Reads `selectedTab` and writes it on click.
  - Tab background/stroke gradient colors are controlled from `SettingsMenu/Style.lua`.
- `SettingsMenu/SettingsPage.lua`
  - Creates one fading `CanvasGroup`.
  - Contains a `ScrollArea`.
  - Uses `Effects.SlideFadeCanvasGroup` with identical open/closed positions for pure fade.
- `SettingsMenu/VolumeSettingsPage.lua`
  - Owns only Volume tab row composition.
- `SettingsMenu/UserSettingsPage.lua`
  - Owns only User tab row composition.
  - Passes `Style.USER_SETTING_ROW_LAYOUT` into `ToggleSettingRow`.
- `SettingsMenu/GameSettingsPage.lua`
  - Owns only Game tab row composition.
  - Passes `Style.GAME_SETTING_ROW_LAYOUT` into `ToggleSettingRow`.
- `SettingsMenu/VolumeSettingRow.lua`
  - Creates rows with label, description, mute toggle, slider, and number input.
- `SettingsMenu/ToggleSettingRow.lua`
  - Creates rows with label, description, and toggle.
- `SettingsMenu/NumberInput.lua`
  - Handles typed percent input.
  - Clamps values to `0-100`.
  - Restores/clamps invalid input on focus lost.
  - Clears the visible number while focused and restores the original value if the user clicks out without typing a valid number.
- `SettingsMenu/SettingsRow.lua`
  - Shared row frame/stroke/gradient shell.
- `SettingsMenu/Style.lua`
  - Central place for SettingsMenu colors, fonts, sizes, and positions.
  - User/Game layout constants should use their own explicit values, even when they match Volume or generic Toggle values, so tabs can be tuned independently.

## Settings Layout Knobs

For manual UI positioning, edit `SettingsMenu/Style.lua`.

Important constants:

- `TAB_STRIP_SIZE`
- `TAB_STRIP_POSITION`
- `TAB_STRIP_ANCHOR_POINT`
- `TAB_BUTTON_SIZE`
- `TAB_BUTTON_CORNER_RADIUS`
- `PAGE_POSITION`
- `PAGE_SIZE`
- `VOLUME_SETTING_ROW_SIZE`
- `TOGGLE_SETTING_ROW_SIZE`
- `VOLUME_LABEL_POSITION`
- `VOLUME_DESCRIPTION_POSITION`
- `VOLUME_TOGGLE_POSITION`
- `VOLUME_SLIDER_POSITION`
- `VOLUME_INPUT_POSITION`
- `TOGGLE_LABEL_POSITION`
- `TOGGLE_DESCRIPTION_POSITION`
- `TOGGLE_SETTING_ROW_LAYOUT`
- `TOGGLE_BUTTON_SIZE`
- `TOGGLE_BUTTON_POSITION`
- `TOGGLE_SWITCH_POSITION`
- `USER_SETTING_ROW_LAYOUT`
- `USER_SETTING_ROW_SIZE`
- `USER_LABEL_SIZE`
- `USER_LABEL_POSITION`
- `USER_DESCRIPTION_SIZE`
- `USER_DESCRIPTION_POSITION`
- `USER_TOGGLE_BUTTON_SIZE`
- `USER_TOGGLE_BUTTON_POSITION`
- `GAME_SETTING_ROW_LAYOUT`
- `GAME_SETTING_ROW_SIZE`
- `GAME_LABEL_SIZE`
- `GAME_LABEL_POSITION`
- `GAME_DESCRIPTION_SIZE`
- `GAME_DESCRIPTION_POSITION`
- `GAME_TOGGLE_BUTTON_SIZE`
- `GAME_TOGGLE_BUTTON_POSITION`

Rows inside a `ScrollArea` with a list layout may show computed Studio positions that are not explicitly written in the row module. The code controls row `Size` and `LayoutOrder`; the `UIListLayout` inside `ScrollArea` computes final row position.

## Reusable Slider And Toggle Components

- `Components/Slider.lua` is reusable and should be used for future numeric sliders.
- `Components/ToggleButton.lua` is reusable for square ON/OFF style buttons.
- `Components/ToggleSwitch.lua` is reusable and should be used for future on/off controls.
- Their prop types are in `UITypes.lua`:
  - `SliderProps`
  - `ToggleButtonProps`
  - `ToggleSwitchProps`
- They support reactive sizing/positioning/styling props.
- `Slider` supports click and drag through `UserInputService`.
- `Slider` clamps to `min`, `max`, and optional `step`.
- `Slider` supports optional fill gradients through `fillGradient` and `fillGradientEffect`.
- `Effects.LiquidGradient` supports an `enabled` option; use `disabledColor` when a slider needs to become a flat inactive color.
- `ToggleButton` uses a `UIAspectRatioConstraint` and is useful when a compact 1:1 control is clearer than a switch.
- `ToggleSwitch` owns click behavior and calls `onChanged` when provided.
- Keep menu-specific row composition outside shared components. Shared components should not know about SettingsMenu labels, descriptions, or neon styling.

## Effects Lessons

- Use `Effects.HoverUIScale` when the whole button, including child text, should visually grow together.
- Scaling only a frame size can leave text visually unchanged or misaligned.
- Use `Effects.SlideFadeCanvasGroup` for menus/pages that should animate visibility and transparency.
- For pure fade page switching, set `openPosition` and `closedPosition` to the same value.
- `SlideFadeCanvasGroup` can hide closed pages with `hideWhenClosed = true`.
- Use `Effects.TweenGuiObjectLayout` for moving/resizing GuiObjects, such as animated toggle knobs.
- Use `Effects.LiquidGradient` on a `UIGradient` for a simple slow endpoint color swap. It keeps `Offset` and `Rotation` fixed and smoothly crossfades point 1 and point 2 colors.

## Button/Menu Creation Pattern

When adding a new top-level menu button like `QuestsButton`, `InventoryButton`, `SettingsButton`, or `ShopButton`:

- Mirror the existing button module structure.
- Add the button module export in `Buttons/init.lua`.
- Add or update menu id types in `UITypes.lua`.
- Create the menu module in `Menus`.
- Add the menu export in `Menus/init.lua`.
- Keep unknown image IDs as `Image = ""` when requested.
- `LayoutOrder` for button order is currently passed into button props from `ButtonBar`, not stored in `UITypes.lua`.

## Type Lessons

- Add shared unions to `UITypes.lua` when several modules need them.
- `SettingsTab` now lives in `UITypes.lua`.
- Keep component prop types in `UITypes.lua` when the component is reusable across menus.
- Menu-local prop types can live in the menu module if they are not used elsewhere.

## Practical Rules For Future Work

- First check existing UIManager components and effects before creating new code.
- If a menu has multiple sections, tabs, cards, rows, info panels, or button strips, split them into child modules.
- Use `Style.lua` for menu-specific sizing and colors when many child modules need the same values.
- Prefer `ScrollArea` for tab/page content that may grow later.
- Keep state local until there is a real gameplay/system integration.
- Do not connect placeholder UI to real systems unless explicitly asked.
- After structural changes, run `rojo sourcemap default.project.json` to verify the project tree sees folder ModuleScripts and child modules correctly.
