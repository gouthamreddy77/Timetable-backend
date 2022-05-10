import random
from tkinter import *
from tkinter import ttk
from ttg.model import *
import ttg.timetable as timetable


POPULATION_SIZE = 25


def initiation(course_list,professor_list,batch_list):

    data = []
    data_length = len(course_list)

    # Create Compound data - for electives
    batch = set()
    for b in batch_list:
        batch.add(b)

    for c in course_list:        
        if c.course_type == "elective":
            course = set()
            course.add(c)
            # print('\n##################  ELECTIVES #######################')
            # print("course === ", c.course_short_form)
            # print('#################################################################\n')
            data.append(Data().create_compound_data(batch, course))


    # Create Lecture data - for regular subjects    
    for i in range(data_length):
        if course_list[i].course_type == 'lecture':
            batch, course, prof = set(), set(), set()
            batch.add(batch_list[i])
            course.add(course_list[i])
            prof.add(professor_list[i])
            # print('\n##################  LECTURES #######################')
            # print('batch === ',batch_list[i].year, "-", batch_list[i].dept_name, "-", batch_list[i].section)
            # print("course === ", course_list[i].course_short_form)
            # print("professor === ", professor_list[i].professor_name)
            # print('#################################################################\n')
            data.append(Data().create_lecture_data(batch,course,prof))


    # Create Lab data - for electives
    # labs = [] #index list of lab courses
    # lab_pairs = []
    # for i in range(data_length):
    #     if course_list[i].course_type == "lab":
    #         labs.append(course_list[i])

    # # labs = [a,b,c,d] - len=4
    # if len(labs) % 2 == 0:
    #     for i in range(0,len(labs),2):
    #         temp = set()
    #         temp.add(labs[i])
    #         temp.add(labs[i+1])
    #         lab_pairs.append(temp)
    # # labs = [a,b,c] - len=3
    # else:        
    #     for i in range(0,len(labs)-1,2):
    #         temp = set()
    #         temp.add(labs[i])
    #         temp.add(labs[i+1])
    #         lab_pairs.append(temp)
    #     temp = set()
    #     temp.add(labs[-2])
    #     temp.add(labs[-1])
    #     lab_pairs.append(temp)


    # for i in range(data_length):
    #     batch = set()
    #     batch.add(batch_list[i])
    #     for pair in lab_pairs:
    #         prof = set()
    #         for l in pair:
    #             prof.add(professor_list[i])
    #             # print('\n##################  LABS #######################')
    #             # print('batch === ',b.year, "-", b.dept_name, "-", b.section)
    #             # print("course === ", l.course_short_form)
    #             # print("professor === ", professor_list[i].professor_name)
    #             # print('#################################################################\n')
    #         data.append(Data().create_lab_data(batch, pair, prof, 3, 1))

    # create pseudo data - for empty slots
    batch = set()
    for b in batch_list:
        batch.add(b)
    data.append(Data().create_pseudo_data(batch,1,3))

    # electives --- All batches + 1 course -- OK
    # lecture -- 1 batch + 1 course + 1 prof -- MAPPING 
    # lab -- 1 batch + split all labs into pairs + all lab profs
    # empty -- all batches + duration + freq

    # data = [
    #     Data().create_compound_data({batch_list[0], batch_list[1]}, {course_list[0]}),
    #     Data().create_lecture_data({batch_list[0]}, {course_list[1]}, {professor_list[7]}),
    #     Data().create_lecture_data({batch_list[0]}, {course_list[2]}, {professor_list[14]}),
    #     Data().create_lecture_data({batch_list[0]}, {course_list[3]}, {professor_list[16]}),
    #     Data().create_lecture_data({batch_list[0]}, {course_list[4]}, {professor_list[4]}),
    #     Data().create_lecture_data({batch_list[0]}, {course_list[5]}, {professor_list[3]}),
    #     Data().create_lab_data({batch_list[0]}, {course_list[6], course_list[7]},
    #                            {professor_list[14], professor_list[15], professor_list[3], professor_list[11]}, 3,
    #                            1),
    #     Data().create_lab_data({batch_list[0]}, {course_list[6], course_list[8]},
    #                            {professor_list[14], professor_list[15], professor_list[21], professor_list[20]}, 3, 1),
    #     Data().create_lab_data({batch_list[0]}, {course_list[7], course_list[8]},
    #                            {professor_list[3], professor_list[11], professor_list[21], professor_list[20]}, 3, 1),
    #     Data().create_pseudo_data({batch_list[0]}, 1, 3),

    #     # Data().create_compound_data({batch_list[1], batch_list[1]}, {course_list[0]}),
    #     Data().create_lecture_data({batch_list[1]}, {course_list[1]}, {professor_list[13]}),
    #     Data().create_lecture_data({batch_list[1]}, {course_list[2]}, {professor_list[10]}),
    #     Data().create_lecture_data({batch_list[1]}, {course_list[3]}, {professor_list[9]}),
    #     Data().create_lecture_data({batch_list[1]}, {course_list[4]}, {professor_list[8]}),
    #     Data().create_lecture_data({batch_list[1]}, {course_list[5]}, {professor_list[23]}),
    #     Data().create_lab_data({batch_list[1]}, {course_list[6], course_list[7]},
    #                            {professor_list[10], professor_list[25], professor_list[23], professor_list[8]}, 3,
    #                            1),
    #     Data().create_lab_data({batch_list[1]}, {course_list[6], course_list[8]},
    #                            {professor_list[10], professor_list[25], professor_list[12], professor_list[17]}, 3, 1),
    #     Data().create_lab_data({batch_list[1]}, {course_list[7], course_list[8]},
    #                            {professor_list[23], professor_list[8], professor_list[12], professor_list[17]}, 3, 1),
    #     Data().create_pseudo_data({batch_list[1]}, 1, 3),
    # ]
    # # print(data, len(data))

    return batch_list, professor_list, course_list, data


def scheduler(course_list,professor_list,batch_list):
    batch_list, professor_list, course_list, data = initiation(course_list,professor_list,batch_list)
    # print(batch_list, professor_list, course_list, data)
    print('\n#################################################################')
    print('data === ', data)
    print('#################################################################\n')
    print("data length === \n",len(data))
    print('#################################################################\n')

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

        if generation > 4000:
            print("Re-Schedule")
            scheduler(course_list,professor_list,batch_list)
