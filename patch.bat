@echo off
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((Get-Content -Raw -LiteralPath '%~f0') -replace '(?s)^.*?#PS\r?\n')"
pause
exit /b
#PS
# Same patch table as patch.py: file offset, original bytes, patched bytes
$patches = @(
  @(0x1EFA273, '0f84d0010000', 'e9d101000090'),
  @(0x1EFA489, '3bc17e05803a02742e803a017429807f30017423f30f10352b850d0166440f6ed1440f28de660f6ec0450f5bd20f5bc0', 'f30f10353f850d01f30f2ac0f3440f2ad1f3410f5ec2f3440f101d70771401f3440f5dd8450f28d3f3440f5ed0eb29'),
  @(0x12DB5669, 'f30f100d5fc521f0f3440f1005e6182df1f3440f100de1182df1f30f1038488b8f80030000f30f5ecf4881c140010000f3440f59c70f28c1f3440f59cff30f5906f30f594e04f30f11442440410f28c0410f14c1440f28d0f20f11442464f30f114c2444f30f117c2460', 'f30f1038488b8f800300004881c140010000f30f1046040f28c8f30f59058db728f0f3440f1006f3410f5dc0f3440f5cc0f3440f59051de325f0450f57c9f30f5ec7f30f5ecff30f11442440f30f114c2444450f28d0f2440f11542464f30f117c246090909090909090'),
  @(0x1B3B48D, 'f30f104c2430488bcbf30f590d3e934d010f297424500f297c2440f30f580d10934d01f30f2dc1f30f104c2434f30f590d1a934d01d1f8f30f580df4924d01660f6ef80f5bfff30f2dc1d1f8660f6ef00f5bf6e8ebb8feffb001f30f1015e1744901f30f5ed00f28caf30f59d60f28742450f30f59cf0f287c2440eb08', '488d4c24204889dae8b6b9fefff30f104c2424f30f590d70675001f30f10442420f30f5dc8f30f5cc1f30f590502934d01f30f104c2430f30f5cc8f30f114c24304889d9e8fab8feff0fc6c000f20f104c2430660f5bc90f5bc90f5ec8660f70d155b001e91c000000cccccccccccccccccccccccccccccccccccccccc'),
  @(0x1B3B571, '488bcfe857b8fefff30f104c2420f30f590d55924d01f30f102541744901f30f5ee0f30f580d25924d01f30f2dc1f30f104c2424f30f590d2f924d01d1f8f30f580d09924d01660f6ec00f5bc0f30f2dc1f30f59c4d1f8f30f1103660f6ec0b0010f5bc0f30f59c4f30f114304f30f10442428f30f114308', '488d4c24304889fae8d2b8fefff30f104c2434f30f590d8c665001f30f10442430f30f5dc8f30f5cc1f30f59051e924d01f30f104c2420f30f5cc8f30f114c24204889f9e816b8feff0fc6c000f20f104c2420660f5bc90f5bc90f5ec8f20f110bf30f10442428f30f114308b00190909090909090909090'),
  @(0x1B58C18, 'f30f104c2420498bcff30f107c2428f3410f59cef3410f58cff30f2dc1f30f104c2424d1f8f3410f59ce66440f6ec0f3410f58cf450f5bc0f30f2dc1d1f8660f6ef00f5bf6e86ee1fcffb001f3440f100d639d4701f3440f5ec8450f28d9450f28e1f3450f59d8f3440f59e6f3440f59cf', '488d4c24704c89fae82be2fcfff30f104c2474f30f590de58f4e01f30f10442470f30f5dc8f30f5cc1f3410f59c7f3440f10442420f3440f5cc04c89f9e876e1fcff450f28d8f3440f5ed8f3440f10642424f3440f5ee0f3440f104c2428f3440f5ec8b001909090909090909090909090')
)
$exe = 'DRAGON QUEST XI.exe', 'Game/Binaries/Win64/DRAGON QUEST XI.exe' | ForEach-Object { Join-Path (Get-Location) $_ } | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (!$exe) { Write-Host 'Game exe not found. Put this file in the DRAGON QUEST XI folder or next to the exe.'; return }
$f = [IO.File]::Open($exe, 'Open', 'ReadWrite')
try {
  $read = { param($off, $n) $b = New-Object byte[] $n; $null = $f.Seek($off, 'Begin'); $null = $f.Read($b, 0, $n); -join ($b | ForEach-Object { $_.ToString('x2') }) }
  # each site must hold either its original or its patched bytes (so older versions of this patch upgrade)
  $nNew = @($patches | Where-Object { (& $read $_[0] ($_[2].Length / 2)) -eq $_[2] }).Count
  $nOld = @($patches | Where-Object { (& $read $_[0] ($_[1].Length / 2)) -eq $_[1] }).Count
  if ($nNew + $nOld -ne $patches.Count) { Write-Host 'Unrecognised exe (different game version?) - nothing was changed.'; return }
  $isOld = $nNew -ne $patches.Count
  foreach ($p in $patches) {
    $hex = if ($isOld) { $p[2] } else { $p[1] }
    $bytes = [byte[]]($hex -split '(..)' -ne '' | ForEach-Object { [Convert]::ToByte($_, 16) })
    $null = $f.Seek($p[0], 'Begin'); $f.Write($bytes, 0, $bytes.Length)
  }
  if ($isOld) { Write-Host 'Patched: ultrawide enabled. Run again to undo.' } else { Write-Host 'Patch removed: exe is back to original. Run again to re-apply.' }
} finally { $f.Close() }
