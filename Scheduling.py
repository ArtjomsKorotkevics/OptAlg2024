import time
from ortools.sat.python import cp_model

def plan_jobs(num_jobs, jobs_data):
    # Izveidojam modeli
    model = cp_model.CpModel()

    # Definējam mainīgos: sākuma un beigu laikus katram darbam
    job_starts = []
    job_intervals = []
    job_ends = []
    penalties = []
    for i in range(num_jobs):
        duration = jobs_data[i]['duration']
        latest_end = jobs_data[i]['deadline']
        priority = jobs_data[i]['priority']
        job_starts.append(model.NewIntVar(0, latest_end, f'start_{i}'))
        job_end = model.NewIntVar(0, latest_end, f'end_{i}')
        job_ends.append(job_end)
        job_intervals.append(model.NewIntervalVar(job_starts[i], duration, job_end, f'interval_{i}'))
        # Pievienojam sodu par vēlu darbu pabeigšanu, atkarībā no prioritātes
        penalty = model.NewIntVar(0, 1000, f'penalty_{i}')
        model.Add(penalty == (latest_end - job_end) * priority)
        penalties.append(penalty)

    # Ierobežojums: viens resurss nevar būt aktīvs vienlaikus diviem darbiem
    resources = set([job['resource'] for job in jobs_data])
    for resource in resources:
        jobs_using_resource = [i for i in range(num_jobs) if jobs_data[i]['resource'] == resource]
        model.AddNoOverlap([job_intervals[i] for i in jobs_using_resource])

    # Mērķis: minimizēt visu darbu beigu laiku un maksimizēt prioritāšu sodus
    max_end_time = model.NewIntVar(0, max(j['deadline'] for j in jobs_data), 'max_end_time')
    model.AddMaxEquality(max_end_time, job_ends)
    total_penalty = model.NewIntVar(0, 100000, 'total_penalty')
    model.Add(total_penalty == sum(penalties))
    model.Minimize(max_end_time - total_penalty)

    # Risināt modeli
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f'Total end time: {solver.Value(max_end_time)}')
        print(f'Total priority penalty: {solver.Value(total_penalty)}')
        sorted_jobs = sorted([(i, solver.Value(job_starts[i]), solver.Value(job_ends[i])) 
                              for i in range(num_jobs)], key=lambda x: x[1])
        for i, start, end in sorted_jobs:
            print(f'{jobs_data[i]["name"]} starts at {start} and ends at {end}')
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
    {'name': 'Job5', 'duration': 1, 'deadline': 4, 'resource': 'A', 'priority': 2}
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
plan_jobs(num_small, small_scenario)
end_time = time.time()

execution_time = end_time - start_time
print(f"Izpildes laiks: {execution_time:.4f} sekundes")