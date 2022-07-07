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


def booking():
    
    import mysql.connector
    mob_no=int(input('Enter your 10 digit mobile number: '))
    name=input('Enter your name: ')
    import datetime
    from datetime import date
    today=date.today()
    try:
        db=mysql.connector.connect(host="localhost",user="root",password='computer',database='movie_theatre')
        print('Welcome',name)
        print('Movies Screening today are: ')
        cursor=db.cursor()
        cursor.execute("SELECT * FROM MOVIE_DETAILS")
        mrecs=cursor.fetchall()
        for x in mrecs:
            print(x)
        ser=int(input("Enter serial number of the movie: "))
        qry="select Movie_Name from movie_details where Serial_Number=%s or Serial_Number=%s;"
        cursor.execute(qry,(ser,ser))
        mrecs=cursor.fetchall()
        for x in mrecs:
            mov=str(x)
            mov=mov[2:-3]
            print('Movie Selected: ',mov)
        qry="select Price_per_Seat from movie_details where Movie_Name=%s or Movie_Name=%s;"
        cursor.execute(qry,(mov,mov))
        mrecs=cursor.fetchall()
        for x in mrecs:
            price=int(str(x)[1:-2])
            print(price)
        seats=int(input('Enter the number of seats: '))
        if ser==1:
            tim='10:00:00'
        elif ser==2:
            tim='13:00:00'
        elif ser==3:
            tim='16:30:00'
        elif ser==4:
            tim='19:00:00'
        elif ser==5:
            tim='22:00:00'
        refchoi=input('Want to add refreshments?(y/n): ')
        if refchoi=='y':
            ref,refprice=refreshment()
        else:
            refprice=0
            ref='  '
        print(ref,refprice)
        totpayable=(price*seats)+refprice
        now=datetime.datetime.now()
        i_no=now.year+now.month+now.day+now.hour+now.minute+now.second
        i_no=int(i_no)
        today=str(today)
        qry='insert into main_customer_bookings values(%s,%s,%s,%s,%s,%s,%s,%s,%s);'
        ins=[mob_no,name,today,tim,seats,ref,totpayable,i_no,mov]
        cursor.execute(qry,ins)
        db.commit()
        print('Your Invoice number is: ',i_no)
        print('Your booking is confirmed! Thank You')
    except Exception as e :
        print(e)
        print('Error in booking')


def enquiry():
        import mysql.connector
        import pandas as pd
        try:
            db=mysql.connector.connect(host="localhost",user="root",password='computer',database='movie_theatre')
            cursor=db.cursor()
            print("Welcome to ABC Movie Theatre: ")
            cursor.execute('Select * from movie_details;')
            head=['S no.','Movie Name','Movie Time','Price per Seat']
            values=[]
            mrecs=cursor.fetchall()
            for x in mrecs:
                values.append(x)
            details=pd.DataFrame(values,columns=head,index=['Hall 1','Hall 2','Hall 3','Hall 4','Hall 5'])
            print(details)
        except:
            print('Error')


def invoice():
    import mysql.connector
    try:
        db=mysql.connector.connect(host="localhost",user="root",password='computer',database='movie_theatre')
        cursor=db.cursor()
        import datetime
        now=datetime.datetime.now()
        dtm=str(now)
        num=int(input("Enter your 10 digit mobile number: "))
        cursor.execute('select * from main_customer_bookings where Customer_Mobile_Number=%s or Customer_Mobile_Number=%s;',(num,num))
        mrecs=cursor.fetchall()
        L=[]
        for x in mrecs:
            print('We are finding your booking')
            L.append(x)
        if len(L)!=0:
            print('Booking Found')
            print('Invoice Printing in Process!!')
            cursor.execute('select Customer_Name from main_customer_bookings where Customer_Mobile_Number=%s or Customer_Mobile_Number=%s;',(num,num))
            mrecs=cursor.fetchall()
            for x in mrecs:
                invo_name=str(x)
                invo_name=invo_name[2:-3]
            cursor.execute('select Invoice_Number from main_customer_bookings where Customer_Mobile_Number=%s or Customer_Mobile_Number=%s;',(num,num))
            mrecs=cursor.fetchall()
            for x in mrecs:
                invo_no=int(str(x)[1:-2])
            cursor.execute('select Total_Payable from main_customer_bookings where Customer_Mobile_Number=%s or Customer_Mobile_Number=%s;',(num,num))
            mrecs=cursor.fetchall()
            for x in mrecs:
                tot_sal=int(str(x)[1:-2])
            cursor.execute('select Movie_Name from main_customer_bookings where Customer_Mobile_Number=%s or Customer_Mobile_Number=%s;',(num,num))
            mrecs=cursor.fetchall()
            for x in mrecs:
                mov_name=str(x)
                mov_name=mov_name[2:-3]
            cursor.execute('select Refreshments from main_customer_bookings where Customer_Mobile_Number=%s or Customer_Mobile_Number=%s;',(num,num))
            mrecs=cursor.fetchall()
            for x in mrecs:
                refresh=str(x)
                refresh=refresh[2:-3]
            cursor.execute('select Number_of_Seats from main_customer_bookings where Customer_Mobile_Number=%s or Customer_Mobile_Number=%s',(num,num))
            mrecs=cursor.fetchall()
            for x in mrecs:
                no_seats=int(str(x)[1:-2])
            print("-"*65)
            print("\t\t\t\tInvoice")
            print("-"*65)
            print()
            print("Date :{0:>55s}".format(dtm))
            print("-"*65)
            print("Customer Mobile Number:\t\t ",num)
            print("Customer Name: \t\t\t",invo_name)
            print("Movie Name: \t\t\t",mov_name)
            print("Number of Seats: \t\t",no_seats)
            print("Refreshments:\t\t",refresh)
            print("Invoice Number: \t\t",invo_no)
            print("Total Payable: \t\t",tot_sal)
            print("-"*65)
            print("\t\tThank You! Vist Again!!")
            print()
            cursor.execute('insert into customer_invoices values(%s,%s,%s,%s,%s,%s,%s);',[num,invo_name,mov_name,no_seats,refresh,invo_no,tot_sal])  
        else:
            print('Booking not found!!')
        db.commit()
    except:
        print('Error ')