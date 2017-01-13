# Chaitali Patel D02
# Alex Dong D01
# Yvonne Hoang D02


#Initialization of 
import sqlite3
import sys
import hashlib
db_file_path = 'hospital.db'
    
#Create or Connect to a Database
conn = sqlite3.connect(db_file_path)

c = conn.cursor()

#For Foreign key constraint of SQLite
c.execute('PRAGMA forteign_keys=ON;')

c.execute("DROP TABLE IF EXISTS charts")
c.execute("DROP TABLE IF EXISTS symptoms")
c.execute("DROP TABLE IF EXISTS diagnoses")
c.execute("DROP TABLE IF EXISTS medications")
c.execute("DROP TABLE IF EXISTS reportedallergies")
c.execute("DROP TABLE IF EXISTS staff")
c.execute("DROP TABLE IF EXISTS patients")
c.execute("DROP TABLE IF EXISTS dosage")
c.execute("DROP TABLE IF EXISTS inferredallergies")
c.execute("DROP TABLE IF EXISTS drugs")    

c.execute("create table staff(staff_id char(5),role char(1),name char(15),\
login char(8),password char(30), primary key(staff_id));")

c.execute("create table patients (hcno char(5),name char(15),age_group char(5),\
address char(30), phone char(10), emg_phone char(10), primary key(hcno));")

c.execute("create table charts(chart_id char(5), hcno char(5), adate date,\
edate date, primary key(chart_id), foreign key(hcno) references patients);")

c.execute("create table symptoms (hcno char(5), chart_id char(5), staff_id char(5),\
obs_date date, symptom char(15), primary key(hcno,chart_id,staff_id,symptom,obs_date),\
foreign key(hcno) references patients, foreign key(chart_id) references charts,\
foreign key(staff_id) references staff);")

c.execute("create table diagnoses (hcno char(5), chart_id char(5), staff_id char(5),\
ddate date, diagnosis char(20), primary key (hcno,chart_id,staff_id,diagnosis,ddate),\
foreign key(hcno) references patients, foreign key(chart_id) references charts,\
foreign key(staff_id) references staff);")

c.execute("create table drugs (drug_name char(15), category char(25),\
primary key(drug_name));")

c.execute("create table dosage (drug_name char(15), age_group char(5), sug_amount int,\
primary key(drug_name,age_group), foreign key (drug_name) references drugs);")

c.execute("create table medications(hcno char(5), chart_id char(5), staff_id char(5),\
mdate date, start_med date, end_med date, amount int, drug_name char(15),\
primary key(hcno,chart_id,staff_id,mdate,drug_name),\
foreign key(hcno) references patients, foreign key(chart_id) references charts,\
foreign key(staff_id) references staff, foreign key(drug_name) references drugs);")

c.execute("create table reportedallergies (hcno char(5), drug_name char(15),\
primary key(hcno,drug_name), foreign key(hcno) references patients,\
foreign key(drug_name) references drugs);")

c.execute("create table inferredallergies (alg char(15), canbe_alg char(15),\
primary key(alg, canbe_alg), foreign key (alg) references drugs,\
foreign key(canbe_alg) references drugs);")
#------------------------------------------------------------------------------
# f = open('Class_Test_Data_P1.sql','r')
# sql = f.read() # watch out for built-in `str`
# c.executescript(sql)
#-------------------------------------------------------------------------------
# DATA
c.execute("insert into staff values \
('11111','D','Ali','ali','04c15392c64c3db52f9a7fcfb7c0c370900e0308007617899430d088'),\
('22222','N','Lovejoy','lovejoy','abd54ed96011c648e7e012dfef1a9f3174b70c86de55d0840f2a576d'),\
('33333','A','Merill','merill','df2d35e91a6553f2970ecdb3132108424b052c5541d6ed791b9af77f'),\
('44444', 'D', 'Fred', 'fred', 'b6054914e27a65fef3800396b9ade843aca7a12951943835ec30edfd'),\
('55555', 'N', 'Denny', 'denny', '680b482d752251dd5b6d4a0106eb5516d30e0d98f41c23a987b0951b'),\
('66666', 'A', 'Kain', 'kain', 'c6044c4cffff98ba4d601fd071c560ddbcf1b3e4cfda5fea161f7e72'),\
('77777', 'D', 'Cecil', 'cecil', '51260abcaedee14d1dc45c319f9e0f514b251f8c268b25e70fd3f1e6'),\
('88888', 'N', 'Rydia', 'rydia', '11f4b68c23ae2028493d27769845ce4c36deb9d112c171fc12e373a5'),\
('99999', 'A', 'Yuna', 'yuna', '92294ccb8315e9330192914d3e260f9189147f83be677f4349c245e8'),\
('12345', 'D', 'Cloud', 'cloud', 'b3fd5c975f2947d2e4531162237f61545dc29f8e08bab904a34c3d72'),\
('12346', 'N', 'Aerith', 'aerith', '06afa612b12427630b0b462526f36baadd7a909cae7ec028398b3b4c'),\
('12347', 'A', 'Roselia', 'roselia', 'ca0813f755afb1e2487f1945f30d4564203932821ee845c55ade5f3a');")

