from flask import render_template, url_for, flash, redirect, request, jsonify
import json
import numpy as np
from ttg import app, db
from ttg.model import Professor, Course, Batch, Lectures, Labs, Electives, Department, Room, User
from ttg.new_scheduler import scheduler
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os
from tkinter import *
from tkinter import ttk

#####################  HOME  ##############################

@app.route('/')
def home():
	return {
	'status': 'SUCCESS'
	}
###################  ADD COURSE  ###########################

@login_required
@app.route('/add_course',methods=['POST'])
def add_course():
	if request.method=='POST':
		msg = None
		'''
		{
			"course_id": 1,
			"course_name": "Dummy Lecture",
			"course_short_form": "DL",
			"course_type": "lecture",
			"preferred_rooms": null
		}
		{
		    "course_id": "18PC1CS12",
		    "course_name": "Dummy Lecture 2",
		    "course_short_form": "DL2",
		    "course_type": "lab",
		    "preferred_rooms": "A108"
		}
		'''
		course_id=request.json['course_id']
		course_name=request.json['course_name']
		course_short_form=request.json['course_short_form']
		course_type=request.json['course_type']
		course_id=request.json['course_id']
		preferred_rooms=request.json['preferred_rooms']

		# check if already in DB
		c1 = Course.query.filter_by(course_name=course_name).first()		
		# If yes, Don't add
		if c1!=None :
			msg = "Course already exists with this name."
			# return redirect(url_for('index'))	
		# If No, Add!
		else:
			duration, frequency = 0, 0
    		# Create course object and initialize
			if course_type == 'elective':
				duration, frequency = 2 , 2 
			elif course_type == 'Lecture':
				duration, frequency = 1 , 4 
			elif course_type == 'lab':
				preferred_rooms = preferred_rooms
			c = Course(course_id = course_id, 
				course_name = course_name, 
				course_short_form = course_short_form,
				course_type = course_type,
				duration = duration,
				frequency = frequency,
				preferred_rooms = preferred_rooms)
			db.session.add(c)
			db.session.commit()

		status = "FAILURE" if msg!=None else "SUCCESS"
		return jsonify({
		'status': status
		})

###################  DELETE COURSE  ###########################

@login_required
@app.route('/delete_course',methods=['POST'])
def delete_course():
	if request.method=='POST':
		'''
		{
	    "course_id": "18PC1CS11"
	    "course_type": "lecture"
		}
		'''
		course_id = request.json["course_id"]
		course_type = request.json["course_type"]
		msg = None
		c=Course.query.filter_by(course_id=course_id).delete()
		# If Course Exists
		if c!=0:
			# c=Course.query.filter_by(course_id=course_id).delete()						
			# Delete its mappings too
			if course_type == 'lecture':
				lec=Lectures.query.filter_by(course_id=course_id).delete()
				if lec == 0:
					msg = "No lecture mapping found. Deleted only course."
			elif course_type == 'elective':
				ele=Electives.query.filter_by(course_id=course_id).delete()
				if ele == 0:
					msg = "No elective mapping found. Deleted only course."
			else:
				lab=Labs.query.filter_by(course_id=course_id).delete()
				if lab == 0:
					msg = "No lab mapping found. Deleted only course."
		# If Course Doesn't Exists
		else:
			msg = "No Course Found."
		db.session.commit()
		status = 'FAILURE' if msg == "No Course Found." else 'SUCCESS'
		return jsonify({
			'status': status,
			'message': msg
			})

###################  VIEW COURSE  ###########################

@app.route('/view_courses',methods=['GET'])
def view_courses():
	if request.method=='GET':
		c=Course.query.all()
		data = []
		for x in c:
			data.append(x.toDict())
		return jsonify({
			'status': 'SUCCESS',
			'data': data
			})

###################  ADD FACULTY  ###########################

@login_required
@app.route('/add_faculty',methods=['POST'])
def add_faculty():
	if request.method=='POST':
		'''
		{
	    	"professor_id": "26",
	    	"professor_name": "P Jyothi"
		}
		'''	
		professor_id=request.json['professor_id']
		professor_name=request.json['professor_name']
		# check if already in DB
		msg = None
		p1 = Professor.query.filter_by(professor_name=professor_name).first()		
		# If yes, Don't add
		if p1!=None :
			msg = "Professor already exists with this name"	
		# If No, Add!
		else:
    		# Create Faculty object and initialize		
			p = Professor(professor_id = professor_id, 
				professor_name = professor_name)
			db.session.add(p)
			db.session.commit()
		status = "FAILURE" if msg!=None else "SUCCESS"
		return jsonify({
		'status': status
		})

