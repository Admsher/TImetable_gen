from classes import Course,Room,Lab
import random
from datetime import datetime, timedelta
import numpy as np
from convert_to_excel import CourseScheduler


##put cdc's first in the list and then the electives to make sure cdc's get the prority while allotment
##there might be courses which might not get alloted any room/timing, please check manually for the same

# def generate_random_degrees():
#     return random.sample(range(1, 6), random.randint(0, 5))
# instances = []
# allocated_degrees = {}

# for i in range(10):
#     course = Course(
#         course_name=f"Course {i+1}",
#         class_frequency=3,
#         class_timings=[],  
#         class_numbers=random.randint(1,3),  
#         course_strength=50,
#         tut_timings=[],  
#         tut_numbers=random.randint(1,3), 
#         degree1=generate_random_degrees(),  
#         degree2=generate_random_degrees(),  
#         degree3=generate_random_degrees(),  
#         degree4=generate_random_degrees(),  
#         degree5=generate_random_degrees(),  
#         degree6=generate_random_degrees(),  
#         degree7=generate_random_degrees(),  
#         degree8=generate_random_degrees(),  
#         degree9=generate_random_degrees(),  
#         degree10=generate_random_degrees(),  
#         degree11=generate_random_degrees(),  
#         degree12=generate_random_degrees(),  
#         prereq=" ",
#         lab_timings=[],  
#         lab_numbers=random.randint(0,4),
#         lab_rooms=['301','302'],
#         class_rooms=[],
#         tut_rooms=[]
#     )
#     instances.append(course)


# room1 = Room("Room 1", 30)
# room2 = Room("Room 2", 55)
# room3 = Room("Room 3", 120)
# room4 = Room("Room 4", 135)
# room5 = Room("Room 5", 100)
# room6 = Room("Room 6", 30)
# room7 = Room("Room 7", 55)
# room8 = Room("Room 8", 120)
# room9 = Room("Room 9", 135)
# room10 = Room("Room 10", 100)
# rooms=[room1,room2,room3,room4,room5,room6,room7,room8,room9,room10]


# lab1=Lab('301',100)
# lab2=Lab('302',100)
# lab_list=[lab1,lab2]



def allot_room(instance,timing,weekday,room_list,sections):
    classes_alloted=0
    rooms_allotement=[]
    # print(sections)
    students_per_room=int(instance.course_strength/sections)
    # print(timing)
    for room in room_list:
        # print(timing)
        if room.room_strength>students_per_room:
            
            # try:
                # print(timing)
                try:
                    time_index=room.schedule[weekday].index(str(timing))
                    # print(time_index,"l")
                except  ValueError:
                    try:
                        time_index=room.schedule[weekday].index(str(timing)[1:])
                        # print(time_index,"l")
                    except:
                        continue
                print(room.room_name,str(room.schedule[weekday][(time_index)]))
                if str(room.schedule[weekday][(time_index)])==str(timing) or str(room.schedule[weekday][(time_index)])==str(timing)[1:]:
                    # print(timing)
                    # print(instance.course_name,"slot found")
                    room.schedule[weekday][time_index]=instance.course_name
                    # print(room.schedule[weekday][time_index])
                    classes_alloted=classes_alloted+1
                    rooms_allotement.append(room)
                    print(classes_alloted,sections)
                    # instance.class_rooms.append(room.room_name)
                if classes_alloted==sections:
                        # print("OGTCHA")
                        break
            # except ValueError:
            #     continue
    print(classes_alloted,sections,instance.course_name)
    if classes_alloted>=sections:
        print("Classes alloted succesfully",instance.course_name)
        return True
    else:
       
        for rooms in rooms_allotement:
            rooms.schedule[weekday][(time_index)]=str(timing)
        # instance.class_rooms=[]
        return False    
    
