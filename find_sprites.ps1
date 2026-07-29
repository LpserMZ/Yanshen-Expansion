$file = "d:\Documents\Paradox Interactive\Europa Universalis IV\mod\YanShen Expansion\interface\MP.gfx"
$lines = Get-Content $file
$i = 0
$results = @()
while ($i -lt $lines.Count) {
    $line = $lines[$i]
    if ($line -match '^\s*spriteType\s*=\s*\{') {
        $startLine = $i + 1
        $blockLines = @()
        $braceCount = 0
        $j = $i
        while ($j -lt $lines.Count) {
            $blockLines += $lines[$j]
            $braceCount += ($lines[$j].ToCharArray() | Where-Object {$_ -eq '{'}).Count
            $braceCount -= ($lines[$j].ToCharArray() | Where-Object {$_ -eq '}'}).Count
            if ($braceCount -eq 0) {
                break
            }
            $j++
        }
        $block = $blockLines -join "`n"
        if ($block -match 'texturefile\s*=\s*"([^"]+)"') {
            $texFile = $matches[1]
            # Check if texturefile does NOT contain "idea_EU4" (substring match, so "ideas_EU4" also matches)
            if ($texFile -notmatch 'idea_EU4') {
                if ($block -match 'name\s*=\s*"([^"]+)"') {
                    $name = $matches[1]
                    $results += [PSCustomObject]@{
                        StartLine = $startLine
                        Name = $name
                        TextureFile = $texFile
                    }
                }
            }
        }
        $i = $j
    }
    $i++
}
$results | ForEach-Object { "{0,-8} | {1,-40} | {2}" -f $_.StartLine, $_.Name, $_.TextureFile }
Write-Host "`n=== 总计: $($results.Count) 个 spriteType 不包含 idea_EU4 ==="
