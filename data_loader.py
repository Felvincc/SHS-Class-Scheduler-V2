import sqlite3

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
        room_schedules = {}
        for room_id in self.rooms:
            room_schedules[room_id] = Section.init_schedule(self, self.ampm)

        # idx for sectiond id starts at 1, incase of future database for schedules
        # course_id is created via iteration, not through a db query. So if there are issues with desync, it probaby stems here
        section_list = []
        for (section_id, (course_id, (course_name, num_sections))) in enumerate(self.courses.items(), start = 1):
            for section_num in range(1, num_sections+1):
                section = Section(self.ampm)
                section.course = course_name
                section.course_id = section_id
                section.section_id = section_num
                section_list.append(section)
        pass

class Section():

    def __init__(self, slots):
        self.course_id = None
        self.section_id = None
        self.course = None
        self.schedule = self.init_schedule(slots)

    def __repr__(self):
        return f"course_id='{self.course_id}', section_id='{self.section_id}'"
        
    def init_schedule(self, slots):
        am_slot, pm_slot = slots
        schedule = {'am': [], 'pm': []}
        for _ in range(am_slot):
            schedule['am'].append([])
        for _ in range(pm_slot):
            schedule['pm'].append([])
        return schedule
    
         
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