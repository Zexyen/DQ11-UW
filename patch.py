#!/usr/bin/env python3
"""DRAGON QUEST XI (Steam, original 2018 release) ultrawide patch - 21:9 HUD variant (v4). Run again to undo.

* Camera / FOV: true ultrawide (Hor+).
* In-game HUD, minimap, battle UI: full 21:9 width.
* Dialog & quest boxes: centred on 21:9 screen.
* Title/main menus, map menu, loading screens and pre-rendered videos: centred 16:9 (unstretched).
* Screen & loading transition fades: full 21:9 width.

Put this in the game folder (or next to the exe) and run it, or pass the exe path."""
import os, sys

# camera projection: (file offset, original bytes, patched bytes)
CAMERA = [
    # never letterbox/pillarbox to the camera's 16:9 aspect
    (0x1efa273, '0f84d0010000',
     'e9d101000090'),
    # ...and keep the 16:9 vertical FOV, widening horizontally (Hor+) instead of cropping
    (0x1efa489, '3bc17e05803a02742e803a017429807f30017423f30f10352b850d0166440f6ed1440f28de660f6ec0450f5bd20f5bc0',
     'f30f10353f850d01f30f2ac0f3440f2ad1f3410f5ec2f3440f101d70771401f3440f5dd8450f28d3f3440f5ed0eb29'),
]

