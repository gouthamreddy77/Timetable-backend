from flask import render_template, url_for, flash, redirect, request
from ttg import app, db
from ttg.model import Professor, Course, Batch, Mapping
from ttg.new_scheduler import scheduler
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os
from tkinter import *
from tkinter import ttk


@app.route('/')
def home():
	return {
	'status': 'SUCCESS'
	}

@login_required
@app.route('/add_course',methods=['GET','POST'])
def add_course():
	if request.method=='POST':
		subject=request.form['subject']
		'''
		{
			course_id: 1,
			course_name: 'ABC DEF',
			course_short_form: 'AD',
			course_type: 'lab/lecture/elective',
			preferred_rooms: None -- only for labs we send it
		}
		'''
		
		# check if already in DB
		c1 = Course.query.filter_by(course_id=subject.course_id).first()		
		# If yes, Don't add
		if c1 :
			flash('Course already exists!','warning')
			return {
			'status': 'FAILURE'
			}
			# return redirect(url_for('index'))	
		# If No, Add!
		else:
			duration, frequency = 0, 0
    		# Create course object and initialize
			if subject.course_type == 'elective':
				duration, frequency = 2 , 2 
			elif oe.course_type == 'Lecture':
				duration, frequency = 1 , 4 
			elif oe.course_type == 'lab':
				preferred_rooms = subject.preferred_rooms
			c = Course(course_id = subject.course_id, 
				course_name = subject.course_name, 
				course_short_form = subject.course_short_form,
				course_type = subject.course_type,
				duration = duration,
				frequency = frequency,
				preferred_rooms = preferred_rooms)
			# db.session.begin_nested()
			db.session.add(c)
			# db.session.flush()
			db.session.commit()
			flash('Course added!','success')
			# return redirect(url_for('index'))
			return {
			'status': 'SUCCESS'
			}

@login_required
@app.route('/delete_course',methods=['GET','POST'])
def delete_course():
	if request.method=='POST':
		course_id=request.form['course_id']	
		c=Course.query.filter_by(course_id=course_id).first()
		# db.session.delete(cart)
		c.delete()
		db.session.commit()
		flash('Course removed!','success')
		return {
			'status': 'SUCCESS'
			}

@app.route('/view_courses',methods=['GET'])
def view_courses():
	if request.method=='GET':
		c=Course.query().all()
		return {
			'status': 'SUCCESS',
			'data': c
			}

###################################################################

@login_required
@app.route('/add_faculty',methods=['GET','POST'])
def add_faculty():
	if request.method=='POST':
		f=request.form['faculty']
		'''
		{
			professor_id: 1,
			professor_name: 'ABC DEF',
			prof_courses: 'c1, c2, c3'
		}
		'''		
		# check if already in DB
		p1 = Professor.query.filter_by(professor_id=f.professor_id).first()		
		# If yes, Don't add
		if p1 :
			flash('Faculty already exists!','warning')
			return {
			'status': 'FAILURE'
			}	
		# If No, Add!
		else:
    		# Create Faculty object and initialize		
			p = Professor(professor_id = f.professor_id, 
				professor_name = f.professor_name,
				prof_courses = f.prof_courses)
			# db.session.begin_nested()
			db.session.add(p)
			# db.session.flush()
			db.session.commit()
			flash('Faculty added!','success')
			# return redirect(url_for('index'))
			return {
			'status': 'SUCCESS'
			}


@login_required
@app.route('/delete_faculty',methods=['GET','POST'])
def delete_faculty():
	if request.method=='POST':
		professor_id=request.form['professor_id']	
		p=Professor.query.filter_by(professor_id=professor_id).first()
		# db.session.delete(cart)
		p.delete()
		db.session.commit()
		flash('Professor removed!','success')
		return {
			'status': 'SUCCESS'
			}

@app.route('/view_faculty',methods=['GET'])
def view_faculty():
	if request.method=='GET':
		p=Professor.query().all()
		return {
			'status': 'SUCCESS',
			'data': p
			}

###################################################################


def tk_print(d):
        class Table:

            def __init__(self, root, temp):
                total_rows = len(temp)
                total_columns = len(temp[0])

                # code for creating table
                for i in range(total_rows):
                    for j in range(total_columns):
                        # self.e = Entry(root, fg='black',width=20,
                        #                font=('Arial', 16, 'bold'))
                        e = Text(root, fg='white',bg = 'black',height=2, width=21,font=('Arial', 16, 'bold'))
                        e.grid(row=i, column=j)
                        e.insert(END, temp[i][j])

                    # take the data

        # create root window
        root = Tk()
        root.title("Tab Widget")
        tabControl = ttk.Notebook(root)
        for i, _ in enumerate(d):
            title = ttk.Frame(tabControl)
            tabControl.add(title, text=str(_))
            t = Table(title, d[_])
        tabControl.pack(expand=1, fill="both")
        root.mainloop()


@login_required
@app.route('/generate_timetable',methods=['GET'])
def generate_timetable():
	if request.method=='GET':
		# b_room = ['R1', 'R2', 'R3', 'R4']
		# for _ in range(4):
		# 	t = Batch('CSE', 4, _ + 1, b_room[_], False)
		# 	batch_list.append(t)

		# b_room = ['R1', 'R2']
		# for _ in range(2):
		# 	t = Batch(4, 'CSE', _+1, b_room[_])
		# 	batch_list.append(t)

		mapped_data = Mapping.query.all()
		batch_list, course_list, professor_list = [], [], []
		for md in mapped_data:
			batch = Batch.query.filter_by(batch_id=md.batch_id).first()
			batch_list.append(batch)
			course = Course.query.filter_by(course_id=md.course_id).first()
			course_list.append(course)
			professor = Professor.query.filter_by(professor_id=md.professor_id).first()
			professor_list.append(professor)


		# batch_list = Batch.query.all()
		print('\n#################################################################')
		print('batch_list === ',batch_list)
		print('#################################################################\n')

		# course_list = Course.query.all()
		print('\n#################################################################')
		print('course_list === ', course_list)
		print('#################################################################\n')

		# faculty_list = p=Professor.query.all()
		print('\n#################################################################')
		print('faculty_list === ', professor_list)
		print('#################################################################\n')

		timetable = {}
		timetable = scheduler(course_list,professor_list,batch_list)
		print('\n#################################################################')
		print("TIMETABLE === \n",timetable)
		print('#################################################################\n')
		tk_print(timetable)
		return {
			'status': 'SUCCESS',
			'data': timetable
			}
		

