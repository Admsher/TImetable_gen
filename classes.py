import datetime
from datetime import timedelta

class Course:
    def __init__(self, course_name, class_frequency, class_timings, class_numbers, 
                 course_strength, tut_timings, tut_numbers, 
                 degree1, degree2, degree3, degree4, degree5,
                 degree6, degree7, degree8, degree9, degree10,
                 prereq, lab_timings, lab_numbers):
        self.course_name = course_name
        self.class_frequency = class_frequency
        self.class_timings = class_timings
        self.class_numbers = class_numbers
        self.course_strength = course_strength
        self.tut_timings = tut_timings
        self.tut_numbers = tut_numbers
        
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
        self.prereq = prereq
        self.lab_timings = lab_timings
        self.lab_numbers = lab_numbers

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

if __name__ == "__main__":
    room1 = Room("Room A", 50)
    # room1.display_room_schedule()
# room1.schedule['Monday'][room1.schedule['Monday'].index('17:00:00')]="ABC"
# print(room1.schedule['Monday'][room1.schedule['Monday'].index('ABC')])

