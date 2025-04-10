import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def enviar_email(destinatario, nome):
    remetente = os.getenv("EMAIL_REMETENTE")
    senha = os.getenv("EMAIL_SENHA")

    mensagem = MIMEMultipart("alternative")
    mensagem["Subject"] = "🙏 Obrigado por se inscrever!"
    mensagem["From"] = f"Intenção de Missa <{remetente}>"
    mensagem["To"] = destinatario

    # Texto simples
    texto = f"""
    Olá {nome},

    Agradecemos por se inscrever no nosso projeto de Intenções de Missa 🙏

    Em breve entraremos em contato com mais informações.

    Deus abençoe!
    """

    # HTML formatado
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #fffaf5; padding: 20px; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e2e2e2; border-radius: 8px; padding: 30px;">
          <h2 style="color: #8B0000; text-align: center;">🙏 Obrigado por se inscrever, {nome.upper()}!</h2>
          <p style="font-size: 16px; line-height: 1.6;">
            É com alegria que recebemos o seu interesse no nosso projeto <strong>Intenções de Missa Online</strong>.
          </p>
          <p style="font-size: 16px; line-height: 1.6;">
            Em breve entraremos em contato com você para explicar os próximos passos e como participar da fase de testes.
          </p>
          <p style="font-size: 16px; line-height: 1.6;">
            Que Deus abençoe você e sua família! 🙏
          </p>
          <p style="text-align: right; font-size: 14px; margin-top: 30px; color: #555;">
            Equipe Intenção de Missa
          </p>
        </div>
      </body>
    </html>
    """

    mensagem.attach(MIMEText(texto, "plain"))
    mensagem.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(remetente, senha)
            servidor.sendmail(remetente, destinatario, mensagem.as_string())
        print(f"✅ E-mail enviado para {destinatario}")
    except Exception as e:
        print("❌ Erro ao enviar e-mail:", e)