# UI: (file offset, original bytes, [prior variants...], this patch's bytes or None)
UI = [
    # UI layer layout: now a jump into the code cave below, which picks full width or a centred 16:9 block
    (0x12db5669,
     'f30f100d5fc521f0f3440f1005e6182df1f3440f100de1182df1f30f1038488b8f80030000f30f5ecf4881c140010000f3440f59c70f28c1f3440f59cff30f5906f30f594e04f30f11442440410f28c0410f14c1440f28d0f20f11442464f30f114c2444f30f117c2460',
     ['f30f1038488b8f800300004881c140010000f30f1046040f28c8f30f59058db728f0f3440f1006f3410f5dc0f3440f5cc0f3440f59051de325f0450f57c9f30f5ec7f30f5ecff30f11442440f30f114c2444450f28d0f2440f11542464f30f117c246090909090909090', 'e9824db1eecccccccccccccccccccccc00cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc', 'e9824db1eecccccccccccccccccccccc00cccccc0000000000007044cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc'],
     'e9664db1eecccccccccccccccccccccc0001cccc00000000000070440000f0440020f04400e0ef44000080bf0000803f00e086440000003fcccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc'),
    # world-anchored widget shifts from the centred-HUD versions (talk bubbles, door prompts):
    # the in-game HUD is full width again, so these three go back to original
    (0x1b3b48d,
     'f30f104c2430488bcbf30f590d3e934d010f297424500f297c2440f30f580d10934d01f30f2dc1f30f104c2434f30f590d1a934d01d1f8f30f580df4924d01660f6ef80f5bfff30f2dc1d1f8660f6ef00f5bf6e8ebb8feffb001f30f1015e1744901f30f5ed00f28caf30f59d60f28742450f30f59cf0f287c2440eb08',
     ['488d4c24204889dae8b6b9fefff30f104c2424f30f590d70675001f30f10442420f30f5dc8f30f5cc1f30f590502934d01f30f104c2430f30f5cc8f30f114c24304889d9e8fab8feff0fc6c000f20f104c2430660f5bc90f5bc90f5ec8660f70d155b001e91c000000cccccccccccccccccccccccccccccccccccccccc'],
     None),
    (0x1b3b571,
     '488bcfe857b8fefff30f104c2420f30f590d55924d01f30f102541744901f30f5ee0f30f580d25924d01f30f2dc1f30f104c2424f30f590d2f924d01d1f8f30f580d09924d01660f6ec00f5bc0f30f2dc1f30f59c4d1f8f30f1103660f6ec0b0010f5bc0f30f59c4f30f114304f30f10442428f30f114308',
     ['488d4c24304889fae8d2b8fefff30f104c2434f30f590d8c665001f30f10442430f30f5dc8f30f5cc1f30f59051e924d01f30f104c2420f30f5cc8f30f114c24204889f9e816b8feff0fc6c000f20f104c2420660f5bc90f5bc90f5ec8f20f110bf30f10442428f30f114308b00190909090909090909090'],
     None),
    (0x1b58c18,
     'f30f104c2420498bcff30f107c2428f3410f59cef3410f58cff30f2dc1f30f104c2424d1f8f3410f59ce66440f6ec0f3410f58cf450f5bc0f30f2dc1d1f8660f6ef00f5bf6e86ee1fcffb001f3440f100d639d4701f3440f5ec8450f28d9450f28e1f3450f59d8f3440f59e6f3440f59cf',
     ['488d4c24704c89fae82be2fcfff30f104c2474f30f590de58f4e01f30f10442470f30f5dc8f30f5cc1f3410f59c7f3440f10442420f3440f5cc04c89f9e876e1fcff450f28d8f3440f5ed8f3440f10642424f3440f5ee0f3440f104c2428f3440f5ec8b001909090909090909090909090'],
     None),
    # code caves (0x18cb1b0, 0x826720) and the hooks that jump into them
    (0x18cb1b0,
     'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc',
     ['c605c2b24e110140534883ec20e954215a01ccccccccccccccccccccccccccccc605a2b24e110040534883ec20e9d4475a01cccccccccccccccccccccccccccc50524150415141524153534889e34881ec900000004883e4f00f295424200f295c24300f296424400f296c2450c644246001803d1d4e770200752f803d47b24e11007526488b056de59d024885c0741a488b88f00600004885c9740ee8ffd8ddfe84c07405c6442460000fb64c24600f285424200f285c24300f286424400f286c24504889dc5b415b415a415941585a5884c90f856f000000f30f100d3f777001f3440f1005c6ca7b02f3440f100dc1ca7b02f30f1038488b8f80030000f30f5ecf4881c140010000f3440f59c70f28c1f3440f59cff30f5906f30f594e04f30f11442440410f28c0410f14c1440f28d0f20f11442464f30f114c2444f30f117c2460e9dbb14e11f30f1038488b8f800300004881c140010000f30f1046040f28c8f30f5905fe687701f3440f1006f3410f5dc0f3440f5cc0f3440f59058e947401450f57c9f30f5ec7f30f5ecff30f11442440f30f114c2444450f28d0f2440f11542464f30f117c2460e973b14e11cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc', 'c605c2b24e110140534883ec20e954215a01ccccccccccccccccccccccccccccc605a2b24e110040534883ec20e9d4475a01cccccccccccccccccccccccccccc50524150415141524153534889e34881ec900000004883e4f00f295424200f295c24300f296424400f296c2450c644246001803d1d4e7702000f85a9000000803d43b24e11000f859c000000488b0565e59d024885c00f848c000000488b88f00600004885c90f847c00000048894c2468e8ead8ddfe84c00f846a000000488b4c2468e888adddfe4885c074418b90c002000085d27e3783fa207e05ba200000004c8b80b80200004d85c0742131c94d8b0cc84d85c97410458b51404183fa1374264183fa147420ffc139d17ce1488b4c2468e81873180984c07407c644246002eb05c6442460000fb64c24600f285424200f285c24300f286424400f286c24504889dc5b415b415a415941585a5880f9010f847800000080f9020f84d7000000f30f100db7767001f3440f10053eca7b02f3440f100d39ca7b02f30f1038488b8f80030000f30f5ecf4881c140010000f3440f59c70f28c1f3440f59cff30f5906f30f594e04f30f11442440410f28c0410f14c1440f28d0f20f11442464f30f114c2444f30f117c2460e953b14e11f30f1038488b8f800300004881c140010000f30f1046040f28c8f30f590576687701f3440f1006f3410f5dc0f3440f5cc0f3440f590506947401450f57c9f30f5ec7f30f5ecff30f11442440f30f114c2444450f28d0f2440f11542464f30f117c2460e9ebb04e11f30f1038f30f1006f30f104e04440f28c0f3440f5905d683a601f3410f5ff8f30f5ec7f30f5ecff30f11442440f30f114c2444450f57c9450f57d2f2440f11542464f30f117c2460488b8f800300004881c140010000e990b04e11ccccccccccccccccccccccccccf30f59058083a6010f5bc9f30f590d75c08b01f30f110512b04e11f30f5dc1f30f100d06b04e11f30f5cc8f30f590dfeaf4e11f30f110df2af4e11f30f118398050000f30f11839c050000e917b60701f30f1005d5af4e110f57c90f2fc176468b883802000083f9017e3b4c8b8830020000ba010000004d8b14d14d85d27420f3410f104a20f30f58c8f3410f114a20f3410f104a28f30f58c8f3410f114a28ffc239ca7cd14c8bc0488d9530040000488d8db0020000e980ff0701cccccccccccccccccccccccccccccccccccccccccccccccccccccc'],
     'c605c2b24e110140534883ec20e954215a01c605b0b24e110040534883ec20e9e2475a0150524150415141524153534889e34881ec900000004883e4f00f295424200f295c24300f296424400f296c2450c644246001803d394e7702000f85e7000000803d5fb24e11000f85da000000488b0581e59d024885c00f84ca000000488b88f00600004885c90f84ba00000048894c2468e806d9ddfe84c00f84a8000000488b4c2468e8a4adddfe4885c074418b90c002000085d27e3783fa207e05ba200000004c8b80b80200004d85c0742131c94d8b0cc84d85c97410458b51404183fa1374644183fa14745effc139d17ce1488b4c2468e83473180984c0753e488b4c2468e81678c3fe4885c074360f57d2488b90b00800004885d274090f2f92181400007217488b90300400004885d274120f2f92181400007202eb07c644246002eb05c6442460000fb64c2460880d75b14e110f285424200f285c24300f286424400f286c24504889dc5b415b415a415941585a5880f9010f847800000080f9020f84d7000000f30f100d8f767001f3440f100516ca7b02f3440f100d11ca7b02f30f1038488b8f80030000f30f5ecf4881c140010000f3440f59c70f28c1f3440f59cff30f5906f30f594e04f30f11442440410f28c0410f14c1440f28d0f20f11442464f30f114c2444f30f117c2460e92bb14e11f30f1038488b8f800300004881c140010000f30f1046040f28c8f30f59054e687701f3440f1006f3410f5dc0f3440f5cc0f3440f5905de937401450f57c9f30f5ec7f30f5ecff30f11442440f30f114c2444450f28d0f2440f11542464f30f117c2460e9c3b04e11f30f1038f30f1006f30f104e04440f28c0f3440f5905ae83a601f3410f5ff8f30f5ec7f30f5ecff30f11442440f30f114c2444450f57c9450f57d2f2440f11542464f30f117c2460488b8f800300004881c140010000e968b04e11f30f59056583a6010f5bc9f30f590d5ac08b01f30f1105f7af4e11f30f5dc1f30f100debaf4e11f30f5cc8f30f590de3af4e11f30f110dd7af4e11f30f118398050000f30f11839c050000e9fcb50701f30f1005baaf4e110f57c90f2fc176468b883802000083f9017e3b4c8b8830020000ba010000004d8b14d14d85d27420f3410f104a20f30f58c8f3410f114a20f3410f104a28f30f58c8f3410f114a28ffc239ca7cd14c8bc0488d9530040000488d8db0020000e965ff0701'),
    (0x826720,
     'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc',
     [],
     'f3440f5cc1f30f11742440803d48fd5812010f848b000000f3410f105d000f2e1d44fd58120f86780000000f2e353bfd5812726f0f2e352efd58127766440f2e052cfd5812725c440f2e0526fd58127752498b0048bad0235b43010000004839d0743748ba981b5c43010000004839d0750e84c97524440f2e0dfbfc5812731a0f28cbf30f5c0ddafc5812f30f590deafc5812f3440f58c1eb090f28f3f30f11742440e90c277512'),
    (0x2e6d310,
     '40534883ec20',
     ['e99bdea5fe90'],
     'e99bdea5fe90'),
    (0x2e6f9b0,
     '40534883ec20',
     ['e91bb8a5fe90'],
     'e90db8a5fe90'),
    (0x2946a94,
     'f30f59053ccd9e000f5bc9f30f118398050000f30f590d290a8400f30f118b9c050000',
     ['e9b749f8fe909090909090909090909090909090909090909090909090909090909090'],
     'e9d249f8fe909090909090909090909090909090909090909090909090909090909090'),
    (0x294b47b,
     '4c8bc0488d9530040000488d8db0020000',
     ['e92000f8fe909090909090909090909090'],
     'e93b00f8fe909090909090909090909090'),
    (0x12f780c9,
     'f30f11742440f3440f5cc1',
     [],
     'e952d88aed909090909090'),
]

