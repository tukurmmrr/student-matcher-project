import math
import models


def create_admin_profile_dict(student: models.Student):
    return {"name": student.name, "course": student.course.name if student.course else "N/A"}


# This function is now ONLY for the admin dashboard
def calculate_jaccard_similarity(students):
    student_interests_sets = {s.id: set(i.name for i in s.interests) for s in students}
    matches = []
    student_list = list(students)

    for i in range(len(student_list)):
        for j in range(i + 1, len(student_list)):
            student1, student2 = student_list[i], student_list[j]
            set1, set2 = student_interests_sets.get(student1.id, set()), student_interests_sets.get(student2.id, set())

            if not set1 or not set2: continue

            intersection = len(set1.intersection(set2))
            union = len(set1.union(set2))
            score = intersection / union if union != 0 else 0

            if student1.course and student2.course and student1.course.id == student2.course.id:
                score += 0.2

            score = min(score, 1.0)

            if score > 0.0:
                matches.append({
                    "student1": create_admin_profile_dict(student1),
                    "student2": create_admin_profile_dict(student2),
                    "score": round(score, 3)
                })

    return sorted(matches, key=lambda x: x['score'], reverse=True)


# This function is now ONLY for the user dashboard
def calculate_cosine_similarity(students, current_user_id):
    matches = []
    current_user_obj = next((s for s in students if s.id == current_user_id), None)
    if not current_user_obj or not current_user_obj.interests: return []

    current_user_interests = set(i.name for i in current_user_obj.interests)

    for other_student in students:
        if other_student.id == current_user_id: continue

        other_student_interests = set(i.name for i in other_student.interests)
        if not other_student_interests: continue

        # We use a simple score for the user view. You can explain this choice in your thesis.
        intersection = len(current_user_interests.intersection(other_student_interests))
        union = len(current_user_interests.union(other_student_interests))
        score = intersection / union if union != 0 else 0

        if current_user_obj.course and other_student.course and current_user_obj.course.id == other_student.course.id:
            score += 0.2

        score = min(score, 1.0)

        if score > 0.0:
            matches.append({"student": other_student, "score": score})

    return sorted(matches, key=lambda x: x['score'], reverse=True)