# ali aaaaa
# lovejoy bbbbb
# merill ccccc
# fred ddddd
# denny eeeee
# kain ffffff
# cecil ggggg
# rydia hhhhh
# yuna iiiii
# cloud jjjjj
# aerith kkkkk
# roselia lllll

c.execute("insert into patients values \
('45671', 'Chai', '18-21', '1234 12 Ave, Edmonton, AB', '7801234567', '7801234568'),\
('45672', 'Kevin', '18-21', '1454 East Broadway, Vancouver, BC', '6045678900', '6045678901'),\
('45673', 'Dennis', '18-21', '1233 34 St, Edmonton, AB', '7802222222', '7802222221'),\
('45674', 'Leslie', '22-30', '8888 11 Ave, Calgary, AB', '4034681556', '4034691234'),\
('45675', 'Jarred', '18-21', '5678 34 Ave, Calgary, AB', '4034651234', '4034500123'),\
('45676', 'Chris', '22-30', '7654 43 Ave, Toronto, ON', '4164671426', '4164091765'),\
('45677', 'Jarred', '18-21', '5678 34 Ave, Vancouver, BC', '6041234567', '6041234568'),\
('45678', 'Chris', '22-30', '7654 43 Ave, Toronto, ON', '4164851668', '4164851669');")

c.execute("insert into charts values \
('98761', '45671', '2015-03-03 13:24:33', '2015-03-05 13:24:33'),\
('98762', '45671', '2016-05-03 13:24:33', '2016-05-05 04:21:32'),\
('98763', '45672', '2015-03-03 13:24:33', '2015-03-04 13:24:33'),\
('98764', '45672', '2016-02-18 13:24:33', NULL),\
('98765', '45673', '2015-12-12 13:24:33', '2015-12-12 04:24:33'),\
('98766', '45674', '2016-04-20 13:24:33', '2016-04-22 13:24:33'),\
('98767', '45675', '2015-07-30 13:24:33', '2015-08-07 09:24:33'),\
('98768', '45676', '2016-06-11 13:24:33', '2016-06-11 10:24:33'),\
('98769', '45677', '2016-08-01 13:24:33', '2016-08-04 13:24:33'),\
('98760', '45678', '2015-12-31 13:24:33', '2016-01-02 12:24:33'),\
('00000', '45671', '2015-04-04 13:24:33', '2015-04-04 03:24:33');")

c.execute("insert into symptoms values \
('45671', '98761', '11111', '2015-03-04 13:24:33', 'headache'),\
('45671', '98761', '11111', '2015-03-04 13:24:33', 'sore muscles'),\
('45671', '98762', '22222', '2016-05-04 13:24:33', 'headache'),\
('45672', '98763', '22222', '2015-03-03 13:24:33', 'stomache ache'),\
('45672', '98764', '44444', '2016-02-19 13:24:33', 'sore muscles'),\
('45673', '98765', '55555', '2015-12-12 13:24:33', 'headache'),\
('45674', '98766', '77777', '2016-04-21 13:24:33', 'headache'),\
('45675', '98767', '88888', '2015-08-01 13:24:33', 'sore muscles'),\
('45675', '98767', '88888', '2015-08-03 13:24:33', 'stomache ache'),\
('45676', '98768', '12345', '2016-06-11 13:24:33', 'sore muscles'),\
('45677', '98769', '12346', '2016-08-02 13:24:33', 'headache'),\
('45678', '98760', '22222', '2016-01-01 13:24:33', 'sore muscles');")

c.execute("insert into diagnoses values \
('45671', '98761', '11111', '2015-03-04 13:24:33', 'fever'),\
('45671', '98762', '11111', '2016-05-04 13:24:33', 'fever'),\
('45672', '98763', '44444', '2015-03-03 13:24:33', 'gastroenteritis'),\
('45672', '98764', '44444', '2016-02-19 13:24:33', 'fibromyalgia'),\
('45673', '98765', '77777', '2015-12-12 13:24:33', 'fever'),\
('45674', '98766', '77777', '2016-04-21 13:24:33', 'migraine'),\
('45675', '98767', '11111', '2015-08-03 13:24:33', 'gastroenteritis'),\
('45676', '98768', '12345', '2016-06-11 13:24:33', 'fibromyalgia'),\
('45677', '98769', '12345', '2016-08-02 13:24:33', 'fever'),\
('45678', '98760', '44444', '2016-01-01 13:24:33', 'fibromyalgia');")

c.execute("insert into drugs values \
('Lyrica', 'anti-epileptic'),\
('ibuprofen', 'anti-inflammatory'),\
('ZZZ', 'anti-biotic'),\
('Tylenol', 'anti-inflammatory');")

c.execute("insert into dosage values \
('Lyrica', '18-21', 8),\
('Lyrica', '22-30', 9),\
('ibuprofen', '18-21', 5),\
('ibuprofen', '22-30', 6),\
('ZZZ', '18-21', 3),\
('ZZZ', '22-30', 4),\
('Tylenol', '18-21', 2),\
('Tylenol', '22-30', 3);")

