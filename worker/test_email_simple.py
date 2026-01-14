# -*- coding: utf-8 -*-
"""
Script de teste rápido de e-mail
Execute: python test_email_simple.py
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

print("=" * 70)
print("📧 TESTE SIMPLES DE E-MAIL")
print("=" * 70)
print()

# Configurações (VOCÊ PRECISA PREENCHER)
SMTP_USER = input("Digite seu e-mail Gmail: ").strip()
SMTP_PASSWORD = input("Digite a senha de app (16 caracteres): ").strip()
DESTINATARIO = "iago.azevedo@alura.com.br"

if not SMTP_USER or not SMTP_PASSWORD:
    print("❌ E-mail ou senha não fornecidos!")
    exit(1)

print()
print(f"📤 Enviando e-mail de teste para: {DESTINATARIO}")
print()

try:
    # Cria mensagem HTML bonita
    html = f"""
    <html>
        <body style="font-family: Arial; padding: 20px; background: #f5f5f5;">
            <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                <div style="background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%); padding: 20px; text-align: center; border-radius: 8px; margin-bottom: 20px;">
                    <h1 style="color: white; margin: 0;">✅ E-MAIL DE TESTE</h1>
                    <p style="color: #c8e6c9; margin: 10px 0 0 0;">Sistema Malga Analytics</p>
                </div>
                
                <h2 style="color: #333;">Teste Bem-Sucedido! 🎉</h2>
                
                <p style="color: #666; line-height: 1.6;">
                    Parabéns! O sistema de alertas por e-mail está <strong style="color: #4caf50;">configurado e funcionando</strong>.
                </p>
                
                <div style="background: #e8f5e9; padding: 15px; border-radius: 5px; border-left: 4px solid #4caf50; margin: 20px 0;">
                    <h3 style="color: #2e7d32; margin: 0 0 10px 0;">📋 Informações</h3>
                    <ul style="color: #2e7d32; margin: 0; line-height: 1.8;">
                        <li><strong>Destinatário:</strong> {DESTINATARIO}</li>
                        <li><strong>Data/Hora:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</li>
                        <li><strong>Status:</strong> ✅ Funcionando</li>
                    </ul>
                </div>
                
                <p style="color: #999; font-size: 12px; text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd;">
                    Sistema de Monitoramento Malga Analytics<br>
                    Você receberá alertas quando a taxa de aprovação cair abaixo de 40%
                </p>
            </div>
        </body>
    </html>
    """
    
    # Cria mensagem
    msg = MIMEMultipart('alternative')
    msg['From'] = SMTP_USER
    msg['To'] = DESTINATARIO
    msg['Subject'] = "✅ Teste de Sistema de Alertas - Malga Analytics"
    
    msg.attach(MIMEText(html, 'html'))
    
    # Envia
    print("🔄 Conectando ao servidor SMTP...")
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        print("🔐 Autenticando...")
        server.login(SMTP_USER, SMTP_PASSWORD)
        print("📨 Enviando mensagem...")
        server.send_message(msg)
    
    print()
    print("=" * 70)
    print("✅ E-MAIL ENVIADO COM SUCESSO!")
    print("=" * 70)
    print()
    print(f"📬 Verifique a caixa de entrada de: {DESTINATARIO}")
    print("   (Pode levar alguns segundos para chegar)")
    print()
    print("🎉 Sistema de alertas configurado e funcionando!")
    print()
    
except smtplib.SMTPAuthenticationError:
    print()
    print("=" * 70)
    print("❌ ERRO DE AUTENTICAÇÃO")
    print("=" * 70)
    print()
    print("💡 Possíveis causas:")
    print("   1. Você está usando a senha NORMAL do Gmail (incorreto)")
    print("   2. Você precisa criar uma SENHA DE APP específica")
    print()
    print("🔗 Como criar senha de app:")
    print("   1. Acesse: https://myaccount.google.com/apppasswords")
    print("   2. Ative verificação em 2 etapas (se não estiver ativado)")
    print("   3. Crie uma nova senha de app:")
    print("      - Escolha 'Outro (nome personalizado)'")
    print("      - Digite 'Malga Analytics'")
    print("      - Clique em 'Gerar'")
    print("   4. Use os 16 caracteres gerados (sem espaços)")
    print()

except Exception as e:
    print()
    print("=" * 70)
    print("❌ ERRO AO ENVIAR E-MAIL")
    print("=" * 70)
    print()
    print(f"Erro: {e}")
    print()
