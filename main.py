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


def menu():
    c = 'y'
    choice=0
    while c == 'y':
        print('Hello')
        print('Welcome to ABC Movie Theatre')
        print('Please make a choice:')
        print('1. Book Tickets')
        print('2. Enquiry of Shows')
        print('3. Printing Invoice')
        print('4. Cancel Booking')
        print('5. Sales Management')
        print('6. Exit')
        choice=int(input('Enter your choice: '))
        if choice==1:
            booking()
        elif choice==2:
            enquiry()
        elif choice==3:
            invoice()
        elif choice==4:
            cancel()
        elif choice==5:
            sales_mgmt()
        elif choice==6:
            print('Thank You! Visit Again')
            break
        else:
            print('Wrong Choice Entered')
        c=input('Do you want to continue?(y/n): ')


def refreshment():
    import mysql.connector
    import pandas as pd
    try:
        db=mysql.connector.connect(host="localhost",user="root",password='computer',database='movie_theatre')
        cursor=db.cursor()
        cursor.execute('select Items,Price from refreshment_counter;')
        mrecs=cursor.fetchall()
        ref=''
        refprice=0
        col=['Items','Price']
        data=[]
        for x in mrecs:
            data.append(x)
        refreshments_disp=pd.DataFrame(data,columns=col)
        print(refreshments_disp)
        mor='y'
        while mor=='y':
            food_no=int(input('Enter serial number: '))
            qty=int(input('Enter quantity: '))
            qry='select Items from refreshment_counter where Serial_Number=%s or Serial_Number=%s;'
            cursor.execute(qry,(food_no,food_no))
            mrecs=cursor.fetchall()
            for x in mrecs:
                item=str(x)[2:-3]
            qry='select Price from refreshment_counter where Serial_Number=%s or Serial_Number=%s;'
            cursor.execute(qry,(food_no,food_no))
            mrecs=cursor.fetchall()
            for x in mrecs:
                tot=(int(str(x)[1:-2]))*qty
            print(qty,item,'=',tot)
            ref=ref+(str(qty)+' '+item+' ')
            refprice=refprice+tot
            mor=input('Want to add more refreshment?(y/n): ')
        print('Thank you for buying')
        return ref,refprice
        print('Thank you for buying!!')
    except Exception as e:
        print(e)
        print('Error')