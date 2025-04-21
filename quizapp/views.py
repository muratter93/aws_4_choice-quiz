from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Choice, AnswerHistory
import random

def quiz(request, question_id=1):
    """ クイズの表示と回答判定（各問題ごとの履歴＆正答率を表示） """
    question = Question.objects.filter(id=question_id).first()

    # 現在のIDの問題がない場合、次の利用可能なIDにリダイレクト
    if not question:
        next_available = Question.objects.filter(id__gt=question_id).order_by('id').first()
        if not next_available:
            next_available = Question.objects.order_by('id').first()  # 最初の問題に戻る
        if next_available:
            return redirect('quiz', question_id=next_available.id)

    next_question = Question.objects.filter(id__gt=question_id).order_by('id').first()
    prev_question = Question.objects.filter(id__lt=question_id).order_by('-id').first()

    result = None
    explanation = None

    if request.method == "POST":
        selected_answer = request.POST.get('answer')
        if question and selected_answer:
            is_correct = selected_answer == question.correct_answer
            result = "正解！ 🎉" if is_correct else "不正解 😢"
            explanation = question.explanation

            # 回答履歴を保存
            AnswerHistory.objects.create(question=question, is_correct=is_correct)

    # **この問題に対する履歴を取得**
    history_queryset = AnswerHistory.objects.filter(question=question)  # クエリセットを保持
    history = history_queryset.order_by('-answered_at')[:10]  # 最新10件のみ取得
    total_answers = history_queryset.count()  # `.filter()` の前に `.count()`
    correct_answers = history_queryset.filter(is_correct=True).count()
    accuracy_rate = (correct_answers / total_answers * 100) if total_answers > 0 else 0

    return render(request, 'index.html', {
        'question': question,
        'choices': question.choices.all() if question else [],
        'next_question': next_question,
        'prev_question': prev_question,
        'result': result,
        'explanation': explanation,
        'history': history,
        'accuracy_rate': accuracy_rate
    })


def category_list(request):
    """ カテゴリ一覧を取得 """
    categories = dict(Question.CATEGORY_CHOICES)

    # 「未分類」を一番下に移動
    sorted_categories = {key: name for key, name in categories.items() if key != 'unclassified'}
    sorted_categories['unclassified'] = categories['unclassified']

    return render(request, 'category_list.html', {'categories': sorted_categories})


def category_questions(request, category):
    """ 指定カテゴリの問題一覧を取得 """
    questions = Question.objects.filter(category=category).order_by('id')
    category_name = dict(Question.CATEGORY_CHOICES).get(category, "未分類")
    return render(request, 'category_questions.html', {'questions': questions, 'category_name': category_name})

def random_quiz(request):
    """ ランダムに1問のクイズを表示し、解答後に正誤判定し履歴を記録 """

    question = None

    if "current" in request.GET:
        # 「今の問題を見る」ボタンが押された場合、セッションから問題を取得
        question_id = request.session.get("last_random_question_id")
        question = Question.objects.filter(id=question_id).first()
    elif request.method == "POST":
        # 「回答する」ボタンが押された場合、セッションから問題を取得
        question_id = request.session.get("last_random_question_id")
        question = Question.objects.filter(id=question_id).first()
    else:
        # 「次のランダム問題へ」ボタンが押された場合、新しい問題を取得
        questions = list(Question.objects.all())  # 全問題を取得
        question = random.choice(questions) if questions else None  # ランダムに1問選ぶ
        if question:
            request.session["last_random_question_id"] = question.id  # 選んだ問題をセッションに保存

    result = None
    explanation = None

    if request.method == "POST" and question:
        selected_answer = request.POST.get("answer")  # ユーザーの選択した答え
        if selected_answer:
            is_correct = selected_answer == question.correct_answer
            result = "正解！ 🎉" if is_correct else "不正解 😢"
            explanation = question.explanation  # 解説を表示

            # **履歴を通常の問題と統一して保存**
            AnswerHistory.objects.create(question=question, is_correct=is_correct)

    # **この問題に対する履歴を取得**
    history_queryset = AnswerHistory.objects.filter(question=question) if question else []
    history = history_queryset.order_by("-answered_at")[:10] if question else []  # 最新10件のみ取得
    total_answers = history_queryset.count() if question else 0
    correct_answers = history_queryset.filter(is_correct=True).count() if question else 0
    accuracy_rate = (correct_answers / total_answers * 100) if total_answers > 0 else 0

    return render(
        request,
        "random_quiz.html",
        {
            "question": question,
            "choices": question.choices.all() if question else [],
            "result": result,
            "explanation": explanation,
            "history": history,
            "accuracy_rate": accuracy_rate,
        },
    )