c.execute("insert into medications values \
('45671', '98761', '11111', '2015-03-04 13:24:33', '2015-03-05 13:24:33', '2015-03-10 13:24:33', 7, 'ZZZ'),\
('45671', '00000', '11111', '2015-04-04 13:24:33', '2015-04-05 13:24:33', '2015-04-10 13:24:33', 5, 'ibuprofen'),\
('45671', '98762', '11111', '2016-05-04 13:24:33', '2016-05-05 13:24:33', '2016-05-10 13:24:33', 5, 'ibuprofen'),\
('45672', '98763', '44444', '2015-03-03 13:24:33', '2015-03-04 13:24:33', '2015-03-11 13:24:33', 3, 'ZZZ'),\
('45672', '98764', '44444', '2016-02-19 13:24:33', '2016-02-20 13:24:33', '2016-02-24 13:24:33', 8, 'Lyrica'),\
('45673', '98765', '77777', '2015-12-12 13:24:33', '2015-12-12 13:24:33', '2015-12-17 13:24:33', 8, 'Tylenol'),\
('45674', '98766', '77777', '2016-04-21 13:24:33', '2016-04-22 13:24:33', '2016-04-24 13:24:33', 4, 'Tylenol'),\
('45675', '98767', '11111', '2015-08-01 13:24:33', '2015-08-03 13:24:33', '2015-08-07 13:24:33', 4, 'ZZZ'),\
('45676', '98768', '12345', '2016-06-11 13:24:33', '2016-06-11 13:24:33', '2016-06-16 13:24:33', 9, 'Lyrica'),\
('45677', '98769', '12345', '2016-08-02 13:24:33', '2016-08-02 13:24:33', '2016-08-04 13:24:33', 5, 'ibuprofen'),\
('45678', '98760', '44444', '2016-01-01 13:24:33', '2016-01-02 13:24:33', '2016-01-09 13:24:33', 9, 'Lyrica');")

c.execute("insert into reportedallergies values \
('45671', 'ZZZ'),\
('45673', 'Lyrica'),\
('45675', 'Tylenol'),\
('45676', 'ibuprofen'),\
('45678', 'ibuprofen'),\
('45672', 'ZZZ');")

c.execute("insert into inferredallergies values \
('ibuprofen', 'ZZZ'),\
('Tylenol', 'Lyrica');")
#-------------------------------------------------------------------------------
conn.commit()

def main():
    conn.commit()
    start()
    
def start():
    while True:
        print("Welcome! To login as an existing user, type 'login'")
        print("To sign up as a new user, type 'signup'")
        print("To exit the program, type 'exit'")
        command = raw_input("What would you like to do: ")
        if command == 'login':
            log_in()
            continue
        
        elif command == 'signup':
            signup()
            continue
        elif command == 'exit':
            break
        else:
            print("Invalid input! \n")
    return
            
def signup():
    print("New User")
    while True:

        staff_id = raw_input("Enter staff ID number: ")
        if len(staff_id) != 5:
            print('Staff ID does not contain 5 digits. Please try again.')
            continue
        else:
            c.execute("SELECT * FROM staff WHERE staff_id = '%s';" % (staff_id))
            login_info = c.fetchone()
            # staff id not found in system, continue
            if login_info == None:
                break
            else:
                print("Invalid ID, try again!")

    name = raw_input("Enter your name: ")
    # check if username exists
    while True:
            try:
                login = raw_input("Enter username: ")
                c.execute("SELECT * FROM staff WHERE login = '%s';" % login)
                username = c.fetchone()
                if username == None:
                    break
                else:
                    print("Username taken, try again!")
            except:
                print("Username Taken. Try again. ")    
    # need function to encrypt this
    password = raw_input("Enter password: ")
    # make sure any case 
    while True:
        try:    
            role = raw_input("Enter D for Doctor, A for Administration or N for Nurse: ")      
            if role == 'D' or role == 'd':
                role = 'D'
                break
            
            elif role == 'N' or role == 'n':
                role = 'N'
                break
                
            elif role == 'A' or role == 'a':
                role = 'A'
                break
            else:
                print("Invalid input, try again.")
        except:
            print("Invalid input, try again.")
    
    # insert all of this into staff table
    # encrypt = encryption(password)
    c.execute("INSERT INTO staff VALUES ('%s', '%s', '%s', '%s', '%s');" % (staff_id, role, name, login, encryption(password)))
    conn.commit()
    c.execute("SELECT * FROM staff;")
    rows = c.fetchall()
    print(rows)  
    #.commit to save any changes in insertions/deletions/updates
    main()

def log_in(): 
    
    print("Log In")
    while True:
        
            login = raw_input("Enter username: ")
            if login == 'exit':
                break
            # check if already in system ??? is it "" idk
            c.execute("SELECT * FROM staff WHERE login = '%s';" % login)
            username = c.fetchone()
            if username == None:
                print("Username does not exist")  
            else:
