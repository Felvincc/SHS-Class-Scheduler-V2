import sqlite3

conn = sqlite3.connect('data.db')

cursor = conn.cursor()

# SEPARATE INTO DIFFERENT FILES IF IT GETS TOO BIG

class Generate():

    def __init__(self, save_name):
        self.save_name = save_name
        cursor.execute("SELECT save_id FROM saves WHERE save_name = ?", (save_name,))
        save_id = cursor.fetchone()[0] 
        fetch = Fetch()
        self.ampm = fetch.fetch_ampm(save_id)
        self.courses = fetch.fetch_courses(save_id)
        self.courses = fetch.fetch_subjects(save_id)
        self.course_subjects = fetch.fetch_course_subjects(save_id)
        self.instructors = fetch.fetch_instructors(save_id)
        self.instructors_subjects = fetch.fetch_instructor_subjects(save_id)
        self.buildings = fetch.fetch_buildings(save_id)
        self.rooms = fetch.fetch_rooms(save_id)


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
        cursor.execute("SELECT course_id, course_name FROM courses WHERE save_id = ?", (save_id,))
        rows = cursor.fetchall()
        result = {}
        for course_id, course_name in rows:
            result[course_id] = course_name
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

Generate('test')

#test = Generate()