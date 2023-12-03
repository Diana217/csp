from collections import namedtuple
from typing import List
from time import time as get_cur_time
from random import randint
from copy import copy

weekdays = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday"}
times = {1: "8:40-10:15", 2: "10:35-12:10", 3: "12:20-13:55", }

Classroom = namedtuple("Classroom", "room is_big")
Time = namedtuple("Time", "weekday time")
Teacher = namedtuple("Teacher", "name")
Subject = namedtuple("Subject", "name")
Group = namedtuple("Group", "name")
Lesson = namedtuple("Lesson", "teacher subject group is_lecture per_week")
Gene = namedtuple("Gene", "lessons classrooms times")
DomainEl = namedtuple("DomainEl", "day time room")

Classroom.__repr__ = lambda c: f"{c.room} ({'lecture auditorium' if c.is_big else 'seminar auditorium'})"
Teacher.__repr__ = lambda t: f"{t.name.split}"
Subject.__repr__ = lambda s: f"{s.name.split}"
Group.__repr__ = lambda g: f"{g.name}"
Lesson.__repr__ = lambda l: f"{l.teacher} | {l.subject} | {l.group} | " \
                            f"{'Lecture' if l.is_lecture else 'Seminar'} {l.per_week}/week"

def gen_repr(g: Gene):
    output = ""
    for i in range(len(g.lessons)):
        output += f"{g.lessons[i]},   {g.classrooms[i]},   {g.times[i]}\n"
    return output
Gene.__repr__ = lambda g: gen_repr(g)

# data for schedule
classrooms = [
    Classroom(1, True),
    Classroom(2, True),
    Classroom(3, True),
    Classroom(4, False),
    Classroom(5, False),
    Classroom(6, False)
]

schedule = [Time(w, n) for w in range(1, len(weekdays.keys()) + 1)
            for n in range(1, len(times.keys()) + 1)]

teachers = [Teacher(name) for name in
            ("Krivolap", "Hlybovets", "Doroshenko", "Tkachenko", 
             "Shishatska", "Voloshin", "Trotsenko", "Krasovska", 
             "Pashko", "Vergunova", "Bobyl", "Taranukha", 
             "Krak", "Stadnik" )]

subjects = [Subject(name) for name in
            ("Mobile platforms", "Intelligent systems", "Methods of parallel calculations", "Information Technology", 
             "Project management", "Decision making theory", "Systems modeling methods", "English", 
             "Statistical modeling", "Intelligent data analysis", "Complexity of algorithms", "Neural networks",
             "Computer linguistics", "Problems of artificial intelligence", "Software development", "Computer algorithms" )]

groups = [Group(name) for name in
          ("MI", "TTP-41", "TTP-42", "TK-41", "TK-42" )]

lessons = [
    #  MI
    Lesson(teachers[11], subjects[15], groups[0], False, 1),
    Lesson(teachers[10], subjects[11], groups[0], False, 1),
    Lesson(teachers[9], subjects[10], groups[0], True, 2),
    Lesson(teachers[3], subjects[3], groups[0:5], True, 2),
    Lesson(teachers[10], subjects[11], groups[0], True, 1),
    Lesson(teachers[11], subjects[12], groups[0], True, 1),
    Lesson(teachers[0], subjects[3], groups[0:5], False, 1),
    Lesson(teachers[7], subjects[7], groups[0:5], True, 1),
    Lesson(teachers[8], subjects[8], groups[0:5], True, 1),
    Lesson(teachers[6], subjects[6], groups[0:5], True, 1),
    Lesson(teachers[5], subjects[5], groups[0:5], True, 1),
    Lesson(teachers[1], subjects[1], groups[0:5], True, 1),
    #  TTP
    Lesson(teachers[0], subjects[0], groups[1:3], False, 1),
    Lesson(teachers[2], subjects[2], groups[1:3], True, 1),
    Lesson(teachers[3], subjects[0], groups[1:3], True, 1),
    Lesson(teachers[4], subjects[4], groups[1:3], True, 1),
    Lesson(teachers[8], subjects[3], groups[1:3], True, 1),
    #  TK
    Lesson(teachers[12], subjects[13], groups[3:5], True, 1),
    Lesson(teachers[11], subjects[13], groups[3:5], False, 1),
    Lesson(teachers[13], subjects[14], groups[3:5], True, 1),
    Lesson(teachers[13], subjects[14], groups[4:5], False, 1),
    Lesson(teachers[8], subjects[9], groups[3:5], True, 1),
    Lesson(teachers[8], subjects[9], groups[3:5], False, 1),
]

def initialize_domains():
    domain = {}
    buf = []
    buf_lecture = []
    for day in weekdays.keys():
        for time in times.keys():
            for room in classrooms:
                buf.append(DomainEl(day, time, room))
                if room.is_big:
                    buf_lecture.append(DomainEl(day, time, room))
    for i in range(len(lessons)):
        if lessons[i].is_lecture:
            domain[i] = copy(buf_lecture)
        else:
            domain[i] = copy(buf)
    return domain

