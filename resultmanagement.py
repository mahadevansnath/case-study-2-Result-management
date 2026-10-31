    # resultmanagement.py                                                                       

def calculate_total(marks):
  
    return sum(marks.values())


def calculate_average(marks):
   
    if not marks:
        return 0.0
    return round(calculate_total(marks) / len(marks), 2)


def get_grade(average):
    
    if average >= 90:
        return "A"
    elif average >= 75:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 40:
        return "D"
    else:
        return "F"


def check_result(marks, pass_mark=40):
    for mark in marks.values():
        if mark < pass_mark:
            return "Fail"
    return "Pass"


def student_summary(student):
    
    marks = student["marks"]
    total = calculate_total(marks)
    average = calculate_average(marks)
    grade = get_grade(average)
    result = check_result(marks)
    return {
        "name": student["name"],
        "total": total,
        "average": average,
        "grade": grade,
        "result": result,
    }


def add_student(data, student_id, name, **marks):
    
    if student_id in data:
        return False
    data[student_id] = {"name": name, "marks": marks}
    return True


def update_marks(data, student_id, **changes):
    return False
    data[student_id]["marks"].update(changes)
    return True


def remove_student(data, student_id):

    if student_id in data:
        data.pop(student_id)
        return True
    return False


def print_report(data):

    print(f"{'ID':<6}{'Name':<8}{'Total':<6}{'Avg':<8}{'Grade':<7}  Result")
    print("-" * 42)

    ranked_list = []
    for s_id, s_info in data.items():
        avg = calculate_average(s_info["marks"])
        ranked_list.append((avg, s_id))

    ranked_list.sort(reverse=True)

    for _, s_id in ranked_list:
        summary = student_summary(data[s_id])
        print(
            f"{s_id:<6}{summary['name']:<8}{summary['total']:<6}"
            f"{summary['average']:<8.2f}{summary['grade']:<7}  {summary['result']}"
        )


def class_statistics(data, *subjects):
    if not data:
        return {"topper": None, "pass_percentage": 0.0, "subject_averages": {}}

    highest_avg = -1
    topper = ""
    pass_count = 0

    for s_id, s_info in data.items():
        summary = student_summary(s_info)
        if summary["average"] > highest_avg:
            highest_avg = summary["average"]
            topper = summary["name"]
        if summary["result"] == "Pass":
            pass_count += 1

    pass_percentage = round((pass_count / len(data)) * 100, 1)

    if subjects:
        target_subjects = list(subjects)
    else:
       
        target_subjects = []
        for s_info in data.values():
            for sub in s_info["marks"]:
                if sub not in target_subjects:
                    target_subjects.append(sub)

    subject_averages = {}
    for sub in target_subjects:
        sub_marks = [
            s_info["marks"][sub]
            for s_info in data.values()
            if sub in s_info["marks"]
        ]
        if sub_marks:
            subject_averages[sub] = round(sum(sub_marks) / len(sub_marks), 1)

    return {
        "topper": topper,
        "pass_percentage": pass_percentage,
        "subject_averages": subject_averages,
    }