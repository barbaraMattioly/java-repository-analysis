from dateutil import parser
from datetime import datetime, timezone

# Função para formatar uma data  do formato ISO (yyyy-MM-ddTHH:mm:ssZ) para dd/MM/yyyy HH:mm:ss
def format_date(iso_date, date_format="%d/%m/%Y %H:%M:%S"):
    date = parser.isoparse(iso_date)
    
    return date.strftime(date_format)

# Função para calcular o tempo em dia entre a data atual e a data recebida
def calculate_time_between_dates_in_days(iso_date):
    creation_date = parser.isoparse(iso_date)
    now = datetime.now(timezone.utc)
    age = (now - creation_date).days
    return age