here = os.path.dirname(os.path.abspath(__file__))
exe = sys.argv[1] if len(sys.argv) > 1 else next(
    (p for p in (os.path.join(here, "DRAGON QUEST XI.exe"),
                 os.path.join(here, "Game", "Binaries", "Win64", "DRAGON QUEST XI.exe")) if os.path.exists(p)), None)
if not exe:
    sys.exit("Game exe not found. Put this file in the DRAGON QUEST XI folder or next to the exe.")
try:
    f = open(exe, "r+b")
except OSError as e:
    sys.exit("Cannot open the exe for writing (is the game running?): %s" % e)
with f:
    def read(off, n):
        f.seek(off)
        return f.read(n).hex()
    def is_at(off, h):
        return read(off, len(h) // 2) == h
    def want(u):
        return u[3] if u[3] else u[1]
    ok = all(is_at(o, a) or is_at(o, b) for o, a, b in CAMERA) and \
         all(any(is_at(u[0], x) for x in [u[1]] + u[2] + ([u[3]] if u[3] else [])) for u in UI)
    if not ok:
        sys.exit("Unrecognised exe (different game version?) - nothing was changed.")
    is_patched = all(is_at(o, b) for o, a, b in CAMERA) and all(is_at(u[0], want(u)) for u in UI)
    if is_patched:
        for o, a, b in CAMERA:
            f.seek(o); f.write(bytes.fromhex(a))
        for u in UI:
            f.seek(u[0]); f.write(bytes.fromhex(u[1]))
        msg = "Patch removed: exe is back to original."
    else:
        for o, a, b in CAMERA:
            f.seek(o); f.write(bytes.fromhex(b))
        for u in UI:
            f.seek(u[0]); f.write(bytes.fromhex(want(u)))
        msg = "Patched: ultrawide enabled (21:9 HUD & fades; centred dialog/quest/menus/map/loading/videos)."
print(msg, "Run again to toggle.")
