from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import re
from groq import Groq
from django.conf import settings
from .models import Quiz, Question, QuizAttempt
from .pdf_utils import render_to_pdf


def generate_quiz_groq(subject, level="medium", count=10):
    """Generate quiz using Groq API"""
    print(f"=== GENERATING {count} QUESTIONS ===")
    print(f"Subject: {subject}, Level: {level}")
    
    try:
        groq_client = Groq(api_key=settings.GROQ_API_KEY)
        
        prompt = f"""
        Generate exactly {count} multiple-choice questions about {subject} with {level} difficulty level.
        
        REQUIREMENTS:
        - Create exactly {count} questions
        - Each question must have exactly 4 options labeled A), B), C), D)
        - Only one correct answer per question
        - Format each question EXACTLY like this:
        
        Q1. [Your question text here?]
        A) [Option A text]
        B) [Option B text]
        C) [Option C text]
        D) [Option D text]
        Answer: [Single letter A, B, C, or D]
        
        Now generate {count} questions about {subject}:
        """
        
        print("Sending request to Groq API...")
        response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=4000
        )
        
        content = response.choices[0].message.content.strip()
        print(f"Successfully generated content, length: {len(content)}")
        
        return content
        
    except Exception as e:
        error_msg = f"Error generating quiz: {str(e)}"
        print(error_msg)
        return error_msg

def parse_quiz_content(content):
    """Parse the generated quiz content"""
    print("=== PARSING QUIZ CONTENT ===")
    
    questions = []
    current_question = None
    
    lines = content.split('\n')
    print(f"Processing {len(lines)} lines")
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Match question pattern: Q1. Question text
        question_match = re.match(r'Q\d+\.\s*(.+)', line)
        if question_match:
            if current_question:
                questions.append(current_question)
                print(f"  Completed question {len(questions)}")
            current_question = {
                'question_text': question_match.group(1),
                'options': {},
                'correct_answer': None
            }
            print(f"  Found new question: {question_match.group(1)[:50]}...")
        
        # Match options: A) Option text
        option_match = re.match(r'([A-D])\)\s*(.+)', line)
        if option_match and current_question:
            option_letter = option_match.group(1)
            option_text = option_match.group(2)
            current_question['options'][option_letter] = option_text
            print(f"    Added option {option_letter}: {option_text[:30]}...")
        
        # Match answer: Answer: X
        answer_match = re.match(r'Answer:\s*([A-D])', line, re.IGNORECASE)
        if answer_match and current_question:
            current_question['correct_answer'] = answer_match.group(1).upper()
            print(f"    Set correct answer: {current_question['correct_answer']}")
    
    # Add the last question
    if current_question:
        questions.append(current_question)
        print(f"  Completed final question {len(questions)}")
    
    print(f"=== PARSING COMPLETE: {len(questions)} QUESTIONS FOUND ===")
    return questions

# Quiz Views
@login_required
def quiz_home(request):
    """Home page with quiz creation form - Only for students"""
    if request.user.role != 'student':
        return redirect('student_dashboard')
    
    if request.method == "POST":
        subject = request.POST.get("subject")
        level = request.POST.get("level", "medium")
        count = int(request.POST.get("count", 10))
        
        # Generate quiz
        quiz_content = generate_quiz_groq(subject, level, count)
        
        if quiz_content and not quiz_content.startswith("Error"):
            # Parse and store in session
            questions = parse_quiz_content(quiz_content)
            
            # Store in session
            request.session['quiz_data'] = {
                'subject': subject,
                'level': level,
                'questions': questions,
                'total_questions': len(questions)
            }
            
            return redirect('take_quiz')
        else:
            return render(request, "quiz/quiz_home.html", {
                "error": quiz_content if quiz_content else "Failed to generate quiz",
                "subject": subject,
                "level": level,
                "count": count
            })
    
    return render(request, "quiz/quiz_home.html")

