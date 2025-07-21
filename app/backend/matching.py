import math
from collections import Counter

COURSE_BOOST = 0.2

def create_student_profile_dict(student):
    return {
        "name": student.name,
        "course": student.course,
        "bio": student.bio,
        "profile_picture_url": student.profile_picture_url
    }

def calculate_jaccard_similarity(students):
    student_interests_sets = {s.id: set(i.name for i in s.interests) for s in students}
    matches = []
    student_list = list(students)

    for i in range(len(student_list)):
        for j in range(i + 1, len(student_list)):
            student1, student2 = student_list[i], student_list[j]
            set1 = student_interests_sets[student1.id]
            set2 = student_interests_sets[student2.id]

            if not set1 or not set2:
                continue

            intersection = len(set1.intersection(set2))
            union = len(set1.union(set2))
            score = intersection / union if union != 0 else 0

            if student1.course and student2.course and student1.course.lower() == student2.course.lower():
                score += COURSE_BOOST

            score = min(score, 1.0)

            if score > 0.0:
                matches.append({"student1": create_student_profile_dict(student1), "student2": create_student_profile_dict(student2), "score": round(score, 3)})

    return sorted(matches, key=lambda x: x['score'], reverse=True)

def calculate_cosine_similarity(students):
    if len(students) < 2:
        return []

    student_interests_lists = {s.id: [i.name for i in s.interests] for s in students}

    # --- Pure Python TF-IDF and Cosine Similarity ---
    all_interests = set()
    for interest_list in student_interests_lists.values():
        all_interests.update(interest_list)

    vocab = sorted(list(all_interests))
    vocab_map = {word: i for i, word in enumerate(vocab)}

    doc_term_matrix = []
    for s in students:
        vec = [0] * len(vocab)
        if s.id in student_interests_lists:
            term_counts = Counter(student_interests_lists[s.id])
            for term, count in term_counts.items():
                if term in vocab_map:
                    vec[vocab_map[term]] = count
        doc_term_matrix.append(vec)

    matches = []
    for i in range(len(students)):
        for j in range(i + 1, len(students)):
            vec1, vec2 = doc_term_matrix[i], doc_term_matrix[j]

            dot_product = sum(a * b for a, b in zip(vec1, vec2))
            mag1 = math.sqrt(sum(a * a for a in vec1))
            mag2 = math.sqrt(sum(b * b for b in vec2))

            if mag1 == 0 or mag2 == 0:
                score = 0.0
            else:
                score = dot_product / (mag1 * mag2)

            if students[i].course and students[j].course and students[i].course.lower() == students[j].course.lower():
                score += COURSE_BOOST

            score = min(score, 1.0)

            if score > 0.0:
                matches.append({"student1": create_student_profile_dict(students[i]), "student2": create_student_profile_dict(students[j]), "score": round(score, 3)})

    return sorted(matches, key=lambda x: x['score'], reverse=True)