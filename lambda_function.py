import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2 = boto3.client('ec2')
sns = boto3.client('sns')

SNS_TOPIC_ARN = 'arn:aws:sns:us-east-2:942088612074:Alerta-Seguridad-Cloud' 

DANGEROUS_PORTS = [22, 80, 443]

def lambda_handler(event, context):
    try:
        response = ec2.describe_security_groups()
        remediations_count = 0

        for sg in response['SecurityGroups']:
            sg_id = sg['GroupId']
            sg_name = sg.get('GroupName', 'Sin Nombre')
            
            for permission in sg.get('IpPermissions', []):
                from_port = permission.get('FromPort')
                
                if from_port in DANGEROUS_PORTS:
                    for ip_range in permission.get('IpRanges', []):
                        if ip_range.get('CidrIp') == '0.0.0.0/0':
                            # 1. Remediacion
                            ec2.revoke_security_group_ingress(GroupId=sg_id, IpPermissions=[permission])
                            
                            # 2. Mensaje de Alerta
                            alert_msg = f"ALERTA DEVSECOPS: Vulnerabilidad remediada.\n\n" \
                                        f"Grupo: {sg_name} ({sg_id})\n" \
                                        f"Acción: Se cerró el puerto {from_port} abierto al mundo.\n" \
                                        f"Estado: INFRAESTRUCTURA SEGURA"
                            
                            # 3. Notificación via SNS
                            sns.publish(TopicArn=SNS_TOPIC_ARN, Message=alert_msg, Subject=" Remediación Automática AWS")
                            
                            logger.info(f"Remediado y notificado: {sg_id}")
                            remediations_count += 1
        
        return {'statusCode': 200, 'body': f"Escaneo completado. Remediaciones: {remediations_count}"}
    except Exception as e:
        logger.error(str(e))
        raise e
