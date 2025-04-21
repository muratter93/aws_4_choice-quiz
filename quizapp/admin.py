from django.contrib import admin
from .models import Question, Choice, AnswerHistory

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0  # デフォルトで新規選択肢を表示しない

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'category', 'correct_answer')
    search_fields = ('question_text',)
    list_filter = ('category',)
    inlines = [ChoiceInline]  # 選択肢をインラインで管理
    fields = ('question_text', 'remarks', 'category', 'correct_answer', 'explanation')  

class AnswerHistoryAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_correct', 'answered_at')  # 履歴の一覧
    list_filter = ('is_correct',)
    search_fields = ('question__question_text',)
    actions = ['delete_selected_histories']  # 複数選択削除を可能に

    def delete_selected_histories(self, request, queryset):
        """ 選択した履歴を削除する """
        queryset.delete()
    delete_selected_histories.short_description = "選択した履歴を削除"

# ✅ `AnswerHistory` を登録する前に、一度 `unregister` する（エラー回避）
try:
    admin.site.unregister(AnswerHistory)
except admin.sites.NotRegistered:
    pass

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(AnswerHistory, AnswerHistoryAdmin) 
