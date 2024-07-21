from django.contrib import admin

from people_queue.models import QueueMember, SpecificQueue


# Register your models here.
class QueueMemberAdmin(admin.TabularInline):
    model = QueueMember
    fields = ('name',)
    extra = 1


@admin.register(SpecificQueue)
class SpecificQueueAdmin(admin.ModelAdmin):
    fields = ('name', 'description',)
    list_display = ('name',)
    search_fields = ('name',)
    inlines = (QueueMemberAdmin,)