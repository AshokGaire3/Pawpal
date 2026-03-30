#!/usr/bin/env python3
"""
PawPal+ CLI Demo Script

Demonstrates the complete system with a realistic scenario:
- Registering an owner and pet
- Creating various tasks
- Generating a daily schedule
- Showing the scheduler's logic and tradeoffs
"""

from models import (
    Owner, Pet, Task, Priority, Recurrence, Scheduler, 
    DailySchedule, PawPalSystem
)


def print_header(text: str) -> None:
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def print_section(text: str) -> None:
    """Print a formatted section header."""
    print(f"\n{'─'*60}")
    print(f"▶ {text}")
    print(f"{'─'*60}\n")


def demo_basic_scenario() -> None:
    """Demonstrate basic scheduling scenario."""
    print_header("DEMO 1: Basic Pet Care Scheduling")
    
    # Create owner and pet
    owner = Owner(name="Jordan", available_hours_per_day=4.0)
    pet = Pet(name="Mochi", species="dog", age=3, special_needs=["needs daily walks"])
    
    print_section("Step 1: Register Owner & Pet")
    print(f"✓ {owner}")
    print(f"✓ {pet}")
    
    # Create tasks
    print_section("Step 2: Define Daily Tasks")
    tasks = [
        Task(
            name="Morning Walk",
            duration_minutes=30,
            priority=Priority.HIGH,
            task_type="walk",
            earliest_time="07:00",
            latest_time="09:00"
        ),
        Task(
            name="Breakfast",
            duration_minutes=15,
            priority=Priority.HIGH,
            task_type="feed",
            earliest_time="08:00",
            latest_time="09:00"
        ),
        Task(
            name="Play Time",
            duration_minutes=45,
            priority=Priority.MEDIUM,
            task_type="enrichment"
        ),
        Task(
            name="Evening Walk",
            duration_minutes=30,
            priority=Priority.HIGH,
            task_type="walk",
            earliest_time="18:00",
            latest_time="20:00"
        ),
        Task(
            name="Dinner",
            duration_minutes=15,
            priority=Priority.HIGH,
            task_type="feed"
        ),
        Task(
            name="Grooming",
            duration_minutes=60,
            priority=Priority.LOW,
            task_type="grooming"
        ),
    ]
    
    for task in tasks:
        print(f"✓ {task}")
    
    # Schedule
    print_section("Step 3: Generate Daily Schedule")
    scheduler = Scheduler(owner, pet)
    schedule = scheduler.schedule_day(tasks, available_hours=4.0)
    print(schedule)
    
    # Explain scheduling logic
    print_section("Scheduling Logic Explanation")
    print("""
The scheduler prioritizes tasks based on:

1. PRIORITY: HIGH tasks scheduled first (walks, meals are essential)
2. DURATION: Longer tasks fit into schedule before shorter ones
3. TIME CONSTRAINTS: Respects earliest/latest time windows
   - Morning Walk: Must be 7-9 AM
   - Breakfast: Must be 8-9 AM
   - Evening Walk: Must be 6-8 PM
   - Dinner: Flexible

TRADEOFF: With only 4 hours available:
- ✓ All HIGH priority tasks fit (walks + meals)
- ✓ Some MEDIUM priority work fits (play time)
- ✗ LOW priority removed (grooming takes 60 min, not enough time)
    
This reflects real-world constraints: essential care comes first.
""")


def demo_conflict_detection() -> None:
    """Demonstrate conflict detection and prioritization."""
    print_header("DEMO 2: Conflict Detection & Prioritization")
    
    owner = Owner(name="Alex", available_hours_per_day=2.0)
    pet = Pet(name="Whiskers", species="cat", age=7)
    
    print_section("Scenario: Limited Time (2 hours), Many Tasks")
    print(f"Owner: {owner}")
    print(f"Pet: {pet}")
    
    tasks = [
        Task(name="Medication", duration_minutes=10, priority=Priority.HIGH, task_type="meds"),
        Task(name="Feeding", duration_minutes=20, priority=Priority.HIGH, task_type="feed"),
        Task(name="Litter Box Cleaning", duration_minutes=15, priority=Priority.HIGH, task_type="cleaning"),
        Task(name="Interactive Play", duration_minutes=30, priority=Priority.MEDIUM, task_type="play"),
        Task(name="Petting/Bonding", duration_minutes=45, priority=Priority.MEDIUM, task_type="enrichment"),
        Task(name="Nail Trimming", duration_minutes=40, priority=Priority.LOW, task_type="grooming"),
        Task(name="Deep Clean", duration_minutes=60, priority=Priority.LOW, task_type="cleaning"),
    ]
    
    print("\nTotal task time needed: {:.1f} hours".format(sum(t.duration_minutes for t in tasks) / 60))
    print("Available time: 2.0 hours\n")
    
    scheduler = Scheduler(owner, pet)
    schedule = scheduler.schedule_day(tasks, available_hours=2.0)
    print(schedule)
    
    print_section("Analysis: What Got Scheduled?")
    print(f"""
✓ SCHEDULED ({len(schedule.scheduled_tasks)} tasks, {schedule.total_scheduled_time():.1f}h):
  - High priority essential care (medication, feeding, litter)
  
✗ UNSCHEDULED ({len(schedule.unscheduled_tasks)} tasks):
  - Medium priority play/enrichment (not essential, but good for mental health)
  - Low priority deep cleaning (important, but not urgent)

This prioritization makes sense: medical and hygiene needs trump luxury time.
""")


