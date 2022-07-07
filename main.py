import mysql.connector
mydb=mysql.connector.connect(host="localhost",user="root",password="computer",database="movie_theatre")
cursor=mydb.cursor()
sql = "CREATE TABLE if not exists customer_invoices (\
                  Customer_Mobile_Nummber int(10) not null PRIMARY KEY,\
                  Customer_Name varchar(30) ,\
                  Movie_Name varchar(30) ,\
                  Number_of_Seats int(3) ,\
                  Refreshments varchar(100),\
                  Invoice_Number int(10),\
                  Total_Sales int(5));"
cursor.execute(sql)
sql = "CREATE TABLE if not exists main_customer_bookings (\
                  Customer_Mobile_Number int(10) not null PRIMARY KEY,\
                  Customer_Name varchar(30) NOT NULL,\
                  Movie_Date date ,\
                  Movie_Time time ,\
                  Number_of_Seats int(3),\
                  Refreshments varchar(100),\
                  Total_Payable int(5),\
                  Invoice_Number int(10),\
                  Movie_Name varchar(30));"
cursor.execute(sql)
sql = "CREATE TABLE if not exists movie_details (\
                  Serial_Number int(2),\
                  Movie_Name varchar(30),\
                  Movie_Time varchar(30) ,\
                  Price_per_Seat int(5));"
cursor.execute(sql)
sql = "CREATE TABLE if not exists refreshment_counter (\
                  Items varchar(50),\
                  Price int(4));"
cursor.execute(sql)