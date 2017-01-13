#Chaitali Patel
#Alex Dong
#Yvonne Hoang

import sqlite3
import sys
import itertools


file_name = raw_input("Enter file name : ")
db_file_path = file_name
#db_file_path = 'MiniProject2-InputExample.db'               

#Create or Connect to a Database
conn = sqlite3.connect(db_file_path)
c = conn.cursor()
#For Foreign key constraint of SQLite
c.execute('PRAGMA foreign_keys=ON;')


def main():
    input_relation = raw_input("Enter a table name to get the FDs from: ")
    input_relation_FD = "Input_FDs_"+input_relation
    func_dep = get_dependencies(input_relation_FD)[0]
    while True:
        
        print("What would you like to do?")
        print('(1) Synthesize a 3NF schema for the given input table')
        print('(2) Decompose the given input table into BCNF')
        print('(3) Compute attribute closure')
        print('(4) Check whether two sets of functional dependencies F1 and F2 are equivalent')  
        print('(5) Exit')        
        choice = raw_input('Enter a number depending on your option: ')
        
        if choice == '1':
            LHS = get_dependencies(input_relation_FD)[2] 
            RHS = get_dependencies(input_relation_FD)[1]            
            schema_3nf(func_dep, LHS, RHS, input_relation_FD)
            continue
        if choice == '2':
            LHS = get_dependencies(input_relation_FD)[2]
            RHS = get_dependencies(input_relation_FD)[1]
            #initialize_R(func_dep, LHS, RHS)
            check_bcnf(func_dep, LHS, RHS, input_relation_FD)
            continue
        if choice == '3':
            attribute_closure()
            continue
        if choice == '4':
            F1_tables = raw_input("Enter table names for set F1: ")
            F1_tables = F1_tables.split(',')
            F2_tables = raw_input("Enter table names for set F2: ")
            F2_tables = F2_tables.split(',')            
            compare_FDS(F1_tables, F2_tables)
            continue
        if choice == '5':
            break
    print("End of program")
    
def attribute_closure():
    
    subset = raw_input("Enter attribute subset to get closure of: ")
    tables = raw_input("Enter tables to compute closure: ")
    subset = subset.split(',')
    tables = tables.split(',')
    
    #get the FDs
    relation_name = []
    func_dep = []
    func_LHS = []
    func_RHS = [] 
    for table_name in tables:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()   
        query = "select * from "+table_name
        c.execute(query)
        for row in c.fetchall():
            func_LHS.append(row["LHS"])
            func_RHS.append(row["RHS"])
            func_dep.append( [row["LHS"].split(","), row["RHS"].split(",")] )
        conn.commit()     
    
    
    closure = compute_closure(set(subset), func_dep)
    print("The closure is: " + ",".join(list(closure)))
    
    return    

    
def check_bcnf(func_dep, LHS, RHS, input_relation_FD):
    
    LHSList = []
    all_func = []
    new_tables = []
    R = all_attributes(LHS,RHS)      
    
    # Check if R is in BCNF (X->Y)
    for i in range(0, len(LHS)):

        #or X is superkey of R
        closure = compute_closure(set(LHS[i].split(',')), func_dep)
    
        keys = set(R)
        LHSList = LHS[i].split(',')
        RHSList = RHS[i].split(',')
        
        if (keys.issubset(closure)):
            print(LHS[i] + " is a superkey!!!!")
        # if Y is not a subset of X or X not a superkey
        
        elif [item for item in LHSList if item in R] and [item for item in RHSList if item in R]:
            R, func_dep, R1, new_tables = decompose_bcnf(func_dep, LHS[i], RHS[i], R,input_relation_FD, new_tables)
            all_func.append(R1)
            
    all_func.append(R)
    
    # get table name
    c.execute("SELECT name FROM sqlite_master WHERE name =?;",(input_relation_FD,))
    name = c.fetchone()
    tbl_name = name[0].split("_", 2)[2]     
    
    # get types of all attributes 
    type_list = []
    relation_name = 'Input_'+tbl_name
    query = "PRAGMA table_info("+relation_name+");"
    for row in c.execute(query):
        type_list.append((row[1], row[2]))  
        
    attr = ''.join(R)
        
    data_table = "Output_"+tbl_name+"_"+attr
    drop_query = "drop table if exists " + data_table + ";"
    c.execute(drop_query)
    conn.commit()     
    
    # CREATE LAST TABLE WITH REMAINING R
    # create Output tables and add columns 
    for i in range(0, len(R)):
        for num in range(len(type_list)):
            if R[i] == type_list[num][0]: 
                if(i==0):
                    # create Output_//_// with one column
                    query = "create table "+data_table+"("+R[0]+" "+type_list[num][1]+");"
                else:
                    # add new columns to table
                    query = "alter table "+data_table+" ADD "+R[i]+" "+type_list[num][1]+";"
                c.execute(query)
                conn.commit()     
    
    c.execute("SELECT name FROM sqlite_master WHERE name =?;",(input_relation_FD,))
    name = c.fetchone()
    tbl_name = name[0].split("_", 2)[2]  
    # check if dependancy preserving
    dep_preserve = compare_FDS(name,new_tables)   
    if(dep_preserve == True):
        print("Dependency preserving!")
    else:
        print("Not dependency preserving....")
        
    fill_data(all_func, tbl_name)

    return
    

