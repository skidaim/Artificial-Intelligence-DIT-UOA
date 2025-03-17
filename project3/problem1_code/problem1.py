import pandas as pd
import sys
from csp import CSP, backtracking_search, forward_checking, mac, min_conflicts, mrv, dom_wdeg
import time
sys.stdout.reconfigure(encoding='utf-8')

# Read the CSV file
file_path = 'h3-data.csv'
course_data = pd.read_csv(file_path)

# Create a LAB version of each lab course
lab_course_data = course_data[course_data['Εργαστήριο (TRUE/FALSE)'] == True].copy()
lab_course_data['Μάθημα'] = lab_course_data['Μάθημα'] + ' LAB'
course_data = pd.concat([course_data, lab_course_data], ignore_index=True)

# Create a dictionary of courses with all their attributes
courses = {}
for _, row in course_data.iterrows():
    courses[row['Μάθημα']] = {
        'semester': row['Εξάμηνο'],
        'teacher': row['Καθηγητής'],
        'is_difficult': row['Δύσκολο (TRUE/FALSE)'],
    }

slots = ['9-12', '12-3', '3-6']  # 3 slots
variables = list(courses.keys())


# Constraint functions
def no_overlap(c1, t1, c2, t2):
    return t1 != t2

def same_day_theory_lab(c1, t1, c2, t2):
    if c1 == c2 + ' LAB': # if c1 and c2 have a course-lab relationship then they must be on the same day and consecutive slots
        return t1[0] == t2[0] and (slots.index(t1[1]) == slots.index(t2[1]) + 1) #lab must be in the next slot
    elif c2 == c1 + ' LAB':
        return t1[0] == t2[0] and (slots.index(t1[1]) == slots.index(t2[1]) - 1)
    return True

def different_days_teacher(c1, t1, c2, t2): # same teacher, different days
    if courses[c1]['teacher'] == courses[c2]['teacher']:
        return t1[0] != t2[0] or (c1 == c2 + ' LAB') or (c2 == c1 + ' LAB') # unless they are course-lab pairs
    return True

def same_semester(c1, t1, c2, t2): # same semester, different days
    if courses[c1]['semester'] == courses[c2]['semester']:
        return t1[0] != t2[0] or (c1 == c2 + ' LAB') or (c2 == c1 + ' LAB') # unless they are course-lab pairs
    return True

def both_difficult(c1, t1, c2, t2): # both difficult courses, different days
    if courses[c1]['is_difficult'] and courses[c2]['is_difficult']:
        return abs(t1[0] - t2[0]) >= 2 or (c1 == c2 + ' LAB') or (c2 == c1 + ' LAB') # unless they are course-lab pairs
    return True

constraint_checks = 0
def exam_constraints(c1, t1, c2, t2):
    global constraint_checks # Keep track of constraint checks
    constraint_checks += 1
    return (no_overlap(c1, t1, c2, t2) and
            same_semester(c1, t1, c2, t2) and
            both_difficult(c1, t1, c2, t2) and
            same_day_theory_lab(c1, t1, c2, t2) and
            different_days_teacher(c1, t1, c2, t2))



# define neighbors, all courses are related due to no_overlap constraint
neighbors = {course: [other_course for other_course in variables if other_course != course] for course in variables}

solution_file = open("solution.txt", "w", encoding='utf-8')
def print_solution(solution):
    for course, value in solution.items():
        print(f"{course}: {value}", file=solution_file)

