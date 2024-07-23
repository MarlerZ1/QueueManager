from django.contrib import admin

from people_queue.models import QueueMember, SpecificQueue, AnswerTime


# Register your models here.
class QueueMemberAdmin(admin.TabularInline):
    model = QueueMember
    fields = ('name', 'start_time')
    extra = 1


class AnswersTimeAdmin(admin.TabularInline):
    model = AnswerTime
    fields = ('name', 'time')
    extra = 1


@admin.register(SpecificQueue)
class SpecificQueueAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'active')
    list_display = ('name', 'active')
    search_fields = ('name',)
    inlines = (QueueMemberAdmin, AnswersTimeAdmin)
