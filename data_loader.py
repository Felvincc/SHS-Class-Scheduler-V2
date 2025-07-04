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
    

    def generate(self):
        # creates empty room schedule dictonary
        room_schedules = {}
        for room_id in self.rooms:
            room_schedules[room_id] = Helper.init_schedule(self.ampm)

        # creates a dictionary for tracking the subject classes for instructor
        instructor_subject_counter = {}
        for instructor_id, subject_ids in self.instructors_subjects.items():
            instructor_subject_counter[instructor_id] = Helper.dict_mapper(subject_ids)

        subject_schedule_counter = Helper.init_schedule(self.ampm)
        all_subject_ids = []
        for x in self.subjects:
            all_subject_ids.append(x)
        for period, schedule in subject_schedule_counter.items():
            for time_slot in schedule:
                schedule[time_slot] = Helper.dict_mapper(all_subject_ids)
            

        section_dict = {}
        section_id = 0
        # loops to create/assign the individual schedules
        for course_id, (course_name, num_sections) in self.courses.items():
        # course_id is created via iteration, not through a db query. So if there are issues with desync, it probaby stems here
            for section_num in range(1, num_sections+1):
                section_id += 1
                section = Section(self)
                section.course_id = course_id
                section.section_num = section_num
                section.section_id =  section_id
                self.assign(section, room_schedules)
                section_dict[section_id] = section
        pass

    # modifies the section object and room_schedules dict for the assignment
    def assign(self, section, room_schedules):
        instructor_id_list = []
        for instructor_id in self.instructors_subjects:
            instructor_id_list.append(instructor_id)
        random.shuffle(instructor_id_list)

        for instructor_id in instructor_id_list:
            instructor_id


class Helper():

    def init_schedule(ampm):
        am_slot, pm_slot = ampm
        schedule = {}
        temp = {}
        for x in range(1, am_slot+1):
            temp[x] = None
        schedule['am'] = temp

        temp = {}
        for x in range(1, pm_slot+1):
            temp[x] = None
        schedule['pm'] = temp
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
        self.schedule = Helper.init_schedule(data.ampm)

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