def main():
    if len(sys.argv) != 4:
        print("Invalid number of arguments")
        print("Usage: python problem3.py <algorithm> <days> <times>")
        print("Example: python problem3.py fc+mrv 5 10")
        return
    # days is second arguement
    days = range(1, int(sys.argv[2])+1)
    domains = {course: [(day, slot) for day in days for slot in slots] for course in courses}
    # Create CSP
    global constraint_checks
    times = int(sys.argv[3])
    statistics = {} # store stats
    if sys.argv[1] == "fc+mrv":
        sum_time = 0
        sum_assigns = 0
        sum_checks = 0
        for i in range(times):
            # reset constraint checks
            constraint_checks = 0
            exam_csp = CSP(variables=variables, domains=domains, neighbors=neighbors, constraints=exam_constraints)
            start = time.time()
            fc_solution = backtracking_search(exam_csp, select_unassigned_variable=mrv, inference=forward_checking)
            end = time.time()
            sum_time += end-start
            sum_assigns += exam_csp.nassigns
            sum_checks += constraint_checks
        statistics["fc"] = (sum_time/times, int(sum_assigns/times), int(sum_checks/times))
        print_solution(fc_solution)
        print("FC solution saved to solution.txt!\n")
        print(f"Statistics (average of {times} runs):")
        print(f"Time: {sum_time/times}, Assigns: {int(sum_assigns/times)}, Checks: {int(sum_checks/times)}")
    elif sys.argv[1] == "mac+mrv":
        sum_time = 0
        sum_assigns = 0
        sum_checks = 0
        for i in range(times):
            # reset constraint checks
            constraint_checks = 0
            exam_csp = CSP(variables=variables, domains=domains, neighbors=neighbors, constraints=exam_constraints)
            start = time.time()
            mac_solution = backtracking_search(exam_csp, select_unassigned_variable=mrv, inference=mac)
            end = time.time()
            sum_time += end-start
            sum_assigns += exam_csp.nassigns
            sum_checks += constraint_checks
        statistics["mac"] = (sum_time/times, int(sum_assigns/times), int(sum_checks/times))
        print_solution(mac_solution)
        print("MAC solution saved to solution.txt!\n")
        print(f"Statistics (average of {times} runs):")
        print(f"Time: {sum_time/times}, Assigns: {int(sum_assigns/times)}, Checks: {int(sum_checks/times)}")
    elif sys.argv[1] == "fc+domwdeg":
        sum_time = 0
        sum_assigns = 0
        sum_checks = 0
        for i in range(times):
            # reset constraint checks
            constraint_checks = 0
            exam_csp = CSP(variables=variables, domains=domains, neighbors=neighbors, constraints=exam_constraints)
            start = time.time()
            fc_solution_dom_wdeg = backtracking_search(exam_csp, select_unassigned_variable=dom_wdeg, inference=forward_checking)
            end = time.time()
            sum_time += end-start
            sum_assigns += exam_csp.nassigns
            sum_checks += constraint_checks
        statistics["fc-dom/wdeg"] = (sum_time/times, int(sum_assigns/times), int(sum_checks/times))
        print_solution(fc_solution_dom_wdeg)
        print("FC with domwdeg solution saved to solution.txt!\n")
        print(f"Statistics (average of {times} runs):")
        print(f"Time: {sum_time/times}, Assigns: {int(sum_assigns/times)}, Checks: {int(sum_checks/times)}")
    elif sys.argv[1] == "mac+domwdeg":
        sum_time = 0
        sum_assigns = 0
        sum_checks = 0
        for i in range(times):
            # reset constraint checks
            constraint_checks = 0
            exam_csp = CSP(variables=variables, domains=domains, neighbors=neighbors, constraints=exam_constraints)
            start = time.time()
            mac_solution_dom_wdeg = backtracking_search(exam_csp, select_unassigned_variable=dom_wdeg, inference=mac)
            end = time.time()
            sum_time += end-start
            sum_assigns += exam_csp.nassigns
            sum_checks += constraint_checks
        statistics["mac-dom/wdeg"] = (sum_time/times, int(sum_assigns/times), int(sum_checks/times))
        print_solution(mac_solution_dom_wdeg)
        print("MAC with domwdeg solution saved to solution.txt!\n")
        print(f"Statistics (average of {times} runs):")
        print(f"Time: {sum_time/times}, Assigns: {int(sum_assigns/times)}, Checks: {int(sum_checks/times)}")
    elif sys.argv[1] == "min-conflicts":
        sum_time = 0
        sum_assigns = 0
        sum_checks = 0
        for i in range(times):
            # reset constraint checks
            constraint_checks = 0
            exam_csp = CSP(variables=variables, domains=domains, neighbors=neighbors, constraints=exam_constraints)
            start = time.time()
            mc_solution = min_conflicts(exam_csp)
            end = time.time()
            sum_time += end-start
            sum_assigns += exam_csp.nassigns
            sum_checks += constraint_checks
        statistics["min-conflicts"] = (sum_time/times, int(sum_assigns/times), int(sum_checks/times))
        print_solution(mc_solution)
        print("MIN-CONFLICTS solution saved to solution.txt!\n")
        print(f"Statistics (average of {times} runs):")
        print(f"Time: {sum_time/times}, Assigns: {int(sum_assigns/times)}, Checks: {int(sum_checks/times)}")
    else:
        print("Invalid argument")
        print("Valid arguments are: fc+mrv, mac+mrv, fc+domwdeg, mac+domwdeg, min-conflicts")
    

if __name__ == '__main__':
	main()