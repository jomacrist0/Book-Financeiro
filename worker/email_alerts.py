# -*- coding: utf-8 -*-
"""
Sistema de Alertas por E-mail
Envia notificações quando a taxa de aprovação fica abaixo de 40%
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Configurações de E-mail
ALERT_EMAIL_TO = "iago.azevedo@alura.com.br"
ALERT_THRESHOLD = 40.0  # Taxa mínima aceitável (%)

# Gmail SMTP (você precisará configurar uma senha de app)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "seu-email@gmail.com"  # Substitua pelo seu e-mail
SMTP_PASSWORD = "sua-senha-app"  # Substitua pela senha de app do Gmail

class EmailAlertSystem:
    """Sistema de alertas por e-mail"""
    
    def __init__(self, threshold=ALERT_THRESHOLD):
        self.threshold = threshold
        self.last_alert_time = None
        self.cooldown_minutes = 30  # Evita spam - envia no máximo 1 e-mail a cada 30min
    
    def check_and_send_alert(self, approval_rate, period='hour', metrics=None):
        """
        Verifica taxa e envia alerta se necessário
        
        Args:
            approval_rate: Taxa de aprovação atual (%)
            period: Período de análise ('minute', 'hour', 'day')
            metrics: Dicionário com métricas adicionais
        """
        if approval_rate >= self.threshold:
            return False  # Taxa OK, não precisa alertar
        
        # Verifica cooldown
        now = datetime.now()
        if self.last_alert_time:
            minutes_since_last = (now - self.last_alert_time).total_seconds() / 60
            if minutes_since_last < self.cooldown_minutes:
                logger.info(f"⏳ Alerta em cooldown ({minutes_since_last:.1f} min desde o último)")
                return False
        
        # Envia alerta
        success = self._send_email_alert(approval_rate, period, now, metrics)
        if success:
            self.last_alert_time = now
        
        return success
    
    def _send_email_alert(self, approval_rate, period, timestamp, metrics=None):
        """Envia e-mail de alerta"""
        try:
            # Prepara conteúdo do e-mail
            subject = f"🚨 ALERTA CRÍTICO: Taxa de Aprovação em {approval_rate:.1f}%"
            
            # Monta corpo do e-mail em HTML
            body_html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                    <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                        
                        <!-- Header -->
                        <div style="background: linear-gradient(135deg, #ff1744 0%, #c62828 100%); padding: 30px; text-align: center;">
                            <h1 style="color: white; margin: 0; font-size: 28px;">
                                🚨 ALERTA CRÍTICO
                            </h1>
                            <p style="color: #ffcdd2; margin: 10px 0 0 0; font-size: 16px;">
                                Taxa de Aprovação Abaixo do Limite
                            </p>
                        </div>
                        
                        <!-- Conteúdo Principal -->
                        <div style="padding: 30px;">
                            <div style="background: #ffebee; border-left: 4px solid #ff1744; padding: 20px; margin-bottom: 20px; border-radius: 4px;">
                                <h2 style="color: #c62828; margin: 0 0 10px 0; font-size: 20px;">
                                    Taxa Atual: {approval_rate:.1f}%
                                </h2>
                                <p style="color: #666; margin: 0; font-size: 14px;">
                                    Limite mínimo esperado: <strong>{self.threshold}%</strong><br>
                                    Diferença: <strong style="color: #ff1744;">-{self.threshold - approval_rate:.1f} pontos percentuais</strong>
                                </p>
                            </div>
                            
                            <h3 style="color: #333; font-size: 16px; margin: 20px 0 10px 0;">📊 Detalhes da Análise</h3>
                            <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                                <tr style="background: #f5f5f5;">
                                    <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold;">Período</td>
                                    <td style="padding: 12px; border: 1px solid #ddd;">{period}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold;">Data/Hora</td>
                                    <td style="padding: 12px; border: 1px solid #ddd;">{timestamp.strftime('%d/%m/%Y %H:%M:%S')}</td>
                                </tr>
            """
            
            # Adiciona métricas extras se disponíveis
            if metrics:
                if 'total_transactions' in metrics:
                    body_html += f"""
                                <tr style="background: #f5f5f5;">
                                    <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold;">Total de Transações</td>
                                    <td style="padding: 12px; border: 1px solid #ddd;">{metrics['total_transactions']:,}</td>
                                </tr>
                    """
                if 'approved_count' in metrics:
                    body_html += f"""
                                <tr>
                                    <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold;">Aprovadas + Canceladas</td>
                                    <td style="padding: 12px; border: 1px solid #ddd;">{metrics.get('approved_count', 0) + metrics.get('cancelled_count', 0):,}</td>
                                </tr>
                    """
                if 'failed_count' in metrics:
                    body_html += f"""
                                <tr style="background: #f5f5f5;">
                                    <td style="padding: 12px; border: 1px solid #ddd; font-weight: bold;">Falhadas</td>
                                    <td style="padding: 12px; border: 1px solid #ddd; color: #ff1744;">{metrics['failed_count']:,}</td>
                                </tr>
                    """
            
            body_html += """
                            </table>
                            
                            <div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; border-radius: 4px;">
                                <h3 style="color: #856404; margin: 0 0 10px 0; font-size: 16px;">⚠️ Ações Recomendadas</h3>
                                <ul style="color: #856404; margin: 0; padding-left: 20px; line-height: 1.8;">
                                    <li>Verificar status das integrações com adquirentes</li>
                                    <li>Analisar configurações do sistema antifraude</li>
                                    <li>Revisar tentativas de transações suspeitas</li>
                                    <li>Verificar logs de erro da plataforma Malga</li>
                                    <li>Contactar suporte técnico se persistir</li>
                                </ul>
                            </div>
                        </div>
                        
                        <!-- Footer -->
                        <div style="background: #f5f5f5; padding: 20px; text-align: center; border-top: 1px solid #ddd;">
                            <p style="color: #999; margin: 0; font-size: 12px;">
                                Sistema de Monitoramento Malga Analytics<br>
                                Este é um alerta automático. Para mais informações, acesse a dashboard.
                            </p>
                        </div>
                        
                    </div>
                </body>
            </html>
            """
            
            # Cria mensagem
            msg = MIMEMultipart('alternative')
            msg['From'] = SMTP_USER
            msg['To'] = ALERT_EMAIL_TO
            msg['Subject'] = subject
            
            # Adiciona corpo HTML
            msg.attach(MIMEText(body_html, 'html'))
            
            # Envia e-mail
            logger.info(f"📧 Enviando alerta por e-mail para {ALERT_EMAIL_TO}...")
            
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.send_message(msg)
            
            logger.info(f"✅ Alerta enviado com sucesso para {ALERT_EMAIL_TO}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao enviar e-mail de alerta: {e}")
            return False
    
    def send_test_email(self):
        """Envia e-mail de teste"""
        try:
            subject = "✅ Teste de Sistema de Alertas - Malga Analytics"
            
            body_html = """
            <html>
                <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                    <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                        
                        <!-- Header -->
                        <div style="background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%); padding: 30px; text-align: center;">
                            <h1 style="color: white; margin: 0; font-size: 28px;">
                                ✅ E-MAIL DE TESTE
                            </h1>
                            <p style="color: #c8e6c9; margin: 10px 0 0 0; font-size: 16px;">
                                Sistema de Alertas Funcionando!
                            </p>
                        </div>
                        
                        <!-- Conteúdo -->
                        <div style="padding: 30px;">
                            <p style="color: #333; font-size: 16px; line-height: 1.6;">
                                Olá! 👋
                            </p>
                            <p style="color: #333; font-size: 16px; line-height: 1.6;">
                                Este é um <strong>e-mail de teste</strong> do sistema de alertas da Malga Analytics.
                            </p>
                            <p style="color: #333; font-size: 16px; line-height: 1.6;">
                                Se você está recebendo esta mensagem, significa que o sistema de notificações está 
                                <strong style="color: #4caf50;">configurado e funcionando corretamente</strong>! 🎉
                            </p>
                            
                            <div style="background: #e8f5e9; border-left: 4px solid #4caf50; padding: 20px; margin: 20px 0; border-radius: 4px;">
                                <h3 style="color: #2e7d32; margin: 0 0 10px 0; font-size: 16px;">📋 Configurações Atuais</h3>
                                <ul style="color: #2e7d32; margin: 0; padding-left: 20px; line-height: 1.8;">
                                    <li>Limite de alerta: <strong>40%</strong></li>
                                    <li>Destinatário: <strong>iago.azevedo@alura.com.br</strong></li>
                                    <li>Cooldown entre alertas: <strong>30 minutos</strong></li>
                                    <li>Status: <strong style="color: #4caf50;">✅ ATIVO</strong></li>
                                </ul>
                            </div>
                            
                            <p style="color: #666; font-size: 14px; line-height: 1.6; margin-top: 20px;">
                                Você receberá alertas automáticos sempre que a taxa de aprovação ficar abaixo de 40%.
                            </p>
                        </div>
                        
                        <!-- Footer -->
                        <div style="background: #f5f5f5; padding: 20px; text-align: center; border-top: 1px solid #ddd;">
                            <p style="color: #999; margin: 0; font-size: 12px;">
                                Sistema de Monitoramento Malga Analytics<br>
                                Teste realizado em """ + datetime.now().strftime('%d/%m/%Y %H:%M:%S') + """
                            </p>
                        </div>
                        
                    </div>
                </body>
            </html>
            """
            
            # Cria mensagem
            msg = MIMEMultipart('alternative')
            msg['From'] = SMTP_USER
            msg['To'] = ALERT_EMAIL_TO
            msg['Subject'] = subject
            
            # Adiciona corpo HTML
            msg.attach(MIMEText(body_html, 'html'))
            
            # Envia e-mail
            print(f"📧 Enviando e-mail de teste para {ALERT_EMAIL_TO}...")
            
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.send_message(msg)
            
            print(f"✅ E-mail de teste enviado com sucesso para {ALERT_EMAIL_TO}!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao enviar e-mail de teste: {e}")
            print(f"\n💡 Dica: Certifique-se de que:")
            print(f"   1. O e-mail remetente está correto em SMTP_USER")
            print(f"   2. Você está usando uma 'Senha de App' do Gmail (não a senha normal)")
            print(f"   3. Para criar uma senha de app: https://myaccount.google.com/apppasswords")
            return False


# Instância global do sistema de alertas
alert_system = EmailAlertSystem(threshold=ALERT_THRESHOLD)


if __name__ == "__main__":
    """Script de teste - execute com: python email_alerts.py"""
    print("=" * 60)
    print("🧪 TESTE DO SISTEMA DE ALERTAS POR E-MAIL")
    print("=" * 60)
    
    # Envia e-mail de teste
    alert_system.send_test_email()
