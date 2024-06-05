import requests
import csv
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Configuración de la API
access_token = 'TU TOKEN'
base_url = 'TU URL'
headers = {
    'Authorization': f'Api-Token {access_token}'
}

def get_problems(start_time, end_time):
    params = {
        'from': start_time,
        'to': end_time
    }
    response = requests.get(base_url, headers=headers, params=params, verify=False)
    response.raise_for_status()  # Para lanzar una excepción si la petición falla
    return response.json().get('problems', [])

def write_problems_to_csv(problems, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Escribir la cabecera del CSV
        writer.writerow(['Problem ID', 'Title', 'Status', 'Impact Level', 'Severity Level', 'Start Time', 'End Time'])
        # Escribir los datos de cada problema
        for problem in problems:
            writer.writerow([
                problem.get('problemId'),
                problem.get('title'),
                problem.get('status'),
                problem.get('impactLevel'),
                problem.get('severityLevel'),
                datetime.fromtimestamp(problem.get('startTime') / 1000).strftime('%Y-%m-%d %H:%M:%S'),
                datetime.fromtimestamp(problem.get('endTime') / 1000).strftime('%Y-%m-%d %H:%M:%S') if problem.get('endTime') else 'N/A'
            ])

def send_email(subject, body, filename, to_addrs, cc_addrs):
    from_addr = 'CORREO'  # Cambia esto por tu dirección de correo
    password = 'PASSWORD'  # Cambia esto por tu contraseña

    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = ', '.join(to_addrs)
    msg['Cc'] = ', '.join(cc_addrs)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(open(filename, 'rb').read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', f'attachment; filename={filename}')
    msg.attach(attachment)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addrs + cc_addrs, msg.as_string())
    server.quit()

def main():
    # Obtener las fechas de la última semana
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)

    # Convertir las fechas a timestamps en milisegundos
    start_timestamp = int(start_date.timestamp() * 1000)
    end_timestamp = int(end_date.timestamp() * 1000)

    problems = get_problems(start_timestamp, end_timestamp)
    filename = f'Informe-dynatrace-{end_date.strftime("%Y-%m-%d")}.csv'
    if problems:
        write_problems_to_csv(problems, filename)
        print(f'Se han exportado {len(problems)} problemas a "{filename}".')
        send_email(
            subject='Informe semanal de Dynatrace',
            body='Adjunto encontrarás el informe semanal de problemas de Dynatrace.',
            filename=filename,
            to_addrs=['PARA QUIEN VA EL CORREO'],
            cc_addrs=['COPIA DEL CORREO'] # Eliminar si no se requiere una copia
        )
        print('Correo enviado con éxito.')
    else:
        print('No se encontraron problemas en la última semana.')

if __name__ == '__main__':
    main()

