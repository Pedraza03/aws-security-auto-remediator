# 🛡️ AWS Sentinel: Remediación Automática de Red

Este proyecto implementa una solución de **DevSecOps** para mitigar riesgos de seguridad en tiempo real dentro de una infraestructura AWS.

## 📋 Arquitectura
- **EventBridge**: Disparador programado (cada 5 min).
- **AWS Lambda**: Lógica de detección y remediación en Python.
- **Boto3**: SDK de AWS para interactuar con EC2 y SNS.
- **SNS**: Alertas inmediatas al equipo de seguridad.

## 🚀 Cómo funciona
1. El sistema audita todos los **Security Groups** buscando reglas de entrada (Inbound) abiertas al mundo (`0.0.0.0/0`).
2. Al identificar una regla insegura en puertos críticos (22, 80, 443), el script la **revoca instantáneamente**.
3. Se envía una notificación por correo electrónico con los detalles del grupo remediado.

## 📸 Evidencias
### Detección en Logs
![Logs de CloudWatch](<img width="1556" height="668" alt="Screenshot 2026-02-22 194733" src="https://github.com/user-attachments/assets/60c52cb0-bcaa-492b-a2b4-781ae218a0e0" />)

### Notificación de Alerta
![Correo SNS](<img width="1519" height="574" alt="Screenshot 2026-02-22 194851" src="https://github.com/user-attachments/assets/577863a1-8a28-4c31-a4d9-1943823122b8" />)
