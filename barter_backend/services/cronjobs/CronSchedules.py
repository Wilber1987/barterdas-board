from datetime import datetime

from barter_backend.services.cronjobs.AutomaticReinvestment import AutomaticReinvestment
import pycron

#@pycron.cron("0 0 7 * *")
@pycron.cron("* * * * */5")  # 0 0 7 * * los 7
async def cronSchedule(timestamp: datetime):
    print(f"##cron job running at {timestamp} ******")
    AutomaticReinvestment().do()

def main():
    # Configuración y programación de tareas pycron aquí
    # ...
    # Inicia pycron
    print(f"cron start--->")
    pycron.start()