def allot_room_lab(instance,timing,weekday,room_list,sections,lab_list):
    classes_alloted=0
    rooms_allotement=[]
    room_list_fitered=[]
    # print(sections)
    for lab_ in room_list:
        # print(lab_)
        for lab in lab_list:
            # print(lab)
            if lab_==lab.room_name:
                # print("here")
                room_list_fitered.append(lab)
    # students_per_room=int(instance.course_strength/sections)
    # print(instance.course_name,sections)

    for room in room_list_fitered:
        # print(room)
        # if room.room_strength>students_per_room:
            
            # try:
                # print(timing)
                try:
                    time_index=room.schedule[weekday].index(str(timing["start_time"]))
                # print(time_index)
                except  ValueError:
                    try:
                        time_index=room.schedule[weekday].index(str(timing["start_time"])[1:])
                    except ValueError:
                        continue

                # print(time_index)

                # print(str(room.schedule[weekday][(time_index)]))
                if str(room.schedule[weekday][(time_index)])==str(timing["start_time"]):
                    # print("HERE")
                    # print(timing)
                    # print("slot found")
                    room.schedule[weekday][time_index]=instance.course_name
                    # print(room.schedule[weekday][time_index])
                    classes_alloted=classes_alloted+1
                    rooms_allotement.append(room)
                    # instance.class_rooms.append(room.room_name)
                    if classes_alloted==sections:
                        # print("All alloted")
                        # print(instance.course_name,"func")
                        
                        break
            # except ValueError:
            #     continue
    
   
    lab_remaining=instance.lab_numbers-classes_alloted
    # if lab_remaining==instance.lab_numbers:
    #     print("NO slotsfound")

    # print(instance.course_name,lab_remaining,"func")
    return lab_remaining
  




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
    
    return False  # No common degrees found, no class


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
def generate_time_slots_2():
    start_time = datetime.strptime("09:00:00", "%H:%M:%S")
    end_time = datetime.strptime("17:00:00", "%H:%M:%S")
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    time_slots = {}

    for weekday in weekdays:
        current_time = start_time
        slots = []
        while current_time < end_time:
            slots.append({
                "start_time": current_time.strftime('%H:%M:%S'),
                "end_time": (current_time + timedelta(hours=2)).strftime('%H:%M:%S'),
                "courses": []
            })
            
            current_time += timedelta(hours=2)
        time_slots[weekday] = slots
        
    return time_slots
time_slots=generate_time_slots()
alloted_tut_array=[]
def allot_tut_timings(instances,rooms):
    # print("WIP")
    
    for weekday, slots in time_slots.items():
        first_slot = slots[0]
        # print(first_slot)
        last_slot = slots[-1]
        for i in instances:
            alloted=False
            # print(i.course_name,i.tut_numbers)
            if not i.tut_timings:
                # print("HERE")
                # print(i.course_name,i.tut_timings)
                if not compare_courses(i,first_slot["courses"]):
                    # print(allot_room(instance=i,weekday=weekday,timing=first_slot["start_time"],room_list=rooms,sections=i.tut_numbers))
                    # print(first_slot)
                    if allot_room(instance=i,weekday=weekday,timing=first_slot["start_time"],room_list=rooms,sections=i.tut_numbers): 
                        # print(i.course_name,"LOL")
                        i.tut_timings=first_slot
                        # print(i.tut_timings)
                        first_slot["courses"].append(i)
                        alloted=True
                    
                    # print(i.course_name," ",weekday," ",first_slot)
                elif not  compare_courses(i,last_slot["courses"]) or alloted==False:
                    # print(last_slot)
                    if  allot_room(instance=i,weekday=weekday,timing=last_slot["start_time"],room_list=rooms,sections=i.tut_numbers):
                        i.tut_timings=last_slot
                        last_slot["courses"].append(i)
                        


     