#Encryption Attempt ***Change upon handing in to compare encryption with encryption
                password = raw_input("Enter password: ")
                password = encryption(password)
#Encryption End; only works for when staff table contains encrypted passwords
             #   password = raw_input("Enter password: ")
#Passwords should not be stored in plain text, should be encrypted and compared.
#End encryption attempt
                c.execute("SELECT * FROM staff WHERE login = '%s' and password='%s';" % (login,password)) 
                check_login = c.fetchone()
                if check_login == None: 
                    print("Incorrect password, try again.")
                else:
                    staff_id = check_login[0]
                    if check_login[1] == "D" or check_login[1] == "N":
                        care_user(check_login[1], staff_id)
                    elif check_login[1] == "A":
                        admin_user()                     

                   
    return 

def care_user(role, staff_id):
    
    if role == 'D' or role == 'd':
        occupation = 'Doctor'
        print('Healthcare system user: Doctor')
    elif role == 'N' or role == 'n':
        occupation = 'Nurse'
        print('Healthcare system user: Nurse')

    
    while True:
        print('What would you like to do?')
        print('(1) List all charts in the system (ordered by admission date)')
        print('(2) Add an entry under symptoms for a given patient (hcno)')
        print('(3) Add an entry under diagnosis for a given patient (hcno)')
        print('(4) Add an entry under medications for a given patient (hcno)')
        print('(5) Create a new open chart for a patient (hcno)')
        print('(6) Close a chart on patient dismissal')
        print('(7) Logout')        
        choice = raw_input('Enter a number depending on your option: ')
        if choice == '7':
            start()
            break
        elif choice == '6':
            if occupation != 'Nurse':
                print('Permission denied, only nurses are granted access')
            else:
                dismissal()
                continue
        elif choice == '5':
            if occupation != 'Nurse':
                print('Permission denied, only nurses are granted access')
                continue
            else:
                admission(staff_id)
                continue
        elif choice == '4':
            if occupation != 'Doctor':
                print('Permission denied, only doctors are granted access')
                continue
            else:
                entry_medication(staff_id)
                continue
            
        elif choice == '3':
            if occupation != 'Doctor':
                print('Permission denied, only doctors are granted access')
                continue
            else:
                entry_diagnosis(staff_id)
                continue
        elif choice == '2':
            entry_symptom(staff_id)
            continue
        elif choice == '1':
            list_chart()
            continue
        else:
            print('Invalid input, try again')
                
#Test if there is a hcno in the system with the same number as input
#QUERY 1 DOCTOR AND 3 NURSE
def list_chart():
    
    print('Please enter the patients hcno')
    print("Type 'exit' to go back to main menu \n")
    
    while True:
        get_hcno = raw_input("Enter patient health care number: ")
        if get_hcno == 'exit':
            break
        elif len(get_hcno) != 5:
            print('Health care number format incorrect. Please enter 5 digit health care number')
     
        else:
            c =	conn.cursor()
            c.execute("select hcno from patients where patients.hcno = '%s';" %(get_hcno))
            if c.fetchone() == None:
                print("No patients registered with that healthcare number.")
            else:
                conn.row_factory = sqlite3.Row
                c = conn.cursor()
                c.execute("SELECT * FROM charts c, patients p WHERE p.hcno = c.hcno AND p.hcno = '%s' ORDER BY adate ;" % (get_hcno)) 
                check_chart = c.fetchall() 
                conn.commit()    
                all_charts = []
                if check_chart == None:
                    print("There are no charts for this hcno")    
                else: 
                    for row in check_chart:
                        if row['edate'] == None:
                            print row['chart_id'] + " open"
                        else:
                            print row['chart_id'] + " closed"
                        all_charts = all_charts + [row['chart_id']]
                    break
                        
    # end while 
    
    while True:
        if get_hcno == 'exit':
            break
        get_chart = raw_input("Enter chart number to view: ")
        if get_chart == 'exit':
            break
        elif get_chart not in all_charts:
            print("Invalid chart number.")
            continue
        else:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()      
            c.execute("SELECT * \
            FROM (SELECT hcno, chart_id, staff_id, obs_date as date, NULL as start_med, NULL as end_med, NULL as amount, symptom \
            FROM symptoms \
            WHERE chart_id = ? \
            UNION \
            SELECT hcno, chart_id, staff_id, ddate as date, NULL as start_med, NULL as end_med, NULL as amount, diagnosis \
            FROM diagnoses \
            WHERE chart_id = ? \
            UNION \
            SELECT hcno, chart_id, staff_id, mdate as date, start_med, end_med, amount, drug_name \
            FROM medications \
            WHERE chart_id = ? \
            ) as x \
            ORDER BY date", (get_chart,get_chart, get_chart))
        
            get_info = c.fetchall() 
        
            for row in get_info:
                if row[4] == None or row[5] == None or row[6] == None:
                    print row['hcno'], row['chart_id'], row['staff_id'], row['date'], row[7]
                else:
                    print row['hcno'], row['chart_id'], row['staff_id'], row['date'], row[4], row[5], row[6], row[7]        
        
          
    return