###################  DELETE FACULTY  ###########################

@login_required
@app.route('/delete_faculty',methods=['POST'])
def delete_faculty():
	if request.method=='POST':
		'''
		{
	    "professor_id": ""
		}
		'''
		professor_id=request.json['professor_id']	
		msg = None
		p=Professor.query.filter_by(professor_id=professor_id).delete()
		# If Professor Exists
		if p!=0:					
			# Delete its mappings too
			lec=Lectures.query.filter_by(professor_id=professor_id).delete()
			ele=Electives.query.filter_by(professor_id=professor_id).delete()
			lab=Labs.query.filter_by(professor_id=professor_id).delete()
			if lec==0 and ele==0 and lab==0:
				msg = "No professor mapping found. Deleted only professor."
		# If Professor Doesn't Exists
		else:
			msg = "No Professor found."

		db.session.commit()
		status = 'FAILURE' if msg == "No Professor found." else 'SUCCESS'
		return jsonify({
			'status': status,
			'message': msg
			})



###################  VIEW FACULTY  ###########################

@app.route('/view_faculty',methods=['GET'])
def view_faculty():
	if request.method=='GET':
		p=Professor.query.all()
		data = []
		for x in p:
			data.append(x.toDict())
		return jsonify({
			'status': 'SUCCESS',
			'data': data
			})

###################  VIEW DEPARTMENTS  ###########################
@app.route('/view_departments',methods=['GET'])
def view_departments():
	if request.method=='GET':
		d=Department.query.all()
		data = []
		for x in d:
			data.append(x.toDict())
		return jsonify({
			'status': 'SUCCESS',
			'data': data
			})

###################  VIEW ROOMS  ###########################
@app.route('/view_rooms',methods=['GET'])
def view_rooms():
	if request.method=='GET':
		r=Room.query.all()
		data = []
		for x in r:
			data.append(x.toDict())
		return jsonify({
			'status': 'SUCCESS',
			'data': data
			})

###################  VIEW BATCH  ###########################
@app.route('/view_batch',methods=['GET'])
def view_batch():
	if request.method=='GET':
		b=Batch.query.all()
		data = []
		for x in b:
			data.append(x.toDict())
		return jsonify({
			'status': 'SUCCESS',
			'data': data
			})

###################  PRINT TT IN TKINTER  ###########################


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


###################  RE FORMAT TIMETABLE  ###########################

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def reformat_timetable(d):
	dic1={}
	first=True
	for i in d:
		if first!=True:
			dic1[i]=d[i]
		first=False
	for i in d:
		for j in range(1,len(d[i])):
			for k in range(len(d[i][j])):
				if d[i][j][k]!=0:
					for l in dic1:
						dic1[l][j][k]=d[i][j][k]
		break
	return dic1


###################  GENERATE TIMETABLE  ###########################

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

		mapped_electives = Electives.query.all()
		mapped_labs = Labs.query.all()
		mapped_lectures = Lectures.query.all()
		batch_list = Batch.query.all()


		# print('\n#################################################################')
		# print('batch_list === ',batch_list)
		# print('#################################################################\n')

		# print('\n#################################################################')
		# print('mapped_labs === ', mapped_labs)
		# print('#################################################################\n')

		# print('\n#################################################################')
		# print('mapped_lectures === ', mapped_lectures)
		# print('#################################################################\n')

		# print('\n#################################################################')
		# print('mapped_electives === ', mapped_electives)
		# print('#################################################################\n')

		timetable = {}
		timetable = scheduler(batch_list,mapped_lectures,mapped_electives,mapped_labs)
		timetable = reformat_timetable(timetable)
		print('\n#################################################################')
		print("TIMETABLE === \n",timetable)
		print('#################################################################\n')
		
		# tk_print(timetable)
		timetable = json.dumps(timetable, cls=NumpyEncoder)
		# timetable = jsonify(timetable)
		return jsonify({
			'status': 'SUCCESS',
			'data': timetable
			})
		

