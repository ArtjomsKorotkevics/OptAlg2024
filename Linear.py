import time
from ortools.linear_solver import pywraplp

def plan_jobs_lp(num_jobs, jobs_data):
    # Izveidojam lineārās programmēšanas solveri
    solver = pywraplp.Solver.CreateSolver('SCIP')

    if not solver:
        print("Solver not found.")
        return

    # Definējam mainīgos: sākuma un beigu laikus katram darbam
    job_starts = [solver.IntVar(0, job['deadline'], f'start_{i}') for i, job in enumerate(jobs_data)]
    job_ends = [solver.IntVar(0, job['deadline'], f'end_{i}') for i, job in enumerate(jobs_data)]

    # Pievienojam attiecības starp sākuma un beigu laikiem
    for i, job in enumerate(jobs_data):
        solver.Add(job_ends[i] == job_starts[i] + job['duration'])

    # Ierobežojums: viens resurss nevar būt aktīvs vienlaikus diviem darbiem
    resources = set([job['resource'] for job in jobs_data])
    for resource in resources:
        jobs_using_resource = [i for i, job in enumerate(jobs_data) if job['resource'] == resource]
        for i in jobs_using_resource:
            for j in jobs_using_resource:
                if i < j:
                    solver.Add(job_starts[i] >= job_ends[j] or job_starts[j] >= job_ends[i])

    # Mērķis: minimizēt visu darbu beigu laiku, ņemot vērā prioritātes
    total_end_time = solver.Sum([job_ends[i] for i in range(num_jobs)])
    total_priority = solver.Sum([(job['deadline'] - job_ends[i]) * job['priority'] for i in range(num_jobs)])
    solver.Maximize(total_priority - total_end_time)

    # Risināt problēmu
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print(f'Total end time: {total_end_time.solution_value()}')
        print(f'Total priority score: {total_priority.solution_value()}')
        # Sagatavojam darbus izvadei pēc to sākuma laika
        sorted_jobs = sorted([(i, job_starts[i].solution_value(), job_ends[i].solution_value()) 
                              for i in range(num_jobs)], key=lambda x: x[1])
        for i, start, end in sorted_jobs:
            job = jobs_data[i]
            print(f'Job {job["name"]} starts at {start} and ends at {end}')
    else:
        print("No solution found.")

start_time = time.time()
# Testa dati
num_small = 5
small_scenario = [
    {'name': 'Job1', 'duration': 2, 'deadline': 5, 'resource': 'A', 'priority': 3},
    {'name': 'Job2', 'duration': 1, 'deadline': 3, 'resource': 'B', 'priority': 2},
    {'name': 'Job3', 'duration': 3, 'deadline': 8, 'resource': 'A', 'priority': 1},
    {'name': 'Job4', 'duration': 2, 'deadline': 6, 'resource': 'B', 'priority': 3},
    {'name': 'Job5', 'duration': 1, 'deadline': 1, 'resource': 'C', 'priority': 2}
]
num_medium = 10
medium_scenario = [
    {'name': 'Job1', 'duration': 2, 'deadline': 7, 'resource': 'A', 'priority': 1},
    {'name': 'Job2', 'duration': 3, 'deadline': 9, 'resource': 'B', 'priority': 3},
    {'name': 'Job3', 'duration': 1, 'deadline': 4, 'resource': 'C', 'priority': 2},
    {'name': 'Job4', 'duration': 2, 'deadline': 5, 'resource': 'A', 'priority': 3},
    {'name': 'Job5', 'duration': 4, 'deadline': 10, 'resource': 'B', 'priority': 1},
    {'name': 'Job6', 'duration': 1, 'deadline': 3, 'resource': 'C', 'priority': 2},
    {'name': 'Job7', 'duration': 2, 'deadline': 8, 'resource': 'A', 'priority': 1},
    {'name': 'Job8', 'duration': 3, 'deadline': 6, 'resource': 'B', 'priority': 3},
    {'name': 'Job9', 'duration': 1, 'deadline': 5, 'resource': 'C', 'priority': 2},
    {'name': 'Job10', 'duration': 2, 'deadline': 7, 'resource': 'A', 'priority': 1}
]
num_large = 20
large_scenario = [
    {'name': 'Job1', 'duration': 2, 'deadline': 7, 'resource': 'A', 'priority': 1},
    {'name': 'Job2', 'duration': 3, 'deadline': 9, 'resource': 'B', 'priority': 3},
    {'name': 'Job3', 'duration': 1, 'deadline': 4, 'resource': 'C', 'priority': 2},
    {'name': 'Job4', 'duration': 2, 'deadline': 5, 'resource': 'A', 'priority': 3},
    {'name': 'Job5', 'duration': 4, 'deadline': 10, 'resource': 'B', 'priority': 1},
    {'name': 'Job6', 'duration': 1, 'deadline': 3, 'resource': 'C', 'priority': 2},
    {'name': 'Job7', 'duration': 2, 'deadline': 8, 'resource': 'A', 'priority': 1},
    {'name': 'Job8', 'duration': 3, 'deadline': 6, 'resource': 'B', 'priority': 3},
    {'name': 'Job9', 'duration': 1, 'deadline': 5, 'resource': 'C', 'priority': 2},
    {'name': 'Job10', 'duration': 2, 'deadline': 7, 'resource': 'A', 'priority': 1},
    {'name': 'Job11', 'duration': 3, 'deadline': 12, 'resource': 'A', 'priority': 3},
    {'name': 'Job12', 'duration': 2, 'deadline': 18, 'resource': 'B', 'priority': 1},
    {'name': 'Job13', 'duration': 4, 'deadline': 22, 'resource': 'C', 'priority': 2},
    {'name': 'Job14', 'duration': 1, 'deadline': 15, 'resource': 'A', 'priority': 3},
    {'name': 'Job15', 'duration': 2, 'deadline': 16, 'resource': 'B', 'priority': 1},
    {'name': 'Job16', 'duration': 3, 'deadline': 19, 'resource': 'C', 'priority': 1},
    {'name': 'Job17', 'duration': 1, 'deadline': 14, 'resource': 'A', 'priority': 1},
    {'name': 'Job18', 'duration': 2, 'deadline': 17, 'resource': 'B', 'priority': 1},
    {'name': 'Job19', 'duration': 4, 'deadline': 19, 'resource': 'C', 'priority': 2},
    {'name': 'Job20', 'duration': 1, 'deadline': 15, 'resource': 'A', 'priority': 3}
]



# Palaižam algoritmu ar testa datiem
plan_jobs_lp(num_small, small_scenario)
end_time = time.time()

execution_time = end_time - start_time
print(f"Izpildes laiks: {execution_time:.4f} sekundes")