# QUERY 2 AND 4 DOCTOR AND NURSE
def entry_symptom(staff_id):
    
    print('Please enter the patients hcno')
    print("Type 'exit' to go back to main menu \n")
    while True:
        get_hcno = raw_input("Enter patient health care number: ")
        if get_hcno == 'exit':
            break
        elif len(get_hcno) != 5:
            print('Health care number format incorrect. Please enter 5 digit health care number')
     
        else:
            c =	conn.cursor()
            c.execute("select hcno from patients where patients.hcno = '%s';" %(get_hcno))
            if c.fetchone() == None:
                print("No patients registered with that healthcare number.")
            else:
                conn.row_factory = sqlite3.Row
                c = conn.cursor()
                c.execute("SELECT * FROM charts c, patients p WHERE p.hcno = c.hcno AND p.hcno = '%s' ORDER BY adate ;" % (get_hcno)) 
                check_chart = c.fetchall() 
                conn.commit()
                open_chart = False
                for row in check_chart:
                    if row['edate'] == None:
                        open_chart = row['chart_id']
                if open_chart == False:
                    print("There are no open charts")
                else:
                    symptom = raw_input("Input symptom name: ")
                    if symptom == 'exit':
                        break                    
                    c = conn.cursor()
                    c.execute("INSERT INTO symptoms VALUES \
                    ('%s', '%s', '%s', datetime('now'), '%s');" \
                              % (get_hcno, open_chart, staff_id, symptom))
                    conn.commit()
                    print("Symptom successfully added.")
                    
                    
    return

#QUERY 3 DOCTORS
def entry_diagnosis(staff_id):
    
    print('Please enter the patients hcno')
    print("Type 'exit' to go back to main menu \n")
    while True:
        get_hcno = raw_input("Enter patient health care number: ")
        if get_hcno == 'exit':
            break
        elif len(get_hcno) != 5:
            print('Health care number format incorrect. Please enter 5 digit health care number')
            continue
     
        else:
            c =	conn.cursor()
            c.execute("select hcno from patients where patients.hcno = '%s';" %(get_hcno))
            if c.fetchone() == None:
                print("No patients registered with that healthcare number.")
                continue
            else:
                conn.row_factory = sqlite3.Row
                c = conn.cursor()
                c.execute("SELECT * FROM charts c, patients p WHERE p.hcno = c.hcno AND p.hcno = '%s' ORDER BY adate ;" % (get_hcno)) 
                check_chart = c.fetchall() 
                conn.commit()
                open_chart = False
                # check if there is an open chart
                for row in check_chart:
                    if row['edate'] == None:
                        open_chart = row['chart_id']
                if open_chart == False:
                    print("There are no open charts")
                else:
                    diagnosis = raw_input("Input diagnosis name: ")
                    if diagnosis == 'exit':
                        break                    
                    c = conn.cursor()
                    # insert diagnosis into table
                    c.execute("INSERT INTO diagnoses VALUES \
                    ('%s', '%s', '%s', datetime('now'), '%s');" \
                              % (get_hcno, open_chart, staff_id, diagnosis))
                    conn.commit()
                    print("Diagnosis successfully added.")
                    
    return

