# app/backend/matching.py

"""
This module contains the core logic for calculating similarity scores
between students based on their interests and courses.
"""

import models


def create_admin_profile_dict(student: models.Student):
    """
    Helper function to create a simplified dictionary representation of a student
    for the admin dashboard view.
    """
    return {"name": student.name, "course": student.course.name if student.course else "N/A"}


def calculate_jaccard_for_admin(students):
    """
    Calculates pairwise Jaccard similarity scores for all students.
    This is used for the admin dashboard.

    Jaccard Index = (Size of Intersection) / (Size of Union)
    """
    # Create a dictionary to hold sets of interest names for each student for efficient lookups.
    student_interests_sets = {s.id: set(i.name for i in s.interests) for s in students}
    matches = []
    student_list = list(students)  # Create a list for indexed access.

    # Iterate through every unique pair of students (i, j) where j > i.
    for i in range(len(student_list)):
        for j in range(i + 1, len(student_list)):
            student1, student2 = student_list[i], student_list[j]
            set1 = student_interests_sets.get(student1.id, set())
            set2 = student_interests_sets.get(student2.id, set())

            # If either student has no interests, they cannot be matched. Skip to the next pair.
            if not set1 or not set2:
                continue

            # Calculate the Jaccard Index.
            intersection = len(set1.intersection(set2))
            union = len(set1.union(set2))
            score = intersection / union if union != 0 else 0

            # Add a bonus to the score if students are enrolled in the same course.
            if student1.course and student2.course and student1.course.id == student2.course.id:
                score += 0.2

            # Cap the score at 1.0 to ensure it remains a valid proportion.
            score = min(score, 1.0)

            # Only include pairs with a match score greater than zero.
            if score > 0.0:
                matches.append({
                    "student1": create_admin_profile_dict(student1),
                    "student2": create_admin_profile_dict(student2),
                    "score": round(score, 3)  # Round for cleaner presentation.
                })

    # Return the list of matches, sorted from the highest score to the lowest.
    return sorted(matches, key=lambda x: x['score'], reverse=True)


def calculate_dice_for_admin(students):
    """
    Calculates pairwise Dice Coefficient similarity scores for all students.
    This is used for the admin dashboard.

    Dice Coefficient = 2 * (Size of Intersection) / (Sum of Sizes of Both Sets)
    """
    # Create a dictionary to hold sets of interest names for each student for efficient lookups.
    student_interests_sets = {s.id: set(i.name for i in s.interests) for s in students}
    matches = []
    student_list = list(students)  # Create a list for indexed access.

    # Iterate through every unique pair of students (i, j) where j > i.
    for i in range(len(student_list)):
        for j in range(i + 1, len(student_list)):
            student1, student2 = student_list[i], student_list[j]
            set1 = student_interests_sets.get(student1.id, set())
            set2 = student_interests_sets.get(student2.id, set())

            # If either student has no interests, they cannot be matched. Skip to the next pair.
            if not set1 or not set2:
                continue

            # Calculate the Dice Coefficient.
            intersection = len(set1.intersection(set2))
            sum_of_lengths = len(set1) + len(set2)
            score = (2 * intersection) / sum_of_lengths if sum_of_lengths != 0 else 0

            # Add a bonus to the score if students are enrolled in the same course.
            if student1.course and student2.course and student1.course.id == student2.course.id:
                score += 0.2

            # Cap the score at 1.0 to ensure it remains a valid proportion.
            score = min(score, 1.0)

            # Only include pairs with a match score greater than zero.
            if score > 0.0:
                matches.append({
                    "student1": create_admin_profile_dict(student1),
                    "student2": create_admin_profile_dict(student2),
                    "score": round(score, 3)  # Round for cleaner presentation.
                })

    # Return the list of matches, sorted from the highest score to the lowest.
    return sorted(matches, key=lambda x: x['score'], reverse=True)


def calculate_matches_for_user(students, current_user_id):
    """
    Calculates match scores for a specific logged-in user against all other users.
    This uses the Jaccard Index as the base calculation.
    """
    matches = []
    # Find the full student object for the currently logged-in user.
    current_user_obj = next((s for s in students if s.id == current_user_id), None)

    # If the user doesn't exist or has no interests, return an empty list of matches.
    if not current_user_obj or not current_user_obj.interests:
        return []

    current_user_interests = set(i.name for i in current_user_obj.interests)

    # Iterate through all other students to compare them with the current user.
    for other_student in students:
        if other_student.id == current_user_id:
            continue  # Don't match a user with themselves.

        other_student_interests = set(i.name for i in other_student.interests)
        if not other_student_interests:
            continue  # Skip users with no interests.

        # Calculate the Jaccard Index.
        intersection = len(current_user_interests.intersection(other_student_interests))
        union = len(current_user_interests.union(other_student_interests))
        score = intersection / union if union != 0 else 0

        # Add a bonus if they share the same course.
        if current_user_obj.course and other_student.course and current_user_obj.course.id == other_student.course.id:
            score += 0.2

        score = min(score, 1.0)

        if score > 0.0:
            matches.append({"student": other_student, "score": score})

    # Sort the matches from highest score to lowest.
    return sorted(matches, key=lambda x: x['score'], reverse=True)