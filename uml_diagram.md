# PawPal+ — Mermaid.js Class Diagram

```mermaid
classDiagram

    class Task {
        +str description
        +int duration_minutes
        +str priority
        +str frequency
        +str start_time
        +bool completed
        +date last_completed_date
        +date next_due_date
        +mark_complete(on_date) None
        +reset() None
        +is_due(on_date) bool
        +priority_rank() int
        +end_time() str
    }

    class Pet {
        +str name
        +str species
        +float age_years
        -list _tasks
        +add_task(task) None
        +remove_task(description) bool
        +get_tasks() list
        +get_due_tasks(on_date) list
        +reset_daily_tasks() None
        +total_task_time() int
    }

    class Owner {
        +str name
        +int available_minutes_per_day
        -list _pets
        +add_pet(pet) None
        +remove_pet(name) bool
        +get_pets() list
        +get_all_tasks() list
        +get_all_due_tasks(on_date) list
        +total_due_minutes(on_date) int
    }

    class Scheduler {
        +Owner owner
        +build_daily_plan(on_date) list
        +sort_by_time(tasks) list
        +filter_tasks(pet_name, completed) list
        +detect_conflicts(plan) list
        +detect_time_conflicts(pairs) list
        +get_unscheduled_tasks(plan, on_date) list
        +advance_day() None
        +summary(plan) str
    }

    Owner "1" *-- "0..*" Pet   : owns
    Pet   "1" *-- "0..*" Task  : has
    Scheduler --> Owner        : schedules for
    Scheduler ..> Pet          : reads via Owner
    Scheduler ..> Task         : reads via Pet
```

## Relationship key

| Symbol | Meaning |
|--------|---------|
| `*--`  | Composition — child cannot exist without the parent |
| `-->`  | Association — Scheduler holds a direct reference to Owner |
| `..>`  | Dependency — Scheduler reads Pet/Task but does not own them |

## Data flow (how Scheduler reaches tasks)

```
Scheduler.build_daily_plan()
    └── owner.get_all_due_tasks()
            └── pet.get_due_tasks()
                    └── task.is_due()

Scheduler.sort_by_time(tasks)
    └── sorted(..., key=lambda t: t.start_time or "99:99")

Scheduler.detect_time_conflicts()
    └── owner.get_all_tasks()
            └── compare HH:MM windows pairwise
```
