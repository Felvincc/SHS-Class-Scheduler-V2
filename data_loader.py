import sqlite3
import random

conn = sqlite3.connect('data.db')

cursor = conn.cursor()

# SEPARATE INTO DIFFERENT FILES IF IT GETS TOO BIG

class Schedule():
    
    def __init__(self, save_name):
        self.save_name = save_name
        cursor.execute("SELECT save_id FROM saves WHERE save_name = ?", (save_name,))
        save_id = cursor.fetchone()[0] 
        fetch = Fetch()
        self.ampm = fetch.fetch_ampm(save_id)
        self.courses = fetch.fetch_courses(save_id)
        self.subjects = fetch.fetch_subjects(save_id)
        self.course_subjects = fetch.fetch_course_subjects(save_id)
        self.instructors = fetch.fetch_instructors(save_id)
        self.instructors_subjects = fetch.fetch_instructor_subjects(save_id)
        self.buildings = fetch.fetch_buildings(save_id)
        self.rooms = fetch.fetch_rooms(save_id)

        self.all_room_ids = []
        for room in self.rooms:
            self.all_room_ids.append(room)

    def generate(self):
        # creates empty room schedule dictonary
        self.room_schedules = {}
        for room_id in self.rooms:
            self.room_schedules[room_id] = Helper.init_schedule_bool(self.ampm)

        # contains all rooms in each schedule slot (book and pop the room id)
        self.room_schedules_tracker = Helper.init_schedule_dict(self.ampm)
       
        for period, schedule in self.room_schedules_tracker.items():
            for time_period, time_slots in schedule.items():
                for slot in time_slots:
                    all_rooms_id_copy = self.all_room_ids[:]
                    random.shuffle(all_rooms_id_copy)
                    schedule[time_period][slot] = all_rooms_id_copy
                
        # creates a dictionary for tracking the subject classes for instructor
        self.instructor_subject_counter = {}
        for instructor_id, subject_ids in self.instructors_subjects.items():
            self.instructor_subject_counter[instructor_id] = Helper.dict_mapper(subject_ids)

        self.subject_schedule_counter = Helper.init_schedule_bool(self.ampm)
        all_subject_ids = []
        for x in self.subjects:
            all_subject_ids.append(x)
        for period, schedule in self.subject_schedule_counter.items():
            for time_period, time_slot in schedule.items():
                for slot in time_slots:
                    schedule[time_period][slot] = Helper.dict_mapper(all_subject_ids)
            
        section_dict = {}
        section_id = 0
        result_schedule = {}
        # loops to create/assign the individual schedules
        for course_id, (course_name, num_sections) in self.courses.items():
        # course_id is created via iteration, not through a db query. So if there are issues with desync, it probaby stems here
            for section_num in range(1, num_sections+1):
                section_id += 1
                section = Section(self)
                section.course_id = course_id
                section.section_num = section_num
                section.section_id =  section_id
                section_dict[section_id] = section
                section_schedule = self.assign(section)

                result_schedule[section_id] = section_schedule

        print(result_schedule)

    # modifies the section object and room_schedules dict for the assignment
    def assign(self, section):
        course_id = section.course_id
        section_id = section.section_id
        section_subjects = self.course_subjects[course_id]
        section_schedule = Helper.init_schedule_dict(self.ampm)

        for day, period_and_time_slots in self.room_schedules_tracker.items():
            for time_period, time_slots in period_and_time_slots.items():
                for time_slot, room_id in time_slots.items():
                    
                    the_chosen_room = self.book_and_pop(day, time_period, time_slot)
                    section_schedule[day][time_period][time_slot]['room'] = the_chosen_room
        return section_schedule
                    
    def book_and_pop(self, day, time_period, time_slot):
        the_chosen_room = self.room_schedules_tracker[day][time_period][time_slot][0]
        self.room_schedules[the_chosen_room][day][time_period][time_slot] = True  
        self.room_schedules_tracker[day][time_period][time_slot].pop(0)
        return the_chosen_room

        
