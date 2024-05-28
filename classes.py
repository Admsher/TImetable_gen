import datetime
from datetime import timedelta

class Course:
    def __init__(self, course_name, class_frequency, class_timings, class_numbers, 
                 course_strength, tut_timings, tut_numbers, 
                 degree1, degree2, degree3, degree4, degree5,
                 degree6, degree7, degree8, degree9, degree10,degree11,degree12,
                 prereq, lab_timings, lab_numbers,class_rooms,tut_rooms,lab_rooms,faculties):
        self.course_name = course_name
        self.class_frequency = class_frequency
        self.class_timings = class_timings if class_timings is not None else []  
        self.class_numbers = class_numbers if class_numbers is not None else []  
        self.course_strength = course_strength if course_strength is not None else []
        self.tut_timings = tut_timings if tut_timings is not None else []  
        self.tut_numbers = tut_numbers if tut_numbers is not None else [] 
        self.degree1 = degree1
        self.degree2 = degree2
        self.degree3 = degree3
        self.degree4 = degree4
        self.degree5 = degree5
        self.degree6 = degree6
        self.degree7 = degree7
        self.degree8 = degree8
        self.degree9 = degree9
        self.degree10 = degree10
        self.degree11 = degree11
        self.degree12 = degree12
        self.prereq = prereq if prereq is not None else []
        self.lab_timings = lab_timings if lab_timings is not None else []  
        self.lab_numbers = lab_numbers if lab_numbers is not None else []
        self.lab_rooms = lab_rooms if lab_rooms is not None else []
        self.class_rooms = class_rooms if class_rooms is not None else []
        self.tut_rooms = tut_rooms if tut_rooms is not None else []
        self.faculties=faculties


    def count_degree_occurrences(self):
        self.degree_count = {}
        for degree_list in [self.degree1, self.degree2, self.degree3, self.degree4, self.degree5,
                            self.degree6, self.degree7, self.degree8, self.degree9, self.degree10,
                            self.degree11, self.degree12]:
            for degree in degree_list:
                if degree in self.degree_count:
                    self.degree_count[degree] += 1
                else:
                    self.degree_count[degree] = 1
        return self.degree_count

    def drop_least_occurrences(self):
        if self.degree_count:
            min_occurrences = min(self.degree_count.values())
            for degree_attr in [self.degree1, self.degree2, self.degree3, self.degree4, self.degree5,
                                self.degree6, self.degree7, self.degree8, self.degree9, self.degree10,
                                self.degree11, self.degree12]:
                for degree in degree_attr[:]:
                    if self.degree_count[degree] == min_occurrences:
                        degree_attr.remove(degree)


class Room:
    def __init__(self, room_name, room_strength):
        self.room_name = room_name
        self.room_strength = room_strength
        self.schedule = self.generate_weekly_schedule()
        

    def generate_weekly_schedule(self):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        schedule = {day: self.generate_daily_schedule() for day in days}
        return schedule

    def generate_daily_schedule(self):
        start_time = timedelta(hours=8)
        end_time = timedelta(hours=18)
        interval = timedelta(hours=1)  
        current_time = start_time
        daily_schedule = []
        while current_time < end_time:
            daily_schedule.append(str(current_time))
            current_time += interval
        return daily_schedule

    def display_room_schedule(self):
        print("Room Name:", self.room_name)
        print("Room Strength:", self.room_strength)
        for day, schedule in self.schedule.items():
            print(day)
            for slot in schedule:
                print(slot)
            print()




class Lab:
    def __init__(self, room_name, room_strength):
        self.room_name = room_name
        self.room_strength = room_strength
        self.schedule = self.generate_weekly_schedule()
        

    def generate_weekly_schedule(self):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        schedule = {day: self.generate_daily_schedule() for day in days}
        return schedule

    def generate_daily_schedule(self):
        start_time = timedelta(hours=9)
        end_time = timedelta(hours=18)
        interval = timedelta(hours=2)  
        current_time = start_time
        daily_schedule = []
        while current_time < end_time:
            daily_schedule.append(str(current_time))
            current_time += interval
        return daily_schedule

    def display_room_schedule(self):
        print("Room Name:", self.room_name)
        print("Room Strength:", self.room_strength)
        for day, schedule in self.schedule.items():
            print(day)
            for slot in schedule:
                print(slot)
            print()
    # room1.display_room_schedule()
# room1.schedule['Monday'][room1.schedule['Monday'].index('17:00:00')]="ABC"
# print(room1.schedule['Monday'][room1.schedule['Monday'].index('ABC')])

