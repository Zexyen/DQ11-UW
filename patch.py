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
    # world-anchored widgets (talk bubbles, door prompts): the UI layer above starts at the 16:9 block's
    # left edge, so shift projected positions left by that margin, (W - min(W, H*16/9)) / 2
    # UWidgetLayoutLibrary::ProjectWorldLocationToWidgetPosition
    (0x1B3B48D,
     "f30f104c2430488bcbf30f590d3e934d010f297424500f297c2440f30f580d10934d01f30f2dc1f30f104c2434f30f590d1a934d01d1f8f30f580df4924d01660f6ef80f5bfff30f2dc1d1f8660f6ef00f5bf6e8ebb8feffb001f30f1015e1744901f30f5ed00f28caf30f59d60f28742450f30f59cf0f287c2440eb08",
     "488d4c24204889dae8b6b9fefff30f104c2424f30f590d70675001f30f10442420f30f5dc8f30f5cc1f30f590502934d01f30f104c2430f30f5cc8f30f114c24304889d9e8fab8feff0fc6c000f20f104c2430660f5bc90f5bc90f5ec8660f70d155b001e91c000000cccccccccccccccccccccccccccccccccccccccc"),
    # ...WithDistance variant
    (0x1B3B571,
     "488bcfe857b8fefff30f104c2420f30f590d55924d01f30f102541744901f30f5ee0f30f580d25924d01f30f2dc1f30f104c2424f30f590d2f924d01d1f8f30f580d09924d01660f6ec00f5bc0f30f2dc1f30f59c4d1f8f30f1103660f6ec0b0010f5bc0f30f59c4f30f114304f30f10442428f30f114308",
     "488d4c24304889fae8d2b8fefff30f104c2434f30f590d8c665001f30f10442430f30f5dc8f30f5cc1f30f59051e924d01f30f104c2420f30f5cc8f30f114c24204889f9e816b8feff0fc6c000f20f104c2420660f5bc90f5bc90f5ec8f20f110bf30f10442428f30f114308b00190909090909090909090"),
    # screen-space widget component layer (same projection, inlined)
    (0x1B58C18,
     "f30f104c2420498bcff30f107c2428f3410f59cef3410f58cff30f2dc1f30f104c2424d1f8f3410f59ce66440f6ec0f3410f58cf450f5bc0f30f2dc1d1f8660f6ef00f5bf6e86ee1fcffb001f3440f100d639d4701f3440f5ec8450f28d9450f28e1f3450f59d8f3440f59e6f3440f59cf",
     "488d4c24704c89fae82be2fcfff30f104c2474f30f590de58f4e01f30f10442470f30f5dc8f30f5cc1f3410f59c7f3440f10442420f3440f5cc04c89f9e876e1fcff450f28d8f3440f5ed8f3440f10642424f3440f5ee0f3440f104c2428f3440f5ec8b001909090909090909090909090"),
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
