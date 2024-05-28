from flask import Flask, request, render_template, redirect, url_for, flash
from logic import allot_class_timings, allot_lab_timings, allot_tut_timings, lastcheck
from classes import Course, Room, Lab
from convert_to_excel import CourseScheduler
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = 'uploaded_file.xlsx'
        filepath = os.path.join(app.root_path, filename)
        file.save(filepath)
        process_excel_file(filepath)
        flash('File successfully processed and output saved as output.xlsx')
        return redirect(url_for('home'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xls', 'xlsx'}

def process_excel_file(filepath):
    processing_file_course = pd.read_excel(io=filepath, sheet_name='Course')
    processing_file_venue = pd.read_excel(io=filepath, sheet_name='Venue')
    
    course_instances = []
    room_instances = []
    lab_instances = []
    
    for index, row in processing_file_course.iterrows():
        course_name = row[0]
        class_frequency = row[1]
        class_timings = []
        class_numbers = row[3]
        course_strength = row[4]
        tut_timings = []
        tut_numbers = row[6]
        degrees = [row[i].split(',') if row[i] else [] for i in range(7, 19)]
        prereq = row[19]
        lab_timings = []
        lab_numbers = row[21]
        lab_rooms = row[22]
        class_rooms = row[23]
        tut_rooms = row[24]
        faculties = row[25].split(',') if row[25] else []
        course_instance = Course(course_name, class_frequency, class_timings, class_numbers, 
                                 course_strength, tut_timings, tut_numbers, 
                                 *degrees, prereq, lab_timings, lab_numbers, 
                                 class_rooms, tut_rooms, lab_rooms, faculties)
        course_instances.append(course_instance)
    
    for index, row in processing_file_venue.iterrows():
        venue_name = row[0]
        venue_strength = row[1]
        venue_type = row[2]
        if venue_type == "Room":
            room_instance = Room(venue_name, venue_strength)
            room_instances.append(room_instance)
        elif venue_type == "Lab":
            lab_instance = Lab(venue_name, venue_strength)
            lab_instances.append(lab_instance)
    
    allot_tut_timings(instances=course_instances, rooms=room_instances)
    allot_class_timings(weekday="Monday", instances=course_instances, instance_number=0, slots_alloted=0, rooms=room_instances)
    allot_lab_timings(instances=course_instances, lab_list=lab_instances)
    lastcheck(instances=course_instances, checks_done=0, rooms=room_instances)
    
    scheduler = CourseScheduler()
    for room in room_instances:
        scheduler.create_room_sheet(room)
    for lab in lab_instances:
        scheduler.create_lab_sheet(lab)
    scheduler.create_course_sheet(course_instances)
    scheduler.save_workbook(filepath="output.xlsx")

if __name__ == '__main__':
    app.run(debug=True)
