import pyodbc
import datetime


class ODBC_MS:
    def __init__(self):
        ''''' initialization '''  
        self.failed = 0
        self.successful = 0
        
    def _GetConnect(self):
        self.conn = pyodbc.connect(DRIVER='{SQL Server}', SERVER='localhost', 
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

    timestamp = datetime.datetime(2018,6,26,10,0,0)
    total = 100
    for num in range(0, total):
        timestamp += datetime.timedelta(minutes=5)
        print("timestamp: {0}".format(timestamp))
        hourid = timestamp.year * 10000 + timestamp.month * 100 + timestamp.day
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
