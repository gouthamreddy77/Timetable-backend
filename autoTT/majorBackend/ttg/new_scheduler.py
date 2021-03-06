import random
from tkinter import *
from tkinter import ttk
from ttg.model import *
import ttg.timetable as timetable
from ttg.model import Professor, Course, Batch, Lectures, Labs, Electives

POPULATION_SIZE = 27

def split_labs_into_pairs(labs):
    # print('\n##################  LABS - paired in function #######################')
    # print('labs === ',labs)
    # print('#################################################################\n')
    lab_pairs = []
    # labs = [a,b,c,d] - len=4
    if len(labs) % 2 == 0:
        for i in range(0,len(labs),2):
            temp = set()
            temp.add(labs[i])
            temp.add(labs[i+1])
            lab_pairs.append(temp)
    # labs = [a,b,c] - len=3
    else:        
        for i in range(0,len(labs)-1,2):
            temp = set()
            temp.add(labs[i])
            temp.add(labs[i+1])
            lab_pairs.append(temp)
        temp = set()
        temp.add(labs[-1])
        lab_pairs.append(temp)
    return lab_pairs



def initiation(batch_list,mapped_lectures,mapped_electives,mapped_labs):

    data = []

    # Create Compound data - for electives
    # electives --- All batches + 1 course -- OK
    batch = set()
    for b in batch_list:
        batch.add(b)

    for e in mapped_electives:
        c = Course.query.filter_by(course_id=e.course_id).first()
        course = set()
        course.add(c)
        # print('\n##################  ELECTIVES #######################')
        # print("course === ", c.course_short_form,"TYPE(c)=",type(c))
        # print('#################################################################\n')
        data.append(Data().create_compound_data(batch, course))


    # Create Lecture data - for regular subjects
    # lecture -- 1 batch + 1 course + 1 prof -- MAPPING     
    for l in mapped_lectures:
        b = Batch.query.filter_by(batch_id=l.batch_id).first()
        c = Course.query.filter_by(course_id=l.course_id).first()
        p = Professor.query.filter_by(professor_id=l.professor_id).first()
        batch, course, prof = set(), set(), set()
        batch.add(b)
        course.add(c)
        prof.add(p)
        # print('\n##################  LECTURES #######################')
        # print('batch === ',b.year, "-", b.dept_name, "-", b.section,"TYPE(b)=",type(b))
        # print("course === ", c.course_short_form,"TYPE(c)=",type(c))
        # print("professor === ", p.professor_name,"TYPE(p)=",type(p))
        # print('#################################################################\n')
        data.append(Data().create_lecture_data(batch,course,prof))


    # Create Lab data - for electives
    # lab -- 1 batch + split all labs into pairs + all lab profs
    for b in batch_list:
        labs = []
        for lab in mapped_labs:
            if lab.batch_id == b.batch_id:
                labs.append(lab)
        # labs = mapped_labs
        pairs = []
        for l in labs:
            if l.can_be_paired == 0:
                c = Course.query.filter_by(course_id=l.course_id).first()
                p = Professor.query.filter_by(professor_id=l.professor_id).first()
                batch, course, prof = set(), set(), set()
                batch.add(b)
                course.add(c)
                prof.add(p)
                # print('\n##################  LABS - Not to be paired #######################')
                # print('batch === ',b.year, "-", b.dept_name, "-", b.section,"TYPE(b)=",type(b))
                # print("course === ", c.course_short_form,"TYPE(c)=",type(c))
                # print("professor === ", p.professor_name,"TYPE(p)=",type(p))
                # print('#################################################################\n')
                data.append(Data().create_lab_data(batch, course, prof, 3, 1))
            else:
                c = Course.query.filter_by(course_id=l.course_id).first()
                pairs.append(c)

        lab_pairs = split_labs_into_pairs(pairs)
        
        
        for pair in lab_pairs:
            # print('\n##################  LABS - paired #######################')
            # print('lab_pairs === ',l, type(l))
            # print('#################################################################\n')
            prof_for_lab_pairs = set()
            for x in pair:                
                l = Labs.query.filter_by(course_id=x.course_id).first()
                p = Professor.query.filter_by(professor_id=l.professor_id).first()
                if p not in prof_for_lab_pairs:
                    prof_for_lab_pairs.add(p)
            
            batch = set()
            batch.add(b)
            # print('\n##################  LABS - Pairable #######################')
            # print('batch === ',b.year, "-", b.dept_name, "-", b.section,"TYPE(b)=",type(b))
            # for x in pair:                
                # print("course === ", x.course_short_form,"TYPE(x)=",type(x))
            # for prof in prof_for_lab_pairs:
                # print("professor === ", prof.professor_name,"TYPE(prof)=",type(prof))
            # print('#################################################################\n')
            data.append(Data().create_lab_data(batch, pair, prof_for_lab_pairs, 3, 1))

    # create pseudo data - for empty slots
    # empty -- all batches + duration + freq
    batch = set()
    for b in batch_list:
        batch.add(b)
    data.append(Data().create_pseudo_data(batch,1,3))


    return batch_list,mapped_lectures,mapped_electives,mapped_labs, data


def scheduler(batch_list,mapped_lectures,mapped_electives,mapped_labs,data=[],retry=False):
    if retry == False:
        batch_list,mapped_lectures,mapped_electives,mapped_labs, data = initiation(batch_list,mapped_lectures,mapped_electives,mapped_labs)

    # print('\n#################################################################')
    # print('data === ', data)
    # print('#################################################################\n')
    # print("data length === \n",len(data))
    # print('#################################################################\n')

    # Start
    generation = 1
    terminate = False
    population = []

    for _ in range(POPULATION_SIZE):
        gnome = timetable.Timetable.create_genome(data)
        population.append(timetable.Timetable(gnome))

    while not terminate:

        # Sorting The Population with Increasing Order of Collisions
        population = sorted(population, key=lambda x: x.collisions)

        # Termination
        if population[0].collisions == 0:
            d = population[0].print_test()
            # Timetable.save(population[0])
            # population[0].tk_print(d)
            # tk_print(d)
            return d
            ch = input('Enter Swap Choice: ')
            while ch == 'y':
                print('Enter Coordinates: ')
                a, b, c, d = map(int, input().split())
                # Static Swap Function call in First Batch
                population[0].swap(batch_list[0], (a, b), (c, d))
                d = population[0].print_test()
                print('Printing...')
                # population[0].tk_print(d)
                # tk_print(d)
                return d
                ch = input('Do you want to Continue Swapping')
            terminate = True
            # TODO: Start Here Data Updating in Data Objects
            break

        new_generation = []

        promotion_marker = int((20 * POPULATION_SIZE) / 100)
        new_generation.extend(population[:promotion_marker])

        balance_filler = int((80 * POPULATION_SIZE) / 100)
        for _ in range(balance_filler):
            parent1 = random.choice(population[:10])
            parent2 = random.choice(population[:10])
            child = parent1.crossover(parent2)
            new_generation.append(child)

        population = new_generation

        generation += 1
        print("generation No : ", generation)
        print("Collisions : ", population[0].collisions)

        if generation > 3333:
            print("Re-Schedule")
            scheduler(batch_list,mapped_lectures,mapped_electives,mapped_labs,data,True)