class Helper():
    @staticmethod

    def init_schedule_bool(ampm):
        am_slot, pm_slot = ampm
        schedule = {1:{}, 2:{}}
        
        for day in range(1,3):
            temp = {}
            for x in range(1, am_slot+1):
                temp[x] = False
            schedule[day]['am'] = temp

            temp = {}
            for x in range(1, pm_slot+1):
                temp[x] = False
            schedule[day]['pm'] = temp
        return schedule
    
    def init_schedule_dict(ampm):
        am_slot, pm_slot = ampm
        schedule = {1:{}, 2:{}}
        
        for day in range(1,3):
            temp = {}
            for x in range(1, am_slot+1):
                temp[x] = {}
            schedule[day]['am'] = temp

            temp = {}
            for x in range(1, pm_slot+1):
                temp[x] = {}
            schedule[day]['pm'] = temp
        return schedule
    
    def dict_mapper(list):
        temp = {}
        for x in list:
            temp[x] = 0
        return temp

class Section():

    def __init__(self, data):
        self.course_id = None 
        self.section_num = None #convert to letters for section name
        self.section_id = None
        self.schedule = Helper.init_schedule_bool(data.ampm)

    def __repr__(self):
        return f"course_id='{self.course_id}', section_num='{self.section_num}', section_id='{self.section_id}'"
        
class Fetch():

    def fetch_ampm(self, save_id):
        cursor.execute("SELECT am_slot, pm_slot FROM ampm WHERE save_id = ?", (save_id,))
        row = cursor.fetchone()
        if row:
            am_slot, pm_slot = row
            return am_slot, pm_slot
        else:
            am_slot, pm_slot = None, None

    def fetch_courses(self, save_id):
        cursor.execute("SELECT course_id, course_name, num_sections FROM courses WHERE save_id = ?", (save_id,))
        rows = cursor.fetchall()
        result = {}
        for course_id, course_name, num_section in rows:
            result[course_id] = (course_name, num_section)
        return result

    def fetch_subjects(self, save_id):
        cursor.execute("SELECT subject_id, subject_name FROM subjects WHERE save_id = ?", (save_id,))
        rows = cursor.fetchall()
        result = {}
        for subject_id, subject_name in rows:
            result[subject_id] = subject_name
        return result

    def fetch_course_subjects(self, save_id):
        cursor.execute("SELECT course_id, subject_id FROM course_subjects WHERE save_id = ?", (save_id,))
        rows = cursor.fetchall()
        result = {}
        for course_id, value in rows:
            if course_id not in result:
                result[course_id] = []
            result[course_id].append(value)
        return result

    def fetch_instructors(self, save_id):
        cursor.execute("SELECT instructor_id, instructor_name FROM instructors WHERE save_id = ?", (save_id,))
        rows = cursor.fetchall()
        result = {}
        for instructor_id, instructor in rows:
            result[instructor_id] = instructor
        return result
            
    def fetch_instructor_subjects(self, save_id):
        cursor.execute("SELECT instructor_id, subject_id FROM instructor_subjects WHERE save_id = ?", (save_id,))
        rows = cursor.fetchall()
        result = {}
        for instructor_id, subject_id in rows:
            if instructor_id not in result:
                result[instructor_id]=[]
            result[instructor_id].append(subject_id)
        return result

    def fetch_buildings(self, save_id):
        cursor.execute("SELECT building_id, building_name FROM buildings WHERE save_id = ?", (save_id,))
        rows = cursor.fetchall()
        result = {}
        for building_id, building_name in rows:
            result[building_id] = building_name
        return result

    def fetch_rooms(self, save_id):
        cursor.execute("SELECT room_id, room_name FROM rooms WHERE save_id = ?", (save_id,))
        rows = cursor.fetchall()
        result = {}
        for room_id, room_name in rows:
            result[room_id] = room_name
        return result

x = Schedule('test')    
x.generate()


#test = Generate()