def mrv(domain):
    min_len = len(weekdays) * len(classrooms) * len(times) * 2
    ind = list(domain.keys())[0]
    for key, value in domain.items():
        if len(value) < min_len:
            min_len = len(value)
            ind = key
    return ind

def degree(domain):
    counts = {}
    for key in domain:
        counts[key] = 0 if lessons[key].is_lecture else 1
        for i in domain:
            if i == key:
                continue
            if lessons[key].teacher == lessons[i].teacher:
                counts[key] += 1
            counts[key] += len(set(map(str, lessons[key].group)) & set(map(str, lessons[i].group)))

    ind = list(counts.keys())[0]
    max = 0
    for key, value in counts.items():
        if value > max:
            max = value
            ind = key
    return ind

def lcv(domain):
    counts = {}
    for i in domain:
        counts[i] = 0
        for key in domain:
            if i == key:
                continue
            
            for d in domain[key]:
                if not (d.day==domain[i][0].day and d.time==domain[i][0].time and d.room==domain[i][0].room) and \
                    not (d.day==domain[i][0].day and d.time==domain[i][0].time and (lessons[key].teacher==lessons[i].teacher or \
                        set(map(str, lessons[key].group)) & set(map(str, lessons[i].group)))):
                    counts[i] += 1
    
    ind = list(counts.keys())[0]
    max = 0
    for key, value in counts.items():
        if value > max:
            max = value
            ind = key
    return ind

def forward_checking(domain):
    return list(domain.keys())[0]

def constraint_propagation(domain):
    for key in domain:
        if len(domain[key]) == 1:
            return key
    while True:
        i = randint(0, len(domain)-1)
        j = randint(0, len(domain)-1)

        i = list(domain.keys())[i]
        j = list(domain.keys())[j]

        if (lessons[i].teacher==lessons[j].teacher or \
            set(map(str, lessons[i].group)) & set(map(str, lessons[j].group))):
            if not len(domain[i]):
                return -1
            k = randint(0, len(domain[i])-1)
            if domain[i][k] in domain[j]:
                del domain[i][k]
            if len(domain[i]) == 1:
                return i

def backtrack(heuristic, domain, schedule):
    if not domain:
        return schedule
    ind = heuristic(domain)
    if ind == -1:
        return None
    for d in domain[ind]:
        sch_copy = copy(schedule)
        sch_copy.times.append(Time(d.day, d.time))
        sch_copy.classrooms.append(d.room)
        sch_copy.lessons.append(lessons[ind])
        
        dom_copy = copy(domain)
        dom_copy.pop(ind)
        dom_copy = update_domain(dom_copy, lessons[ind], d.day, d.time, d.room)

        res = backtrack(heuristic, dom_copy, sch_copy)
        if res:
            return res
    return None

def update_domain(domain, lesson, day, time, room):
    for key in domain:
        buf = []
        for d in domain[key]:
            if not (d.day==day and d.time==time and d.room==room) and \
                not (d.day==day and d.time==time and (lessons[key].teacher==lesson.teacher or \
                    set(map(str, lessons[key].group)) & set(map(str, lesson.group)))):
                buf.append(d)
        domain[key] = buf
    return domain

def print_schedule(solution: Gene, ):
    for day in weekdays:
        print('\n' + '=' * 100)
        print(f"{weekdays[day].upper()}")
        for time in times:
            print('\n\n' + times[time])
            for c in classrooms:
                print(f'\n{c}', end='\t\t')
                for i in range(len(solution.lessons)):
                    if solution.times[i].weekday == day and solution.times[i].time == time and \
                            solution.classrooms[i].room == c.room:
                        print(solution.lessons[i], end='')

def test():
    #  Minimum Remaining Values
    start_time = get_cur_time()
    schedule = backtrack(mrv, initialize_domains(), Gene([], [], []))
    print(f"MRV: {get_cur_time()-start_time}")
    #  print_schedule(schedule)

    #  Least Constraining Value
    start_time = get_cur_time()
    schedule = backtrack(lcv, initialize_domains(), Gene([], [], []))
    print(f"LCV: {get_cur_time()-start_time}")
    #  print_schedule(schedule)

    #  Degree heuristic
    start_time = get_cur_time()
    schedule = backtrack(degree, initialize_domains(), Gene([], [], []))
    print(f"Degree: {get_cur_time()-start_time}")
    #  print_schedule(schedule)

    #  Forward checking
    start_time = get_cur_time()
    schedule = backtrack(forward_checking, initialize_domains(), Gene([], [], []))
    print(f"Forward: {get_cur_time()-start_time}")
    #  print_schedule(schedule)

    #  Constraint propagation
    start_time = get_cur_time()
    schedule = backtrack(constraint_propagation, initialize_domains(), Gene([], [], []))
    print(f"Constraint: {get_cur_time()-start_time}")
    #  print_schedule(schedule)

test()