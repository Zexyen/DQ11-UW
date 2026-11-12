#!/usr/bin/env python3
"""DRAGON QUEST XI (Steam, original 2018 release) ultrawide patch. Run again to undo.
Put this in the game folder (or next to the exe) and run it, or pass the exe path."""
import os, sys

# (file offset, original bytes, patched bytes)
PATCHES = [
    # camera projection: never letterbox/pillarbox to the camera's 16:9 aspect
    (0x1EFA273, "0f84d0010000", "e9d101000090"),
    # ...and keep the 16:9 vertical FOV, widening horizontally (Hor+) instead of cropping
    (0x1EFA489,
     "3bc17e05803a02742e803a017429807f30017423f30f10352b850d0166440f6ed1440f28de660f6ec0450f5bd20f5bc0",
     "f30f10353f850d01f30f2ac0f3440f2ad1f3410f5ec2f3440f101d70771401f3440f5dd8450f28d3f3440f5ed0eb29"),
    # UI layer: lay the HUD/menus out as a centred 16:9 block instead of a left-aligned one
    (0x12DB5669,
     "f30f100d5fc521f0f3440f1005e6182df1f3440f100de1182df1f30f1038488b8f80030000f30f5ecf4881c140010000f3440f59c70f28c1f3440f59cff30f5906f30f594e04f30f11442440410f28c0410f14c1440f28d0f20f11442464f30f114c2444f30f117c2460",
     "f30f1038488b8f800300004881c140010000f30f1046040f28c8f30f59058db728f0f3440f1006f3410f5dc0f3440f5cc0f3440f59051de325f0450f57c9f30f5ec7f30f5ecff30f11442440f30f114c2444450f28d0f2440f11542464f30f117c246090909090909090"),
]

here = os.path.dirname(os.path.abspath(__file__))
exe = sys.argv[1] if len(sys.argv) > 1 else next(
    (p for p in (os.path.join(here, "DRAGON QUEST XI.exe"),
                 os.path.join(here, "Game", "Binaries", "Win64", "DRAGON QUEST XI.exe")) if os.path.exists(p)), None)
if not exe:
    sys.exit("Game exe not found. Put this file in the DRAGON QUEST XI folder or next to the exe.")
with open(exe, "r+b") as f:
    def read(off, n):
        f.seek(off)
        return f.read(n).hex()
    # each site must hold either its original or its patched bytes (so older versions of this patch upgrade)
    done = [read(off, len(new) // 2) == new for off, old, new in PATCHES]
    if not all(d or read(off, len(old) // 2) == old for d, (off, old, new) in zip(done, PATCHES)):
        sys.exit("Unrecognised exe (different game version?) - nothing was changed.")
    dst, msg = (0, "Patch removed: exe is back to original.") if all(done) else (1, "Patched: ultrawide enabled.")
    for p in PATCHES:
        f.seek(p[0])
        f.write(bytes.fromhex(p[1 + dst]))
print(msg, "Run again to toggle.")
