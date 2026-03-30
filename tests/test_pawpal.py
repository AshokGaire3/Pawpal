"""
Basic tests for PawPal+ — run with:  python -m pytest
"""

import sys
import os

# Allow imports from the parent directory (where pawpal_system.py lives)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet


def test_task_completion():
    """mark_complete() should flip completed from False to True."""
    task = Task("Morning walk", duration_minutes=30, priority="high", frequency="daily")

    assert task.completed is False  # starts incomplete

    task.mark_complete()

    assert task.completed is True   # now marked done


def test_add_task_increases_pet_task_count():
    """Adding a task to a Pet should increase its task count by 1."""
    pet = Pet(name="Mochi", species="dog")

    assert len(pet.get_tasks()) == 0  # no tasks yet

    pet.add_task(Task("Breakfast feeding", duration_minutes=10, priority="high", frequency="daily"))

    assert len(pet.get_tasks()) == 1  # one task added
