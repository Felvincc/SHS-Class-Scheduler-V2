
# Command-Line Interface

import cmd
import os
import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()
cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS saves(
        save_id INTEGER PRIMARY KEY AUTOINCREMENT,
        save_name TEXT NOT NULL
    )""")
conn.commit()

class MyCommand(cmd.Cmd):
    prompt = "jmdy_scheduler_v2> "

    def do_quit(self, arg):
        '''Exits Program'''
        return True

    def do_generate(self, arg):
        '''Generates Class Schedules'''
        pass

    def do_inputdata(self, arg):
        '''This is where you input the data for the generating class schedules'''
        condition = True
        cls()

        print("Please keep spelling the same and consistent.")
        print("Write 'next', when you are finished entering the data for the current field.")

        save_name = input("Enter save name> ")

        cursor.execute(f"INSERT INTO saves (save_name) VALUES ('{save_name}')")
        conn.commit()

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

        print(address_data)

        amslots = int(input("Enter AM slots> "))
        pmslots = int(input("Enter PM slots> "))

        instructor_availability_condition = input("Do you want to add instructor availabilty? (Y/N)> ").lower()

        if instructor_availability_condition == 'y':
            pass
        else:
            pass

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {save_name}_instructors(
            instructor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL)
        """)

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {save_name}_instructors_subjects(
            instructor_id INTEGER,
            subject TEXT NOT NULL,
            FOREIGN KEY (instructor_id) REFERENCES {save_name}(instructor_id))
        """)

        conn.commit()

        
        for instructor in instructors_data:
            cursor.execute(f"INSERT INTO {save_name}_instructors (name) VALUES ('{instructor[0]}')") 
            conn.commit()

        for i, instructor_data in enumerate(instructors_data):
            instructor_id = i + 1
            for subject in instructor_data[1]:
                cursor.execute(f"INSERT INTO {save_name}_instructors_subjects (instructor_id, subject) VALUES ('{instructor_id}', '{subject}')")
        conn.commit()

        #[course, number of sections, [subject, subject, ...]]
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {save_name}_courses(
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course TEXT NOT NULL,
            num_sections INTEGER NOT NULL
            )""")
        
        for course in course_data:
            cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {save_name}_{course[0]}_subjects(
                subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL
            )""")
            cursor.execute(f"INSERT INTO {save_name}_courses (course, num_sections) VALUES ('{course[0]}', '{course[1]}')")
            for subject in course[2]:
                cursor.execute(f"INSERT INTO {save_name}_{course[0]}_subjects (subject) VALUES ('{subject}')")
        conn.commit()

        # [building, num_floors, [rooms]], address_data
        # make Building Address insert queries 

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {save_name}_buildings(
                building_id INTEGER PRIMARY KEY AUTOINCREMENT,
                building TEXT NOT NULL,
                num_floors INTEGER NOT NULL
            )""")
        conn.commit()

        for address in address_data:
            cursor.execute(f"INSERT INTO {save_name}_buildings (building, num_floors) VALUES ('{address[0]}', '{address[1]}')")
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {address[0]}_rooms(
                    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    room TEXT NOT NULL)
                           """)
            
            for room in address[2]:
                cursor.execute(f"INSERT INTO {address[0]}_rooms (room) VALUES ('{room}')")
            conn.commit()
            


            


        #print(temp_course)
        #print(instructor_data)
        #print(address_data)
                
    def do_seedata(self, arg):
        commands = {
            "instructors": self.show_instructors,
            "course": self.show_levels,
            "address": self.show_address,
            "amslots": self.show_amslots,
            "pmslots": self.show_pmslots,
            "subjects": self.show_subjects
        }

        command = commands.get(arg.strip(), self.invalid_input)
        command()

    def invalid_input(self):
        print("Invalid input, try again")

    def show_instructors(self):
        print("the sky falls when")
        pass

    def show_levels(self):
        pass

    def show_address(self):
        pass

    def show_amslots(self):
        pass

    def show_pmslots(self):
        pass

    def show_subjects(self):
        pass

def cls():
    os.system("cls")


MyCommand().cmdloop()
