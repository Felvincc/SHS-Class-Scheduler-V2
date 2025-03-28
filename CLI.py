
# Command-Line Interface

import cmd
import os

class MyCommand(cmd.Cmd):
    prompt = "Scheduler> "

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

        instructor_data = [] # [instructor, subject, subject,...]
        while condition:
            temp_instructor_subject = []
            temp_instructor = input("Enter Instructor's name> ")
            
            if temp_instructor == "next":
                temp_instructor = []
                break
            else:

                temp_instructor_subject.append(temp_instructor)
                while condition:
                    subject = input("Enter the Subjects teach> ")

                    if subject == "next":
                        subject = []
                        instructor_data.append(temp_instructor_subject)
                        break
                    else:
                        temp_instructor_subject.append(subject)

        course_data = [] #[course, number of sections, [subject, subject, ...]]
        while condition:
            subjects = []
            temp_course = input("Enter course name> ")
            if temp_course == "next":
                temp_course = []
                break
            else:
                temp_num_sections = input("Enter the number of sections in this course> ")

                while condition:
                    temp_subject = input("Enter the subjects in this course> ")     

                    if temp_subject == "next":
                        temp_subject = []
                        temp_course_data = [temp_course, temp_num_sections, subjects]
                        course_data.append(temp_course_data)
                        break
                    else:
                        subjects.append(temp_subject)

        address_data = [] # []
        while condition:
            temp_building = input("Enter building name> ")

            if temp_building == "next":
                break
            else:
                num_of_floors = int(input("Enter number of floors in the building> "))
                rooms = []

                for x in range(num_of_floors):
                    temp_rooms = []

                    while condition:
                        temp_room = input(f"Enter the rooms in floor {x+1}> ")

                        if temp_room == "next":
                             
                            rooms.append(temp_rooms)
                            break

                        else:
                            temp_rooms.append(temp_room)
                
                temp_address_data = [temp_building, num_of_floors, rooms]
            
            address_data.append(temp_address_data)

        amslots = int(input("Enter AM slots> "))
        pmslots = int(input("Enter PM slots> "))

        cls()

        print(temp_course)
        print(instructor_data)
        print(address_data)

        

                    

                
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
