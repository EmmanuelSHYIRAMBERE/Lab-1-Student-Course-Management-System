#!/usr/bin/env python3
"""
Student Course Management System
Main entry point for the console application.
"""

import sys
from typing import Dict, List, Optional
from colorama import Fore, Style, init

from src.models.student import Student, UndergraduateStudent, GraduateStudent, InternationalStudent
from src.models.course import Course
from src.utils.helpers import create_menu, get_user_input, validate_email
from src.reports.report_generator import StudentReport, CourseReport, EnrollmentReport

# Initialize colorama
init(autoreset=True)

class StudentCourseManagementSystem:
    """Main application class."""
    
    def __init__(self):
        self.students: Dict[str, Student] = {}
        self.courses: Dict[str, Course] = {}
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample data for testing."""
        # Add sample students
        student1 = UndergraduateStudent("S001", "Alice Johnson", "alice@example.com", 2)
        student2 = GraduateStudent("S002", "Bob Smith", "bob@example.com", "Machine Learning")
        student3 = InternationalStudent("S003", "Carlos Rodriguez", "carlos@example.com", "Spain", 3)
        
        self.students = {
            "S001": student1,
            "S002": student2,
            "S003": student3
        }
        
        # Add sample courses
        course1 = Course("CS101", "Introduction to Programming", 3, "Dr. Williams", 30)
        course1.set_schedule("Monday", "10:00-12:00")
        course1.set_schedule("Wednesday", "10:00-12:00")
        
        course2 = Course("CS201", "Data Structures", 4, "Dr. Garcia", 25)
        course2.set_schedule("Tuesday", "14:00-16:00")
        course2.set_schedule("Thursday", "14:00-16:00")
        
        course3 = Course("MATH101", "Calculus I", 4, "Prof. Miller", 35)
        course3.set_schedule("Monday", "13:00-15:00")
        course3.set_schedule("Wednesday", "13:00-15:00")
        
        self.courses = {
            "CS101": course1,
            "CS201": course2,
            "MATH101": course3
        }
        
        # Enroll some students
        course1.add_student(student1)
        course1.add_student(student3)
        course2.add_student(student2)
        course3.add_student(student1)
        
        # Add some grades
        student1.add_grade("CS101", 3.7)
        student1.add_grade("MATH101", 3.3)
        student2.add_grade("CS201", 4.0)
    
    def run(self):
        """Main application loop."""
        while True:
            self._clear_screen()

            print(Fore.YELLOW + "="*60)
            print("Welcome to the Student Course Management System")
            print("="*60 + Style.RESET_ALL)
            
            options = [
                "Student Management",
                "Course Management",
                "Enrollment Management",
                "Generate Reports",
                "View Statistics"
            ]
            
            create_menu(options)
            
            choice = get_user_input("Enter your choice: ", 
                                   lambda x: x.isdigit() and 0 <= int(x) <= len(options))
            
            choice = int(choice)
            
            if choice == 0:
                print(Fore.GREEN + "\nThank you for using the system. Goodbye!")
                break
            elif choice == 1:
                self._student_management_menu()
            elif choice == 2:
                self._course_management_menu()
            elif choice == 3:
                self._enrollment_management_menu()
            elif choice == 4:
                self._reports_menu()
            elif choice == 5:
                self._view_statistics()
    
    def _student_management_menu(self):
        """Student management submenu."""
        while True:
            self._clear_screen()
            print(Fore.CYAN + "\n📋 STUDENT MANAGEMENT")
            print("="*40)
            
            options = [
                "Add Undergraduate Student",
                "Add Graduate Student",
                "Add International Student",
                "View All Students",
                "View Student Details",
                "Update Student Info",
                "Back to Main Menu"
            ]
            
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")
            print("0. Back")
            
            choice = get_user_input("Enter your choice: ",
                                   lambda x: x.isdigit() and 0 <= int(x) <= len(options))
            choice = int(choice)
            
            if choice == 0:
                break
            elif choice == 1:
                self._add_undergraduate_student()
            elif choice == 2:
                self._add_graduate_student()
            elif choice == 3:
                self._add_international_student()
            elif choice == 4:
                self._view_all_students()
            elif choice == 5:
                self._view_student_details()
            elif choice == 6:
                self._update_student_info()
            
            input("\nPress Enter to continue...")
    
    def _add_undergraduate_student(self):
        """Add a new undergraduate student."""
        print(Fore.CYAN + "\n➕ ADD UNDERGRADUATE STUDENT")
        print("-"*30)
        
        student_id = get_user_input("Student ID: ", 
                                   lambda x: x not in self.students,
                                   "Student ID already exists!")
        
        name = get_user_input("Full Name: ",
                            lambda x: len(x.strip()) >= 2,
                            "Name must be at least 2 characters!")
        
        email = get_user_input("Email: ",
                             validate_email,
                             "Invalid email format!")
        
        year = int(get_user_input("Year (1-4): ",
                                lambda x: x.isdigit() and 1 <= int(x) <= 4,
                                "Year must be between 1 and 4!"))
        
        student = UndergraduateStudent(student_id, name, email, year)
        self.students[student_id] = student
        print(Fore.GREEN + f"✅ Undergraduate student {name} added successfully!")
    
    def _add_graduate_student(self):
        """Add a new graduate student."""
        print(Fore.CYAN + "\n➕ ADD GRADUATE STUDENT")
        print("-"*30)
        
        student_id = get_user_input("Student ID: ",
                                   lambda x: x not in self.students,
                                   "Student ID already exists!")
        
        name = get_user_input("Full Name: ",
                            lambda x: len(x.strip()) >= 2,
                            "Name must be at least 2 characters!")
        
        email = get_user_input("Email: ",
                             validate_email,
                             "Invalid email format!")
        
        research_topic = get_user_input("Research Topic (optional): ")
        
        student = GraduateStudent(student_id, name, email, research_topic)
        
        add_advisor = get_user_input("Add advisor? (y/n): ",
                                   lambda x: x.lower() in ['y', 'n'])
        if add_advisor.lower() == 'y':
            advisor = get_user_input("Advisor name: ")
            student.advisor = advisor
        
        self.students[student_id] = student
        print(Fore.GREEN + f"✅ Graduate student {name} added successfully!")
    
    def _add_international_student(self):
        """Add a new international student."""
        print(Fore.CYAN + "\n➕ ADD INTERNATIONAL STUDENT")
        print("-"*30)
        
        student_id = get_user_input("Student ID: ",
                                   lambda x: x not in self.students,
                                   "Student ID already exists!")
        
        name = get_user_input("Full Name: ",
                            lambda x: len(x.strip()) >= 2,
                            "Name must be at least 2 characters!")
        
        email = get_user_input("Email: ",
                             validate_email,
                             "Invalid email format!")
        
        country = get_user_input("Country of Origin: ",
                               lambda x: len(x.strip()) >= 2,
                               "Country name must be at least 2 characters!")
        
        year = int(get_user_input("Year (1-4): ",
                                lambda x: x.isdigit() and 1 <= int(x) <= 4,
                                "Year must be between 1 and 4!"))
        
        student = InternationalStudent(student_id, name, email, country, year)
        self.students[student_id] = student
        print(Fore.GREEN + f"✅ International student {name} from {country} added successfully!")
    
    def _view_all_students(self):
        """View all students."""
        if not self.students:
            print(Fore.YELLOW + "No students in the system.")
            return
        
        print(Fore.CYAN + "\n📋 ALL STUDENTS")
        print("-"*50)
        
        for student_id, student in sorted(self.students.items()):
            print(f"{student}")
            print(f"  📧 {student.email}")
            print(f"  📚 Courses: {len(student.get_enrolled_courses())}")
            print(f"  📊 GPA: {student.calculate_gpa():.2f}")
            print(f"  💰 Tuition: ${student.calculate_tuition():.2f}")
            print()
    
    def _view_student_details(self):
        """View detailed information about a specific student."""
        if not self.students:
            print(Fore.YELLOW + "No students in the system.")
            return
        
        print(Fore.CYAN + "\n🔍 STUDENT DETAILS")
        print("-"*30)
        
        # Show available students
        for student_id, student in self.students.items():
            print(f"{student_id}: {student.name}")
        
        student_id = get_user_input("\nEnter Student ID: ",
                                  lambda x: x in self.students,
                                  "Student not found!")
        
        student = self.students[student_id]
        
        print(Fore.CYAN + "\n" + "="*50)
        print(f"STUDENT DETAILS: {student.name}")
        print("="*50)
        print(f"ID: {student.student_id}")
        print(f"Type: {student.get_student_type()}")
        print(f"Email: {student.email}")
        print(f"Enrollment Date: {student.enrollment_date.strftime('%Y-%m-%d')}")
        print(f"GPA: {student.calculate_gpa():.2f}")
        print(f"Tuition: ${student.calculate_tuition():.2f}")
        
        # Show enrolled courses
        enrolled = student.get_enrolled_courses()
        if enrolled:
            print("\n📚 Enrolled Courses:")
            for course_code in enrolled:
                course = self.courses.get(course_code)
                if course:
                    print(f"  • {course.name} ({course_code})")
        else:
            print("\n📭 No courses enrolled")
    
    def _update_student_info(self):
        """Update student information."""
        if not self.students:
            print(Fore.YELLOW + "No students in the system.")
            return
        
        print(Fore.CYAN + "\n✏️ UPDATE STUDENT INFO")
        print("-"*30)
        
        student_id = get_user_input("Enter Student ID: ",
                                  lambda x: x in self.students,
                                  "Student not found!")
        
        student = self.students[student_id]
        
        print(f"Updating: {student.name}")
        
        # Update name
        new_name = get_user_input(f"New name (Enter to keep '{student.name}'): ")
        if new_name:
            student.name = new_name
        
        # Update email
        new_email = get_user_input(f"New email (Enter to keep '{student.email}'): ",
                                 lambda x: not x or validate_email(x),
                                 "Invalid email format!")
        if new_email:
            student.email = new_email
        
        print(Fore.GREEN + "✅ Student information updated successfully!")
    
    def _course_management_menu(self):
        """Course management submenu."""
        while True:
            self._clear_screen()
            print(Fore.CYAN + "\n📚 COURSE MANAGEMENT")
            print("="*40)
            
            options = [
                "Add New Course",
                "View All Courses",
                "View Course Details",
                "Update Course Info",
                "View Course Roster",
                "Back to Main Menu"
            ]
            
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")
            print("0. Back")
            
            choice = get_user_input("Enter your choice: ",
                                   lambda x: x.isdigit() and 0 <= int(x) <= len(options))
            choice = int(choice)
            
            if choice == 0:
                break
            elif choice == 1:
                self._add_course()
            elif choice == 2:
                self._view_all_courses()
            elif choice == 3:
                self._view_course_details()
            elif choice == 4:
                self._update_course_info()
            elif choice == 5:
                self._view_course_roster()
            
            input("\nPress Enter to continue...")
    
    def _add_course(self):
        """Add a new course."""
        print(Fore.CYAN + "\n➕ ADD NEW COURSE")
        print("-"*30)
        
        course_code = get_user_input("Course Code: ",
                                    lambda x: x not in self.courses,
                                    "Course code already exists!")
        
        name = get_user_input("Course Name: ",
                            lambda x: len(x.strip()) >= 3,
                            "Course name must be at least 3 characters!")
        
        credits = int(get_user_input("Credits (1-6): ",
                                   lambda x: x.isdigit() and 1 <= int(x) <= 6,
                                   "Credits must be between 1 and 6!"))
        
        instructor = get_user_input("Instructor Name: ",
                                  lambda x: len(x.strip()) >= 2,
                                  "Instructor name must be at least 2 characters!")
        
        max_students = int(get_user_input("Maximum Students (default 30): ") or "30")
        
        course = Course(course_code, name, credits, instructor, max_students)
        
        # Add schedule
        add_schedule = get_user_input("Add schedule? (y/n): ",
                                    lambda x: x.lower() in ['y', 'n'])
        if add_schedule.lower() == 'y':
            day = get_user_input("Day (e.g., Monday): ")
            time = get_user_input("Time (e.g., 10:00-12:00): ")
            course.set_schedule(day, time)
        
        self.courses[course_code] = course
        print(Fore.GREEN + f"✅ Course {name} added successfully!")
    
    def _view_all_courses(self):
        """View all courses."""
        if not self.courses:
            print(Fore.YELLOW + "No courses in the system.")
            return
        
        print(Fore.CYAN + "\n📚 ALL COURSES")
        print("-"*50)
        
        for course_code, course in sorted(self.courses.items()):
            summary = course.get_enrollment_summary()
            print(f"{course}")
            print(f"  👨‍🏫 Instructor: {course.instructor}")
            print(f"  📊 Enrollment: {summary['enrolled']}/{summary['capacity']}")
            print(f"  📅 Schedule: {course.get_schedule()}")
            print()
    
    def _view_course_details(self):
        """View detailed information about a specific course."""
        if not self.courses:
            print(Fore.YELLOW + "No courses in the system.")
            return
        
        print(Fore.CYAN + "\n🔍 COURSE DETAILS")
        print("-"*30)
        
        # Show available courses
        for course_code, course in self.courses.items():
            print(f"{course_code}: {course.name}")
        
        course_code = get_user_input("\nEnter Course Code: ",
                                   lambda x: x in self.courses,
                                   "Course not found!")
        
        course = self.courses[course_code]
        summary = course.get_enrollment_summary()
        
        print(Fore.CYAN + "\n" + "="*50)
        print(f"COURSE DETAILS: {course.name}")
        print("="*50)
        print(f"Code: {course.course_code}")
        print(f"Credits: {course.credits}")
        print(f"Instructor: {course.instructor}")
        print(f"Schedule: {course.get_schedule()}")
        print(f"Enrollment: {summary['enrolled']}/{summary['capacity']}")
        print(f"Available Seats: {summary['available']}")
        
        if summary['is_full']:
            print(Fore.YELLOW + "⚠️ Course is full!")
    
    def _update_course_info(self):
        """Update course information."""
        if not self.courses:
            print(Fore.YELLOW + "No courses in the system.")
            return
        
        print(Fore.CYAN + "\n✏️ UPDATE COURSE INFO")
        print("-"*30)
        
        course_code = get_user_input("Enter Course Code: ",
                                   lambda x: x in self.courses,
                                   "Course not found!")
        
        course = self.courses[course_code]
        
        print(f"Updating: {course.name}")
        
        # Update name
        new_name = get_user_input(f"New name (Enter to keep '{course.name}'): ")
        if new_name:
            course.name = new_name
        
        # Update instructor
        new_instructor = get_user_input(f"New instructor (Enter to keep '{course.instructor}'): ")
        if new_instructor:
            course.instructor = new_instructor
        
        print(Fore.GREEN + "✅ Course information updated successfully!")
    
    def _view_course_roster(self):
        """View the roster for a specific course."""
        if not self.courses:
            print(Fore.YELLOW + "No courses in the system.")
            return
        
        print(Fore.CYAN + "\n📋 COURSE ROSTER")
        print("-"*30)
        
        course_code = get_user_input("Enter Course Code: ",
                                   lambda x: x in self.courses,
                                   "Course not found!")
        
        course = self.courses[course_code]
        students = course.get_student_list()
        
        print(Fore.CYAN + f"\n📋 ROSTER: {course.name}")
        print("="*50)
        
        if not students:
            print(Fore.YELLOW + "No students enrolled in this course.")
            return
        
        print(f"Total Students: {len(students)}")
        print("-"*30)
        
        for i, student in enumerate(sorted(students, key=lambda s: s.name), 1):
            print(f"{i}. {student.name} ({student.student_id}) - {student.get_student_type()}")
    
    def _enrollment_management_menu(self):
        """Enrollment management submenu."""
        while True:
            self._clear_screen()
            print(Fore.CYAN + "\n📝 ENROLLMENT MANAGEMENT")
            print("="*40)
            
            options = [
                "Enroll Student in Course",
                "Drop Student from Course",
                "View Student Enrollments",
                "Add Grade for Student",
                "Back to Main Menu"
            ]
            
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")
            print("0. Back")
            
            choice = get_user_input("Enter your choice: ",
                                   lambda x: x.isdigit() and 0 <= int(x) <= len(options))
            choice = int(choice)
            
            if choice == 0:
                break
            elif choice == 1:
                self._enroll_student()
            elif choice == 2:
                self._drop_student()
            elif choice == 3:
                self._view_student_enrollments()
            elif choice == 4:
                self._add_grade()
            
            input("\nPress Enter to continue...")
    
    def _enroll_student(self):
        """Enroll a student in a course."""
        if not self.students or not self.courses:
            print(Fore.YELLOW + "Need both students and courses to enroll!")
            return
        
        print(Fore.CYAN + "\n📝 ENROLL STUDENT")
        print("-"*30)
        
        # Show available students
        print("\nAvailable Students:")
        for student_id, student in self.students.items():
            print(f"{student_id}: {student.name}")
        
        student_id = get_user_input("\nEnter Student ID: ",
                                  lambda x: x in self.students,
                                  "Student not found!")
        
        # Show available courses
        print("\nAvailable Courses:")
        for course_code, course in self.courses.items():
            if not course.is_full:
                summary = course.get_enrollment_summary()
                print(f"{course_code}: {course.name} ({summary['available']} seats available)")
        
        course_code = get_user_input("\nEnter Course Code: ",
                                   lambda x: x in self.courses,
                                   "Course not found!")
        
        student = self.students[student_id]
        course = self.courses[course_code]
        
        if course.add_student(student):
            print(Fore.GREEN + f"✅ {student.name} enrolled in {course.name} successfully!")
        else:
            print(Fore.RED + "❌ Enrollment failed! Course might be full or already enrolled.")
    
    def _drop_student(self):
        """Drop a student from a course."""
        print(Fore.CYAN + "\n🗑️ DROP STUDENT FROM COURSE")
        print("-"*30)
        
        student_id = get_user_input("Enter Student ID: ",
                                  lambda x: x in self.students,
                                  "Student not found!")
        
        student = self.students[student_id]
        enrolled = student.get_enrolled_courses()
        
        if not enrolled:
            print(Fore.YELLOW + "Student is not enrolled in any courses.")
            return
        
        print(f"\n{student.name} is enrolled in:")
        for course_code in enrolled:
            course = self.courses.get(course_code)
            if course:
                print(f"  • {course_code}: {course.name}")
        
        course_code = get_user_input("\nEnter Course Code to drop: ",
                                   lambda x: x in enrolled,
                                   "Student not enrolled in this course!")
        
        course = self.courses[course_code]
        
        if course.remove_student(student):
            print(Fore.GREEN + f"✅ {student.name} dropped from {course.name} successfully!")
        else:
            print(Fore.RED + "❌ Failed to drop student from course.")
    
    def _view_student_enrollments(self):
        """View all enrollments for a specific student."""
        if not self.students:
            print(Fore.YELLOW + "No students in the system.")
            return
        
        print(Fore.CYAN + "\n🔍 VIEW STUDENT ENROLLMENTS")
        print("-"*30)
        
        student_id = get_user_input("Enter Student ID: ",
                                  lambda x: x in self.students,
                                  "Student not found!")
        
        student = self.students[student_id]
        enrolled = student.get_enrolled_courses()
        
        print(Fore.CYAN + f"\n📋 ENROLLMENTS: {student.name}")
        print("="*50)
        
        if not enrolled:
            print(Fore.YELLOW + "Student is not enrolled in any courses.")
            return
        
        for course_code in enrolled:
            course = self.courses.get(course_code)
            if course:
                print(f"• {course.name} ({course_code})")
                print(f"  Instructor: {course.instructor}")
                print(f"  Schedule: {course.get_schedule()}")
                print()
    
    def _add_grade(self):
        """Add a grade for a student in a course."""
        print(Fore.CYAN + "\n📊 ADD GRADE")
        print("-"*30)
        
        student_id = get_user_input("Enter Student ID: ",
                                  lambda x: x in self.students,
                                  "Student not found!")
        
        student = self.students[student_id]
        enrolled = student.get_enrolled_courses()
        
        if not enrolled:
            print(Fore.YELLOW + "Student is not enrolled in any courses.")
            return
        
        print(f"\n{student.name}'s enrolled courses:")
        for course_code in enrolled:
            course = self.courses.get(course_code)
            if course:
                print(f"  • {course_code}: {course.name}")
        
        course_code = get_user_input("\nEnter Course Code: ",
                                   lambda x: x in enrolled,
                                   "Student not enrolled in this course!")
        
        grade = float(get_user_input("Enter grade (0.0 - 4.0): ",
                                   lambda x: x.replace('.','').isdigit() and 0 <= float(x) <= 4,
                                   "Grade must be between 0.0 and 4.0!"))
        
        student.add_grade(course_code, grade)
        print(Fore.GREEN + f"✅ Grade {grade} added for {student.name} in {course_code}!")
    
    def _reports_menu(self):
        """Reports generation submenu."""
        while True:
            self._clear_screen()
            print(Fore.CYAN + "\n📊 REPORTS")
            print("="*40)
            
            options = [
                "Generate Student Report",
                "Generate Course Report",
                "Generate Enrollment Report",
                "Generate All Reports",
                "Back to Main Menu"
            ]
            
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")
            print("0. Back")
            
            choice = get_user_input("Enter your choice: ",
                                   lambda x: x.isdigit() and 0 <= int(x) <= len(options))
            choice = int(choice)
            
            if choice == 0:
                break
            elif choice == 1:
                self._generate_student_report()
            elif choice == 2:
                self._generate_course_report()
            elif choice == 3:
                self._generate_enrollment_report()
            elif choice == 4:
                self._generate_all_reports()
            
            input("\nPress Enter to continue...")
    
    def _generate_student_report(self):
        """Generate and display student report."""
        report = StudentReport(list(self.students.values()))
        print(report.generate())
        
        # Option to save to file
        save = get_user_input("\nSave report to file? (y/n): ",
                            lambda x: x.lower() in ['y', 'n'])
        if save.lower() == 'y':
            filename = f"student_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w') as f:
                f.write(report.generate())
            print(Fore.GREEN + f"✅ Report saved to {filename}")
    
    def _generate_course_report(self):
        """Generate and display course report."""
        report = CourseReport(list(self.courses.values()))
        print(report.generate())
        
        # Option to save to file
        save = get_user_input("\nSave report to file? (y/n): ",
                            lambda x: x.lower() in ['y', 'n'])
        if save.lower() == 'y':
            filename = f"course_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w') as f:
                f.write(report.generate())
            print(Fore.GREEN + f"✅ Report saved to {filename}")
    
    def _generate_enrollment_report(self):
        """Generate and display enrollment report."""
        report = EnrollmentReport(list(self.students.values()), 
                                 list(self.courses.values()))
        print(report.generate())
        
        # Option to save to file
        save = get_user_input("\nSave report to file? (y/n): ",
                            lambda x: x.lower() in ['y', 'n'])
        if save.lower() == 'y':
            filename = f"enrollment_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w') as f:
                f.write(report.generate())
            print(Fore.GREEN + f"✅ Report saved to {filename}")
    
    def _generate_all_reports(self):
        """Generate all reports."""
        self._generate_student_report()
        print("\n" + "="*50)
        self._generate_course_report()
        print("\n" + "="*50)
        self._generate_enrollment_report()
    
    def _view_statistics(self):
        """View system statistics."""
        print(Fore.CYAN + "\n📊 SYSTEM STATISTICS")
        print("="*50)
        
        total_students = len(self.students)
        total_courses = len(self.courses)
        
        # Enrollment statistics
        total_enrollments = sum(len(s.get_enrolled_courses()) for s in self.students.values())
        avg_courses_per_student = total_enrollments / total_students if total_students else 0
        
        # Course capacity statistics
        total_capacity = sum(c._max_students for c in self.courses.values())
        total_enrolled_in_courses = sum(c.current_enrollment for c in self.courses.values())
        avg_course_utilization = (total_enrolled_in_courses / total_capacity * 100) if total_capacity else 0
        
        # Student type breakdown
        student_types = {}
        for student in self.students.values():
            s_type = student.__class__.__name__
            student_types[s_type] = student_types.get(s_type, 0) + 1
        
        print(f"👥 Total Students: {total_students}")
        print(f"📚 Total Courses: {total_courses}")
        print(f"📝 Total Enrollments: {total_enrollments}")
        print(f"📊 Avg Courses per Student: {avg_courses_per_student:.2f}")
        print(f"📈 Course Capacity Utilization: {avg_course_utilization:.1f}%")
        
        print("\n👤 Student Type Breakdown:")
        for s_type, count in student_types.items():
            percentage = (count / total_students * 100) if total_students else 0
            print(f"  • {s_type}: {count} ({percentage:.1f}%)")
        
        # GPA statistics
        gpas = [s.calculate_gpa() for s in self.students.values() if s.calculate_gpa() > 0]
        if gpas:
            print(f"\n📊 GPA Statistics:")
            print(f"  • Average GPA: {sum(gpas)/len(gpas):.2f}")
            print(f"  • Highest GPA: {max(gpas):.2f}")
            print(f"  • Lowest GPA: {min(gpas):.2f}")
    
    def _clear_screen(self):
        """Clear the console screen."""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """Main entry point."""
    try:
        system = StudentCourseManagementSystem()
        system.run()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n⚠️ Program interrupted by user.")
    except Exception as e:
        print(Fore.RED + f"\n❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print(Fore.GREEN + "\nGoodbye!")

if __name__ == "__main__":
    main()