#QUERY 4 DOCTOR 
def entry_medication(staff_id):
    # while loop for hcno testing
    
    while True:
        patient_hcno= raw_input('Please enter the patients hcno: ')
        print("Type 'exit' to go back to main menu \n")
        if patient_hcno == 'exit':
            return
        if len(patient_hcno) != 5:
            print('Health care number format incorrect. Please enter 5 digit health care number')
            continue
        c = conn.cursor()
        c.execute("select patients.hcno from patients where patients.hcno = '%s';" %(patient_hcno))
        if c.fetchone() == None:
            print("No patients registered with that healthcare number.")
            continue
        else:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT * FROM charts c, patients p WHERE p.hcno = c.hcno AND p.hcno = '%s' ORDER BY adate ;" % (patient_hcno)) 
            check_chart = c.fetchall() 
            conn.commit()
            open_chart_id = False
            for row in check_chart:
                if row['edate'] == None:
                    open_chart_id = row['chart_id']
            if open_chart_id == False:
                print("There are no open charts")  
            else:
                break
            
    # speed up user inputs -------------
    # while loop for time
    while True:
        c.execute("select datetime('now');")
        add_mdate = c.fetchone()[0]
        print('Dates should be entered in a YYYY-MM-DD HH:MM:SS format')
        while True:       
            add_start_med = raw_input('Enter the time in which medication should begin: ')
            if date_test(add_start_med) is False:
                print("Incorrect format for date, please re-enter the start time of the medication")
                continue
            break
        while True:
            add_end_med = raw_input('Enter the time in which medication should end: ')
            if date_test(add_end_med) is False:
                print("Incorrect format for date, please re-enter the end time of the medication")
                continue
            break
        break
    # while loop for drugs
    while True:
        add_drug = raw_input('Enter the name of the medication to register into the chart: ')  
        c.execute("select drug_name from drugs where drug_name = ?", (add_drug,))
        if c.fetchone() is None:
            print("Drug name is not in database")
            print("Please enter a valid drug name from the database")
            continue
        add_amount = raw_input('Enter the amount to prescribe: ')
        try:
            add_amount = int(add_amount)
        except:
            print("Invalid input for prescription amount")
            continue
        if int(add_amount) <= 0:
            print('Invalid amount')
            continue
        # see if exceeds sug_dosage with age_group
        # patients, dosage, variable medication drug_name
        c.execute("select d.sug_amount from dosage d, patients p where p.age_group = d.age_group and d.drug_name =? and p.hcno = ?;", (add_drug,patient_hcno,))
        suggested_amount = c.fetchone()[0]
        if int(suggested_amount) < int(add_amount):
            print("Warning: amount to be added exceeds suggested amount for age group")
            override = raw_input("Would you still like to add the entry in? (Y/N): ")
            if override == 'Y' or override == 'y':
                print("Warning issued but entry continues")
            elif override == 'N' or override =='n':
                print("Warning issued and readjusting drug medication")
                continue
            # assumes that amount is viable/amount is overridden
            # test if the drug is a potentially allergic to the patient
            # reportedallergies(drug_name) reportedallergies(hcno)
            # inferredallergies(drug_name) = add_drug / inferredallergies(canbe_alg)
            # if the patient could be allergic to the prescribed drug_name
            # select all the drugs that the patient has been prescribed and see if it could cause allergies
        for row in c.execute("select ra.drug_name, d.category from reportedallergies ra, drugs d where ra.hcno = ? and ra.drug_name = d.drug_name;", (patient_hcno,)):
            reported_drug = row[0]
            reported_category = row[1]
            for row2 in c.execute("select * from inferredallergies ia"):
                allergy = row2[0]
                canbe_allergy = row2[1]
                if reported_drug == allergy and canbe_allergy == add_drug:
                    print 'Warning the patient reported allergies of', reported_drug
                    print 'Because of this, the patient can be allergic to', canbe_allergy
                    print 'Therefore, the patient can be allergic to the drug being given'
                    override_alg = raw_input("Would you still like to add the entry in (Y/N): ")
                    break
                elif reported_drug == add_drug:
                    print 'Patient has been allergic to', reported_drug
                    print 'This drug is categorized as', reported_category
                    override_alg = raw_input("Would you still like to add the entry in (Y/N): ")
                    break
        try:
            if override_alg == 'Y' or override_alg == 'y':
                print("Warning issued but entry continues")
            elif override_alg == 'N' or override_alg =='n':
                print("Warning issued and moved to drug medication")
                continue
        except:
            pass
            # execute the insertion of the drug and the name
        c.execute("insert into medications values (?,?,?,?,?,?,?,?);", (patient_hcno, open_chart_id,staff_id,add_mdate,add_start_med,add_end_med,add_amount,add_drug))
        conn.commit()
        print("The entry has been added to the medications table")
        print("Returning to the main menu")
        break          
            
            
    return

#QUERY 1 NURSE
def admission(staff_id):
    
    while True:
        # if chart was closed due to one of this loops (45672's chart id)
        # would create a new one if there are no closed
        admission_hcno = raw_input("Please enter patients hcno: ")
        # check if the hcno is present in the system or not
        if len(admission_hcno) != 5:
            print("Invalid hcno!")
            continue
        c.execute("select patients.hcno from patients where patients.hcno = ?;", (admission_hcno,))
        if c.fetchone() == None:
            print("There are no patients with that hcno present in the system.")
            add_patient = raw_input("Would you like to add them into the system? (Y/N) : ")
            if add_patient == 'Y' or add_patient == 'y':
                print("Please enter the following information to add the patient into the system")
                add_name = raw_input("Please enter your name: ")
                add_age = raw_input("Please enter your age range: ")
                add_address = raw_input("Please enter your address: ")
                add_phone = raw_input("Please enter your phone number: ")
                add_emg_phone = raw_input("Please enter your emergency phone number: ")
                c.execute("insert into patients values (?,?,?,?,?,?);", (admission_hcno,add_name,add_age,add_address,add_phone,add_emg_phone,))
                conn.commit()
                print("Patient information has been added!")
                continue
            elif add_patient == 'N' or add_patient == 'n':
                print("Patient information will not be added into the system")
                print("Returning to main menu of system")
                break
            else:
                print("Invalid input, please reply with (Y/N)")
                continue
            #after hcno is okay
        else:
            # check if there are any open charts
            c.execute("select charts.chart_id, charts.edate from charts,patients where charts.edate IS NULL and charts.hcno = patients.hcno and patients.hcno = ?;", (admission_hcno,))
            chart = c.fetchone()
            if chart != None:
                open_chart_id = chart[0]
                open_chart = chart[1]
                if open_chart == None:
                    print("There is an open chart for the patient")
                    close_to_new = raw_input("Would you like to close the chart? (Y/N) ")
                    if close_to_new == 'y' or close_to_new == 'Y':
                        c.execute("select datetime('now');")
                        close_date = c.fetchone()[0]
                        open_chart = close_date
                        c.execute("update charts set edate = ? where chart_id = ?;",(open_chart,open_chart_id,))
                        conn.commit()
                    elif close_to_new == 'n' or close_to_new == 'N':
                        print("System will not create a new chart")
                        break
            else:
                print("There is no open charts currently for the patient")
                print("System will now create an open chart for this patient")
                add_open_id = 0
                
                while True:
                    for row in c.execute("select charts.chart_id from charts"):
                        if str(add_open_id).zfill(5) == row[0]:
                            add_open_id = add_open_id + 1
                            continue
                    break
                # add chart id as a 5 char value
                insert_id = str(add_open_id).zfill(5)
                
                c.execute("insert into charts values(?,?,datetime('now'), NULL);", (insert_id, admission_hcno,))
                conn.commit()
                print 'System has now opened another chart for patient hcno of', admission_hcno
                print '\n'
                break
            # if it is not null, then
                #----- tbc
        #when creating a new chart, the system also must provide the functionality to add the patient information, if the patient is not already in the system.
    #either the patient has been registered or already is registered
    
    return

