from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Lesson, Enrollment, Question, Choice, Submission

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.get(user=request.user, course=course)
    
    if request.method == 'POST':
        selected_choice_ids = []
        for key, value in request.POST.lists():
            if key.startswith('choice_'):
                for choice_id in value:
                    selected_choice_ids.append(int(choice_id))
        
        submission = Submission.objects.create(enrollment=enrollment)
        for choice_id in selected_choice_ids:
            choice = Choice.objects.get(pk=choice_id)
            submission.choices.add(choice)
        submission.save()
        
        return HttpResponseRedirect(reverse('onlinecourse:show_exam_result', args=(course.id, submission.id)))

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    total_score = 0
    selected_choices = submission.choices.all()
    
    questions = course.question_set.all()
    for question in questions:
        correct_choices = question.choice_set.filter(is_correct=True)
        user_choices_for_q = selected_choices.filter(question=question)
        
        correct_ids = set(correct_choices.values_list('id', flat=True))
        user_ids = set(user_choices_for_q.values_list('id', flat=True))
        
        if correct_ids == user_ids and len(correct_ids) > 0:
            total_score += question.grade

    context = {
        'course': course,
        'submission': submission,
        'grade': total_score,
        'selected_choices': selected_choices,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
