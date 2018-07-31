import pyodbc
import datetime


DB_CH1_SCP98 = 'RTKPIData1-PHX-VIP.AdsPSSCPSQL-Prod-CH1.Ch1.ap.phx.gb'
DB_BN1_SCP98 = 'RTKPIData1-PHX-VIP.AdsPSSCPSQL-Prod-BN1.Bn1.ap.phx.gb'
DB_CO4_SCP98 = 'RTKPIData1-VIP.AdsPSSCPSQL-INT-CO4.CO4.ap.gbl'
DB_LOCAL = 'localhost'

class ODBC_MS:
        
    def __init__(self):
        ''''' initialization '''  
        self.failed = 0
        self.successful = 0
        
    def _GetConnect(self):    
        self.conn = pyodbc.connect(DRIVER='{SQL Server}', SERVER=DB_LOCAL,
                                   DATABASE='RTKPIData', UID='scp', PWD='scp#1')
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "connected failed!")
        else:
            return cur

    def ExecQuery(self, sql):
        cur = self._GetConnect()
        cur.execute(sql)
        ret = cur.fetchall()
        cur.close()
        self.conn.close()

        return ret

    def ExecNoQuery(self, sql):
        try:
            cur = self._GetConnect()
            cur.execute(sql)
            self.conn.commit()
            cur.close()
            self.conn.close()
        except Exception as err:
            self.failed += 1
            print(err)
        else:
            self.successful += 1
            print("Insert successfully!")
    

def main():
    ms = ODBC_MS()

    begin_timestamp = datetime.datetime(2018,7,6,9,0,0)
    end_timestamp = datetime.datetime(2019,1,6,9,0,0)
    timestamp = begin_timestamp
    total = 0
    while timestamp < end_timestamp:
        total +=1
        timestamp += datetime.timedelta(minutes=5)
        print("timestamp: {0}".format(timestamp))
        hourid = timestamp.year * 1000000 + timestamp.month * 10000 + timestamp.day * 100 + timestamp.hour
        print("hourid: {0}".format(hourid))
        timestamp5min = datetime.datetime(timestamp.year,timestamp.month,timestamp.day,timestamp.hour,
                                          int(timestamp.minute / 5 * 5), 0)
        print("timestamp5min: {0}".format(timestamp5min))
        timestamp10min = datetime.datetime(timestamp.year,timestamp.month,timestamp.day,timestamp.hour,
                                           int(timestamp.minute / 10) * 10, 0)
        print("timestamp10min: {0}".format(timestamp10min))
        timestamp15min = datetime.datetime(timestamp.year, timestamp.month, timestamp.day, timestamp.hour,
                                           int(timestamp.minute / 15) * 15, 0)
        print("timestamp15min: {0}".format(timestamp15min))
        timestamp30min = datetime.datetime(timestamp.year, timestamp.month, timestamp.day, timestamp.hour,
                                           int(timestamp.minute / 30) * 30, 0)
        print("timestamp30min: {0}".format(timestamp30min))
        timestamp1hour = datetime.datetime(timestamp.year, timestamp.month, timestamp.day, timestamp.hour,
                                           0, 0)
        print("timestamp1hour: {0}".format(timestamp1hour))
        day = timestamp.date()
        print("day: {0}".format(day))

        sql = '''
         INSERT INTO [dbo].[DimTime]
                    ([HourId]
                    ,[Timestamp]
                    ,[Timestamp5min]
                    ,[Timestamp10min]
                    ,[Timestamp15min]
                    ,[Timestamp30min]
                    ,[Timestamp1hour]
                    ,[Day])
              VALUES
                    ({0}
                    ,'{1}'
                    ,'{2}'
                    ,'{3}'
                    ,'{4}'
                    ,'{5}'
                    ,'{6}'
                    ,'{7}')
         '''.format(hourid, timestamp, timestamp5min, timestamp10min, timestamp15min, timestamp30min, timestamp1hour, day)

        print(sql)
        ms.ExecNoQuery(sql)
    print("total: {0}, successful: {1}, failed: {2}".format(total, ms.successful, ms.failed))

if __name__ == '__main__':
    main()
