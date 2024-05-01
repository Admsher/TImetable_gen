from classes import Course,Room
import random
from datetime import datetime, timedelta
import numpy as np

def generate_random_degrees():
    return random.sample(range(1, 6), random.randint(0, 5))
instances = []
allocated_degrees = {}

for i in range(10):
    course = Course(
        course_name=f"Course {i+1}",
        class_frequency=3,
        class_timings=[],  
        class_numbers=random.randint(1,3),  
        course_strength=50,
        tut_timings=[],  
        tut_numbers=random.randint(1,3), 
        degree1=generate_random_degrees(),  
        degree2=generate_random_degrees(),  
        degree3=generate_random_degrees(),  
        degree4=generate_random_degrees(),  
        degree5=generate_random_degrees(),  
        degree6=generate_random_degrees(),  
        degree7=generate_random_degrees(),  
        degree8=generate_random_degrees(),  
        degree9=generate_random_degrees(),  
        degree10=generate_random_degrees(),  
        prereq=" ",
        lab_timings=random.randint(1,12),  
        lab_numbers=[301, 302]  
    )
    instances.append(course)


room1 = Room("Room 1", 30)
room2 = Room("Room 2", 55)
room3 = Room("Room 3", 120)
room4 = Room("Room 4", 135)
room5 = Room("Room 5", 100)
rooms=[room1,room2,room3,room4,room5]



def allot_room(instance,timing,weekday,room_list,sections):
    classes_alloted=0
    rooms_allotement=[]
    students_per_room=int(instance.course_strength/sections)

    for room in room_list:
        # print(timing)
        if room.room_strength>students_per_room:
            try:
                time_index=room.schedule[weekday].index(timing)
                
                if str(room.schedule[weekday][(time_index)])==timing:
                    # print("slot found")
                    room.schedule[weekday][time_index]=instance.course_name
                    # print(room.schedule[weekday][time_index])
                    classes_alloted=classes_alloted+1
                    rooms_allotement.append(room)
            except ValueError:
                continue
    
    if classes_alloted==instance.class_numbers:
        # print("CLasses alloted succesfully")
        return True
    else:
        for rooms in rooms_allotement:
            rooms.schedule['Monday'][(time_index)]=timing
        return False    




def compare_courses(course, courses_in_slot):
    # Extract degree arrays of the course being allotted
    course_degrees = [getattr(course, f"degree{i}") for i in range(1, 11) if getattr(course, f"degree{i}")]
    
    for course_in_slot in courses_in_slot:
        # Extract degree arrays of the course in the time slot
        course_in_slot_degrees = [getattr(course_in_slot, f"degree{i}") for i in range(1, 11) if getattr(course_in_slot, f"degree{i}")]
        
        # Check if there are any common degree numbers between the two courses
        for degree_list1 in course_degrees:
            for degree_list2 in course_in_slot_degrees:
                if set(degree_list1) & set(degree_list2):
                    return True  # Common degrees found, there's a clash
    
    return False  # No common degrees found, no clas


def generate_time_slots():
    start_time = datetime.strptime("08:00:00", "%H:%M:%S")
    end_time = datetime.strptime("17:00:00", "%H:%M:%S")
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    time_slots = {}

    for weekday in weekdays:
        current_time = start_time
        slots = []
        while current_time < end_time:
            slots.append({
                "start_time": current_time.strftime('%H:%M:%S'),
                "end_time": (current_time + timedelta(hours=1)).strftime('%H:%M:%S'),
                "courses": []
            })
            
            current_time += timedelta(hours=1)
        time_slots[weekday] = slots
        
    return time_slots
time_slots=generate_time_slots()
def allot_tut_timings(instances):
    
    for weekday, slots in time_slots.items():
        first_slot = slots[0]
        last_slot = slots[-1]
        for i in instances:
            
            if not i.tut_timings:
                # print("empty")
                if not compare_courses(i,first_slot["courses"]):
                 if allot_room(instance=i,weekday=weekday,timing=first_slot["start_time"],room_list=rooms,sections=i.tut_numbers):
                    i.tut_timings=first_slot
                    first_slot["courses"].append(i)
                    # print(i.course_name," ",weekday," ",first_slot)
                elif not compare_courses(i,last_slot["courses"]):
                  if allot_room(instance=i,weekday=weekday,timing=last_slot["start_time"],room_list=rooms,sections=i.tut_numbers):
                    i.tut_timings=last_slot
                    last_slot["courses"].append(i)
                    # print(i.course_name," ",weekday," ",last_slot)
                else:
                    continue
                    
def allot_class_timings(weekday,instances,instance_number,slots_alloted):
        prev_slots=slots_alloted
        i=instances[instance_number]
        for slot in time_slots[weekday]:
                # print(weekday)
                if not compare_courses(i,slot["courses"]):
                    if allot_room(instance=i,weekday=weekday,timing=slot["start_time"],room_list=rooms,sections=i.class_numbers):
                        i.class_timings.append([weekday,slot])
                        slots_alloted=slots_alloted+1
                        slot["courses"].append(i)

                        # print(i.course_name," ",i.class_timings)
                        if weekday=="Monday":
                            weekday="Wednesday"
                        elif weekday=="Tuesday":
                            weekday="Thursday"
                        else:
                            weekday="Friday"
                        break
                else:
                    continue
        if prev_slots-slots_alloted==0:
            if weekday=="Monday":
                weekday="Tuesday"

        

        if slots_alloted==i.class_frequency:
            instance_number=instance_number+1
            if instance_number< len(instances):
                allot_class_timings(weekday="Monday",instances=instances,instance_number=instance_number,slots_alloted=0)
            else:
                return
        else:
            try:
                allot_class_timings(weekday=weekday,instances=instances,instance_number=instance_number,slots_alloted=slots_alloted)
            except RecursionError:
                instance_number=instance_number+1
                if instance_number< len(instances):
                    allot_class_timings(weekday="Monday",instances=instances,instance_number=instance_number,slots_alloted=0)
                

               
    
                




allot_tut_timings(instances=instances)
allot_class_timings(weekday="Monday",instances=instances,instance_number=1,slots_alloted=0)
for room in rooms:
    print(room.schedule)