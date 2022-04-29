from configparser import ConfigParser 
import psycopg2 
import csv 
import re

conn = psycopg2.connect(
    host = 'localhost',
    database = 'phonebook',
    user = 'postgres',
    password = '4477'
)

conn.autocommit = True

def create_table():
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE phonebook(
        name VARCHAR(50),
        number VARCHAR(16)
    );
    ''')
    cursor.close();
def delete_table():
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE phonebook''')
    cursor.close()

def run(command, cursor):
    if command == 1:
    	t = input('Do you want to find users by pattern? y | n\n')
    	if(t == 'y'):
    		pattern = input('Enter the pattern\n')
    		request = f"select * from getUserFromPattern('%{pattern}%');"
    		cursor.execute(request);
    	else:
        	pagination = input('Dou you want to get pages? y | n\n')
        	if pagination == 'y' :
        		page = input('Enter which page you want to see?\n')
        		request = f"select * from getUsersWithPagination({int(page)}, 10);"
        		cursor.execute(request);
        	else:    
        		user = input('Enter name or number or /all\n')
        		if user == '/all' :
        			request = '''select *from phonebook'''
        			cursor.execute(request);
        		else :
        			request = f'''select * from phonebook where name = \'{user}\' or number = \'{user}\''''
        			cursor.execute(request);
    elif command == 2:
        t = input("From console? (y/n) ")
        if t == 'y':
        	n = input('How many users you want to insert?\n')
        	for i in range(int(n)) :
	            name, number = input("Name: "), input("Phone number: ")
	            print(name)
	            print(number)
	            if re.match("[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]", number):
	            	request = f"call insertUser('{name}', '{number}');"
	            	#f"insert into phonebook (name, number) values ('{name}','{number}');"
	            	cursor.execute(request);
	            else :
	            	print('Your phone is in incorrect format')
        else:
            file = input("Path to file: ") 
            with open(file, 'r') as f :
                data = f.readlines()

            for i in range(len(data)) :
                data[i] = data[i].removesuffix('\n')
                data[i] = f"({data[i]})"

            request = f"insert into phoneBook (name, phone) values {','.join(data)};"
        cursor.execute(request);


    elif command == 3:
        user = input('Enter name you want to delete\n')
        if user == '/all' :
            request = '''
                delete from phonebook;
            '''
        else :
            request = f'''
                delete from phonebook
                where name = \'{user}\''
            '''
       	cursor.execute(request);

    #cursor.execute(request);
    if command == 1:
        numbers = cursor.fetchall()
        #print(numbers)
        if len(numbers) > 0 :
            for i in numbers:
                print(i)
        else :
            print('No such data')
    return True

running  = True
print('Phonebook:')

#create_table()
#delete_table()

while running:
    print("""Help: 
    1 - query
    2 - insert 
    3 - delete 
    0 - exit""")
    command = input()
    if(command.isdigit() and int(command) < 4):
        command = int(command)
        if(command == 0):
            running = False
            break
        with conn.cursor() as cursor:
         running = run(command, cursor)

conn.close()