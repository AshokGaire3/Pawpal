"""
PawPal+ Tests (pytest)

Comprehensive test suite for core system behaviors:
- Task priority and duration handling
- Scheduler logic and conflict detection
- Time constraint validation
- Owner/Pet registration
"""

import pytest
from models import (
    Owner, Pet, Task, Priority, Recurrence, Scheduler, 
    DailySchedule, ScheduledTask, PawPalSystem
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def owner():
    """Standard owner for testing."""
    return Owner(name="Test Owner", available_hours_per_day=8.0)


@pytest.fixture
def pet():
    """Standard pet for testing."""
    return Pet(name="Test Pet", species="dog", age=3)


@pytest.fixture
def scheduler(owner, pet):
    """Standard scheduler for testing."""
    return Scheduler(owner, pet)


@pytest.fixture
def simple_tasks():
    """Simple task set for testing."""
    return [
        Task(
            name="Walk",
            duration_minutes=30,
            priority=Priority.HIGH,
            task_type="walk"
        ),
        Task(
            name="Feeding",
            duration_minutes=15,
            priority=Priority.HIGH,
            task_type="feed"
        ),
        Task(
            name="Play",
            duration_minutes=45,
            priority=Priority.MEDIUM,
            task_type="play"
        ),
    ]


# ============================================================================
# Owner & Pet Tests
# ============================================================================

class TestOwner:
    """Test Owner class."""
    
    def test_owner_creation(self):
        """Owner can be created with name and hours."""
        owner = Owner(name="Jordan", available_hours_per_day=6.0)
        assert owner.name == "Jordan"
        assert owner.available_hours_per_day == 6.0
    
    def test_owner_default_hours(self):
        """Owner has default 8 hours available."""
        owner = Owner(name="Alex")
        assert owner.available_hours_per_day == 8.0
    
    def test_owner_string_representation(self, owner):
        """Owner string representation shows name and hours."""
        result = str(owner)
        assert "Test Owner" in result
        assert "8.0h" in result


class TestPet:
    """Test Pet class."""
    
    def test_pet_creation(self):
        """Pet can be created with name, species, age."""
        pet = Pet(name="Fluffy", species="cat", age=5)
        assert pet.name == "Fluffy"
        assert pet.species == "cat"
        assert pet.age == 5
    
    def test_pet_special_needs(self):
        """Pet can have special needs."""
        pet = Pet(
            name="Mochi",
            species="dog",
            special_needs=["diabetic", "anxiety"]
        )
        assert len(pet.special_needs) == 2
        assert "diabetic" in pet.special_needs
    
    def test_pet_string_representation(self, pet):
        """Pet string representation includes name and species."""
        result = str(pet)
        assert "Test Pet" in result
        assert "dog" in result


# ============================================================================
# Task Tests
# ============================================================================

class TestTask:
    """Test Task class."""
    
    def test_task_creation(self):
        """Task can be created with required fields."""
        task = Task(
            name="Walk",
            duration_minutes=30,
            priority=Priority.HIGH,
            task_type="walk"
        )
        assert task.name == "Walk"
        assert task.duration_minutes == 30
        assert task.priority == Priority.HIGH
    
    def test_task_duration_hours(self):
        """Task duration converts to hours correctly."""
        task = Task(
            name="Test",
            duration_minutes=90,
            priority=Priority.MEDIUM,
            task_type="test"
        )
        assert task.duration_hours() == 1.5
    
    def test_task_with_time_constraints(self):
        """Task can have time constraints."""
        task = Task(
            name="Morning Walk",
            duration_minutes=30,
            priority=Priority.HIGH,
            task_type="walk",
            earliest_time="07:00",
            latest_time="09:00"
        )
        assert task.earliest_time == "07:00"
        assert task.latest_time == "09:00"
    
    def test_task_string_representation(self):
        """Task string representation is readable."""
        task = Task(
            name="Test Task",
            duration_minutes=45,
            priority=Priority.MEDIUM,
            task_type="test"
        )
        result = str(task)
        assert "Test Task" in result
        assert "45" in result
        assert "MEDIUM" in result


# ============================================================================
# Daily Schedule Tests
# ============================================================================

class TestDailySchedule:
    """Test DailySchedule class."""
    
    def test_schedule_creation(self, owner, pet):
        """Schedule can be created."""
        schedule = DailySchedule(owner, pet, available_hours=4.0)
        assert schedule.owner == owner
        assert schedule.pet == pet
        assert schedule.available_hours == 4.0
    
    def test_total_scheduled_time(self, owner, pet):
        """Total scheduled time is calculated correctly."""
        schedule = DailySchedule(owner, pet, available_hours=4.0)
        
        task1 = Task(
            name="Task 1", duration_minutes=30, 
            priority=Priority.HIGH, task_type="test"
        )
        task2 = Task(
            name="Task 2", duration_minutes=90,
            priority=Priority.HIGH, task_type="test"
        )
        
        st1 = ScheduledTask(task1, "08:00", "08:30")
        st2 = ScheduledTask(task2, "08:30", "10:00")
        
        schedule.add_scheduled_task(st1)
        schedule.add_scheduled_task(st2)
        
        assert schedule.total_scheduled_time() == 2.0  # 30 + 90 minutes = 2 hours
    
    def test_remaining_time(self, owner, pet):
        """Remaining time is calculated correctly."""
        schedule = DailySchedule(owner, pet, available_hours=4.0)
        
        task = Task(
            name="Task", duration_minutes=60,
            priority=Priority.HIGH, task_type="test"
        )
        st = ScheduledTask(task, "08:00", "09:00")
        schedule.add_scheduled_task(st)
        
        assert schedule.remaining_time() == 3.0
    
    def test_add_scheduled_task_success(self, owner, pet):
        """Task can be added if time is available."""
        schedule = DailySchedule(owner, pet, available_hours=4.0)
        task = Task(
            name="Test", duration_minutes=60,
            priority=Priority.HIGH, task_type="test"
        )
        st = ScheduledTask(task, "08:00", "09:00")
        
        result = schedule.add_scheduled_task(st)
        assert result is True
        assert len(schedule.scheduled_tasks) == 1
    
    def test_add_scheduled_task_insufficient_time(self, owner, pet):
        """Task cannot be added if insufficient time."""
        schedule = DailySchedule(owner, pet, available_hours=1.0)
        task = Task(
            name="Test", duration_minutes=120,
            priority=Priority.HIGH, task_type="test"
        )
        st = ScheduledTask(task, "08:00", "10:00")
        
        result = schedule.add_scheduled_task(st)
        assert result is False


# ============================================================================
# Scheduler Tests
# ============================================================================

class TestScheduler:
    """Test Scheduler class."""
    
    def test_scheduler_creation(self, owner, pet):
        """Scheduler can be created."""
        scheduler = Scheduler(owner, pet)
        assert scheduler.owner == owner
        assert scheduler.pet == pet
    
    def test_schedule_day_empty_tasks(self, scheduler):
        """Schedule with no tasks produces empty schedule."""
        schedule = scheduler.schedule_day([])
        assert len(schedule.scheduled_tasks) == 0
        assert schedule.total_scheduled_time() == 0.0
    
    def test_schedule_day_high_priority_first(self, scheduler):
        """High priority tasks are scheduled before low priority."""
        tasks = [
            Task(
                name="Low Priority",
                duration_minutes=60,
                priority=Priority.LOW,
                task_type="play"
            ),
            Task(
                name="High Priority",
                duration_minutes=30,
                priority=Priority.HIGH,
                task_type="feed"
            ),
        ]
        
        schedule = scheduler.schedule_day(tasks, available_hours=1.0)
        
        # With only 1 hour available and both tasks (90 min total),
        # high priority should fit, low should not
        assert len(schedule.scheduled_tasks) == 1
        assert schedule.scheduled_tasks[0].task.name == "High Priority"
        assert len(schedule.unscheduled_tasks) == 1
    
    def test_schedule_day_respects_time_constraints(self, scheduler):
        """First task placed respects time constraints."""
        task_early = Task(
            name="Early Task",
            duration_minutes=30,
            priority=Priority.HIGH,
            task_type="test",
            earliest_time="07:00",
            latest_time="08:30"
        )
        
        schedule = scheduler.schedule_day([task_early], available_hours=8.0)
        
        # Task should be scheduled
        assert len(schedule.scheduled_tasks) == 1
        scheduled = schedule.scheduled_tasks[0]
        assert scheduled.start_time >= "07:00"
        assert scheduled.end_time <= "08:30"
    
    def test_schedule_insufficient_total_time(self, scheduler):
        """Scheduler handles insufficient total time."""
        tasks = [
            Task(name="A", duration_minutes=60, priority=Priority.HIGH, task_type="test"),
            Task(name="B", duration_minutes=60, priority=Priority.HIGH, task_type="test"),
            Task(name="C", duration_minutes=60, priority=Priority.MEDIUM, task_type="test"),
        ]
        
        schedule = scheduler.schedule_day(tasks, available_hours=2.0)
        
        # Both high priority should fit, medium should not
        assert len(schedule.scheduled_tasks) == 2
        assert len(schedule.unscheduled_tasks) == 1
    
    def test_minutes_to_time_conversion(self):
        """Minute to time conversion works."""
        assert Scheduler._minutes_to_time(480) == "08:00"  # 8*60
        assert Scheduler._minutes_to_time(540) == "09:00"  # 9*60
        assert Scheduler._minutes_to_time(495) == "08:15"  # 8:15
    
    def test_time_to_minutes_conversion(self):
        """Time to minute conversion works."""
        assert Scheduler._time_to_minutes("08:00") == 480
        assert Scheduler._time_to_minutes("09:00") == 540
        assert Scheduler._time_to_minutes("08:15") == 495


# ============================================================================
# System Tests
# ============================================================================

class TestPawPalSystem:
    """Test PawPalSystem class."""
    
    def test_system_creation(self):
        """System can be created."""
        system = PawPalSystem()
        assert len(system.owners) == 0
        assert len(system.pets) == 0
    
    def test_register_owner(self):
        """Owner can be registered."""
        system = PawPalSystem()
        owner = Owner(name="Owner 1")
        system.register_owner(owner)
        
        assert "Owner 1" in system.owners
        assert system.owners["Owner 1"] == owner
    
    def test_register_pet(self):
        """Pet can be registered."""
        system = PawPalSystem()
        pet = Pet(name="Pet 1", species="dog")
        owner = Owner(name="Owner 1")
        system.register_owner(owner)
        system.register_pet(pet, "Owner 1")
        
        assert "Pet 1" in system.pets
        assert system.pets["Pet 1"] == pet
    
    def test_add_task(self):
        """Task can be added to a pet."""
        system = PawPalSystem()
        pet = Pet(name="Pet 1", species="dog")
        task = Task(
            name="Walk", duration_minutes=30,
            priority=Priority.HIGH, task_type="walk"
        )
        
        system.register_pet(pet, "Owner 1")
        system.add_task("Pet 1", task)
        
        assert len(system.tasks["Pet 1"]) == 1
        assert system.tasks["Pet 1"][0] == task
    
    def test_generate_schedule(self):
        """Schedule can be generated through system."""
        system = PawPalSystem()
        owner = Owner(name="Owner 1", available_hours_per_day=4.0)
        pet = Pet(name="Pet 1", species="dog")
        task = Task(
            name="Walk", duration_minutes=60,
            priority=Priority.HIGH, task_type="walk"
        )
        
        system.register_owner(owner)
        system.register_pet(pet, "Owner 1")
        system.add_task("Pet 1", task)
        
        schedule = system.generate_schedule("Owner 1", "Pet 1")
        
        assert schedule is not None
        assert len(schedule.scheduled_tasks) == 1


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration:
    """Integration tests for complete workflows."""
    
    def test_full_workflow(self):
        """Complete workflow: create owner, pet, tasks, schedule."""
        system = PawPalSystem()
        
        # Register
        owner = Owner(name="Jordan", available_hours_per_day=3.0)
        pet = Pet(name="Mochi", species="dog")
        system.register_owner(owner)
        system.register_pet(pet, "Jordan")
        
        # Add tasks
        tasks = [
            Task(
                name="Walk", duration_minutes=45,
                priority=Priority.HIGH, task_type="walk",
                earliest_time="07:00", latest_time="09:00"
            ),
            Task(
                name="Feed", duration_minutes=20,
                priority=Priority.HIGH, task_type="feed"
            ),
            Task(
                name="Play", duration_minutes=60,
                priority=Priority.MEDIUM, task_type="play"
            ),
        ]
        
        for task in tasks:
            system.add_task("Mochi", task)
        
        # Generate schedule
        schedule = system.generate_schedule("Jordan", "Mochi")
        
        # Verify
        assert schedule is not None
        assert schedule.pet.name == "Mochi"
        assert schedule.owner.name == "Jordan"
        assert len(schedule.scheduled_tasks) > 0
        assert schedule.total_scheduled_time() <= 3.0