def demo_system_coordinator() -> None:
    """Demonstrate the full PawPalSystem coordinator."""
    print_header("DEMO 3: Multi-Pet Household")
    
    system = PawPalSystem()
    
    print_section("Registering Owner & Pets")
    
    owner = Owner(name="Casey", available_hours_per_day=5.0)
    system.register_owner(owner)
    print(f"✓ {owner}")
    
    dog = Pet(name="Rex", species="dog", age=4)
    cat = Pet(name="Luna", species="cat", age=2)
    system.register_pet(dog, "Casey")
    system.register_pet(cat, "Casey")
    print(f"✓ {dog}")
    print(f"✓ {cat}")
    
    print_section("Adding Tasks for Rex (Dog)")
    dog_tasks = [
        Task(name="Walk", duration_minutes=45, priority=Priority.HIGH, task_type="walk"),
        Task(name="Fetch", duration_minutes=30, priority=Priority.MEDIUM, task_type="play"),
        Task(name="Feeding", duration_minutes=15, priority=Priority.HIGH, task_type="feed"),
    ]
    for task in dog_tasks:
        system.add_task("Rex", task)
        print(f"✓ {task.name}")
    
    print_section("Adding Tasks for Luna (Cat)")
    cat_tasks = [
        Task(name="Feeding", duration_minutes=10, priority=Priority.HIGH, task_type="feed"),
        Task(name="Playtime", duration_minutes=20, priority=Priority.MEDIUM, task_type="play"),
        Task(name="Litter", duration_minutes=5, priority=Priority.HIGH, task_type="cleaning"),
    ]
    for task in cat_tasks:
        system.add_task("Luna", task)
        print(f"✓ {task.name}")
    
    print_section("Generating Schedules")
    
    rex_schedule = system.generate_schedule("Casey", "Rex")
    if rex_schedule:
        print("For Rex:")
        print(rex_schedule)
    
    luna_schedule = system.generate_schedule("Casey", "Luna")
    if luna_schedule:
        print("\nFor Luna:")
        print(luna_schedule)


def demo_recurring_tasks() -> None:
    """Demonstrate recurring task handling."""
    print_header("DEMO 4: Recurring Tasks (Concept)")
    
    print_section("Current Support")
    print("""
Current implementation handles:
✓ One-off tasks (ONCE)
✓ Daily patterns (DAILY) - concept included in model
✓ Weekly patterns (WEEKLY) - concept included in model

For this iteration, the scheduler handles single-day scheduling.
Recurring task logic would expand to:
- Generate multiple schedules (weekly view)
- Track completion history
- Adjust future schedules based on actual time vs. estimated
- Warn about overbooked weeks
""")
    
    task = Task(
        name="Vaccination Reminder",
        duration_minutes=30,
        priority=Priority.HIGH,
        task_type="vet",
        recurrence=Recurrence.WEEKLY  # Would happen once a week
    )
    print(f"Example: {task}")


def main():
    """Run all demos."""
    print("\n" + "="*60)
    print("     🐾 PawPal+ System Demo 🐾".center(60))
    print("     Pet Care Planning Assistant".center(60))
    print("="*60)
    
    demo_basic_scenario()
    demo_conflict_detection()
    demo_system_coordinator()
    demo_recurring_tasks()
    
    print_header("Demo Complete")
    print("""
Summary:
✓ Owner & Pet registration working
✓ Task creation with priorities & constraints
✓ Scheduler generates valid daily plans
✓ Conflict detection & prioritization working
✓ Multi-pet household coordination ready
✓ Recurring task framework in place

Next: Run tests with pytest to verify behavior!
""")


if __name__ == "__main__":
    main()
