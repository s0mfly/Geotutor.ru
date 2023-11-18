from django.contrib import admin
from .models import Articles, Polzakt, TeachersAkt, TasksAkt


class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'anons', 'full_text', 'date')
    list_display_links = ('title', 'anons')
    search_fields = ('title', 'anons',)


admin.site.register(Articles, ArticlesAdmin)


class PolzaktAdmin(admin.ModelAdmin):
    list_display = ('idpolz', 'famil', 'name', 'telefon', 'electpoch', 'chr_class', 'datareg',
                    'pole1', 'pole2', 'pole3', 'pole4', 'pole5')
    list_display_links = ('pole1', 'pole2', 'pole3', 'pole4', 'pole5')
    search_fields = ('idpolz', 'famil', 'name', 'telefon', 'electpoch', 'chr_class', 'datareg',)


admin.site.register(Polzakt, PolzaktAdmin)


class TeachersAktAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'patronymic', 'email', 'idTeacher', 'number',
                    'pole1', 'pole2', 'pole3', 'pole4', 'pole5')
    list_display_links = ('pole1', 'pole2', 'pole3', 'pole4', 'pole5')
    search_fields = ('surname', 'name', 'patronymic', 'email', 'idTeacher', 'number')


admin.site.register(TeachersAkt, TeachersAktAdmin)


class TasksAktAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacherId', 'studentId',
                    'pole1', 'pole2', 'pole3', 'pole4', 'pole5', 'pole6', 'pole7', 'pole8', 'pole9', 'pole10', 'pole11',
                    'pole12')
    list_display_links = ('pole1', 'pole2', 'pole3', 'pole4', 'pole5', 'pole6', 'pole7', 'pole8', 'pole9', 'pole10',
                          'pole11', 'pole12')
    search_fields = ('teacherId', 'studentId')


admin.site.register(TasksAkt, TasksAktAdmin)



