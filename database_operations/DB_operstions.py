import sqlite3
# from App_Logging.Logging import get_logs
import pandas as pd
from datetime import datetime

# getting the current date and time
current_datetime = datetime.now()


class DBOperations:
    def __init__(self):
        # self.logger = get_logs( open("Logs//DatabaseOperations.txt" , "a+"))
        pass

    def create_Database_Table(self):
        """
        Method Name : create_Database_Table

        Description : This method is written to create/connect database TrainingData.db and
                      Create / delete-Create table in database 'Train' used to save training data.

        Parameters : None

        Returns : None

        Written By : Yatrik Shah
        """
        # self.logger.write_logs("Entered function create_Database_Table.")
        conn = sqlite3.connect('database//predictionDatabase.db')
        # self.logger.write_logs("Created / Connected prediction Database successfully!")
        cursor_obj = conn.cursor()
        cursor_obj.execute('''CREATE TABLE if not exists Predictions(Time VARCHAR(25), Number_Plate VARCHAR(15))'''); # Sr INTEGER AUTOINCREMENT,
        # self.logger.write_logs("Train Table created successfully!")
        conn.close()

    def enter_recordTo_Table(self ,number_plate ):
        # cement, blast_furnace_slag, fly_ash, water, superplasticizer, coarse_aggregate, fine_aggregate, age
        """
        Method Name : enter_recordTo_Table

        Description : This method is written to enter a single/multiple record to the Train table

        Parameters : column Values for the table

        Returns : None

        Written By : Yatrik Shah
        """
        # self.logger.write_logs("Entered function enter_recordTo_Table.")
        conn = sqlite3.connect('database//predictionDatabase.db')
        cursor_obj = conn.cursor()

        current_date_time = current_datetime.strftime("%m/%d/%Y, %H:%M:%S")
        print("current date and time = ", current_date_time)

        cursor_obj.execute(
            "insert into Predictions(Time, Number_Plate) values(?,? )",
            [str(current_date_time), number_plate])
        conn.commit()
        conn.close()

    def showTable(self):
        """
        Method Name : showTable

        Description : This method is written to show the table Train.

        Parameters : None

        Returns : full_data(str), rows(List[Tuple])

        Written By : Yatrik Shah
        """
        # self.logger.write_logs("Entered function showTable.")
        conn = sqlite3.connect('database//predictionDatabase.db')
        cursor_obj = conn.cursor()
        output = cursor_obj.execute("select * from Predictions")

        data = cursor_obj.execute('''SELECT * FROM Predictions''')
        full_data = ''
        for column in data.description:
            print("cols", column[0] , end="\t")
            full_data = full_data+str(column[0])+ "\t"
        print("")
        full_data = full_data + '\n'
        rows = []
        for row in output:
            print("row", row)
            rows.append(row)
            row = list(row)
            for ele in row:
                full_data = full_data + str(ele) + '\t'
            full_data = full_data + '\n'
        conn.close()
        return full_data, rows

    def dropTabel(self):
        """
        Method Name : dropTabel

        Description : This method is written to drop the table Train if already exists.

        Parameters : None

        Returns : None

        Written By : Yatrik Shah
        """
        # self.logger.write_logs("Entered function dropTabel.")
        conn = sqlite3.connect('database//predictionDatabase.db')
        cursor_obj = conn.cursor()
        cursor_obj.execute('''drop table if exists Predictions''')
        conn.commit()
        conn.close()
        print("entered droptable.")
        # self.logger.write_logs("Table Train dropped successfully.")

    def show_all_tables(self):
        """
        Method Name : show_all_tables

        Description : This method is written to show all the tables exists in the database TrainingData.db .

        Parameters : None

        Returns : None

        Written By : Yatrik Shah
        """
        conn = sqlite3.connect('TrainingDatabase/TrainingData.db')
        cursor_obj = conn.cursor()
        cursor_obj.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(cursor_obj.fetchall())

    def Dataframetodatabase(self, data):
        """
        Method Name : Dataframetodatabase

        Description : This method is written to save the entire dataframe into the Train schema into TrainingData.db .

        Parameters : data : The data to convert into the database schema

        Returns : None

        Written By : Yatrik Shah
        """
        # self.logger.write_logs("Entered function Dataframetodatabase.")
        conn = sqlite3.connect('TrainingDatabase/TrainingData.db')
        try:
            data.to_sql(name='Train', con=conn , index=False)
        except:
            conn.execute("DROP TABLE Train")
            data.to_sql(name='Train', con=conn, index=False)


    def getDatafromDatabase(self):
        """
        Method Name : getDatafromDatabase

        Description : This method is written to get the Training data in form of pandas dataframe from Train schema TrainingData.

        Parameters : None

        Returns : Training data from schema 'Train'

        Written By : Yatrik Shah
        """
        connection = sqlite3.connect('database//predictionDatabase.db')
        data = pd.read_sql_query("select * from Predictions", connection)
        return data


# if __name__ == '__main__':
#     db = DBOperations()
#     _, y = db.showTable()
#     print(y)
#
