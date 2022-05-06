import random
from tkinter import *
from tkinter import ttk
from ttg.model import *
import ttg.timetable as timetable


POPULATION_SIZE = 25


def initiation(course_list,professor_list,batch_list):

    data = []

    # Create Compound data
    for c in course_list:
        course = set()
        course.add(c)
        if c.course_type == "elective":
            batch = set()
            for b in batch_list:
                batch.add(b)
            data.append(Data().create_compound_data(batch, course))


    # Create Lecture Data 
    for b in batch_list:
        batch = set()
        batch.add(b)
        for c in course_list:
            course = set()
            course.add(c)
            for p in professor_list:
                prof = set()
                prof.add(p)
                if c.course_id in p.prof_courses.split(", ") and c.course_type=="lecture":
                    data.append(Data().create_lecture_data(batch, course, prof))
                    break

    # create lab data 
    for b in batch_list:
        batch = set()
        batch.add(b)
        courses = set()
        for c in courses:
            if c.course_type == "lab":
                courses.add(c)
        prof = set()
        for p in professor_list:
            for pc in p.prof_courses.split(", "):
                if pc in courses:
                    prof.add(p)
        data.append(Data().create_lab_data(batch, courses, prof, 3, 1))

    # create pseudo data - for empty slots
    for b in batch_list:
        batch = set()
        batch.add(b)
        data.append(Data().create_pseudo_data(batch,1,3))





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
