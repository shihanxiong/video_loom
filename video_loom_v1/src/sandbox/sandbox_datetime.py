from datetime import datetime

print(datetime.strptime("0:01:15", "%H:%M:%S").time().total_seconds())