def decompose_bcnf(func_dep, LHS, RHS, R, input_relation_FD, new_tables):
    # pick FD: X-> Y that holds in R' and violates BCNF
    # If X->Y and X^Y = empty set, decompose R into XY and R-Y
    LHS = LHS.split(',')
    RHS = RHS.split(',')
    
    for i in range(0, len(RHS)):
        if RHS[i] not in R:
            RHS.remove(RHS[i])
    for j in range(0, len(LHS)):
        if LHS[j] not in R:
            LHS.remove(LHS[j])
    R1 = list(LHS + RHS)
# Create the tables of the FDS that were violating the BCNF rules

    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name =?;", (input_relation_FD,))
    name = c.fetchone()
    tbl_name = name[0].split("_", 2)[2]
    FD_table_name = 'Output_FDS_'+tbl_name+'_'+''.join(R1)
    new_tables.append(FD_table_name)
    query_drop = 'drop table if exists '+FD_table_name+';'
    c.execute(query_drop)
    query = 'create table '+FD_table_name+' (LHS TEXT,RHS TEXT);'
    c.execute(query)
    join_LHS = ','.join(LHS)
    join_RHS = ','.join(RHS)
    query = "insert into "+FD_table_name+" (LHS,RHS) values ('"+join_LHS+"','"+join_RHS+"');"
    c.execute(query)
    conn.commit()
# Create the tables with the values of the FDS that were violating BCNF rules

    FD_data_table = 'Output_'+tbl_name+'_'+''.join(R1)
    query_drop = 'drop table if exists '+FD_data_table+';'
    c.execute(query_drop)
    type_list = []

    final_attribute = []
    for attribute in R1:
        if attribute not in final_attribute:
            final_attribute.append(attribute)
    relation_name = 'Input_'+tbl_name
    query = "PRAGMA table_info("+relation_name+");"
    for row in c.execute(query):
        type_list.append((row[1], row[2]))   
    
    searched_type = []
    all_attribute = join_LHS+','+join_RHS
    for i in range(len(type_list)):
        for attribute in all_attribute.split(','):
            if type_list[i][0] == attribute:
                searched_type.append(type_list[i])
                
    whole = ''
    for row in searched_type:
        whole = whole+' '.join(row)+','
    query = "create table "+FD_data_table+"("+whole+"PRIMARY KEY("+join_LHS+"));"
    c.execute(query)
    conn.commit()
# End making tables
    for fd in func_dep:
        if set(fd[1]).issubset(set(RHS)):
            func_dep.remove(fd)
        # then delete FDs X->Y containing 'Y'
        elif set(fd[0]).issubset(set(RHS)):
            func_dep.remove(fd)
        elif set(RHS).issubset(fd[1]):
            fd[1] = list(set(fd[1]).difference(RHS))
            

    R = list(set(R).difference(RHS))
    
    return R, func_dep, R1, new_tables

