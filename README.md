# DRAGON QUEST XI ultrawide patch

Removes the black bars at 21:9 (and any other aspect wider than 16:9). The view keeps its
16:9 height and gains width at the sides. For the original 2018 Steam release
(not the Definitive Edition).

## Install
1. Copy `patch.bat` (Windows) or `patch.py` (Linux / Steam Deck) into the game folder,
   the one containing `Dlc`, `Engine` and `Game`.
   Next to `DRAGON QUEST XI.exe` works too.
   (Steam: right-click the game > Manage > Browse local files.)
2. Windows: double-click `patch.bat`. Linux: `python3 patch.py`.
3. Play in borderless window mode (`FullscreenMode=1`, what the game picked by default
   on the machine this was made on); it uses the whole screen whatever resolution is
   selected.
   The game's resolution list is 16:9 only, so exclusive fullscreen needs `ResolutionSizeX` /
   `ResolutionSizeY` set by hand in
   `Documents\My Games\DRAGON QUEST XI\Saved\Config\WindowsNoEditor\GameUserSettings.ini`
   (untested).

What you get:
- The 3D view fills the screen.
- The in-game HUD, minimap and battle UI use the full width, and so do screen and loading fades.
- Dialogue and quest boxes are centred.
- Title and main menus, the map menu, loading screens and pre-rendered videos stay a centred,
  unstretched 16:9 block.

Already patched with an older version? Just run the new one, it upgrades the exe in place.

## Uninstall
Run it again; it toggles the patch off and restores the original bytes.
Steam's "Verify integrity of game files" also undoes it.

It edits about 1,300 bytes of `Game/Binaries/Win64/DRAGON QUEST XI.exe` and refuses to touch an
exe it does not recognise.
