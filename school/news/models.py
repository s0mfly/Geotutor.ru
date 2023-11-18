from django.db import models


class Articles(models.Model):
    title = models.CharField('Название', max_length=50)
    anons = models.CharField('Анонс', max_length=250)
    full_text = models.TextField('Статья')
    date = models.DateTimeField('Дата публикации')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/news/{self.id}'

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Polzakt(models.Model):
    idpolz = models.CharField('id пользователя', max_length=4000)
    famil = models.CharField('Фамилия', max_length=30)
    name = models.CharField('Имя', max_length=30)
    otshist = models.CharField('Отчество', max_length=100)
    telefon = models.CharField('Телефон', max_length=30)
    electpoch = models.CharField('Электронная почта', max_length=50)
    klass = models.CharField('Класс', max_length=150, default='0')
    chr_class = models.CharField('Буква класса', max_length=150, default='0')
    datareg = models.CharField('Дата регистрации', max_length=30)
    pole1 = models.TextField('Поле1', default='0')
    pole2 = models.TextField('Поле2', default='0')
    pole3 = models.TextField('Поле3', default='0')
    pole4 = models.TextField('Поле4', default='0')
    pole5 = models.TextField('Поле5', default='0')

    #razdel = models.ForeignKey('Razdely', null=True, on_delete=models.PROTECT, verbose_name='Раздел123')

    def __str__(self):
        return self.idpolz #return f'Тема: {self.temazad}'

    class Meta:
        verbose_name = 'Актив пользователей'
        verbose_name_plural = 'Актив пользователей'
        ordering = ['id']


class TeachersAkt(models.Model):
    surname = models.CharField('Фамилиия', max_length=30)
    name = models.CharField('Имя', max_length=30)
    patronymic = models.CharField('Отчество', max_length=50)
    email = models.CharField('Электронная почта', max_length=500)
    idTeacher = models.CharField('Логин учителя', max_length=4000)
    number = models.CharField('Номер телефона', max_length=11)
    pole1 = models.TextField('Поле1', default='0')
    pole2 = models.TextField('Поле2', default='0')
    pole3 = models.TextField('Поле3', default='0')
    pole4 = models.TextField('Поле4', default='0')
    pole5 = models.TextField('Поле5', default='0')

    def __str__(self):
        return self.idTeacher


class TasksAkt(models.Model):
    teacherId = models.CharField('Логин учителя', max_length=30)
    studentId = models.CharField('Логин ученика', max_length=100)
    pole1 = models.TextField('Поле1', default='0') # все задачи
    pole2 = models.TextField('Поле2', default='0') # все ответы
    pole3 = models.TextField('Поле3', default='0') # дата и время начала и конца и время на работу
    pole4 = models.TextField('Поле4', default='0') # кол-во вариантов
    pole5 = models.TextField('Поле5', default='0') # статус работы
    pole6 = models.CharField('Поле6', max_length=100) # название работы
    pole7 = models.CharField('Поле7', max_length=200) # фио учителя
    pole8 = models.CharField('Поле8', max_length=100) # пароль к работе
    pole9 = models.CharField('Поле9', max_length=30) # время начала работы
    pole10 = models.CharField('Поле10', max_length=500) # введённые ответы
    pole11 = models.CharField('Поле11', max_length=500, default='0')  #
    pole12 = models.CharField('Поле12', max_length=500, default='0')  #

    def __str__(self):
        return self.teacherId