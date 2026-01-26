from datetime import datetime

class NBADataProcessor:
    @staticmethod
    def format_birth_date(raw_date):
        try:
            dt = datetime.strptime(raw_date, "%b %d, %Y")
            return dt.strftime("%d/%m/%Y")
        except Exception:
            return raw_date