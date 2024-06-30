import mysql.connector

class Database:
    def __init__(self) -> None:
        self.mydb = mysql.connector.connect(
            host="tcc-g06-ecm-2024-tcc-transporte-escolar.l.aivencloud.com",
            user="avnadmin",
            password="AVNS_yBm5abDexKF2ThjVx_z",
            database="tcc-g06"
        )
    
    def get_cursor(self):
        return self.mydb.cursor()
    