def schema_3nf(func_dep, LHS1, RHS1, input_relation_FD):  
    
    R = all_attributes(LHS1, RHS1)
           
    #make RHS of func_dep single attributes
    single_dep = []
    for i in func_dep:
        for j in i[1]:
            y = [i[0], [j]]
            single_dep.append(y) 
    
    #find redundant left hand sides   
    for x in single_dep:         
        for L in range(0, len(x[0])):
            for subset in itertools.combinations(x[0], L):
                closure = compute_closure(set(subset), single_dep)
                if(set(x[1]).issubset(closure) == True):
                        x[0] = list(subset)
                    
    # delete redundant FDs
    T = single_dep
    old_len = ''
    while(len(T) != old_len):
        old_len = len(T)
        for x in T:
            f = T.pop(0)
            closure = compute_closure(set(f[0]), T)
            if(set(f[1]).issubset(closure) == False):
                T.append(f)

    conn = sqlite3.connect(db_file_path)    
    conn.text_factory = str
    c = conn.cursor()

    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name =?;",(input_relation_FD,))
    name = c.fetchone()
    tbl_name = name[0].split("_", 2)[2]
    
    # get the list of columns and types into a list
    type_list = []
    relation_name = 'Input_'+tbl_name
    query = "PRAGMA table_info("+relation_name+");"
    for row in c.execute(query):
        type_list.append((row[1], row[2]))
        
    func_num = len(T)
    all_func = []
    
    #Partition by same LHS
    while(len(T) != 0):
        R1 = [T.pop(0)]
        
        for relation in T:
            if relation[0] == R1[0][0]:
                R1.append(relation)
                T.remove(relation)
                
        merged = list(itertools.chain(*R1))
        lmerged = list(itertools.chain(*merged))

        # make a unique list of attributes
        final_attribute = []
        for attribute in lmerged:
            if attribute not in final_attribute:
                final_attribute.append(attribute)
        concat = ''.join(final_attribute)
        
        all_func.append(final_attribute)
        
        # drop table Output_//_//
        FD_table = "Output_" + tbl_name + "_" + concat
        drop_query = "drop table if exists " + FD_table + ";"
        c.execute(drop_query)
        conn.commit()   
        # drop table Output_//_FDS_//
        FDS_table = "Output_FDS_" + tbl_name + "_" + concat
        drop_query = "drop table if exists " + FDS_table + ";"
        c.execute(drop_query)
        conn.commit() 
        # original input table name 
        old_table = "Input_" + tbl_name
        
        # create Output FDS table with columns LHS and RHS
        query = "create table "+FDS_table+"(LHS TEXT, RHS TEXT);"
        c.execute(query)
        conn.commit()
        
        LHS = ','.join(merged[0])
        key = merged[0]
        
        for FD in merged:
            if(FD == key):
                merged.remove(FD)
        
        RHS = ','.join(list(itertools.chain(*merged)))
        join_LHS = LHS
        join_RHS = RHS
        searched_type = []
        all_attribute = join_LHS+','+join_RHS
        
        for i in range(len(type_list)):
            for attribute in all_attribute.split(','):
                if type_list[i][0] == attribute:
                    searched_type.append(type_list[i])
        whole = ''
        for row in searched_type:
            whole = whole+' '.join(row)+','
        # Create table
        query_drop = 'drop table if exists '+FD_table+';'
        c.execute(query_drop)
        query = "create table "+FD_table+"("+whole+"PRIMARY KEY("+join_LHS+"));"
        c.execute(query)
        conn.commit()        

        insert_query = "INSERT INTO "+FDS_table+" (LHS, RHS) VALUES ('"+ LHS +"','"+RHS+"');"
        c.execute(insert_query)
        conn.commit()        
        
        
    keys = set(R)
    
    relation_name = []
    func_dep = []
    func_LHS = []
    func_RHS = [] 
    conn = sqlite3.connect(db_file_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()   
    query = "select * from sqlite_master where type = 'table' and tbl_name like '%Output_FDS%';"
    for row in c.execute(query):
        relation_name.append(row['tbl_name'])
    # get all the FDS for the new tables 
    for table in relation_name:    
        query = "select * from "+table+";"
        c.execute(query)      
        for row in c.fetchall():
            func_LHS.append(row["LHS"])
            func_RHS.append(row["RHS"])
            func_dep.append( [row["LHS"].split(","), row["RHS"].split(",")] )
        conn.commit()     
    # Check if 3NF schema has a superkey
    superkey = False
    longest_closure = ''
    for i in range(len(func_LHS)):
        
        closure = compute_closure(set(func_LHS[i].split(',')), func_dep)
        
        if(len(closure) > len(longest_closure)):
            longest_closure = closure
            cand_key = set(func_LHS[i].split(','))
             
        keys = set(R)
        LHSList = func_LHS[i].split(',')
        RHSList = func_RHS[i].split(',')
        
        if (keys.issubset(closure)):
            superkey = True 
    
    if(superkey == False):       
        add_keys = keys.difference(longest_closure)
        new_superkey = list(add_keys.union(cand_key))
        
        key = ''.join(new_superkey)
        all_func.append(new_superkey)
        key_table = "Output_"+ tbl_name +"_"+key
        drop_query = "drop table if exists " + key_table + ";"
        c.execute(drop_query)
        conn.commit()         
  
        # create Output tables and add columns for last table
        for i in range(0, len(new_superkey)):
            for num in range(len(type_list)):
                if new_superkey[i] == type_list[num][0]: 
                    if(i==0):
                        # create Output_//_// with one column
                        query = "create table "+key_table+"("+new_superkey[0]+" "+type_list[num][1]+");"
                    else:
                        # add new columns to table
                        query = "alter table "+key_table+" ADD "+new_superkey[i]+" "+type_list[num][1]+";"
                    c.execute(query)
                    conn.commit()          
               
    fill_data(all_func, tbl_name)

    return

def get_dependencies(input_relation_FD):
    
    relation_name = []
    func_dep = []
    func_LHS = []
    func_RHS = [] 
    
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    for row in c.execute("select tbl_name from sqlite_master where tbl_name = ?;", (input_relation_FD,)):
        relation_name.append(row['tbl_name'])
    query = "select * from "+relation_name[0]
    c.execute(query)
    for row in c.fetchall():
        func_LHS.append(row["LHS"])
        func_RHS.append(row["RHS"])
        func_dep.append( [row["LHS"].split(","), row["RHS"].split(",")] )
    conn.commit() 
    
    return func_dep, func_RHS, func_LHS

    
def fill_data(all_func, tbl_name):
    
    # put data into tables
    fill_table = raw_input("Fill table with data? (Y/N) : ")
    if( fill_table == 'y' or fill_table == 'Y'):             
        for dep in all_func:            
            name = ''.join(dep)
            FD_table = "Output_" + tbl_name + "_" + name
            old_table = "Input_" + tbl_name                       
            query =  "INSERT INTO " + FD_table + " SELECT DISTINCT "
            for col in dep:
                query = query + col + ","
            query = query[:-1] + " FROM " + old_table + ";"
            c.execute(query)
            conn.commit()      
    return

def compute_closure(closure, func_dep):
    
    old = ''
    while(old != closure):
        old = closure
        for x in func_dep:
            if set(x[0]).issubset(closure):
                closure = closure.union(set(x[1]))  
    
    return closure

def all_attributes(LHS, RHS):
    
    R = []
    for i in LHS:
        for j in RHS:
            x = i.split(",")
            y = j.split(",")
            for index in range(0, len(x)):
                for index1 in range(0, len(y)):
                    
                    if x[index] not in R:
                
                        R.append(x[index])
                    elif y[index1] not in R:
                        R.append(y[index1])    
    
    
    return R

def compare_FDS(F1_tables, F2_tables):  
    
    func1_dep = []
    func1_LHS = []
    func1_RHS = [] 
    func2_dep = []
    func2_LHS = []
    func2_RHS = []
    
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    # get FD for F1
    for table in F1_tables:
        query = "select * from "+table
        c.execute(query)
        for row in c.fetchall():
            func1_LHS.append(row["LHS"])
            func1_RHS.append(row["RHS"])
            func1_dep.append( [row["LHS"].split(","), row["RHS"].split(",")] )
        conn.commit()
    #get FD for F2
    for table in F2_tables:
        query = "select * from "+table
        c.execute(query)
        for row in c.fetchall():
            func2_LHS.append(row["LHS"])
            func2_RHS.append(row["RHS"])
            func2_dep.append( [row["LHS"].split(","), row["RHS"].split(",")] )
        conn.commit()    
    

    
    closure_F1 = []
    closure_F2 = []
    # check if closures are equal
    equal_FD = True
    for a in func1_LHS:
        closure_F1 = compute_closure(set(a.split(",")), func1_dep)
        closure_F2 = compute_closure(set(a.split(",")), func2_dep)
        if closure_F1 != closure_F2:
            print("These FDs are not equivalent!")
            equal_FD = False
            break 
        
    if (equal_FD == True):    
        for a in func2_LHS:
            closure_F1 = compute_closure(set(a.split(",")), func1_dep)
            closure_F2 = compute_closure(set(a.split(",")), func2_dep)
            if closure_F1 != closure_F2:
                print("These FDs are not equivalent!")
                equal_FD = False
                break  
            
    if(equal_FD == True):
        print("These FDs are equivalent...")
        
    return equal_FD
    
    
    
main()