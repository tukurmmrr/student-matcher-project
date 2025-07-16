# app/backend/matching.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

COURSE_BOOST = 0.2


def create_student_profile_dict(student):
    """Helper function to create a dictionary with student profile info."""
    return {
        "name": student.name,
        "course": student.course,
        "bio": student.bio,
        "profile_picture_url": student.profile_picture_url
    }


def calculate_jaccard_similarity(students):
    student_interests_sets = {s.id: {i.name for i in s.interests} for s in students}
    matches = []
    student_list = list(students)

    for i in range(len(student_list)):
        for j in range(i + 1, len(student_list)):
            student1 = student_list[i]
            student2 = student_list[j]

            set1 = student_interests_sets[student1.id]
            set2 = student_interests_sets[student2.id]

            intersection = len(set1.intersection(set2))
            union = len(set1.union(set2))

            score = intersection / union if union != 0 else 0

            if student1.course and student2.course and student1.course.lower() == student2.course.lower():
                score += COURSE_BOOST

            score = min(score, 1.0)

            if score > 0.2:
                matches.append({
                    "student1": create_student_profile_dict(student1),
                    "student2": create_student_profile_dict(student2),
                    "score": round(score, 3)
                })

    return sorted(matches, key=lambda x: x['score'], reverse=True)


def calculate_cosine_similarity(students):
    if len(students) < 2:
        return []

    docs = [" ".join([i.name for i in s.interests]) for s in students]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(docs)
    cosine_sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    matches = []
    for i in range(len(cosine_sim_matrix)):
        for j in range(i + 1, len(cosine_sim_matrix)):
            score = cosine_sim_matrix[i][j]

            if students[i].course and students[j].course and students[i].course.lower() == students[j].course.lower():
                score += COURSE_BOOST

            score = min(score, 1.0)

            if score > 0.2:
                matches.append({
                    "student1": create_student_profile_dict(students[i]),
                    "student2": create_student_profile_dict(students[j]),
                    "score": round(score, 3)
                })

    return sorted(matches, key=lambda x: x['score'], reverse=True)