
# Command-Line Interface

import cmd
import os
import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")
cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS saves(
        save_id INTEGER PRIMARY KEY AUTOINCREMENT,
        save_name TEXT NOT NULL
    )""")
conn.commit()

class MyCommand(cmd.Cmd):
    prompt = "jmdy_scheduler_v2> "

    def do_exit(self, arg):
        '''are you dumb'''
        return True

    def do_generate(self, arg):
        '''Generates class schedules
Usage: generate <save name>'''
        pass

    def do_inputdata(self, arg):
        '''Starts the data gathering process
Usage: inputdata'''

        condition = True
        
        cls()

        print("Please keep spelling the same and consistent.")
        print("Write 'next', when you are finished entering the data for the current field.")

        data = DataManagement()
        save_name = data.input_saves()

        cursor.execute(f"INSERT INTO saves (save_name) VALUES ('{save_name}')")
        conn.commit()

        instructors_data = data.input_instructors()
        course_data = data.input_course()
        address_data = data.input_address()
        amslots, pmslots = data.input_slots()
        instructor_availability = data.input_instructor_avail()

        cursor.execute(f"SELECT * FROM saves WHERE save_name = '{save_name}'")
        save_id = cursor.fetchall()[0][0]
    
        data.create_tables()
        
        cursor.execute("INSERT INTO ampm (save_id, am_slot, pm_slot) VALUES (?, ?, ?)", (save_id, amslots, pmslots))

        data.commit_instructors(save_id, instructors_data)
        data.commit_course(save_id, course_data)
        data.commit_address(save_id, address_data)
        conn.commit()  


    def do_seedata(self, arg):
        '''Shows data from a specific save\n
Usage: 
seedata <save name> <data>          - View specific data from save
seedata saves                       - View all save files

Available data types: \nsaves \ninstructors  \ncourse \naddress \nbuildings \nrooms \nsubjects \nslots'''

        queries = Queries()

        commands = {
            "instructors": queries.see_instructors,
            "courses": queries.see_courses,
            "address": queries.see_address,
            "buildings": queries.see_buildings,
            "rooms": queries.see_rooms,
            "subjects": queries.see_subjects,
            "slots": queries.see_slots
        }

        if arg == "saves":
            cursor.execute(f"SELECT * FROM saves")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            conn.commit()
            return

        try:
            save_name, data_type = arg.split()
            cursor.execute("SELECT save_id FROM saves WHERE save_name = ?", (save_name,))
            result = cursor.fetchone()
            save_id = result[0]
            print(save_id)
            print(commands[data_type])
            rows = commands[data_type](save_id)
            for row in rows:
                print(row)
            
        except ValueError:
            print("Usage: seedata <save_name> <data>")
            return
        except KeyError:
            print(f"Data type, '{data_type}', does not exist")
            return
        except sqlite3.OperationalError:
            print(f"Save file, '{save_name}', does not exist ")
            return
    
class Queries:

    def __init__(self):
        pass

    def see_instructors(self, save_id):
        cursor.execute("SELECT * FROM instructors WHERE save_id = ?", (save_id,))
        return cursor.fetchall()

    def see_courses(self, save_id):
        cursor.execute("SELECT * FROM courses WHERE save_id = ?", (save_id,))
        return cursor.fetchall()

    def see_address(self, save_id):
        cursor.execute("SELECT * FROM buildings WHERE save_id = ?", (save_id,))
        return cursor.fetchall()

    # NOT DONE
    def see_buildings(self, save_id):
        cursor.execute("SELECT * FROM buildings WHERE save_id = ?", (save_id,))
        return cursor.fetchall()
    
    def see_rooms(self, save_id):
        cursor.execute("SELECT * FROM rooms WHERE save_id = ?", (save_id,))
        return cursor.fetchall()
        
    def see_slots(self, save_id):
        cursor.execute("SELECT * FROM ampm WHERE save_id = ?", (save_id,))
        return cursor.fetchall()

    def see_subjects(self, save_id):
        cursor.execute("SELECT * FROM subjects WHERE save_id = ?", (save_id,))
        return cursor.fetchall()

class DataManagement:
    
    def commit_instructors(self, save_id, instructors_data):
        for x in instructors_data:
            instructor = x[0]
            subjects = x[1]

            cursor.execute("INSERT INTO instructors (save_id, instructor_name) VALUES (?, ?)", (save_id, instructor))
            instructor_id = cursor.lastrowid

            for sub in subjects:
                cursor.execute("INSERT INTO subjects(save_id, subject_name) VALUES (?, ?) ON CONFLICT (save_id, subject_name) DO NOTHING", (save_id, sub))
                cursor.execute("SELECT subject_id FROM subjects WHERE subject_name = ?", (sub,))

                result = cursor.fetchone()
                subject_id = result[0]
                cursor.execute("INSERT INTO instructor_subjects(instructor_id, subject_id) VALUES (?, ?)", (instructor_id, subject_id))
        return


    def commit_course(self, save_id, course_data):
        for x in course_data:
            course_name = x[0]
            course_sections = x[1]
            course_subjects = x[2]

            cursor.execute("INSERT INTO courses(save_id, course_name, num_sections) VALUES (?, ?, ?)", (save_id, course_name, course_sections))
            course_id = cursor.lastrowid
                    

            for sub in course_subjects:
                cursor.execute("INSERT INTO subjects(save_id, subject_name) VALUES (?, ?) ON CONFLICT (save_id, subject_name) DO NOTHING", (save_id, sub))
                cursor.execute("SELECT subject_id FROM subjects WHERE subject_name = ?", (sub,))

                result = cursor.fetchone()
                subject_id = result[0]
                cursor.execute("INSERT INTO course_subjects(course_id, subject_id) VALUES (?, ?)", (course_id, subject_id))
        return


    def commit_address(self, save_id, address_data):
        for x in address_data:
            building_name = x[0]
            num_floors = x[1]
            rooms = x[2]

            cursor.execute("INSERT INTO buildings(save_id, floors, building_name) VALUES (?, ?, ?)", (save_id, num_floors, building_name))
            building_id = cursor.lastrowid

            for room in rooms:
                cursor.execute("INSERT INTO rooms(building_id, room_name, save_id) VALUES (?, ?, ?)", (building_id, room, save_id))
        return
    
    def input_saves(self):
        save_name = input("Enter save name> ")
        return save_name

    def input_instructors(self):
        condition = True
        instructors_data = [] # [[instructor, [subject, subject]],...]
        while condition:
            temp_instructor_subject = []
            temp_instructor = input("Enter Instructor's name> ").lower()
            
            if temp_instructor == "next":
                temp_instructor = []
                break
            else:
                temp = []
                temp_instructor_subject.append(temp_instructor)
                while condition:
                    subject = input("Enter the Subjects teach> ").lower()

                    if subject == "next":
                        subject = []
                        temp_instructor_subject.append(temp)
                        instructors_data.append(temp_instructor_subject)
                        break
                    else:
                        temp.append(subject)

        return instructors_data
    
    def input_course(self):
        condition = True
        course_data = [] #[course, number of sections, [subject, subject, ...]]
        while condition:
            subjects = []
            temp_course = input("Enter course name> ").lower()
            if temp_course == "next":
                temp_course = []
                break
            else:
                temp_num_sections = int(input("Enter the number of sections in this course> "))

                while condition:
                    temp_subject = input("Enter the subjects in this course> ").lower()     

                    if temp_subject == "next":
                        temp_subject = []
                        temp_course_data = [temp_course, temp_num_sections, subjects]
                        course_data.append(temp_course_data)
                        break
                    else:
                        subjects.append(temp_subject)
        
        return course_data
    
    def input_address(self):
        condition = True
        address_data = [] # [building, num_floors, [rooms], [...]]
        while condition:
            temp_building = input("Enter building name> ").lower()

            if temp_building == "next":
                break
            else:
                num_of_floors = int(input("Enter number of floors in the building> "))
                rooms = []

                for x in range(num_of_floors):
                    while condition:
                        temp_room = input(f"Enter the rooms in floor {x+1}> ").lower()
                        if temp_room == "next":
                            break

                        else:
                            rooms.append(temp_room)
                
                temp_address_data = [temp_building, num_of_floors, rooms]
            
            address_data.append(temp_address_data)
        return address_data
    
    def input_slots(self):
        amslots = int(input("Enter AM slots> "))
        pmslots = int(input("Enter PM slots> "))
        return amslots, pmslots
    
    def input_instructor_avail(self):
        instructor_availability_condition = input("Do you want to add instructor availabilty? (Y/N)> ").lower()
        if instructor_availability_condition == 'y':
            condition = True
        else:
            condition = False

        return condition
    
    def create_tables(self):
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS ampm(
                ampm_id INTEGER PRIMARY KEY AUTOINCREMENT,
                save_id INTEGER NOT NULL,
                am_slot INTEGER NOT NULL,
                pm_slot INTEGER NOT NULL,
                FOREIGN KEY (save_id) REFERENCES saves(save_id) ON DELETE CASCADE
                )
            """)

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS courses(
                course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                save_id INTEGER NOT NULL,
                course_name TEXT NOT NULL,
                num_sections INTEGER NOT NULL,
                FOREIGN KEY (save_id) REFERENCES saves(save_id) ON DELETE CASCADE
                )
            """)
        
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS subjects(
                subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
                save_id INTEGER NOT NULL,
                subject_name TEXT NOT NULL,
                FOREIGN KEY (save_id) REFERENCES saves(save_id) ON DELETE CASCADE,
                UNIQUE (save_id, subject_name)) 
            """)
        
        #junction table
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS course_subjects(
                course_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                PRIMARY KEY (course_id, subject_id),
                FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
                FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE
                )
            """)
        
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS instructors(
                instructor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                save_id INTEGER NOT NULL,
                instructor_name TEXT NOT NULL,
                FOREIGN KEY (save_id) REFERENCES saves(save_id) ON DELETE CASCADE
                )
            """)
        
        #junction table
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS instructor_subjects(
                instructor_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                PRIMARY KEY (instructor_id, subject_id),
                FOREIGN KEY (instructor_id) REFERENCES instructors(instructor_id) ON DELETE CASCADE,
                FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE
                )
            """)
        
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS buildings(
                building_id INTEGER PRIMARY KEY AUTOINCREMENT,
                save_id INTEGER NOT NULL,
                floors INTEGER NOT NULL,
                building_name TEXT NOT NULL,
                FOREIGN KEY (save_id) REFERENCES saves(save_id) ON DELETE CASCADE
                ) 
            """)
        
        cursor.execute(f""" 
            CREATE TABLE IF NOT EXISTS rooms(
                room_id INTEGER PRIMARY KEY AUTOINCREMENT,
                building_id INTEGER NOT NULL,
                save_id INTEGER NOT NULL,
                room_name TEXT NOT NULL,
                FOREIGN KEY (building_id) REFERENCES buildings(building_id) ON DELETE CASCADE
                )
            """)
        conn.commit()

        return



def cls():
    os.system("cls")


MyCommand().cmdloop()