@login_required
def take_quiz(request):
    """Display quiz questions with radio buttons - Only for students"""
    if request.user.role != 'student':
        return redirect('student_dashboard')
    
    quiz_data = request.session.get('quiz_data')
    
    if not quiz_data:
        return redirect('quiz_home')
    
    # Get toast message from session and remove it
    toast_message = request.session.pop('toast_message', None)
    
    context = {
        "subject": quiz_data['subject'],
        "level": quiz_data['level'],
        "questions": quiz_data['questions'],
        "total_questions": quiz_data['total_questions'],
        "toast_message": toast_message,
    }
    return render(request, "quiz/take_quiz.html", context)

@login_required
def append_questions(request):
    """Append 5 more questions to the current quiz - Only for students"""
    if request.user.role != 'student':
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    print("=== APPEND QUESTIONS FUNCTION CALLED ===")
    
    if request.method == "POST":
        quiz_data = request.session.get('quiz_data')
        
        print(f"Quiz data exists: {bool(quiz_data)}")
        
        if not quiz_data:
            print("No quiz data found - redirecting to home")
            return redirect('quiz_home')
        
        try:
            # Generate 5 more questions
            subject = quiz_data['subject']
            level = quiz_data['level']
            current_count = len(quiz_data['questions'])
            
            print(f"Generating 5 more questions for: {subject} ({level})")
            print(f"Current question count: {current_count}")
            
            quiz_content = generate_quiz_groq(subject, level, 5)
            
            print(f"Generated content preview: {quiz_content[:200] if quiz_content else 'None'}...")
            
            if quiz_content and not quiz_content.startswith("Error"):
                new_questions = parse_quiz_content(quiz_content)
                print(f"Successfully parsed {len(new_questions)} new questions")
                
                if new_questions:
                    # Append new questions to existing ones
                    quiz_data['questions'].extend(new_questions)
                    quiz_data['total_questions'] = len(quiz_data['questions'])
                    
                    # Update session
                    request.session['quiz_data'] = quiz_data
                    request.session.modified = True
                    
                    print(f"Success! Total questions now: {quiz_data['total_questions']}")
                    
                    # Store toast message in session
                    request.session['toast_message'] = {
                        'type': 'success',
                        'message': f'✅ Added {len(new_questions)} new questions! Total: {quiz_data["total_questions"]}'
                    }
                    
                else:
                    print("No questions were parsed from generated content")
                    request.session['toast_message'] = {
                        'type': 'error',
                        'message': '❌ Failed to parse new questions. Please try again.'
                    }
            else:
                print(f"Error generating questions: {quiz_content}")
                request.session['toast_message'] = {
                    'type': 'error',
                    'message': f'❌ {quiz_content}'
                }
                
        except Exception as e:
            print(f"Exception in append_questions: {str(e)}")
            import traceback
            print(traceback.format_exc())
            request.session['toast_message'] = {
                'type': 'error',
                'message': f'❌ Error: {str(e)}'
            }
        
        return redirect('take_quiz')
    
    print("Not a POST request - redirecting to home")
    return redirect('quiz_home')


@login_required
def submit_quiz(request):
    """Calculate and display quiz results - Only for students"""
    if request.user.role != 'student':
        return redirect('student_dashboard')
    
    if request.method == "POST":
        quiz_data = request.session.get('quiz_data')
        
        if not quiz_data:
            return redirect('quiz_home')
        
        questions = quiz_data['questions']
        score = 0
        total = len(questions)
        results = []
        
        for i, question in enumerate(questions):
            user_answer = request.POST.get(f'question_{i}')
            is_correct = (user_answer == question['correct_answer'])
            
            if is_correct:
                score += 1
            
            results.append({
                'question': question,
                'user_answer': user_answer,
                'correct_answer': question['correct_answer'],
                'is_correct': is_correct,
                'question_number': i + 1
            })
        
        percentage = (score / total) * 100 if total > 0 else 0
        
        # Save quiz attempt to database (quiz is None for AI-generated quizzes)
        quiz_attempt = QuizAttempt.objects.create(
            student=request.user,
            quiz=None,  # AI-generated, not from database
            score=score,
            total_questions=total,
            time_taken=0,
            subject=quiz_data['subject'],
            difficulty=quiz_data['level']
        )
        
        # Store results in session for report generation
        request.session['quiz_results'] = {
            'subject': quiz_data['subject'],
            'level': quiz_data['level'],
            'score': score,
            'total': total,
            'percentage': percentage,
            'results': results,
            'attempt_id': quiz_attempt.id
        }
        
        context = {
            "subject": quiz_data['subject'],
            "level": quiz_data['level'],
            "score": score,
            "total": total,
            "percentage": round(percentage, 1),
            "results": results,
        }
        
        return render(request, "quiz/quiz_result.html", context)
    
    return redirect('take_quiz')

