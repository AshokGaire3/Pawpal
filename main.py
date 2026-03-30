"""
PawPal+ CLI demo — run with:  python main.py
"""

from pawpal_system import Task, Pet, Owner, Scheduler


# ---------------------------------------------------------------------------
# 1. Create owner
# ---------------------------------------------------------------------------

jordan = Owner(name="Jordan", available_minutes_per_day=180)

# ---------------------------------------------------------------------------
# 2. Create pets
# ---------------------------------------------------------------------------

mochi = Pet(name="Mochi", species="dog", age_years=3)
luna  = Pet(name="Luna",  species="cat", age_years=5)

# ---------------------------------------------------------------------------
# 3. Add tasks to Mochi (dog)
# ---------------------------------------------------------------------------

mochi.add_task(Task("Morning walk",       duration_minutes=30, priority="high",   frequency="daily"))
mochi.add_task(Task("Breakfast feeding",  duration_minutes=10, priority="high",   frequency="daily"))
mochi.add_task(Task("Obedience training", duration_minutes=20, priority="medium", frequency="daily"))
mochi.add_task(Task("Flea treatment",     duration_minutes=15, priority="high",   frequency="weekly"))

# ---------------------------------------------------------------------------
# 4. Add tasks to Luna (cat)
# ---------------------------------------------------------------------------

luna.add_task(Task("Dinner feeding",   duration_minutes=10, priority="high",   frequency="daily"))
luna.add_task(Task("Litter box clean", duration_minutes=10, priority="medium", frequency="daily"))
luna.add_task(Task("Playtime",         duration_minutes=25, priority="low",    frequency="daily"))
luna.add_task(Task("Vet check-up",     duration_minutes=60, priority="high",   frequency="as_needed"))

# ---------------------------------------------------------------------------
# 5. Register pets with owner
# ---------------------------------------------------------------------------

jordan.add_pet(mochi)
jordan.add_pet(luna)

# ---------------------------------------------------------------------------
# 6. Build today's schedule
# ---------------------------------------------------------------------------

scheduler = Scheduler(owner=jordan)
plan = scheduler.build_daily_plan()

# ---------------------------------------------------------------------------
# 7. Print results
# ---------------------------------------------------------------------------

print("=" * 55)
print("        PawPal+  --  Today's Schedule")
print("=" * 55)
print()
print(scheduler.summary(plan))

# -- Unscheduled tasks (didn't fit in time budget) --
skipped = scheduler.get_unscheduled_tasks(plan)
if skipped:
    print()
    print("Tasks that did not fit today's time budget:")
    for pet, task in skipped:
        print(f"  * {task.description} ({pet.name}, {task.duration_minutes} min, priority={task.priority})")

# -- Conflict check --
conflicts = scheduler.detect_conflicts(plan)
if conflicts:
    print()
    print("Scheduling conflicts detected:")
    for c in conflicts:
        print(f"  * {c}")
else:
    print()
    print("No scheduling conflicts.")

print()
print("=" * 55)
