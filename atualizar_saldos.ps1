# Script para atualizar planilha de saldos no GitHub
# Use: .\atualizar_saldos.ps1

Write-Host "================================" -ForegroundColor Cyan
Write-Host "📤 Atualizando Saldos no GitHub" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Verificar se há mudanças
$status = git status --porcelain "data/1Saldos - ecossistema.xlsx"

if ($null -eq $status) {
    Write-Host "✅ Nenhuma mudança detectada" -ForegroundColor Green
    exit 0
}

Write-Host "`n📝 Mudanças detectadas:" -ForegroundColor Yellow
Write-Host $status

# Adicionar arquivo
Write-Host "`n📌 Adicionando arquivo..." -ForegroundColor Cyan
git add "data/1Saldos - ecossistema.xlsx"

# Fazer commit
$dataAtual = Get-Date -Format "dd/MM/yyyy HH:mm"
Write-Host "💾 Fazendo commit..." -ForegroundColor Cyan
git commit -m "⬆️ Atualizar saldos - $dataAtual"

# Fazer push
Write-Host "🚀 Enviando para GitHub..." -ForegroundColor Cyan
git push origin main

Write-Host "`n✅ Planilha atualizada no GitHub!" -ForegroundColor Green
Write-Host "`n📌 Próximo passo no Dashboard:" -ForegroundColor Yellow
Write-Host "   Clique em 🔄 Atualizar Dados" -ForegroundColor Yellow