@login_required
def generate_report(request):
    """Generate a detailed PDF report of the quiz - Only for students"""
    if request.user.role != 'student':
        return redirect('student_dashboard')
    
    quiz_results = request.session.get('quiz_results')
    
    if not quiz_results:
        return redirect('quiz_home')
    
    # Pre-process the data to include option texts
    processed_results = []
    for result in quiz_results['results']:
        processed_result = result.copy()
        
        # Add option texts to the result
        user_answer_text = ""
        if result['user_answer'] == 'A':
            user_answer_text = f"A) {result['question']['options'].get('A', '')}"
        elif result['user_answer'] == 'B':
            user_answer_text = f"B) {result['question']['options'].get('B', '')}"
        elif result['user_answer'] == 'C':
            user_answer_text = f"C) {result['question']['options'].get('C', '')}"
        elif result['user_answer'] == 'D':
            user_answer_text = f"D) {result['question']['options'].get('D', '')}"
        else:
            user_answer_text = "Not answered"
            
        correct_answer_text = ""
        if result['correct_answer'] == 'A':
            correct_answer_text = f"A) {result['question']['options'].get('A', '')}"
        elif result['correct_answer'] == 'B':
            correct_answer_text = f"B) {result['question']['options'].get('B', '')}"
        elif result['correct_answer'] == 'C':
            correct_answer_text = f"C) {result['question']['options'].get('C', '')}"
        elif result['correct_answer'] == 'D':
            correct_answer_text = f"D) {result['question']['options'].get('D', '')}"
            
        processed_result['user_answer_text'] = user_answer_text
        processed_result['correct_answer_text'] = correct_answer_text
        processed_results.append(processed_result)
    
    context = {
        "subject": quiz_results['subject'],
        "level": quiz_results['level'],
        "score": quiz_results['score'],
        "total": quiz_results['total'],
        "percentage": quiz_results['percentage'],
        "results": processed_results,
    }
    
    return render(request, "quiz/quiz_report.html", context)

@login_required
def quiz_list(request):
    """Show list of available quizzes - Only for students"""
    if request.user.role != 'student':
        return redirect('student_dashboard')
    
    # For AI-generated quizzes, we don't have pre-made quizzes
    # So we'll show the quiz creation form
    return redirect('quiz_home')

@login_required 
def quiz_history(request):
    """Show student's quiz attempt history - Only for students"""
    if request.user.role != 'student':
        return redirect('student_dashboard')
    
    attempts = QuizAttempt.objects.filter(student=request.user).order_by('-attempted_at')
    
    context = {
        'attempts': attempts
    }
    return render(request, 'quiz/quiz_history.html', context)

def debug_quiz(request):
    """Debug view to check session data"""
    quiz_data = request.session.get('quiz_data', {})
    return JsonResponse({
        'has_quiz_data': bool(quiz_data),
        'subject': quiz_data.get('subject', 'None'),
        'total_questions': quiz_data.get('total_questions', 0),
        'questions_count': len(quiz_data.get('questions', [])),
        'session_keys': list(request.session.keys())
    })