def allot_class_timings(weekday,instances,instance_number,slots_alloted,rooms):
      
        prev_slots=slots_alloted
        i=instances[instance_number]
        temp_time_slots = {day: slots[:] for day, slots in time_slots.items()}
        
        if  len(i.class_timings)<i.class_frequency:
            for day in temp_time_slots:
                    if len(temp_time_slots[day]) > 0:
                        temp_time_slots[day].pop(0)  # Remove the first slot
                        temp_time_slots[day].pop(-1)
                
            
            for slot in temp_time_slots[weekday]:
                        # print(weekday)
                        if not compare_courses(i,slot["courses"]):
                            if  allot_room(instance=i,weekday=weekday,timing=slot["start_time"],room_list=rooms,sections=i.class_numbers):
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
                    
                    if i.prereq:
                        for j in instances:
                            if j.course_name==i.prereq:
                                
                                j.class_timings=i.class_timings
                                # print(i.class_timings)
                                # total_runtime=int(len(j.class_numbers))/2
                                # print("TR",total_runtime)
                                j_ran=0
                                for timing in j.class_timings:
                                    print(timing)
                                    weekday=timing[0]
                                    slot=timing[1]
                                    allot_room(instance=j,weekday=weekday,timing=slot["start_time"],room_list=rooms,sections=j.class_numbers)
                                    j_ran=j_ran+1
                                    print(j_ran)
                                    # if j_ran==total_runtime:
                                    #      print("Breaking")
                                    #      break
                    instance_number=instance_number+1
                    
                    
            else:
                    try:
                        allot_class_timings(weekday=weekday,instances=instances,instance_number=instance_number,slots_alloted=slots_alloted,rooms=rooms)
                    except RecursionError:
                         
                     instance_number=instance_number+1
        
        else:
             instance_number=instance_number+1
        
        if instance_number< len(instances):
                            allot_class_timings(weekday="Monday",instances=instances,instance_number=instance_number,slots_alloted=0,rooms=rooms)         
        else:
             return      
        
       

                
def allot_lab_timings(instances,lab_list):
    
    time_slots=generate_time_slots_2()
    slot_list=[]
    
    for instance in instances:
            final_lab=instance.lab_numbers
            # print(instance.course_name,final_lab)
            room=instance.lab_rooms
            for weekday,slots in time_slots.items():
                flag=False
                slot3=slots[2]
                slot2=slots[3]
                # slot_list.append(slot1)
                slot_list.append(slot2)
                slot_list.append(slot3)
                if instance.lab_numbers==0:
                    
                    break
                for i in  slot_list:
                    # print(instance.course_name,instance.lab_numbers)
                    instance.lab_numbers= allot_room_lab(instance=instance,weekday=weekday,timing=i,room_list=room,sections=instance.lab_numbers,lab_list=lab_list)
                    # print(instance.course_name,instance.lab_numbers)
                    # print(instance.lab_timings)
                    if instance.lab_numbers==0:
                        flag=True
                        
                        break
                if flag==True:
                    instance.lab_numbers=final_lab
                    break


checks_done=0
def lastcheck(instances,checks_done,rooms):
    if checks_done>=1:
        return
    class_empty=[]
    tut_empty=[]
    insatnce_overall_empty=[]
    for i in instances:
        if i.class_timings == [] or i.tut_timings==[]:
            i.count_degree_occurrences()
            i.drop_least_occurrences()

        if i.class_timings==[]:
            class_empty.append(i)
        if class_empty!=[]:
            allot_class_timings(weekday="Monday",instances=class_empty,instance_number=0,slots_alloted=0,rooms=rooms)
        if i.tut_timings==[]:
            tut_empty.append(i)
        if tut_empty!=[]:    
            print("HERE")
            allot_tut_timings(instances=tut_empty,rooms=rooms)
    for i in instances:
        if i.class_timings == [] or i.tut_timings==[]:
            print(i.course_name,i.tut_timings,i.class_timings)
            insatnce_overall_empty.append(i)
            
    if insatnce_overall_empty!=[]:
            # print("YES")
            try:
                checks_done=checks_done+1
                lastcheck(instances=insatnce_overall_empty,checks_done=checks_done,rooms=rooms)
            except RecursionError:
                # print("MRP")
                
        
                return

               
    
                

