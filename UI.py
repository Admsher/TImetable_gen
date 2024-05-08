import tkinter as tk
from tkinter import filedialog, messagebox
from logic import allot_class_timings,allot_lab_timings,allot_tut_timings,lastcheck
from classes import Course,Room,Lab
from convert_to_excel import CourseScheduler
import pandas as pd

def process_excel_file():
    # Open file dialog to select Excel file
    filepath = filedialog.askopenfilename()
    
    if filepath:
        # Call function from logic.py to process the Excel file
        # output_data = logic.process_excel(filepath)
        processing_file_course=pd.read_excel(io=filepath,sheet_name='Course')
        processing_file_venue=pd.read_excel(io=filepath,sheet_name='Venue')
      
        course_instances = []
        room_instances=[]
        lab_instances=[]
        for index,row in processing_file_course.iterrows():
            print(row)
            course_name = row[0]
            class_frequency = row[1]
            class_timings = []
            class_numbers = row[3]
            course_strength = row[4]
            tut_timings = []
            tut_numbers = row[6]
            degree1 = row[7].split(',') if row[7] else []
            degree2 = row[8].split(',') if row[8] else []
            degree3 = row[9].split(',') if row[9] else []
            degree4 = row[10].split(',') if row[10] else []
            degree5 = row[11].split(',') if row[11] else []
            degree6 = row[12].split(',') if row[12] else []
            degree7 = row[13].split(',') if row[13] else []
            degree8 = row[14].split(',') if row[14] else []
            degree9 = row[15].split(',') if row[15] else []
            degree10 = row[16].split(',') if row[16] else []
            degree11 = row[17].split(',') if row[17] else []
            degree12 = row[18].split(',') if row[18] else []
            prereq = row[19]
            lab_timings = []
            lab_numbers = row[21]
            lab_rooms = row[22]
            class_rooms = row[23]
            tut_rooms = row[24]
            course_instance = Course(course_name, class_frequency, class_timings, class_numbers, 
                             course_strength, tut_timings, tut_numbers, 
                             degree1, degree2, degree3, degree4, degree5,
                             degree6, degree7, degree8, degree9, degree10,degree11,degree12,
                             prereq, lab_timings, lab_numbers,class_rooms,tut_rooms,lab_rooms)
    
            # Append the course instance to the list of course instances
            course_instances.append(course_instance)
        for index,row in processing_file_venue.iterrows():
            venue_name = row[0]
            venue_strength= row[1]
            venue_type= row[2]

            if venue_type=="Room":
                room_instance=Room(venue_name,venue_strength)
                room_instances.append(room_instance)
            elif venue_type=="Lab":
                lab_instance=Lab(venue_name,venue_strength)
                lab_instances.append(lab_instance)
        allot_tut_timings(instances=course_instances,rooms=room_instances)
        allot_class_timings(weekday="Monday",instances=course_instances,instance_number=0,slots_alloted=0,rooms=room_instances)
        allot_lab_timings(instances=course_instances,lab_list=lab_instances)
        lastcheck(instances=course_instances,checks_done=0,rooms=room_instances)
        scheduler = CourseScheduler()

# Create sheets for rooms
        for room in room_instances:
            scheduler.create_room_sheet(room)

# Create sheets for labs
        for lab in lab_instances:
            scheduler.create_lab_sheet(lab)

# Create sheet for courses
        scheduler.create_course_sheet(course_instances)

# Save the workbook
        scheduler.save_workbook()

              
        # Save the output to a new Excel file
        output_filepath = "output.xlsx"
        # logic.save_excel(output_data, output_filepath)
        messagebox.showinfo("Success", "Output file saved as 'output.xlsx'")
        
def show_excel_preview():
    # Open file dialog to select Excel file
    filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    
    if filepath:
        # Read Excel file to display preview
        with open(filepath, 'r') as file:
            preview_text.delete(1.0, tk.END)
            preview_text.insert(tk.END, file.read())

# Create GUI window
root = tk.Tk()
root.title("Course Scheduler")  # Set window title
root.configure(bg='#1E90FF')  # Set background color
root.geometry("600x400")  # Set window size

# Create button to select Excel file for processing
process_button = tk.Button(root, text="Process Excel File", command=process_excel_file, bg='#FF6347', fg='white')
process_button.pack(pady=10)

# Create button to select Excel file for preview
preview_button = tk.Button(root, text="Preview Excel File", command=show_excel_preview, bg='#e1caad', fg='black')
preview_button.pack(pady=10)

# Create text widget for displaying Excel preview
preview_text = tk.Text(root, wrap="word", height=15, width=50)
preview_text.pack(pady=10)

root.mainloop()