def dismissal():
    # Close chart when patient is dimissed. edate = current
    # check which chart is NULL in edate to see what chart is open for them.
    # chart.hcno = patient.hcno, edate = date(current), dont need to select certain chart_id
    # any chart that is edate = null and patients hcno = dismiss_hcno
    print("Type 'exit' to go back to main menu \n")
    while True:
        get_hcno = raw_input("Enter health care number of patient to be discharged: ")
        if get_hcno == 'exit':
            break
        elif len(get_hcno) != 5:
            print('Health care number format incorrect. Please enter 5 digit health care number')
     
        else:
            c = conn.cursor()
            c.execute("select hcno from patients where patients.hcno = '%s';" %(get_hcno))
            if c.fetchone() == None:
                print("No patients registered with that healthcare number.")
            else:        
                conn.row_factory = sqlite3.Row         
                c = conn.cursor()                
                c.execute("SELECT * FROM charts c, patients p WHERE p.hcno = c.hcno AND p.hcno = '%s' ORDER BY adate ;" % (get_hcno)) 
                check_chart = c.fetchall() 
                conn.commit()                
                open_chart = False
                for row in check_chart:
                    if row['edate'] == None:
                        open_chart = row['chart_id']
                if open_chart == False:
                    print("There are no open charts")
                else:
                    c.execute("UPDATE charts SET edate = datetime('now') WHERE hcno = '%s' AND chart_id = '%s';" % (get_hcno, open_chart))
                    conn.commit() 
                   
    return

def admin_user():
    print('Administration User')
    print('(1) Create a report of total amount of each drug from a doctor over a period of time')
    print('(2) List total amount of each drug in a category in a period of time')
    print('(3) List for a given diagnosis all possible medications that have been prescribed overtime')
    print('(4) All diagnoses made before prescribing the drug over all charts')
    print('(5) Logout')
    while True:
        choice = raw_input('Please input your option: ')
        if choice == '1':
            doctor_report()
            continue
        elif choice == '2':
            drug_category_total()
            continue
        elif choice == '3':
            diagnosis_medication()
            continue
        elif choice == '4':
            drug_diagnosis()
            continue
        elif choice == '5':
            start()
            break
        else:
            print('Invalid input. Try again.')
    return

#QUERY ONE ADMIN
def doctor_report():
    
    while True:
        # Enter the starting time of the desired period of time and confirm
        startTime = raw_input("Enter starting date in YYYY-MM-DD HH:MM:SS format: ")
        confirmStart = raw_input("Is the start date you entered " + startTime + "? (Y/N) ")
        # If confirmed, enter ending time of the desired period of time then confirm 
        if confirmStart == 'Y' or confirmStart == 'y':
            endTime = raw_input("Enter ending date in YYYY-MM-DD HH:MM:SS format: ")
            confirmEnd = raw_input("Is the end date you entered " + endTime + "? (Y/N) ")
            # Outputs the data
            if confirmEnd == 'Y' or confirmEnd == 'y':
                print("Displaying name and total amount of each drug that the doctor prescribed between " + startTime + " and " + endTime)
            # If inputted data incorrectly, reenter
            elif confirmEnd == 'N' or confirmEnd == 'n':
                endTime = raw_input("Enter ending date in YYYY-MM-DD HH:MM:SS format: ")
            else:
                print("Invalid input, please reply with (Y/N)")
                continue
        elif confirmStart == 'N' or confirmStart == 'n':
            startTime = raw_input("Enter starting date in YYYY-MM-DD HH:MM:SS format: ")
        else:
            print("Invalid input, please reply with (Y/N)")
            continue
        
        # Lists for each doctor, the name and total amount of each drug that the doctor prescribed in a specified period of time
        conn.row_factory = sqlite3.Row
        c = conn.cursor()         
        c.execute("SELECT DISTINCT s.name, m.drug_name, SUM(m.amount) AS total FROM staff s, medications m WHERE s.staff_id=m.staff_id AND m.mdate BETWEEN ? AND ? GROUP BY s.name, m.drug_name", (startTime, endTime)) 
        # Print result
        get_info = c.fetchall()  
        conn.commit() 
        for row in get_info:
            print row['name'], row['drug_name'], row['total']        
        
        break
    return

