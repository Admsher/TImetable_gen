import pandas as pd


class CourseScheduler:
    def __init__(self):
        self.workbook = pd.ExcelWriter("course_schedule.xlsx", engine='xlsxwriter' )

    def create_room_sheet(self, room):
        df = pd.DataFrame.from_dict(room.schedule)
        df.to_excel(self.workbook, sheet_name=room.room_name)

    def create_lab_sheet(self, lab):
        df = pd.DataFrame.from_dict(lab.schedule)
        df.to_excel(self.workbook, sheet_name=lab.room_name)

    def create_course_sheet(self, instances):
        df = pd.DataFrame([
            [
                instance.course_name, instance.class_frequency,
                instance.class_timings, instance.class_numbers,
                instance.course_strength, instance.tut_timings,
                instance.tut_numbers, instance.degree1,
                instance.degree2, instance.degree3,
                instance.degree4, instance.degree5,
                instance.degree6, instance.degree7,
                instance.degree8, instance.degree9,
                instance.degree10,instance.degree11,instance.degree12, instance.prereq,
                instance.lab_timings, instance.lab_numbers,
                ','.join(instance.lab_rooms), ','.join(instance.class_rooms),
                ','.join(instance.tut_rooms)
            ] for instance in instances
        ], columns=[
            "Course Name", "Class Frequency", "Class Timings", "Class Sections",
            "Course Strength", "Tut Timings", "Tut Sections", "CSIS", "ECE",
            "EE", "EIE", "MECH", "CHE", "ECO", "MATH",
            "PHY", "CHEM","BIO","HUM", "Prerequisite", "Lab Timings", "Lab Sections",
            "Lab Rooms", "Class Rooms", "Tut Rooms"
        ])
        df.to_excel(self.workbook, sheet_name="Courses", index=False)

    def save_workbook(self):
        self.workbook._save()