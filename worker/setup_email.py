# -*- coding: utf-8 -*-
"""
Script para configurar e testar o sistema de e-mails
Execute este script para configurar suas credenciais de e-mail
"""

import os
import sys

print("=" * 70)
print("📧 CONFIGURAÇÃO DO SISTEMA DE ALERTAS POR E-MAIL")
print("=" * 70)
print()

print("Para enviar e-mails via Gmail, você precisa:")
print("1. Ativar a verificação em 2 etapas na sua conta Google")
print("2. Criar uma 'Senha de App' específica para este sistema")
print()
print("🔗 Criar senha de app: https://myaccount.google.com/apppasswords")
print("   (Escolha: Outro > Digite 'Malga Analytics')")
print()
print("-" * 70)
print()

# Solicita informações
email_from = input("Digite seu e-mail remetente (Gmail): ").strip()
if not email_from:
    email_from = "seu-email@gmail.com"

print()
print("⚠️  IMPORTANTE: Use a SENHA DE APP, não sua senha normal do Gmail!")
senha_app = input("Digite a senha de app (16 caracteres): ").strip()

print()
print("-" * 70)
print("📝 Resumo da Configuração:")
print(f"   E-mail remetente: {email_from}")
print(f"   E-mail destinatário: iago.azevedo@alura.com.br")
print(f"   Senha configurada: {'✅ Sim' if senha_app else '❌ Não'}")
print("-" * 70)
print()

if not senha_app:
    print("❌ Senha não fornecida. Configuração cancelada.")
    sys.exit(1)

# Atualiza o arquivo email_alerts.py
try:
    with open('email_alerts.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Substitui as credenciais
    content = content.replace('SMTP_USER = "seu-email@gmail.com"', f'SMTP_USER = "{email_from}"')
    content = content.replace('SMTP_PASSWORD = "sua-senha-app"', f'SMTP_PASSWORD = "{senha_app}"')
    
    with open('email_alerts.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Arquivo email_alerts.py atualizado com sucesso!")
    print()
    
    # Testa o envio
    print("=" * 70)
    print("🧪 ENVIANDO E-MAIL DE TESTE...")
    print("=" * 70)
    print()
    
    # Importa e testa
    from email_alerts import alert_system
    alert_system.send_test_email()
    
except Exception as e:
    print(f"❌ Erro: {e}")
    print()
    print("💡 Execute este script no diretório 'worker/':")
    print("   cd worker")
    print("   python setup_email.py")
