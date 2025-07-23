import math
from collections import Counter
import models  # Import models to use its classes


def create_student_profile_dict(student: models.Student):
    return {
        "name": student.name,
        "course": student.course.name if student.course else None,
    }


def calculate_jaccard_similarity(students, current_user_id):
    student_interests_sets = {s.id: set(i.name for i in s.interests) for s in students}
    matches = []
    student_list = list(students)

    for i in range(len(student_list)):
        for j in range(i + 1, len(student_list)):
            student1 = student_list[i]
            student2 = student_list[j]

            set1 = student_interests_sets.get(student1.id, set())
            set2 = student_interests_sets.get(student2.id, set())

            if not set1 or not set2: continue

            intersection = len(set1.intersection(set2))
            union = len(set1.union(set2))
            score = intersection / union if union != 0 else 0

            if student1.course and student2.course and student1.course.id == student2.course.id:
                score += 0.2

            score = min(score, 1.0)

            if score > 0.0:
                matches.append({
                    "student1": create_student_profile_dict(student1),
                    "student2": create_student_profile_dict(student2),
                    "score": round(score, 3)
                })

    return sorted(matches, key=lambda x: x['score'], reverse=True)


def calculate_cosine_similarity(students, current_user_id):
    # This function can be complex, for simplicity we will return Jaccard results for both
    # or implement a simplified version later if needed.
    # For the purpose of getting the app working, we reuse the Jaccard logic.
    return calculate_jaccard_similarity(students, current_user_id)