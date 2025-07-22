# app/backend/matching.py
import math
from collections import Counter

COURSE_BOOST = 0.2


def get_course_name(student, students_with_courses):
    # Helper to find course name from student object
    for s in students_with_courses:
        if s.id == student.id:
            # Assuming the student object has a relationship to course
            return s.course.name if s.course else ""
    return ""


def calculate_jaccard_similarity(students, current_user_id):
    student_interests_sets = {s.id: set(i.name for i in s.interests) for s in students}
    matches = []

    current_user_set = student_interests_sets.get(current_user_id)
    if not current_user_set:
        return []

    for other_student in students:
        if other_student.id == current_user_id:
            continue

        other_student_set = student_interests_sets.get(other_student.id)
        if not other_student_set:
            continue

        intersection = len(current_user_set.intersection(other_student_set))
        union = len(current_user_set.union(other_student_set))
        score = intersection / union if union != 0 else 0

        current_user_obj = next((s for s in students if s.id == current_user_id), None)
        if current_user_obj.course and other_student.course and current_user_obj.course.id == other_student.course.id:
            score += COURSE_BOOST

        score = min(score, 1.0)

        if score > 0.0:
            matches.append({"student": other_student, "score": round(score, 3)})

    return sorted(matches, key=lambda x: x['score'], reverse=True)


def calculate_cosine_similarity(students, current_user_id):
    if len(students) < 2:
        return []

    # Simplified Cosine Similarity implementation for clarity
    all_interests_list = sorted(list(set(interest.name for student in students for interest in student.interests)))
    interest_map = {interest: i for i, interest in enumerate(all_interests_list)}

    student_vectors = {}
    for student in students:
        vec = [0] * len(all_interests_list)
        for interest in student.interests:
            vec[interest_map[interest.name]] = 1
        student_vectors[student.id] = vec

    current_user_vector = student_vectors.get(current_user_id)
    if not current_user_vector:
        return []

    matches = []
    for other_student in students:
        if other_student.id == current_user_id:
            continue

        other_student_vector = student_vectors.get(other_student.id)
        if not other_student_vector:
            continue

        dot_product = sum(a * b for a, b in zip(current_user_vector, other_student_vector))
        mag1 = math.sqrt(sum(a * a for a in current_user_vector))
        mag2 = math.sqrt(sum(b * b for b in other_student_vector))

        score = dot_product / (mag1 * mag2) if mag1 != 0 and mag2 != 0 else 0

        current_user_obj = next((s for s in students if s.id == current_user_id), None)
        if current_user_obj.course and other_student.course and current_user_obj.course.id == other_student.course.id:
            score += COURSE_BOOST

        score = min(score, 1.0)

        if score > 0.0:
            matches.append({"student": other_student, "score": round(score, 3)})

    return sorted(matches, key=lambda x: x['score'], reverse=True)