#QUERY TWO ADMIN
def drug_category_total():
   
    while True:
        # Enter starting time of the desired period of time and confirm
        startTime = raw_input("Enter starting date in YYYY-MM-DD HH:MM:SS format: ")
        confirmStart = raw_input("Is the start date you entered " + startTime + "? (Y/N) ")
        # Enter the ending time of the desired period of time and confirm
        if confirmStart == 'Y' or confirmStart == 'y':
            endTime = raw_input("Enter ending date in YYYY-MM-DD HH:MM:SS format: ")
            confirmEnd = raw_input("Is the end date you entered " + endTime + "? (Y/N) ")
            # Outputs
            if confirmEnd == 'Y' or confirmEnd == 'y':
                print("The medications that have been prescribed over time after that diagnosis between " + startTime + " and " + endTime + "are: ")
            elif confirmEnd == 'N' or confirmEnd == 'n':
                endTime = raw_input("Enter ending date in YYYY-MM-DD HH:MM:SS format: ")
            else:
                print("Invalid input, please reply with (Y/N)")
                continue
        # Reenter starting time if inputted incorrectly
        elif confirmStart == 'N' or confirmStart == 'n':
            startTime = raw_input("Enter starting date in YYYY-MM-DD HH:MM:SS format: ")
        else:
            print("Invalid input, please reply with (Y/N)")
            continue
        
        # List for a given diagnosis all possible medications that have been prescribed over time after that diagnosis
        c.execute("SELECT DISTINCT d.category, m.drug_name, SUM(DISTINCT m.amount), SUM(DISTINCT m2.amount) FROM drugs d, drugs d2, medications m, medications m2 WHERE d.drug_name=m.drug_name AND d2.drug_name=m2.drug_name AND m.mdate BETWEEN ? AND ?  AND m2.mdate BETWEEN ? AND ? GROUP BY m.drug_name, d2.category EXCEPT SELECT DISTINCT d.category, m.drug_name, SUM(DISTINCT m.amount), SUM(DISTINCT m2.amount) FROM drugs d, drugs d2, medications m, medications m2 WHERE d.drug_name=m.drug_name AND d2.drug_name=m2.drug_name AND d.drug_name!=d2.drug_name AND m.mdate BETWEEN ? AND ?  AND m2.mdate BETWEEN ? AND ? GROUP BY m.drug_name, d2.category", (startTime, endTime, startTime, endTime, startTime, endTime, startTime, endTime))
        
        # Print result
        print c.fetchall()
        break    
    return

#QUERY THREE ADMIN
def diagnosis_medication():
    # list for a given diagnosis all possible medications that have been prescribed overtime after the diagnosis (over all charts)
    # list ordered by frequency of the medication for the given diagnosis.
   
    while True:
        diagnosis_input = raw_input("Enter a diagnosis: ")
        c.execute("SELECT d.diagnosis, m.drug_name, COUNT(m.drug_name) FROM diagnoses d, medications m WHERE d.chart_id=m.chart_id AND d.ddate <= m.mdate AND lower(d.diagnosis)=(?) GROUP BY m.drug_name ORDER BY COUNT(m.drug_name)", (diagnosis_input.lower(),))
        print c.fetchall()
        break
    return

#QUERY 4 ADMIN  
def drug_diagnosis():
    # list for a given drug all the diagnoses that have been made before prescribing the drug (over all charts)
    # list ordered by average amount of the drug prescribed over all diagnosis
  
    while True:
            drug_input = raw_input("Enter a drug name: ")
            c.execute("SELECT m.drug_name, d.diagnosis, AVG(m.amount) FROM diagnoses d, medications m WHERE d.chart_id=m.chart_id AND d.ddate <= m.mdate AND lower(m.drug_name)=(?) GROUP BY d.diagnosis", (drug_input.lower(),))
            print c.fetchall()
            break    
    return

def encryption(word):
    # take the password and encrypt it and return the encrypted password in hex
    encrypt_pass = hashlib.sha224(word)
    encrypt_pass = encrypt_pass.hexdigest()
    return encrypt_pass

def date_test(date):
    # test if date is correct length 19
    if len(date) != 19:
        return False
    if date[4] != '-' or date[7] != '-':
        return False
    if date[13] != ':' or date[16] != ':':
        return False
    if int(date[5:7]) > 12 or int(date[5:7]) == 0:
        return False
    if int(date[11:13]) > 59:
        return False
    if int(date[14:16]) > 59:
        return False
    if int(date[17:19]) > 59:
        return False
    return True

main()
