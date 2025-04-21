
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

        cursor.execute(f"SELECT * FROM saves WHERE save_name = '{save_name}'")
        save_id = cursor.fetchall()[0][0]
        print(save_id)

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {save_name}_ampm_slots(
            save_id INTEGER,
            am_slot INTEGER NOT NULL,
            pm_slot INTEGER NOT NULL,
            FOREIGN KEY (save_id) REFERENCES saves(save_id) ON DELETE CASCADE
            )
        """)

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {save_name}_instructors(
            instructor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            save_id INTEGER,
            name TEXT NOT NULL,
            FOREIGN KEY (save_id) REFERENCES saves(save_id) ON DELETE CASCADE)
        """)

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {save_name}_instructors_subjects(
            instructor_id INTEGER,
            subject TEXT NOT NULL,
            FOREIGN KEY (instructor_id) REFERENCES {save_name}_instructors(instructor_id) ON DELETE CASCADE)
        """)

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {save_name}_courses(
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            save_id INTEGER,
            course TEXT NOT NULL,
            num_sections INTEGER NOT NULL,
            FOREIGN KEY (save_id) REFERENCES saves(save_id) ON DELETE CASCADE
        )""")
        
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {save_name}_buildings(
            building_id INTEGER PRIMARY KEY AUTOINCREMENT,
            save_id INTEGER,
            building TEXT NOT NULL,
            num_floors INTEGER NOT NULL,
            FOREIGN KEY (save_id) REFERENCES saves(save_id) ON DELETE CASCADE
        )""")
        conn.commit()

        cursor.execute(f"INSERT INTO {save_name}_ampm_slots (am_slot, pm_slot, save_id) VALUES ({amslots}, {pmslots}, {save_id})") 

        
        for instructor in instructors_data:
            cursor.execute(f"INSERT INTO {save_name}_instructors (name, save_id) VALUES ('{instructor[0]}', '{save_id}')") 
        conn.commit()

        for i, instructor_data in enumerate(instructors_data):
            instructor_id = i + 1
            for subject in instructor_data[1]:
                cursor.execute(f"INSERT INTO {save_name}_instructors_subjects (instructor_id, subject) VALUES ('{instructor_id}', '{subject}')")
        conn.commit()

        #[course, number of sections, [subject, subject, ...]]
        for course in course_data:
            cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {save_name}_{course[0]}_subjects(
                subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER,
                subject TEXT NOT NULL,
                FOREIGN KEY (course_id) REFERENCES {save_name}_courses(course_id) ON DELETE CASCADE
            )""")
            cursor.execute(f"INSERT INTO {save_name}_courses (course, num_sections, save_id) VALUES ('{course[0]}', '{course[1]}', '{save_id}')")
            for subject in course[2]:
                cursor.execute(f"INSERT INTO {save_name}_{course[0]}_subjects (subject) VALUES ('{subject}')")
        conn.commit()

        # [building, num_floors, [rooms]], address_data
        for address in address_data:
            cursor.execute(f"INSERT INTO {save_name}_buildings (building, num_floors) VALUES ('{address[0]}', '{address[1]}')")
            cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {save_name}_{address[0]}_rooms(
                room_id INTEGER PRIMARY KEY AUTOINCREMENT,
                building_id INTEGER,
                room TEXT NOT NULL,
                FOREIGN KEY (building_id) REFERENCES {save_name}_buildings(building_id) ON DELETE CASCADE)
                """)
            
            for room in address[2]:
                cursor.execute(f"INSERT INTO {save_name}_{address[0]}_rooms (room) VALUES ('{room}')")
            conn.commit()
        
        cursor.execute(f"INSERT INTO {save_name}_ampm_slots (am_slot, pm_slot) VALUES ('{amslots}', '{pmslots}')")

     
    def do_seedata(self, arg):
        '''Shows data from a specific save\n
Usage: 
seedata <save name> <data>          - View specific data from save
seedata saves                       - View all save files

Available data types: \nsaves \ninstructors  \ncourse \naddress \nslots \nsubjects '''

        commands = {
            "instructors": self.see_instructors,
            "course": self.see_courses,
            "address": self.see_address,
            "slots": self.see_amslots,
            "subjects": self.see_subjects
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
            rows = commands[data_type](save_name)
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
    
    def see_instructors(self, save_name):
        cursor.execute(f"SELECT * FROM {save_name}_instructors")
        return cursor.fetchall()

    def see_courses(self, save_name):
        cursor.execute(f"SELECT * FROM {save_name}_courses")
        return cursor.fetchall()

    def see_address(self, save_name):
        cursor.execute(f"SELECT * FROM {save_name}_buildings")
        temp = cursor.fetchall()
        buildings = []
        address = []
        for val in temp:
            buildings.append([val[1]])
        for idx, building in enumerate(buildings):
            cursor.execute(f"SELECT * FROM {save_name}_{building[0]}_rooms")
            temp = cursor.fetchall()
            address.append([building])
            for x in temp:
                address[idx].append(x[1])
        return address
                
    def see_amslots(self, save_name):
        cursor.execute(f"SELECT * FROM {save_name}_ampm_slots")
        rows = cursor.fetchall()
        am_slots = [row['am_slot'] for row in rows]
        return am_slots

    def see_pmslots(self, save_name):
        cursor.execute(f"SELECT * FROM {save_name}_ampm_slots")
        rows = cursor.fetchall()
        am_slots = [row['pm_slot'] for row in rows]
        return am_slots
        

    def see_subjects(self):
        pass

def cls():
    os.system("cls")


MyCommand().cmdloop()
