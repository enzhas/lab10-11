from configparser import ConfigParser 
import psycopg2 
import csv 

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

def name_format(name):
    s = ""
    for i in name:
        if i.isalpha():
            s += i
    return s

def number_format(num):
    s = ""
    for i in num:
        if i.isdigit():
            s += i
    return s    

def run(command, cursor):
    if command == 1:
        user = input('Enter name or number or /all\n')
        if user == '/all' :
            request = '''
                select *
                from phonebook
            '''
        else :
            request = f'''
                select *
                from phonebook
                where name = \'{user}\' or number = \'{user}\'
            '''
    elif command == 2:
        name, num = input("Name: "), input("Number: ") 
        t = input("Change name? (y/n) ") 
        if t == 'y': 
            request = f"update phonebook set number = \'{num}\' where name = \'{name}\'"
        else: 
            request = f"update phonebook set name =\'{name}\' where number = \'{num}\'"

    elif command == 3:
        t = input("From console? (y/n) ")
        if t == 'y':
            name, number = input("Name: "), input("Phone number: ")
            print(name)
            print(number)
            name = name_format(name)
            number = number_format(number)
            request = f"insert into phonebook (name, number) values ('{name}','{number}');"
        else:
            file = input("Path to file: ") 
            with open(file, 'r') as f :
                data = f.readlines()

            for i in range(len(data)) :
                data[i] = data[i].removesuffix('\n')
                data[i] = f"({data[i]})"

            request = f"insert into phoneBook (name, phone) values {','.join(data)};"


    elif command == 4:
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
    2 - update 
    3 - insert 
    4 - delete 
    0 - exit""")
    command = input()
    if(command.isdigit() and int(command) < 5):
        command = int(command)
        if(command == 0):
            running = False
            break
        with conn.cursor() as cursor:
         running = run(command, cursor)

conn.close()