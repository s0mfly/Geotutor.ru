from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from news.models import Polzakt, TeachersAkt, TasksAkt
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail, BadHeaderError
from random import randint, sample, randrange
import time
from django.conf import settings
from datetime import datetime, timedelta
from django.http import HttpResponse
import requests


def begin(request):
    alph = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    txt, otv = [], []
    k = randint(2, 9)
    piffTr = [[3, 4, 5], [5, 12, 13], [8, 15, 17]]
    k1 = randint(0, 2)
    count = randint(1, 3)
    if count == 1:
        txt.append('1. В прямоугольном треугольнике катеты равны ' + str(piffTr[k1][0] * k) + ' и ' + str(piffTr[k1][1] * k)
                   + '. Найдите гипотенузу без использования теоремы Пифагора.')
        otv.append(str(piffTr[k1][2] * k))
    if count == 2:
        txt.append('1. В прямоугольном треугольнике катет равен ' + str(piffTr[k1][0] * k) + ' и гипотенуза равна ' + str(piffTr[k1][2] * k)
            + '. Найдите другой катет без использования теоремы Пифагора.')
        otv.append(str(piffTr[k1][1] * k))
    if count == 3:
        txt.append(
            '1. В прямоугольном треугольнике катет равен ' + str(piffTr[k1][1] * k) + ' и гипотенуза равна ' + str(
                piffTr[k1][2] * k)
            + '. Найдите другой катет без использования теоремы Пифагора.')
        otv.append(str(piffTr[k1][0] * k))
    k = randint(2, 9)
    piffTr.remove(piffTr[k1])
    k1 = randint(0, 1)
    txt.append('2. Найдите катет в прямоугольном треугольнике, гипотенуза в котором равна ' + str(piffTr[k1][2] * k) +
               ', а другой катет равен ' + str(piffTr[k1][0] * k) + '.')
    otv.append(str(piffTr[k1][1] * k))
    a, b, c, m = sample(alph, 4)
    k, k1 = randint(5, 75), randint(7, 75)
    txt.append('3. Высоты ' + a + a + '1' + ' и ' + b + b + '1' +
               ' треугольника ' + a + b + c + ' пересекаются в точке ' + m + '. Найдите ' + a + b + m +
               ', если ' + a + ' = ' + str(k) + '˚, ' + b + ' = ' + str(k1) + '˚')
    otv.append(str(180 - (90 - k) - (90 - k1)))
    a, b, c, d = sample(alph, 4)
    k = randrange(2, 78, 2)
    count = randint(1, 4)
    if count == 1:
        txt.append('4. В треугольник ' + c + a + b + ', прямым углом в котором явлеятся угол ' + b +
                   ', вписана окружность с центром в точке ' + d + '. Найдите угол ' + a + d + b +
                   ', если угол ' + a + c + b + ' равен ' + str(k) + ' градусов.')
        otv.append(str(180 - 45 - ((90 - k) // 2)))
    if count == 2:
        txt.append('4. В треугольник ' + b + c + a + ', прямым углом в котором явлеятся угол ' + b +
                   ', вписана окружность с центром в точке ' + d + '. Найдите угол ' + a + d + b +
                   ', если угол ' + b + a + c + ' равен ' + str(k) + ' градусов.')
        otv.append(str(180 - 45 - (k // 2)))
    if count == 3:
        txt.append('4. В треугольник ' + c + a + b + ', прямым углом в котором явлеятся угол ' + b +
                   ', вписана окружность с центром в точке ' + d + '. Найдите угол ' + b + d + c +
                   ', если угол ' + a + c + b + ' равен ' + str(k) + ' градусов.')
        otv.append(str(180 - 45 - (k // 2)))
    if count == 4:
        txt.append('4. В треугольник ' + a + b + c + ', прямым углом в котором явлеятся угол ' + b +
                   ', вписана окружность с центром в точке ' + d + '. Найдите угол ' + b + d + c +
                   ', если угол ' + b + a + c + ' равен ' + str(k) + '°.')
        otv.append(str(180 - 45 - ((90 - k) // 2)))
    tx = '${!$%^'.join(txt)
    ot = '${!$%^'.join(otv)
    uz = Polzakt.objects.get(idpolz=request.user.username)
    uz.pole1 = tx
    uz.pole2 = ot
    answer = request.GET
    if 'go' in answer:
        uz.save()
        request.session['ti_contr'] = time.time()
        request.session['non_zad'] = 1
        request.session['flag_pos'] = 0
        return redirect('zada4i')
    return render(request, 'main/go.html')


def zada4i(request):
    uz = Polzakt.objects.get(idpolz=request.user.username)
    text = uz.pole1.split('${!$%^')
    otvet = uz.pole2.split('${!$%^')
    text_s = []
    k = 0
    count = 0
    for i in text:
        text_s.append([str(k + 1), i])
        k += 1
    answer = request.GET
    if 'answers1' in answer:
        tm = time.time() - request.session['ti_contr']
        ot = []
        flag = 0
        for i in answer:
            ot.append(answer[i])
        ot = ot[:-1]
        for i in range(len(ot)):
            if ot[i] == '':
                ot[i] = 0
        for i in range(len(otvet)):
            if int(int(otvet[i]) * 1000) / 1000 == int(int(ot[i]) * 1000) / 1000:
                count += 1
        tm += 1000 * (4 - count)  # 4 - кол-во задач !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        uz = Polzakt.objects.get(idpolz=request.user.username)
        str_rec = uz.pole3.split('$')
        rec = [round(float(i)) for i in str_rec]
        razn = round((rec[request.session['non_zad'] - 1] - tm))
        if rec[request.session['non_zad'] - 1] == 10000:
            flag = 1
        absRazn = -razn
        sm = 0
        for i in str_rec[:-1]:
            sm += int(i)
        str_rec[-1] = str(sm)

        ### находим позицию для старого кол-ва очков

        allPolz = Polzakt.objects.all()
        mas = [[int(k) for k in i.pole3.split('$')] + [i.idpolz] for i in allPolz]
        usName = request.user.username

        last_position = 0
        mas.sort(key=lambda x: x[request.session['non_zad'] - 1])
        for i in range(len(mas)):
            if mas[i][-1] == usName:
                last_position = i + 1
                break

        if razn > 0:
            rec[request.session['non_zad'] - 1] = round(tm)
            rec[-1] -= razn
            str_rec = '$'.join(str(i) for i in rec)
            uz = Polzakt.objects.get(idpolz=request.user.username)
            uz.pole3 = str_rec
            uz.save()
        absRazn = round(tm - rec[request.session['non_zad'] - 1])
        score = round(tm)
        output = [[i] for i in text]
        for i in range(len(output)):
            output[i].append(otvet[i])
            output[i].append(ot[i])

        allPolz = Polzakt.objects.all()
        mas = [[int(k) for k in i.pole3.split('$')] + [i.idpolz] for i in allPolz]

        mas.sort(key=lambda x: x[request.session['non_zad'] - 1])
        for i in range(len(mas)):
            if mas[i][-1] == usName:
                position = i + 1
                break

        request.session['flag_pos'] = 1 if last_position != position else 0
        if position <= 3:
            request.session['pos'] = position
        return render(request, 'main/pohvala.html', {'razn': razn, 'absRazn': absRazn + 1, 'scores': score,
                                                     'output': output, 'flag': flag, 'pos': position,
                                                     'flag_pos': request.session['flag_pos']})
    return render(request, 'main/zada4i.html', {'txt': text_s})


def kubok(request):
    return render(request, 'main/kubok.html', {'pos': request.session['pos']})


def begin2(request):
    alph = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '123456789'
    txt, otv = [], []
    k1, k2, k3, k4 = 7, 7, 7, 7
    while 360 % (int(k1) + int(k2) + int(k3) + int(k4)) != 0:
        k1, k2, k3, k4 = sample(numbers, 4)
    a, b, c, d = sample(alph, 4)
    txt.append('1. Найдите больший угол четырёхугольника ' + a + b + c + d + ', если его все его углы отностся как ' +
               k1 + ':' + k2 + ':' + k3 + ':' + k4 + '.')
    otv.append(str((360 // (int(k1) + int(k2) + int(k3) + int(k4))) * max(int(k1), int(k2), int(k3), int(k4))))
    k = randint(50, 150)
    k1 = randint(50, 150)
    a, b, c, d = sample(alph, 4)
    txt.append('2. Найдите периметр четырёхугольника ' + a + b + c + d + ', в который вписана окружность. ' + a + b +
               ' = ' + str(k) + ' и ' + c + d + ' = ' + str(k1) + '.')
    otv.append(str(2 * (k1 + k)))
    k = randint(129, 179)
    k1 = randint(50, 120)
    txt.append('3.Найдите отрезок, который соединяет середины диагоналей трапеции, если её основания равны ' +
               str(k) + ' и ' + str(k1) + '.')
    otv.append(str((k - k1) // 2))
    k = randint(10, 20)
    k1 = randint(21, 35)
    txt.append('4. Основания трапеции равны ' + str(k) + ' и ' + str(k1) + '. Найдите больший из отрезков, '
               'на которые делит среднюю линию этой трапеции одна из ее диагоналей.')
    otv.append(str(k1 // 2))
    tx = '${!$%^'.join(txt)
    ot = '${!$%^'.join(otv)
    uz = Polzakt.objects.get(idpolz=request.user.username)
    uz.pole1 = tx
    uz.pole2 = ot
    answer = request.GET
    if 'go' in answer:
        uz.save()
        request.session['ti_contr'] = time.time()
        request.session['non_zad'] = 2
        return redirect('zada4i')
    return render(request, 'main/go.html')


def begin3(request):
    alph = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    txt, otv = [], []
    k1 = randint(5, 30) # радиус вписанной окружности
    k = randint(int(k1 * 5.2), int(k1 * 5.2) + 50) * 2 # периметр треугольника
    txt.append('1. Периметр треугольника равен ' + str(k) + ', а радиус вписанной окружности равен ' + str(k1) +
               '. Найдите площадь этого треугольника.')
    otv.append(str((k * k1) // 2))
    k1 = randint(20, 60)
    x = k1
    while x == k1:
        x = randint(20, 60)
    k = (k1 + x) * 2
    txt.append('2. В четырёхугольник, периметр которого равен ' + str(k) + ' , вписана окружность, одна его сторона '
                                                                           'равна ' +
               str(k1) + '. Найдите длину стороны, которая лежит напротив неё.')
    otv.append(str(x))
    k = randrange(22, 36, 2)
    k1 = randrange(38, 56, 2)
    k2 = randrange(6, 20, 2)
    txt.append('3. В равнобедренной трапеции провели высоту, делящую два основанию пополам. Найдите эту высоту,'
               ' если в получившиеся четырёхугольники вписали окружность и основания равны ' + str(k) + ' и ' + str(k1)
               + ' соответственно, а боковая сторона равна ' + str(k2) + '.')
    otv.append(str(k + k1 - k2))
    a, b, c, d = sample(alph, 4)
    k = randint(15, 50)
    k1 = randint(60, 87)
    txt.append('4. Найдите угол ' + a + b + c + ' четырёхугольника ' + d + b + a + c + ', который вписан в окружность,'
                                                                                       ' если углы ' +
               c + a + d + ' и ' + a + b + d + ' равны ' + str(k) + '° и ' + str(k1) + '° соответственно.')
    otv.append(str(k + k1))
    tx = '${!$%^'.join(txt)
    ot = '${!$%^'.join(otv)
    uz = Polzakt.objects.get(idpolz=request.user.username)
    uz.pole1 = tx
    uz.pole2 = ot
    answer = request.GET
    if 'go' in answer:
        uz.save()
        request.session['ti_contr'] = time.time()
        request.session['non_zad'] = 3
        return redirect('zada4i')
    return render(request, 'main/go.html')


def begin4(request):
    alph = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    piffTr = [[3, 4, 5], [5, 12, 13], [8, 15, 17]]
    txt, otv = [], []
    k = randint(99, 222)
    txt.append('1. Радиус окружности, описанной около квадрата, равен ' + str(k) + ' корней из 2.'
               ' Найдите длину стороны этого квадрата.')
    otv.append(str(k * 2))
    k = randint(79, 234)
    txt.append('2. Радиус вписанной в квадрат окружности равен ' + str(k) + ' корней из 2. Найдите радиус окружности, '
               'описанной около этого квадрата.')
    otv.append(str(k * 2))
    k = randint(90, 169)
    a, b, c, d = sample(alph, 4)
    txt.append('3. Около равнобедренного треугольника ' + b + a + c + ' описана окружность с центром в точке ' + d +
               '. Найдите угол ' + b + d + c + ', если ' + a + b + ' = ' + b + c + ' и угол ' + a + b + c + ' равен '
               + str(k) + '°.')
    otv.append(str(180 - k))
    a, b, c = sample(alph, 3)
    d = randint(0, 2)
    f, f2 = 1, 0
    k, k1 = piffTr[d][f], piffTr[d][f2]
    txt.append('4. Найдите радиус вписанной окружности треугольника ' + c + b + a + ', если его стороны ' + c + a +
               ' и ' + b + c + ' равны ' + str(k) + ' и ' + str(k1) + ' соответственно. Угол ' + c + ' равен 90°.')
    otv.append(str((k + k1 - piffTr[d][-1]) // 2))
    tx = '${!$%^'.join(txt)
    ot = '${!$%^'.join(otv)
    uz = Polzakt.objects.get(idpolz=request.user.username)
    uz.pole1 = tx
    uz.pole2 = ot
    answer = request.GET
    if 'go' in answer:
        uz.save()
        request.session['ti_contr'] = time.time()
        request.session['non_zad'] = 4
        return redirect('zada4i')
    return render(request, 'main/go.html')


def regist(request):
# return redirect('logout')
    data = request.session['registration2'].split('*#@^')
    if request.method == 'GET':
        answer = request.GET
        if 'fam' in answer and 'name' in answer and 'lg' in answer and 'email' in answer:
            f = answer.__getitem__('fam').replace(' ', '').capitalize()
            n = answer.__getitem__('name').replace(' ', '').capitalize()
            p = answer.__getitem__('email').replace(' ', '').capitalize()
            if f == '' or n == '': return redirect('regist')
            k = answer.__getitem__('kl').replace(' ', '')
            lg = answer.__getitem__('lg')
            if len(f) < 2 or len(n) < 2 or len(f) > 25 or\
                    len(n) > 25 or len(k) > 25 or len(lg) > 30 or len(lg) < 3 or len(p) < 5:
                return redirect('regist')
            if User.objects.filter(username=lg).exists():
                return render(request, 'main/ujuse.html')
            if Polzakt.objects.filter(electpoch=p).exists() or TeachersAkt.objects.filter(email=p).exists():
                return render(request, 'main/view_message3.html',
                              {'link': 'regist',
                               'ms': 'Такая почта уже зарегестрирована. Проверьте свои данные!'
                               }
                              )
            else:
                try:
                    send_mail(
                        'Оповещение для ученика платформы GeoTutor!',
                        'Добро пожаловать! Мы рады приветствовать вас на нашей платформе)',
                        'geometrix2023_2024@mail.ru',
                        [p],
                        fail_silently=False,
                    )
                except BadHeaderError:
                    data[0], data[1], data[2], data[3], data[4] = lg, p, f, n, k
                    request.session['registration2'] = '*#@^'.join(data)
                    mess = 'В почте неправильные заголовки, попробуйте ещё раз!'
                    return render(request, 'main/error7.html', {'mess': mess})
                except Exception as e:
                    data[0], data[1], data[2], data[3], data[4] = lg, p, f, n, k
                    request.session['registration2'] = '*#@^'.join(data)
                    mess = 'Ошибка при отправке письма, проверьте название вашей почты и попробуйте ещё раз!'
                    return render(request, 'main/error7.html', {'mess': mess})
                Polzakt(idpolz=lg, pole1='0', famil=f, name=n, otshist=k, electpoch=p,
                        pole3='10000$10000$10000$10000$40000').save()
                User.objects.create_user(lg, '', '4591423', first_name=f + '$#$%' + n + '$#$%' + k).save()
                user = authenticate(request, username=lg, password='4591423')
                login(request, user)
                chat_id = 914614230  # Здесь можно использовать chat_id пользователя или группы
                message_text = "На сайте появился новый ученик:\nЛогин: " + lg + '\nФИО: ' + \
                               f + ' ' + n + '\nEmail: ' + p
                send_telegram_message(chat_id, message_text)
                return render(request, 'main/uspreg.html')
    return render(request, 'main/main_reg.html', {'data': data})


def index(request):
    answer = request.GET
    user_id = request.user.username
    if (user_id != ''):
        flag = request.user.last_name
        if flag == '1':
            mess = 'Извините, чтобы зайти в тренировку, нужно выйти из учительского аккаунта и зарегистрироваться учеником!'
            return render(request, 'main/error2.html', {'mess': mess})
        else:
            name = request.user.first_name.split('$#$%')
            nm = name[0] + ' ' + name[1]
    else:
        nm = ''
    # if request.method == 'GET':
    # answer = request.GET
    if 'reg' in answer: return redirect('regist')
    if 'intlg' in answer:
        lg = answer.__getitem__('lg')
        if len(lg) < 3: return redirect('index')
        if User.objects.filter(username=lg).exists() == 1:
            if User.objects.get(username=lg).last_name == '1':
                mess = 'Вы не можете зайти в аккаунт ученика под логином учителя!'
                return render(request, 'main/error2.html', {'mess': mess})
            else:
                user = authenticate(request, username=lg, password='4591423')
                login(request, user)
                return redirect('index')
        else:
            return render(request, 'main/nezar.html')
    return render(request, 'main/index.html', {'nm': nm})


def table(request):
    allPolz = Polzakt.objects.all()
    mas = [[int(k) for k in i.pole3.split('$')] + [i.famil, i.name, i.idpolz] for i in allPolz]
    usName = request.user.username
    mas.sort(key=lambda x: x[0])

    mas1 = [[i + 1, mas[i][-3], mas[i][-2], str(mas[i][0])] for i in range(3)]
    for i in range(len(mas)):
        if mas[i][-1] == usName:
            mas1.append([i + 1, mas[i][-3], mas[i][-2], str(mas[i][0])])

    mas.sort(key=lambda x: x[1])
    mas2 = [[i + 1, mas[i][-3], mas[i][-2], str(mas[i][1])] for i in range(3)]
    for i in range(len(mas)):
        if mas[i][-1] == usName:
            mas2.append([i + 1, mas[i][-3], mas[i][-2], str(mas[i][1])])

    mas.sort(key=lambda x: x[2])
    mas3 = [[i + 1, mas[i][-3], mas[i][-2], str(mas[i][2])] for i in range(3)]
    for i in range(len(mas)):
        if mas[i][-1] == usName:
            mas3.append([i + 1, mas[i][-3], mas[i][-2], str(mas[i][2])])

    mas.sort(key=lambda x: x[3])
    mas4 = [[i + 1, mas[i][-3], mas[i][-2], str(mas[i][3])] for i in range(3)]
    for i in range(len(mas)):
        if mas[i][-1] == usName:
            mas4.append([i + 1, mas[i][-3], mas[i][-2], str(mas[i][3])])

    mas.sort(key=lambda x: x[4])
    masSum = [[i + 1, mas[i][-3], mas[i][-2], str(mas[i][4])] for i in range(3)]
    for i in range(len(mas)):
        if mas[i][-1] == usName:
            masSum.append([i + 1, mas[i][-3], mas[i][-2], str(mas[i][4])])

    return render(request, 'main/table.html', {'mas1': mas1, 'mas2': mas2, 'mas3': mas3, 'mas4': mas4,
                                               'masSum': masSum})


def about(request):
    return render(request, 'main/about.html')


def zada4i_tems(request):
    return render(request, 'main/zada4i_tems.html')


def developers(request):
    return render(request, 'main/developers.html')


def instruction(request):
    return render(request, 'main/instruction.html')


def studentStart(request):
    return render(request, 'main/studentStart.html')

def error(request):
    return render(request, 'main/error.html')


def error2(request):
    return render(request, 'main/error2.html')


def error3(request):
    return render(request, 'main/error3.html')

def workStatus(request):
    return render(request, 'main/workStatus.html')


def predCheckStartWork(request):
    answer = request.GET
    if 'check' in answer:
        alph = 'abcdefghijklmnopqrstuvwxyzABCDEFGHJKLMNOPQRSTUVWXYZ1234567890'
        key_alph = ')*(&^%$@!?/[]{}'
        tema = request.GET['tema']
        txt, otv = [], []
        tx, ot = '', ''
        alph = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        piffTr = [[3, 4, 5], [5, 12, 13], [8, 15, 17], [7, 24, 25], [9, 12, 15], [9, 40, 41], [11, 60, 61],
                  [12, 35, 37], [13, 84, 85]]
        if tema == '7start':
            count = randint(1, 8)
            if count == 1:
                txt.append('Дан треугольник, в котором одна сторона равна ***, другая сторона на ***'
                                                ' больше первой, а третья сторона на *** больше первой. '
                                                                                      'Найти периметр треугольника.')
            elif count == 2:

                txt.append('Дан треугольник, в котором одна сторона равна ***, другая сторона на '
                           '*** больше первой, а третья сторона на *** меньше первой. '
                                                                                      'Найти периметр треугольника.')
            elif count == 3:
                txt.append('Дан треугольник, в котором одна сторона равна ***, другая сторона на '
                           '*** меньше первой, а третья сторона на *** больше первой. '
                                                                                      'Найти периметр треугольника.')
            elif count == 4:
                txt.append('Дан треугольник, в котором одна сторона равна ***, другая сторона на *** '
                                                    'меньше первой, а третья сторона на *** меньше первой. '
                                                                                      'Найти периметр треугольника.')
            elif count == 5:
                txt.append('Дан треугольник, в котором одна сторона равна ***, другая сторона на '
                           '*** больше первой, а третья сторона на *** больше второй. '
                                                                                      'Найти периметр треугольника.')
            elif count == 6:
                txt.append('Дан треугольник, в котором одна сторона равна ***, другая сторона на '
                           '*** больше первой, а третья сторона на *** меньше второй. '
                                                                                      'Найти периметр треугольника.')
            elif count == 7:
                txt.append('Дан треугольник, в котором одна сторона равна ***, другая сторона на '
                           '*** меньше первой, а третья сторона на *** больше второй. '
                                                                                      'Найти периметр треугольника.')
            elif count == 8:
                txt.append('Дан треугольник, в котором одна сторона равна ***, другая сторона на '
                           '*** меньше первой, а третья сторона на *** меньше второй. '
                                                                                      'Найти периметр треугольника.')

            count = randint(1, 2)
            if count == 1:
                txt.append('Найдите площадь квадрата, если его периметр равен ***.')
            elif count == 2:
                txt.append('Найдите периметр квадрата. если его площадь равна ***.')

            count = randint(1, 4)
            if count == 1:
                txt.append('Дан прямоугольник. Одна сторона в нём равна ***, другая в *** раз(a) больше неё, '
                           'найти периметр прямоугольника.')
            elif count == 2:
                txt.append('Дан прямоугольник. Одна сторона в нём равна ***, другая в *** раз(a) больше неё, '
                           'найти площадь прямоугольника.')
            if count == 3:
                txt.append('Дан прямоугольник. Одна сторона в нём равна ***, другая в *** раз(a) меньше неё, '
                           'найти периметр прямоугольника.')
            if count == 4:
                txt.append('Дан прямоугольник. Одна сторона в нём равна ***, другая в *** раз(a) меньше неё, '
                           'найти площадь прямоугольника.')

            count2 = randint(1, 2)
            a, b, k = sample(alph, 3)
            if count2 == 1:
                count = randint(1, 2)
                if count == 1:
                    txt.append('Дан отрезок ' + str(a) + str(b) + ' длиной ***'
                                    ' см, на нём отметили точку ' + str(k) + ' так, что отрезок ' + str(a) + str(k) +
                               ' равен *** см, '
                                                    'чему равен отрезок ' + str(b) + str(k) + '?')
                elif count == 2:
                    txt.append('Дан отрезок ' + str(a) + str(b) + ' длиной *** см, на нём отметили точку ' + str(k) + ' так, что отрезок ' + str(b) + str(k) +
                               ' равен *** см, '
                                                    'чему равен отрезок ' + str(a) + str(k) + '?')
            elif count2 == 2:
                count = randint(1, 2)
                if count == 1:
                    txt.append('Дан отрезок ' + str(a) + str(b) + '. На нём лежит точка ' + str(k) +
                               ' и ' + str(a) + str(k) + ' равен *** см,'
                                                                              ' а ' + str(b) + str(k) + ' равен *** см, найдите длину отрезка ' +
                               str(a) + str(b) + '.')
                else:
                    txt.append('Дан отрезок ' + str(a) + str(b) + '. На нём лежит точка ' + str(k) +
                               ' и ' + str(b) + str(k) + ' равен *** см,'
                                                                              ' а ' + str(a) + str(k) + ' равен ***'
                                                                                    ' см, найдите длину отрезка ' +
                               str(a) + str(b) + '.')

            count = randint(1, 2)
            if count == 1:
                a, b, c, d = sample(alph, 4)
                txt.append('Внутри угла ' + str(a) + str(b) + str(c) + ' проведен луч ' + str(b) + str(d) +
                           '. Найти угол ' + str(a) + str(b) + str(c) + ', если угол ' + str(a) +
                           str(b) + str(d) + ' равен *** градусов, '
                                                                  'а угол ' + str(c) + str(b) + str(d) + ' на ***'
                                                                                                ' градусов больше.')
            elif count == 2:
                a, b, c, d = sample(alph, 4)
                txt.append('Внутри угла ' + str(a) + str(b) + str(c) + ' проведен луч ' + str(b) + str(d) +
                           '. Найти угол ' + str(a) + str(b) + str(d) + ', если угол ' + str(a) +
                           str(b) + str(c) + ' равен *** градусов, '
                                                                  'а угол ' + str(c) + str(b) + str(d) + ' на ***'
                                                                                            ' градусов меньше.')

            count = randint(1, 2)
            if count == 1:
                txt.append('Квадрат со стороной ** разделили на 2 прямоугольника так, что площадь одного '
                                                             'из них в **'
                           ' раз(а) больше другого. Найдите площадь большего прямоугольника.')
            else:
                txt.append('Квадрат со стороной ** разделили на 2 прямоугольника так, что площадь одного '
                                                             'из них в ***'
                           ' раз(а) больше другого. Найдите площадь меньшего прямоугольника.')

            # конец генерации стартовой работы за 7 класс

        if tema == '8start':
            alph = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            piffTr = [[3, 4, 5], [5, 12, 13], [8, 15, 17]]
            count = randint(1, 2)
            if count == 1:
                txt.append('Найдите больший смежный угол, если известно, что он на *** больше другого.')
            if count == 2:
                txt.append('Найдите меньший смежный угол, если известно, что он на *** меньше другого.')

            mass = []
            for i in range(1, 30):
                for j in range(1, 30):
                    if 180 % (i + j) == 0:
                        if i != j:
                            mass.append([i, j])
            count1 = randint(1, 2)
            count = randint(1, len(mass) - 1)
            k, m = mass[count]
            if count1 == 1:
                txt.append('Смежные углы относятся как ' + str(k) + ':***. Найдите величину большего из углов.')
                otv.append(str((180 // (k + m)) * max(k, m)))
            elif count1 == 2:
                txt.append('Смежные углы относятся как ***:' + str(m) +
                           '. Найдите величину меньшего из углов.')

            a, b, c = sample(alph, 3)
            p = randrange(100, 500, 2)
            x = randrange(50, 75, 2)
            txt.append('Дан равнобедренный треугольник ' + str(a) + str(b) + str(c) +
                       '. Найдите ' + str(b) + str(c) + ', если его периметр'
                                                        ' равен ***, а основание ' + str(a) + str(
                c) + ' равно ' + str(x) + '.')

            a, b, c, d = sample(alph, 4)
            count = randint(1, 4)
            mass = [50, 52, 54, 56, 60, 63, 64, 66, 68, 70, 72, 75, 76, 78, 80, 81, 84, 88, 90, 92, 96, 98, 99,
                    100, 102, 104, 105,
                    108, 110, 112, 114, 116, 117, 120, 124, 126, 128, 130, 132, 135, 136, 138]
            t1 = randint(1, len(mass) - 1)
            t = mass[t1]
            mass2 = []
            for i in range(1, 30):
                for j in range(1, 30):
                    if t % (i + j) == 0:
                        if i != j:
                            mass2.append([i, j])
            ln = len(mass2)
            count2 = randint(1, ln - 1)
            k, m = mass2[count2]
            if count == 1:
                txt.append('Дан треугольник ' + str(a) + str(b) + str(c) +
                           '. Его внешний угол ' + str(a) + str(b) + str(d) + ' равен ' + str(
                    t) + '°, а внутренние углы, '
                         'не смежные с ним, относятся как ' + str(k) + ':***. Найдите величину большего из этих углов.')
            elif count == 2:
                txt.append('Дан треугольник ' + str(a) + str(b) + str(c) +
                           '. Его внешний угол ' + str(a) + str(b) + str(d) + ' равен ' + str(
                    t) + '°, а внутренние углы, '
                         'не смежные с ним, относятся как ***:' + str(m) +
                           '. Найдите величину меньшего из этих углов.')
            if count == 3:
                txt.append('Дан треугольник ' + str(a) + str(b) + str(c) +
                           '. Его внешний угол ' + str(b) + str(c) + str(d) + ' равен ' + str(
                    t) + '°, а внутренние углы, '
                         'не смежные с ним, относятся как ' + str(k) + ':***. Найдите величину большего из этих углов.')
            if count == 4:
                txt.append('Дан треугольник ' + str(a) + str(b) + str(c) +
                           '. Его внешний угол ' + str(b) + str(c) + str(d) + ' равен ' + str(
                    t) + '°, а внутренние углы, '
                         'не смежные с ним, относятся как ***:' + str(m) +
                           '. Найдите величину меньшего из этих углов.')
            if count == 5:
                txt.append('Дан треугольник ' + str(a) + str(b) + str(c) +
                           '. Его внешний угол ' + str(b) + str(a) + str(d) + ' равен ' + str(
                    t) + '°, а внутренние углы, '
                         'не смежные с ним, относятся как ***:' + str(m) +
                           '. Найдите величину большего из этих углов.')
            if count == 6:
                txt.append('Дан треугольник ' + str(a) + str(b) + str(c) +
                           '. Его внешний угол ' + str(b) + str(a) + str(d) + ' равен ' + str(
                    t) + '°, а внутренние углы, '
                         'не смежные с ним, относятся как ' + str(k) + ':***. Найдите величину меньшего из этих углов.')

            count = randint(1, 4)
            a, b, c, d, m, n = sample(alph, 6)
            if count == 1:
                txt.append('Дан равнобедренный треугольник ' + str(a) + str(b) + str(c) + ' с основанием ' +
                           str(a) + str(c) + '. Биссектрисы углов при основании '
                                             'пересекаются в точке ' + str(d) + '. ∠' + str(b) + ' = ***°. '
                                                'Найдите величину угла ' + str(a) + str(d) + str(c) + '.')
            if count == 2:
                txt.append('Дан равнобедренный треугольник ' + str(a) + str(b) + str(c) + ' с основанием ' +
                           str(a) + str(c) + '. Биссектрисы углов при основании '
                                             'пересекаются в точке ' + str(d) + ', а также пересекают стороны ' +
                           str(a) + str(b) + ' и ' + str(b) + str(c) + ' в точках ' + str(m) + ' и ' + str(n) +
                           ' соответственно. ∠' + str(n) + str(d) + str(c) + ' = ***°. Найдите величину угла ' + str(b) + '.')
            if count == 3:
                txt.append('Дан равнобедренный треугольник ' + str(a) + str(b) + str(c) + ' с основанием ' +
                           str(a) + str(c) + '. Биссектрисы углов при основании '
                                             'пересекаются в точке ' + str(d) + ', а также пересекают стороны ' +
                           str(a) + str(b) + ' и ' + str(b) + str(c) + ' в точках ' + str(m) + ' и ' + str(n) +
                           ' соответственно. ∠' + str(m) + str(d) + str(a) + ' = ***°. Найдите величину угла ' + str(b) + '.')
            if count == 4:
                x = 2 * randint(50, 80)
                txt.append('Дан равнобедренный треугольник ' + str(a) + str(b) + str(c) + ' с основанием ' +
                           str(a) + str(c) + '. Биссектрисы углов при основании '
                                             'пересекаются в точке ' + str(d) + ', а также пересекают стороны ' +
                           str(a) + str(b) + ' и ' + str(b) + str(c) + ' в точках ' + str(m) + ' и ' + str(n) +
                           ' соответственно. ∠' + str(m) + str(d) + str(n) + ' = ***°. Найдите величину угла ' + str(b) + '.')

            count = randint(1, 4)
            a, b, c, d = sample(alph, 4)
            x = randint(80, 130)
            x += 1
            if count == 1:
                txt.append('Дан треугольник ' + str(a) + str(b) + str(c) + ' с прямым углом ' + str(b) +
                           '. Биссектриса этого угла образует с гипотенузой '
                           '∠' + str(b) + str(d) + str(c) + ' = ***. '
                                                                             'Найдите больший острый угол треугольника.')
                otv.append(str(max(135 - x, x - 45)))
            if count == 2:
                txt.append('Дан треугольник ' + str(a) + str(b) + str(c) + ' с прямым углом ' + str(b) +
                           '. Биссектриса этого угла образует с гипотенузой '
                           '∠' + str(b) + str(d) + str(c) + ' = ***. '
                                                                             'Найдите меньший острый угол треугольника.')
                otv.append(str(min(135 - x, x - 45)))
            if count == 3:
                txt.append('Дан треугольник ' + str(a) + str(b) + str(c) + ' с прямым углом ' + str(b) +
                           '. Биссектриса этого угла образует с гипотенузой '
                           '∠' + str(b) + str(d) + str(a) + ' = ***. '
                                                                             'Найдите больший острый угол треугольника.')
                otv.append(str(max(135 - x, x - 45)))
            if count == 4:
                txt.append('Дан треугольник ' + str(a) + str(b) + str(c) + ' с прямым углом ' + str(b) +
                           '. Биссектриса этого угла образует с гипотенузой '
                           '∠' + str(b) + str(d) + str(a) + ' = ***. '
                                                                             'Найдите меньший острый угол треугольника.')
                otv.append(str(min(135 - x, x - 45)))

            count = randint(1, 3)
            a, b, c = sample(alph, 3)
            mass = [50, 52, 54, 56, 60, 63, 64, 66, 68, 70, 72, 75, 76, 78, 80, 81, 84, 88, 90, 92, 96, 98, 99,
                    100, 102, 104, 105,
                    108, 110, 112, 114, 116, 117, 120, 124, 126, 128, 130, 132, 135, 136, 138]
            t1 = randint(1, len(mass) - 1)
            t = mass[t1]
            mass2 = []
            for i in range(2, t - 1):
                if t % i == 0:
                    mass2.append(i)
            count2 = randint(0, len(mass2) - 1)
            if count == 1:
                x = mass2[count2]
                y = randint(2, t // x)
                txt.append('Дан треугольник ' + str(a) + str(b) + str(c) + '. Сторона ' + str(b) + str(c) +
                           ' равна ' + str(t) + ', а сторона ' + str(a) + str(b) + ' меньше неё в ***'
                                                ' раз(a), сторона ' + str(a) + str(c) + ' на ***'
                                ' меньше ' + str(b) + str(c) + '. Найти периметр треугольника.')
                otv.append(str(t + (t // x) + t - y))
            if count == 2:
                x = randint(2, 3)
                y = randint((t * x - t), t * x - t + 50)
                txt.append('Дан треугольник ' + str(a) + str(b) + str(c) + '. Сторона ' + str(b) + str(c) +
                           ' равна ' + str(t) + ', а сторона ' + str(a) + str(b) + ' больше неё в ***'
                                            ' раз(a), сторона ' + str(a) + str(c) + ' на ' + str(y) +
                           ' больше ' + str(b) + str(c) + '. Найти периметр треугольника.')
                otv.append(str(t + (t * x) + t + y))
            if count == 3:
                x = mass2[count2]
                y = randint(1, t // x)
                txt.append('Дан треугольник ' + str(a) + str(b) + str(c) + '. Сторона ' + str(b) + str(c) +
                           ' равна ' + str(t) + ', а сторона ' + str(a) + str(b) + ' меньше неё в ***'
                                            ' раз(a), сторона ' + str(a) + str(c) + ' на ' + str(y) +
                           ' больше ' + str(b) + str(c) + '. Найти периметр треугольника.')
                otv.append(str(t + (t // x) + t + y))

            # конец генерации стартовой для 8

            # начало генерации стартовой для 9 класса
        if tema == '9start':
            count = randint(1, 2)
            a, b, c = sample(alph, 3)
            x = randrange(40, 120, 2)
            if count == 1:
                txt.append('В равнобедренном треугольнике ' + str(a) + str(b) + str(c) +
                           ' с основанием ' + str(a) + str(c) + ' угол ' + str(b) + ' равен *** градусов. '
                                                                                        'Найдите величину угла ' + str(
                    a) + '.')
            if count == 2:
                txt.append('В равнобедренном треугольнике ' + str(a) + str(b) + str(c) +
                           ' с основанием ' + str(a) + str(c) + ' угол ' + str(b) + ' равен *** градусов. '
                                                                                                         'Найдите величину угла ' + str(
                    c) + '.')

            count = randint(1, 8)
            count2 = 2
            count3 = randint(1, 2)
            x, y = piffTr[count][0] * count2, piffTr[count][1] * count2
            a, b, c, d = sample(alph, 4)
            if count3 == 1:
                txt.append('В ромбе ' + str(a) + str(b) + str(c) + str(d) + ' диагональ ' + str(a) + str(c) +
                           ' равна ***, a диагональ ' + str(b) + str(d) + ' равна ' + str(x) +
                           '. Найдите сторону ромба.')
                otv.append(str(piffTr[count][2]))
            elif count3 == 2:
                txt.append('В ромбе ' + str(a) + str(b) + str(c) + str(d) + ' диагональ ' + str(a) + str(c) +
                           ' равна ***, a диагональ ' + str(b) + str(d) + ' равна ' + str(x) +
                           '. Найдите площадь ромба.')
                otv.append(str((x * y) // 2))

            count = randint(1, 4)
            a, b, c, d, k = sample(alph, 5)
            x, y = randint(10, 50), randint(25, 60)
            if count == 1:
                txt.append('В параллелограмме ' + str(a) + str(b) + str(c) + str(d) + ' провели биссектрису '
                                                                                      'угла ' + str(
                    a) + ' так, что ' + str(c) + str(k) + ' = ' + str(x) +
                           ' и ' + str(k) + str(b) + ' = ***, найдите периметр ' + str(a) + str(b) + str(c) + str(d) + '.')
            if count == 2:
                txt.append('В параллелограмме ' + str(a) + str(b) + str(c) + str(d) + ' провели биссектрису '
                                                                                      'угла ' + str(
                    b) + ' так, что ' + str(d) + str(k) + ' = ' + str(x) +
                           ' и ' + str(k) + str(a) + ' = ***, найдите периметр ' + str(a) + str(b) + str(c) + str(d) + '.')
            if count == 3:
                txt.append('В параллелограмме ' + str(a) + str(b) + str(c) + str(d) + ' провели биссектрису '
                                                                                      'угла ' + str(
                    c) + ' так, что ' + str(a) + str(k) + ' = ' + str(x) +
                           ' и ' + str(k) + str(d) + ' = ***, найдите периметр ' + str(a) + str(b) + str(c) + str(d) + '.')
            if count == 4:
                txt.append('В параллелограмме ' + str(a) + str(b) + str(c) + str(d) + ' провели биссектрису '
                                                                                      'угла ' + str(
                    d) + ' так, что ' + str(b) + str(k) + ' = ' + str(x) +
                           ' и ' + str(k) + str(c) + ' = ***, найдите периметр ' + str(a) + str(b) + str(c) + str(d) + '.')

            count = randint(1, 4)
            a, b, c, d = sample(alph, 4)
            x, y = randrange(40, 80, 2), randrange(82, 120, 2)
            if count == 1:
                txt.append('Дана равнобедренная трапеция ' + str(a) + str(b) + str(c) + str(d) +
                           '. Меньшее основание ' + str(b) + str(c) + ' равно ' + str(x) + ', а основание '
                           + str(a) + str(d) + ' равно ***, '
                                                                    'угол ' + str(b) + ' равен 120. Найдите ' + str(
                    a) + str(b) + '.')
            elif count == 2:
                txt.append('Дана равнобедренная трапеция ' + str(a) + str(b) + str(c) + str(d) +
                           '. Меньшее основание ' + str(b) + str(c) + ' равно ' + str(x) + ', а основание '
                           + str(a) + str(d) + ' равно ***, '
                                                                    'угол ' + str(c) + ' равен 120. Найдите ' + str(
                    a) + str(b) + '.')
            elif count == 3:
                txt.append('Дана равнобедренная трапеция ' + str(a) + str(b) + str(c) + str(d) +
                           '. Меньшее основание ' + str(b) + str(c) + ' равно ' + str(x) + ', а основание '
                           + str(a) + str(d) + ' равно ***, '
                                                                    'угол ' + str(b) + ' равен 120. Найдите ' + str(
                    c) + str(d) + '.')
            elif count == 4:
                txt.append('Дана равнобедренная трапеция ' + str(a) + str(b) + str(c) + str(d) +
                           '. Меньшее основание ' + str(b) + str(c) + ' равно ' + str(x) + ', а основание '
                           + str(a) + str(d) + ' равно ***, '
                                                                    'угол ' + str(c) + ' равен 120. Найдите ' + str(
                    c) + str(d) + '.')

            count = randint(1, 8)
            count2 = randint(2, 3)
            x, y = piffTr[count][2] * count2, piffTr[count][0] * count2
            txt.append('На высоте трегольника лежит центр описанной окружности, который делит её на отрезки, '
                       'равные *** и ***. Найдите площадь этого треугольника.')

            a, b, c, d = sample(alph, 4)
            x, k = randrange(100, 300, 4), randrange(150, 500, 4)
            y = randint((x + k) // 4, (x + k) // 2)
            txt.append('Четырёхугольник ' + str(a) + str(b) + str(c) + str(d) + ' описали вокруг окружности. ' +
                       str(a) + str(b) + ' = ***, ' + str(a) + str(d) + ' = ' + str(y) +
                       ', ' + str(c) + str(d) + ' = ***. Найдите ' + str(b) + str(c) + '.')

            a, b, c, d, k = sample(alph, 5)
            number = '23456789'
            count = randint(1, 4)
            if count == 1:
                x, y = sample(number, 2)
                x, y = int(x), int(y)
                w = y * x * randint(2, 10)
                txt.append('Хорда ' + str(a) + str(b) + ' и хорда ' + str(c) + str(d) + ' пересекаются в точке ' +
                           str(k) + '. Найдите ' + str(a) + str(k) + ', если ' + str(k) + str(b) + ' = ' +
                           str(x) + ', ' + str(d) + str(k) + ' = ' + str(y) +
                           ', ' + str(c) + str(k) + ' = ***.')
                otv.append(str((w * y) // x))
            elif count == 2:
                x, y = sample(number, 2)
                x, y = int(x), int(y)
                w = y * x * randint(2, 10)
                txt.append('Хорда ' + str(a) + str(b) + ' и хорда ' + str(c) + str(d) + ' пересекаются в точке ' +
                           str(k) + '. Найдите ' + str(b) + str(k) + ', если ' + str(k) + str(a) + ' = ' +
                           str(x) + ', ' + str(d) + str(k) + ' = ' + str(y) +
                           ', ' + str(c) + str(k) + ' = ***.')
                otv.append(str((w * y) // x))
            elif count == 3:
                w, y = sample(number, 2)
                w, y = int(x), int(y)
                x = y * w * randint(2, 5)
                txt.append('Хорда ' + str(a) + str(b) + ' и хорда ' + str(c) + str(d) + ' пересекаются в точке ' +
                           str(k) + '. Найдите ' + str(c) + str(k) + ', если ' + str(k) + str(b) + ' = ' +
                           str(x) + ', ' + str(a) + str(k) + ' = ' + str(y) +
                           ', ' + str(d) + str(k) + ' = ***.')
                otv.append(str((x * y) // w))
            elif count == 4:
                w, y = sample(number, 2)
                w, y = int(x), int(y)
                x = y * w * randint(2, 10)
                txt.append('Хорда ' + str(a) + str(b) + ' и хорда ' + str(c) + str(d) + ' пересекаются в точке ' +
                           str(k) + '. Найдите ' + str(d) + str(k) + ', если ' + str(k) + str(b) + ' = ' +
                           str(x) + ', ' + str(a) + str(k) + ' = ' + str(y) +
                           ', ' + str(c) + str(k) + ' = ***.')
                otv.append(str((x * y) // w))

        # конец генерации работы для 9 класса

        # начало генерации стратовой работы для 10 класса
        if tema == '10start':
            a, b, c, d = sample(alph, 4)
            x = randrange(30, 60, 2)
            count = randint(1, 3)
            if count == 1:
                txt.append('В треугольнике ' + str(a) + str(b) + str(c) + ', прямым углом в котором является угол ' +
                           str(b) + ', вписана окружность '
                                    'с центром в точке ' + str(d) + '. Найдите угол ' + str(a) + str(d) + str(b) +
                           ', если угол ' + str(a) + str(c) + str(b) + ' равен ***.')
            if count == 2:
                txt.append('В треугольнике ' + str(a) + str(b) + str(c) + ', прямым углом в котором является угол ' +
                           str(a) + ', вписана окружность '
                                    'с центром в точке ' + str(d) + '. Найдите угол ' + str(b) + str(d) + str(a) +
                           ', если угол ' + str(b) + str(c) + str(a) + ' равен ***.')
            if count == 3:
                txt.append('В треугольнике ' + str(a) + str(b) + str(c) + ', прямым углом в котором является угол ' +
                           str(c) + ', вписана окружность '
                                    'с центром в точке ' + str(d) + '. Найдите угол ' + str(c) + str(d) + str(b) +
                           ', если угол ' + str(c) + str(a) + str(b) + ' равен ***.')


            data = [30, 45, 60, 90, 120, 180]
            count = randint(0, 5)
            y = data[count]
            l = ''.join(sample(alph, 1))
            otvet = randrange(2, 16, 2)
            x = (otvet * (360 // y)) // 2
            txt.append('Пусть ' + str(l) + ' – длина дуги окружности радиусом ***, градусная мера которой равна ***. '
                                                                    'В ответе укажите величину ' + str(l) + '/pi')

            count = randint(1, 4)
            a, d = sample(alph, 2)
            if count == 1:
                txt.append('Из точки ' + str(a) + ' проведены две касательные к окружности с центром в точке ' + str(d)
                           + '. Радиус окружности равен *** см, угол между касательными равен 60°. '
                                                                     'Найти расстояние ' + str(a) + str(d) + '.')
            if count == 2:
                txt.append('Из точки ' + str(a) + ' проведены две касательные к окружности с центром в точке ' + str(d)
                           + '. Диаметр окружности равен *** см, угол между касательными равен 60°. '
                                                                      'Найти расстояние ' + str(a) + str(d) + '.')
            if count == 3:
                txt.append('Из точки ' + str(a) + ' проведены две касательные к окружности с центром в точке ' + str(d)
                           + '. Расстояние от точки ' + str(a) + ' до точки ' + str(d) + ' равно ***, '
                                                'угол между касательными равен 60°. Найдите радус окружности.')
            if count == 4:
                txt.append('Из точки ' + str(a) + ' проведены две касательные к окружности с центром в точке ' + str(d)
                           + '. Расстояние от точки ' + str(a) + ' до точки ' + str(d) + ' равно ***, '
                                    'угол между касательными равен 60°. Найдите диаметр окружности.')

            count = randint(1, 4)
            a, b, c, d = sample(alph, 4)
            if count == 1:
                x = randint(10, 23)
                y = randint(25, 40)
                z = x + randint(22, 31)
                txt.append('Четырёхугольник ' + str(a) + str(b) + str(c) + str(d) +
                           ' описан около окружности. ' + str(c) + str(d) + '=' + str(x) +
                           ', ' + str(a) + str(d) + '=***, ' + str(b) + str(c) + '=' + str(z) +
                           '. Найдите ' + str(a) + str(b) + '.')
            elif count == 2:
                x = randint(10, 23)
                y = randint(25, 40)
                z = x + randint(22, 31)
                txt.append('Четырёхугольник ' + str(a) + str(b) + str(c) + str(d) +
                           ' описан около окружности. ' + str(a) + str(b) + '=' + str(x) +
                           ', ' + str(a) + str(d) + '=***, ' + str(b) + str(c) + '=' + str(z) +
                           '. Найдите ' + str(c) + str(d) + '.')
            elif count == 3:
                x = randint(10, 23)
                y = randint(25, 40)
                z = x + randint(22, 31)
                txt.append('Четырёхугольник ' + str(a) + str(b) + str(c) + str(d) +
                           ' описан около окружности. ' + str(a) + str(d) + '=' + str(x) +
                           ', ' + str(a) + str(b) + '= ***, ' + str(d) + str(c) + '=' + str(z) +
                           '. Найдите ' + str(b) + str(c) + '.')
            elif count == 4:
                x = randint(10, 23)
                y = randint(25, 40)
                z = x + randint(22, 31)
                txt.append('Четырёхугольник ' + str(a) + str(b) + str(c) + str(d) +
                           ' описан около окружности. ' + str(b) + str(c) + '=' + str(x) +
                           ', ' + str(a) + str(b) + '= ***, ' + str(d) + str(c) + '=' + str(z) +
                           '. Найдите ' + str(a) + str(d) + '.')

            a, b, c, d = sample(alph, 4)
            v_a, v_b, v_c, v_d = (randint(1, 4), randint(1, 3)), (randint(2, 5), randint(1, 2)), \
                                 (randint(1, 2), randint(3, 6)), (randint(1, 7), randint(4, 6))
            x = v_a[0] * v_b[0] * v_c[0] * v_d[0]
            y = v_a[1] * v_b[1] * v_c[1] * v_d[1]
            otvet = x + y
            txt.append('На плоскости даны точки ' + str(a) + str(v_a) + ', ' + str(b) + str(v_b) + ', ' +
                       str(d) + str(v_d) + ', ' + str(c) + str(v_c) + '. Найдите скалярное произведение векторов.')

            a, b, c = sample(alph, 3)
            nums = '012345678'
            count = randint(1, 3)
            if count == 1:
                count1, count2, count3 = sample(nums, 3)
                count1, count2, count3 = int(count1), int(count2), int(count3)
                v_a, v_b, v_c = (piffTr[count1][1], piffTr[count1][0]), \
                                (piffTr[count2][0], piffTr[count2][1]), \
                                (piffTr[count3][1], piffTr[count3][0])
                txt.append('Даны векторы ' + str(a) + str(v_a) + ', ' + str(b) + str(v_b) +
                           ' и ' + str(c) + str(v_c) + '. '
                                                       'Найдите длину вектора ' + str(a) + ' + ' + str(b) + ' + ' + str(
                    c) + '.')
            elif count == 2:
                nums1 = '012'
                nums2 = '345'
                nums3 = '78'
                count1 = ''.join(sample(nums1, 1))
                count2 = ''.join(sample(nums3, 1))
                count3 = ''.join(sample(nums2, 1))
                count1, count2, count3 = int(count1), int(count2), int(count3)
                v_a, v_b, v_c = (piffTr[count1][1], piffTr[count1][0]), \
                                (piffTr[count2][0], piffTr[count2][1]), \
                                (piffTr[count3][1], piffTr[count3][0])
                txt.append('Даны векторы ' + str(a) + str(v_a) + ', ' + str(b) + str(v_b) +
                           ' и ' + str(c) + str(v_c) + '. '
                                                       'Найдите длину вектора ' + str(a) + ' + ' + str(
                    b) + ' - ' + str(c) + '.')
            elif count == 3:
                nums1 = '012'
                nums2 = '345'
                nums3 = '678'
                count1 = ''.join(sample(nums3, 1))
                count2 = ''.join(sample(nums2, 1))
                count3 = ''.join(sample(nums1, 1))
                count1, count2, count3 = int(count1), int(count2), int(count3)
                v_a, v_b, v_c = (piffTr[count1][1], piffTr[count1][0]), \
                                (piffTr[count2][0], piffTr[count2][1]), \
                                (piffTr[count3][1], piffTr[count3][0])
                txt.append('Даны векторы ' + str(a) + str(v_a) + ', ' + str(b) + str(v_b) +
                           ' и ' + str(c) + str(v_c) + '. '
                                                       'Найдите длину вектора ' + str(a) + ' - ' + str(
                    b) + ' + ' + str(c) + '.')
        tems = {'7start': 'Стартовая работа для 7 класса',
                '8start': 'Стартовая работа для 8 класса',
                '9start': 'Стартовая работа для 9 класса',
                '10start': 'Стартовая работа для 10 класса'
                }
        tx = '${!$%^'.join(txt)
        return render(request, 'main/CheckStartWork.html', {'data': txt, 'tema': tems[tema]})
    return render(request, 'main/predCheckStartWork.html')


def start(request):
    request.session['registration'] = '*#@^' * 6
    request.session['registration2'] = '*#@^' * 6
    return render(request, 'main/start.html')


def teacherTask(request):
    answer = request.GET
    if 'workStartStud' in answer:
        password = answer['password']
        name = answer['name']
        surname = answer['surname']
        pin = answer['pin']
        if TasksAkt.objects.filter(pole8=password).exists():
            data = TasksAkt.objects.get(pole8=password)
            if data.pole5 == '2':
                return render(request, 'main/ujresh.html')
            if data.pole5 != '1' and data.pole5 != '2':
                data.pole9 = str(datetime.now() + timedelta(hours=3))[0:19]
            if data.pole5 == '1':
                name2, surname2, pin2 = data.studentId.split('{#{%%')
                if name2 == answer['name'] and surname2 == answer['surname'] and \
                        pin2 == answer['pin']:
                    return redirect('Zada4iStud')
                else:
                    mess = 'Введённые данные не совпадают!'
                    return render(request, 'main/error4.html', {'mess': mess})
            request.session['id_work'] = TasksAkt.objects.get(pole8=password).id
            table = TasksAkt.objects.get(id=request.session['id_work'])
            zada4i = table.pole1.split('${!$%^')
            request.session['zada4a_num'] = 0
            data.studentId = str(name) + '{#{%%' + str(surname) + '{#{%%' + str(pin)
            data.pole11 = '$%&^' * (len(zada4i) - 1)
            data.pole5 = '1'
            data.save()
            return redirect('Zada4iStud')
        else:
            return render(request, 'main/badpass.html')
    return render(request, 'main/teacherTask.html', {'data': ((datetime.strptime(str(datetime.now() + timedelta(hours=3))[0:19], "%Y-%m-%d %H:%M:%S")))})

# def teacherReg(request):
#     return render(request, 'main/teacherReg.html')


def Zada4iStud(request):
    table = TasksAkt.objects.get(id=request.session['id_work'])
    zada4i = table.pole1.split('${!$%^')
    prav_otvet = table.pole2.split('${!$%^')
    lst = table.pole11.split('$%&^')
    answer = request.GET
    zada4a = ''
    date_open = datetime.strptime(table.pole3.split('#*)&^')[0], "%Y-%m-%dT%H:%M")
    date_end = datetime.strptime(table.pole3.split('#*)&^')[1], "%Y-%m-%dT%H:%M")
    ds = int(float(table.pole3.split('#*)&^')[-1])) * 60 + 1
    seconds = ds - ((datetime.strptime(str(datetime.now() + timedelta(hours=3))[0:19], "%Y-%m-%d %H:%M:%S") -
                     datetime.strptime(table.pole9, "%Y-%m-%d %H:%M:%S")).seconds)
    if date_end > datetime.strptime(table.pole9, "%Y-%m-%d %H:%M:%S") >= date_open:
        if (date_end - datetime.strptime(table.pole9, "%Y-%m-%d %H:%M:%S")).seconds >= seconds:
            work_seconds = seconds + 1
        else:
            work_seconds = seconds + 1 - \
                           (date_end - datetime.strptime(str(datetime.now() + timedelta(hours=3))[0:19], "%Y-%m-%d %H:%M:%S")).seconds
    elif date_end < datetime.strptime(table.pole9, "%Y-%m-%d %H:%M:%S"):
        mess = 'Работа уже закрыта...Вы опоздали!'
        return render(request, 'main/outofdate.html', {'mess': mess})
    elif datetime.strptime(table.pole9, "%Y-%m-%d %H:%M:%S") < date_open:
        mess = 'Работа ещё не началась! Она откроется ' + str(datetime.strptime(table.pole9, "%Y-%m-%d %H:%M:%S"))
        table.pole5 = '0'
        table.save()
        return render(request, 'main/outofdate.html', {'mess': mess})

    # if work_seconds <= 0:
    #     # table.pole5 = '2'
    #     # table.save()
    #     return redirect('studentItogStat')

    request.session['zada4a_num'] = parse_otveti(lst, request.session['zada4a_num'])

    if work_seconds <= 0:
        table.pole10 = table.pole11
        table.pole5 = '2'
        table.save()
        mass = []
        for i in range(len(zada4i)):
            if lst[i] == '':
                mass.append([zada4i[i], 'Ответа нет!!!'])
            else:
                mass.append([zada4i[i], lst[i]])
        request.session['zada4i'] = zada4i
        return redirect('studentItogStat')

    if request.session['zada4a_num'] == 999 and work_seconds > 0:
        table.pole5 = '2'
        table.pole10 = table.pole11
        table.save()
        mass = []
        for i in range(len(zada4i)):
            if lst[i] == '':
                mass.append([zada4i[i], 'Ответа нет!!!'])
            else:
                mass.append([zada4i[i], lst[i]])
        request.session['zada4i'] = zada4i
        return redirect('studentStat')

    zada4a = zada4i[request.session['zada4a_num']]

    if 'confirm' in answer:
        lst[request.session['zada4a_num']] = answer['otvet']
        request.session['zada4a_num'] = (request.session['zada4a_num'] + 1) % len(lst)
        table.pole11 = '$%&^'.join(lst)
        table.save()
        return redirect('Zada4iStud')

    if 'prop' in answer:
        request.session['zada4a_num'] = (request.session['zada4a_num'] + 1) % len(lst)
        return redirect('Zada4iStud')

    if 'change' in answer:
        mass = []
        count = 0
        for i in range(len(zada4i)):
            if lst[i] == '':
                mass.append([zada4i[i], 'Ответа нет!!!'])
                count += 1
            else:
                mass.append([zada4i[i], lst[i]])
        request.session['zada4i'] = zada4i
        if count == len(mass):
            return redirect('Zada4iStud')
        return redirect('studentStat')

    if 'end' in answer:
        table.pole10 = table.pole11
        table.pole5 = '2'
        table.save()
        mass = []
        for i in range(len(zada4i)):
            if lst[i] == '':
                mass.append([zada4i[i], 'Ответа нет!!!'])
            else:
                mass.append([zada4i[i], lst[i]])
        request.session['zada4i'] = zada4i
        work_seconds = 0
        return redirect('studentItogStat')

    return render(request, 'main/Zada4iStud.html', {'zada4a': zada4a, 'zada4a_num': request.session['zada4a_num'] + 1,
                                                    'time': work_seconds})


def parse_otveti(lst, num):
    kolvo = len(lst)
    for i in range(num, num + kolvo):
        if lst[i % kolvo] == '':
            return i % kolvo
    return 999

# print(parse_otveti(['1111', '2222', '3333'], 3))


def studentStat(request):
    answer = request.GET
    table = TasksAkt.objects.get(id=request.session['id_work'])
    lst = table.pole11.split('$%&^')
    zada4i = request.session['zada4i']
    mass = []
    date_open = datetime.strptime(table.pole3.split('#*)&^')[0], "%Y-%m-%dT%H:%M")
    date_end = datetime.strptime(table.pole3.split('#*)&^')[1], "%Y-%m-%dT%H:%M")
    ds = int(float(table.pole3.split('#*)&^')[-1])) * 60 + 1
    seconds = ds - ((datetime.strptime(str(datetime.now() + timedelta(hours=3))[0:19], "%Y-%m-%d %H:%M:%S") -
                     datetime.strptime(table.pole9, "%Y-%m-%d %H:%M:%S")).seconds)
    if date_end > datetime.strptime(table.pole9, "%Y-%m-%d %H:%M:%S") >= date_open:
        if (date_end - datetime.strptime(table.pole9, "%Y-%m-%d %H:%M:%S")).seconds >= seconds:
            work_seconds = seconds + 1
        else:
            work_seconds = seconds + 1 - \
                           (date_end - datetime.strptime(str(datetime.now() + timedelta(hours=3))[0:19], "%Y-%m-%d %H:%M:%S")).seconds
    else:
        return render(request, 'main/outofdate.html')


    for i in range(len(zada4i)):
        if lst[i] != '':
            mass.append([i + 1, zada4i[i], lst[i]])


    if work_seconds <= 0:
        table.pole10 = table.pole11
        table.pole5 = '2'
        table.save()
        request.session['zada4i'] = zada4i
        return redirect('studentItogStat')

    if 'change' in answer:
        num = answer['zada4a_num']
        if num == '':
            return redirect('studentStat')
        zada4a_num = int(num)
        otvet = answer['otvet']
        lst = table.pole11.split('$%&^')
        lst[zada4a_num - 1] = otvet
        table.pole11 = '$%&^'.join(lst)
        table.pole10 = table.pole11
        table.save()
        return redirect('studentStat')

    if 'back' in answer:
        return redirect('Zada4iStud')

    if 'end' in answer:
        table.pole10 = table.pole11
        table.pole5 = '2'
        table.save()
        mass = []
        for i in range(len(zada4i)):
            if lst[i] == '':
                mass.append([i + 1, zada4i[i], 'Ответа нет!!!'])
            else:
                mass.append([i + 1, zada4i[i], lst[i]])
        request.session['zada4i'] = zada4i
        work_seconds = 0
        return redirect('studentItogStat')

    return render(request, 'main/studentStat.html', {'otveti': mass, 'time': work_seconds})


def studentItogStat(request):
    answer = request.GET
    table = TasksAkt.objects.get(id=request.session['id_work'])
    lst = table.pole11.split('$%&^')
    zada4i = request.session['zada4i']
    true_ans = table.pole2.split('${!$%^')
    mass = []

    prav = 0

    for i in range(len(zada4i)):
        if lst[i] == '':
            mass.append([i + 1, zada4i[i], 'Ответа нет!!!', true_ans[i]])
        else:
            if lst[i] == true_ans[i]:
                prav += 1
            mass.append([i + 1, zada4i[i], lst[i], true_ans[i]])

    itog = int((prav / len(zada4i)) * 100)

    return render(request, 'main/studentItogStat.html', {'otveti': mass, 'itog': itog})

def teacherRegist(request):
    data = request.session['registration'].split('*#@^')
    if request.method == 'GET':
        answer = request.GET
        if 'sur' in answer and 'name' in answer and 'patr' in answer and 'id' in answer and 'email' in answer:
            surname = answer.__getitem__('sur').replace(' ', '').capitalize()
            name = answer.__getitem__('name').replace(' ', '').capitalize()
            patronymic = answer.__getitem__('patr').replace(' ', '').capitalize()
            email = answer.__getitem__('email').replace(' ', '')
            if surname == '' or name == '' or patronymic == '': return redirect('teacherRegist')
            lg = answer.__getitem__('id')
            password = answer['password']
            password2 = answer['password2']
            if password2 == password:
                if len(surname) < 2 or len(name) < 2 or len(surname) > 25 or\
                        len(name) > 25 or len(lg) > 30 or len(email) < 6:
                    return redirect('teacherRegist')
                if User.objects.filter(username=lg).exists():
                    return render(request, 'main/ujteacheruse.html')
                if TeachersAkt.objects.filter(email=email).exists() or Polzakt.objects.filter(electpoch=email).exists():
                    return render(request, 'main/view_message2.html',
                                  {'link': 'teacherRegist',
                                    'ms': 'Такая почта уже зарегестрирована. Проверьте свои данные!'
                                   }
                                  )
                else:
                    try:
                        send_mail(
                            'Оповещение для учителя платформы GeoTutor!',
                            'Добро пожаловать! Мы рады приветствовать вас на нашей платформе)',
                            'geometrix2023_2024@mail.ru',
                            [email],
                            fail_silently=False,
                        )
                    except BadHeaderError:
                        data[0], data[1], data[2], data[3], data[4], data[5], data[6] = surname, name, patronymic, email,\
                                                                                        lg, password, password2
                        request.session['registration'] = '*#@^'.join(data)
                        mess = 'В почте неправильные заголовки, попробуйте ещё раз!'
                        return render(request, 'main/error3.html', {'mess': mess})
                    except Exception as e:
                        data[0], data[1], data[2], data[3], data[4], data[5], data[6] = surname, name, patronymic, email, \
                                                                               lg, password, password2
                        request.session['registration'] = '*#@^'.join(data)
                        mess = 'Ошибка при отправке письма, проверьте название вашей почты и попробуйте ещё раз!'
                        return render(request, 'main/error3.html', {'mess': mess})
                    TeachersAkt(idTeacher=lg, surname=surname, name=name, patronymic=patronymic,
                                email=email).save()
                    User.objects.create_user(lg, '', password, first_name=name + '{^@$' + surname + '{^@$' +
                                                                                         patronymic).save()
                    user = authenticate(request, username=lg, password=password)
                    login(request, user)
                    uz = TeachersAkt.objects.get(idTeacher=request.user.username)
                    uz.pole3 = password
                    uz.save()
                    teacher = User.objects.get(username=lg)
                    teacher.last_name = '1'
                    teacher.save()
                    mess = 'Пароли не совпадают, попробуйте ещё раз!'
                    chat_id = 914614230  # Здесь можно использовать chat_id пользователя или группы
                    message_text = "На сайте появился новый пользователь:\nЛогин: " + lg + '\nФИО: ' + \
                                   surname + ' ' + name + ' ' + patronymic + '\nEmail: ' + email
                    send_telegram_message(chat_id, message_text)
                    return render(request, 'main/uspTeacherReg.html', {'nm': name + ' ' + patronymic})
            else:
                data[0], data[1], data[2], data[3], data[4] = surname, name, patronymic, email, lg
                request.session['registration'] = '*#@^'.join(data)
                mess = 'Пароли не совпадают, попробуйте ещё раз!'
                return render(request, 'main/notmatch.html', {'mess': mess})
    return render(request, 'main/teacherReg.html', {'data': data})



def is_russian(text):
    russian_alphabet = set(
        range(ord('а'), ord('я') + 1))  # Кодовые точки символов русского алфавита

    for char in text:
        if ord(char.lower()) not in russian_alphabet:
            return False

    return True


def is_english(text):
    russian_alphabet = set(
        range(ord('a'), ord('z') + 1))  # Кодовые точки символов русского алфавита

    for char in text:
        if ord(char.lower()) not in russian_alphabet:
            return False

    return True



def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot6565010045:AAEDNDSr8auFdpAloDoihYC2A8HwsqWX8Vc/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, json=data)
    return response.json()


def teacherReg(request):
    answer = request.GET
    user_id = request.user.username
    fl0 = '0'
    if (user_id != ''):
        teacher = User.objects.get(username=user_id)
        if teacher.last_name != '1':
            mess = 'Увы, вы не учитель...'
            return render(request, 'main/error2.html', {'mess': mess})
        nm = request.user.first_name.split('{^@$')
        fl = 1
        nm = nm[0] + ' ' + nm[-1]
    else:
        nm = ''
        fl = 0
    # if request.method == 'GET':
    # answer = request.GET
    if 'reg1' in answer:
        return redirect('teacherRegist')
    if 'intlg1' in answer:
        lg = answer.__getitem__('lg')
        password = answer.__getitem__('password')
        if len(lg) < 3: return redirect('teacherReg')
        if User.objects.filter(username=lg).exists() == 1:
            teacher = User.objects.get(username=lg)
            if teacher.last_name == '1':
                if password == TeachersAkt.objects.get(idTeacher=lg).pole3:
                    user = authenticate(request, username=lg, password=password)
                    login(request, user)
                    return redirect('teacherReg')
                else:
                    return render(request, 'main/wrong_password.html')
            else:
                mess = 'Увы, вы не учитель...'
                return render(request, 'main/error2.html', {'mess': mess})
        else:
            return render(request, 'main/nezar2.html')
    if 'createWork' in answer:
        return redirect('createWork')
    return render(request, 'main/teacherStart.html', {'nm': nm, 'fl': fl, 'fl0': fl0})

def summary_of_work(request):
    answer = request.GET
    name_of_work = request.session['name_of_work']
    data = []
    work_name, date, time, tema = '', '', '', ''
    if TasksAkt.objects.filter(pole6=name_of_work).exists() == 1:
        rows = TasksAkt.objects.filter(pole6=name_of_work)
        work_name = name_of_work
        time = rows[0].pole3.split('#*)&^')[-1]
        date = 'с ' + ' '.join(rows[0].pole3.split('#*)&^')[0].split('T')) + ' по ' + \
               ' '.join(rows[0].pole3.split('#*)&^')[1].split('T'))
        tema = rows[0].pole12
        count = 0
        for j in rows:
            lst = j.pole11.split('$%&^')
            zada4i = j.pole1.split('${!$%^')
            true_ans = j.pole2.split('${!$%^')
            dano = 0
            prav = 0

            if len(lst) == 1 and lst[0] == '0':
                dano, prav = 0, 0
            else:
                for i in range(len(zada4i)):
                    if lst[i] != '':
                        dano += 1
                        if lst[i] == true_ans[i]:
                            prav += 1

            if j.studentId == '':
                name, surname = 'Не ', 'выполнено'
            else:
                name, surname = j.studentId.split('{#{%%')[0], j.studentId.split('{#{%%')[1]

            itog = int((prav / len(zada4i)) * 100)
            password = j.pole8

            data.append([count + 1, name, surname, dano, prav, itog, password])
            count += 1
    else:
        mess = 'Такой работы не существует...проверьте название ещё раз!)'
        return render(request, 'main/error5.html', {'mess': mess})
    if 'check' in answer:
        passw = answer['password']
        if TasksAkt.objects.filter(pole8=passw).exists() == 1:
            request.session['password2'] = passw
            return redirect('TeacherCheckStat')
        else:
            mess = 'Увы, такой работы не существует....'
            return render(request, 'main/error6.html', {'mess': mess})
    return render(request, 'main/summary_of_work.html', {'data': data, 'work_name': work_name,
                                                         'tema': tema, 'date': date, 'time': time})

def CheckStartWork(request):
    return render(request, 'main/CheckStartWork.html')


def createWork(request):
    answer = request.GET
    if 'create' in answer:
        teacher_id = request.user.username
        work_name = answer['work_name']
        lst = []
        start_date = answer['start_date']
        end_date = answer['end_date']
        if start_date == end_date:
            mess = 'Даты совпадают, попробуйте заново!'
            return render(request, 'main/error.html', {'mess': mess})
        elif end_date < start_date:
            mess = 'Дата конца раньше, чем дата начала. Попробуйте ещё раз!'
            return render(request, 'main/error.html', {'mess': mess})
        elif datetime.strptime(end_date, "%Y-%m-%dT%H:%M") < \
                datetime.strptime(str(datetime.now() + timedelta(hours=3))[0:19], "%Y-%m-%d %H:%M:%S"):
            mess = 'Дата конца раньше нынешней. Попробуйте ещё раз!'
            return render(request, 'main/error.html', {'mess': mess})
        time = answer['time']
        if not (time.isdigit()):
            message = 'Введите целое числовое значение длительности работы в минутах!'
            return render(request, 'main/error.html', {'mess': message})
        lst.append(str(answer['start_date']))
        lst.append(str(answer['end_date']))
        lst.append(str(answer['time']))
        dates = '#*)&^'.join(lst)
        counter = answer['count']
        if not(counter.isdigit()):
            message = 'Введите целое числовое значение кол-ва вариантов!'
            return render(request, 'main/error.html', {'mess': message})
        passwords, keys = [], []
        for i in range(int(counter)):
            alph = 'abcdefghijklmnopqrstuvwxyzABCDEFGHJKLMNOPQRSTUVWXYZ1234567890'
            key_alph = ')*(&^%$@!?/[]{}'
            work_password = ''.join(sample(alph, 12))
            tema = request.GET['tema']
            txt, otv = [], []
            tx, ot = '', ''
            alph = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            piffTr = [[3, 4, 5], [5, 12, 13], [8, 15, 17], [7, 24, 25], [9, 12, 15], [9, 40, 41], [11, 60, 61],
                      [12, 35, 37], [13, 84, 85]]
            if tema == '7start':
                count = randint(1, 8)
                if count == 1:
                    a, x, y = randint(15, 150), randint(10, 50), randint(10, 50)
                    txt.append('Дан треугольник, в котором одна сторона равна ' + str(a) + ', другая сторона на ' +
                               str(x) + ' больше первой, а третья сторона на ' + str(y) + ' больше первой. '
                                                                                        'Найти периметр треугольника.')
                    otv.append(str(3 * a + x + y))
                elif count == 2:
                    a = randint(50, 150)
                    x = randint(2, 30)
                    y = randint(2, a - x)
                    txt.append('Дан треугольник, в котором одна сторона равна ' + str(a) + ', другая сторона на ' +
                               str(x) + ' больше первой, а третья сторона на ' + str(y) + ' меньше первой. '
                                                                                        'Найти периметр треугольника.')
                    otv.append(str(3 * a + x - y))
                elif count == 3:
                    a = randint(50, 150)
                    y = randint(2, 30)
                    x = randint(2, a - y)
                    txt.append('Дан треугольник, в котором одна сторона равна ' + str(a) + ', другая сторона на ' +
                               str(x) + ' меньше первой, а третья сторона на ' + str(y) + ' больше первой. '
                                                                                        'Найти периметр треугольника.')
                    otv.append(str(3 * a + y - x))
                elif count == 4:
                    a = randint(50, 150)
                    x = randint(2, 30)
                    minn = a - x
                    y = randint(2, a - minn)
                    txt.append('Дан треугольник, в котором одна сторона равна ' + str(a) + ', другая сторона на ' +
                               str(x) + ' меньше первой, а третья сторона на ' + str(y) + ' меньше первой. '
                                                                                        'Найти периметр треугольника.')
                    otv.append(str(3 * a - x - y))
                elif count == 5:
                    a = randint(50, 150)
                    x = randint(2, 30)
                    y = randint(2, a)
                    txt.append('Дан треугольник, в котором одна сторона равна ' + str(a) + ', другая сторона на ' +
                               str(x) + ' больше первой, а третья сторона на ' + str(y) + ' больше второй. '
                                                                                        'Найти периметр треугольника.')
                    otv.append(str(3 * a + 2 * x + y))
                elif count == 6:
                    a = randint(15, 150)
                    x = randint(2, 30)
                    y = randint(2, a)
                    txt.append('Дан треугольник, в котором одна сторона равна ' + str(a) + ', другая сторона на ' +
                               str(x) + ' больше первой, а третья сторона на ' + str(y) + ' меньше второй. '
                                                                                        'Найти периметр треугольника.')
                    otv.append(str(3 * a + 2 * x - y))
                elif count == 7:
                    a = randint(50, 150)
                    x = randint(2, 30)
                    y = randint(2, 50)
                    txt.append('Дан треугольник, в котором одна сторона равна ' + str(a) + ', другая сторона на ' +
                               str(x) + ' меньше первой, а третья сторона на ' + str(y) + ' больше второй. '
                                                                                        'Найти периметр треугольника.')
                    otv.append(str(3 * a + y - 2 * x))
                elif count == 8:
                    a = randint(50, 150)
                    x = randint(2, 20)
                    y = randint(2, 10)
                    txt.append('Дан треугольник, в котором одна сторона равна ' + str(a) + ', другая сторона на ' +
                               str(x) + ' меньше первой, а третья сторона на ' + str(y) + ' меньше второй. '
                                                                                        'Найти периметр треугольника.')
                    otv.append(str(3 * a - 2 * x - y))


                a = randint(3, 200)
                if a % 10 == 0:
                    a = randint(3, 99)
                count = randint(1, 2)
                if count == 1:
                    p = a * 4
                    txt.append('Найдите площадь квадрата, если его периметр равен ' + str(p) + '.')
                    otv.append(str(a ** 2))
                elif count == 2:
                    s = a ** 2
                    txt.append('Найдите периметр квадрата. если его площадь равна ' + str(s) + '.')
                    otv.append(str(a * 4))


                count = randint(1, 4)
                if count == 1:
                    a = randint(12, 50)
                    k = randint(2, 9)
                    txt.append('Дан прямоугольник. Одна сторона в нём равна ' + str(a) + ', другая в ' + str(k) +
                               ' раз(a) больше неё, '
                               'найти периметр прямоугольника.')
                    otv.append(str(2 * a + (2 * a * k)))
                elif count == 2:
                    a = randint(12, 50)
                    k = randint(2, 9)
                    txt.append('Дан прямоугольник. Одна сторона в нём равна ' + str(a) + ', другая в ' + str(k) +
                               ' раз(a) больше неё, '
                               'найти площадь прямоугольника.')
                    otv.append(str(a * (a * k)))
                if count == 3:
                    nums = [i for i in range(12, 50) if check_prost(i)]
                    a = nums[randint(0, len(nums) - 1)]
                    dels = [i for i in range(2, a - 1) if a % i == 0]
                    k = dels[randint(0, len(dels) - 1)]
                    txt.append('Дан прямоугольник. Одна сторона в нём равна ' + str(a) + ', другая в ' + str(k) +
                               ' раз(a) меньше неё, '
                               'найти периметр прямоугольника.')
                    otv.append(str(2 * a + (2 * (a // k))))
                if count == 4:
                    nums = [i for i in range(12, 50) if check_prost(i)]
                    a = nums[randint(0, len(nums) - 1)]
                    dels = [i for i in range(2, a - 1) if a % i == 0]
                    k = dels[randint(0, len(dels) - 1)]
                    txt.append('Дан прямоугольник. Одна сторона в нём равна ' + str(a) + ', другая в ' + str(k) +
                               ' раз(a) меньше неё, '
                               'найти площадь прямоугольника.')
                    otv.append(str(a * (a // k)))


                count2 = randint(1, 2)
                a, b, k = sample(alph, 3)
                if count2 == 1:
                    count = randint(1, 2)
                    if count == 1:
                        x = randint(25, 150)
                        y = randint(10, x - 5)
                        txt.append('Дан отрезок ' + str(a) + str(b) + ' длиной ' + str(x) +
                                   ' см, на нём отметили точку ' + str(k) + ' так, что отрезок ' + str(a) + str(k) +
                                   ' равен ' + str(y) + ' см, '
                                   'чему равен отрезок ' + str(b) + str(k) + '?')
                        otv.append(str(x - y))
                    elif count == 2:
                        x = randint(25, 150)
                        y = randint(10, x - 5)
                        txt.append('Дан отрезок ' + str(a) + str(b) + ' длиной ' + str(x) +
                                   ' см, на нём отметили точку ' + str(k) + ' так, что отрезок ' + str(b) + str(k) +
                                   ' равен ' + str(y) + ' см, '
                                   'чему равен отрезок ' + str(a) + str(k) + '?')
                        otv.append(str(x - y))
                elif count2 == 2:
                    count = randint(1, 2)
                    if count == 1:
                        x = randint(10, 54)
                        y = randint(15, 78)
                        txt.append('Дан отрезок ' + str(a) + str(b) + '. На нём лежит точка ' + str(k) +
                                   ' и ' + str(a) + str(k) +' равен ' + str(x) + ' см,'
                                   ' а ' + str(b) + str(k) + ' равен ' + str(y) + ' см, найдите длину отрезка ' +
                                   str(a) + str(b) + '.')
                        otv.append(str(x + y))
                    else:
                        x = randint(10, 54)
                        y = randint(15, 78)
                        txt.append('Дан отрезок ' + str(a) + str(b) + '. На нём лежит точка ' + str(k) +
                                   ' и ' + str(b) + str(k) +' равен ' + str(x) + ' см,'
                                   ' а ' + str(a) + str(k) + ' равен ' + str(y) + ' см, найдите длину отрезка ' +
                                   str(a) + str(b) + '.')
                        otv.append(str(x + y))


                count = randint(1, 2)
                if count == 1:
                    a, b, c, d = sample(alph, 4)
                    x, y = randint(50, 89), randint(16, 49)
                    txt.append('Внутри угла ' + str(a) + str(b) + str(c) + ' проведен луч ' + str(b) + str(d) +
                               '. Найти угол ' + str(a) + str(b) + str(c) + ', если угол ' + str(a) +
                               str(b) + str(d) + ' равен ' + str(x) + ' градусов, '
                               'а угол ' + str(c) + str(b) + str(d) + ' на ' + str(y) + ' градусов больше.')
                    otv.append(str(2 * x + y))
                elif count == 2:
                    a, b, c, d = sample(alph, 4)
                    x, y = randint(99, 169), randint(16, 48)
                    txt.append('Внутри угла ' + str(a) + str(b) + str(c) + ' проведен луч ' + str(b) + str(d) +
                               '. Найти угол ' + str(a) + str(b) + str(d) + ', если угол ' + str(a) +
                               str(b) + str(c) + ' равен ' + str(x) + ' градусов, '
                               'а угол ' + str(c) + str(b) + str(d) + ' на ' + str(y) + ' градусов меньше.')
                    otv.append(str(y))


                count = randint(1, 2)
                if count == 1:
                    a = randint(4, 10)
                    dels = [i for i in range(2, a ** 2 - 1) if a % i == 0]
                    k = dels[randint(0, len(dels) - 1)]
                    txt.append('Квадрат со стороной ' + str(a) + ' разделили на 2 прямоугольника так, что площадь одного '
                               'из них в ' + str(k - 1) + ' раз(а) больше другого. Найдите площадь большего прямоугольника.')
                    otv.append(str((a ** 2 // (k + 1)) * k))
                else:
                    a = randint(4, 10)
                    dels = [i for i in range(3, a ** 2 - 1) if a % i == 0]
                    k = dels[randint(0, len(dels) - 1)]
                    txt.append('Квадрат со стороной ' + str(a) + ' разделили на 2 прямоугольника так, что площадь одного '
                               'из них в ' + str(k - 1) + ' раз(а) больше другого. Найдите площадь меньшего прямоугольника.')
                    otv.append(str((a ** 2 // k)))

                # конец генерации стартовой работы за 7 класс


            if tema == '8start':
                alph = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                piffTr = [[3, 4, 5], [5, 12, 13], [8, 15, 17]]
                count = randint(1, 2)
                if count == 1:
                    a = randrange(30, 120, 2)
                    txt.append('Найдите больший смежный угол, если известно, что он на ' + str(a) + ' больше другого.')
                    otv.append(str((180 - a) // 2 + a))
                if count == 2:
                    a = randrange(30, 120, 2)
                    txt.append('Найдите меньший смежный угол, если известно, что он на ' + str(a) + ' меньше другого.')
                    otv.append(str((180 - a) // 2))

                mass = []
                for i in range(1, 30):
                    for j in range(1, 30):
                        if 180 % (i + j) == 0:
                            if i != j:
                                mass.append([i, j])
                count1 = randint(1, 2)
                count = randint(1, len(mass) - 1)
                k, m = mass[count]
                if count1 == 1:
                    txt.append('Смежные углы относятся как ' + str(k) + ':' + str(m) +
                                '. Найдите величину большего из углов.')
                    otv.append(str((180 // (k + m)) * max(k, m)))
                elif count1 == 2:
                    txt.append('Смежные углы относятся как ' + str(k) + ':' + str(m) +
                                '. Найдите величину меньшего из углов.')
                    otv.append(str((180 // (k + m)) * min(k, m)))


                a, b, c = sample(alph, 3)
                p = randrange(100, 500, 2)
                x = randrange(50, 75, 2)
                txt.append('Дан равнобедренный треугольник ' + str(a) + str(b) + str(c) +
                           '. Найдите ' + str(b) + str(c) + ', если его периметр'
                           ' равен ' + str(p) + ', а основание ' + str(a) + str(c) + ' равно ' + str(x) + '.')
                otv.append(str((p - x) // 2))


                a, b, c, d = sample(alph, 4)
                count = randint(1, 4)
                mass = [50, 52, 54, 56, 60, 63, 64, 66, 68, 70, 72, 75, 76, 78, 80, 81, 84, 88, 90, 92, 96, 98, 99,
                        100, 102, 104, 105,
                        108, 110, 112, 114, 116, 117, 120, 124, 126, 128, 130, 132, 135, 136, 138]
                t1 = randint(1, len(mass) - 1)
                t = mass[t1]
                mass2 = []
                for i in range(1, 30):
                    for j in range(1, 30):
                        if t % (i + j) == 0:
                            if i != j:
                                mass2.append([i, j])
                ln = len(mass2)
                count2 = randint(1, ln - 1)
                k, m = mass2[count2]
                if count == 1:
                    txt.append('Дан треугольник ' + str(a) + str(b) + str(c) +
                               '. Его внешний угол ' + str(a) + str(b) + str(d) + ' равен ' + str(t) + '°, а внутренние углы, '
                               'не смежные с ним, относятся как ' + str(k) + ':' + str(m) +
                               '. Найдите величину большего из этих углов.')
                    otv.append(str((t // (k + m)) * max(k, m)))
                elif count == 2:
                    txt.append('Дан треугольник ' + str(a) + str(b) + str(c) +
                               '. Его внешний угол ' + str(a) + str(b) + str(d) + ' равен ' + str(t) + '°, а внутренние углы, '
                               'не смежные с ним, относятся как ' + str(k) + ':' + str(m) +
                               '. Найдите величину меньшего из этих углов.')
                    otv.append(str((t // (k + m)) * min(k, m)))
                if count == 3:
                    txt.append('Дан треугольник ' + str(a) + str(b) + str(c) +
                               '. Его внешний угол ' + str(b) + str(c) + str(d) + ' равен ' + str(t) + '°, а внутренние углы, '
                               'не смежные с ним, относятся как ' + str(k) + ':' + str(m) +
                               '. Найдите величину большего из этих углов.')
                    otv.append(str((t // (k + m)) * max(k, m)))
                if count == 4:
                    txt.append('Дан треугольник ' + str(a) + str(b) + str(c) +
                               '. Его внешний угол ' + str(b) + str(c) + str(d) + ' равен ' + str(t) + '°, а внутренние углы, '
                               'не смежные с ним, относятся как ' + str(k) + ':' + str(m) +
                               '. Найдите величину меньшего из этих углов.')
                    otv.append(str((t // (k + m)) * min(k, m)))
                if count == 5:
                    txt.append('Дан треугольник ' + str(a) + str(b) + str(c) +
                               '. Его внешний угол ' + str(b) + str(a) + str(d) + ' равен ' + str(t) + '°, а внутренние углы, '
                               'не смежные с ним, относятся как ' + str(k) + ':' + str(m) +
                               '. Найдите величину большего из этих углов.')
                    otv.append(str((t // (k + m)) * max(k, m)))
                if count == 6:
                    txt.append('Дан треугольник ' + str(a) + str(b) + str(c) +
                               '. Его внешний угол ' + str(b) + str(a) + str(d) + ' равен ' + str(t) + '°, а внутренние углы, '
                               'не смежные с ним, относятся как ' + str(k) + ':' + str(m) +
                               '. Найдите величину меньшего из этих углов.')
                    otv.append(str((t // (k + m)) * min(k, m)))


                count = randint(1, 4)
                a, b, c, d, m, n = sample(alph, 6)
                if count == 1:
                    x = 4 * randint(30, 35)
                    txt.append('Дан равнобедренный треугольник ' + str(a) + str(b) + str(c) + ' с основанием ' +
                          str(a) + str(c) + '. Биссектрисы углов при основании '
                                            'пересекаются в точке ' + str(d) + '. ∠' + str(b) + ' = ' + str(x) +
                          '°. Найдите величину угла ' + str(a) + str(d) + str(c) + '.')
                    otv.append(str(180 - ((180 - x) // 2)))
                if count == 2:
                    x = 2 * randint(15, 40)
                    txt.append('Дан равнобедренный треугольник ' + str(a) + str(b) + str(c) + ' с основанием ' +
                          str(a) + str(c) + '. Биссектрисы углов при основании '
                                            'пересекаются в точке ' + str(d) + ', а также пересекают стороны ' +
                          str(a) + str(b) + ' и ' + str(b) + str(c) + ' в точках ' + str(m) + ' и ' + str(n) +
                          ' соответственно. ∠' + str(n) + str(d) + str(c) + ' = ' + str(x) +
                          '°. Найдите величину угла ' + str(b) + '.')
                    otv.append(str(180 - 2 * x))
                if count == 3:
                    x = 2 * randint(15, 40)
                    txt.append('Дан равнобедренный треугольник ' + str(a) + str(b) + str(c) + ' с основанием ' +
                          str(a) + str(c) + '. Биссектрисы углов при основании '
                                            'пересекаются в точке ' + str(d) + ', а также пересекают стороны ' +
                          str(a) + str(b) + ' и ' + str(b) + str(c) + ' в точках ' + str(m) + ' и ' + str(n) +
                          ' соответственно. ∠' + str(m) + str(d) + str(a) + ' = ' + str(x) +
                          '°. Найдите величину угла ' + str(b) + '.')
                    otv.append(str(180 - 2 * x))
                if count == 4:
                    x = 2 * randint(50, 80)
                    txt.append('Дан равнобедренный треугольник ' + str(a) + str(b) + str(c) + ' с основанием ' +
                          str(a) + str(c) + '. Биссектрисы углов при основании '
                                            'пересекаются в точке ' + str(d) + ', а также пересекают стороны ' +
                          str(a) + str(b) + ' и ' + str(b) + str(c) + ' в точках ' + str(m) + ' и ' + str(n) +
                          ' соответственно. ∠' + str(m) + str(d) + str(n) + ' = ' + str(x) +
                          '°. Найдите величину угла ' + str(b) + '.')
                    otv.append(str(180 - (180 - x) * 2))


                count = randint(1, 4)
                a, b, c, d = sample(alph, 4)
                x = randint(80, 130)
                x += 1
                if count == 1:
                    txt.append('Дан треугольник ' + str(a) + str(b) + str(c) + ' с прямым углом ' + str(b) +
                          '. Биссектриса этого угла образует с гипотенузой '
                          '∠' + str(b) + str(d) + str(c) + ' = ' + str(x) + '. '
                                                                            'Найдите больший острый угол треугольника.')
                    otv.append(str(max(135 - x, x - 45)))
                if count == 2:
                    txt.append('Дан треугольник ' + str(a) + str(b) + str(c) + ' с прямым углом ' + str(b) +
                          '. Биссектриса этого угла образует с гипотенузой '
                          '∠' + str(b) + str(d) + str(c) + ' = ' + str(x) + '. '
                                                                            'Найдите меньший острый угол треугольника.')
                    otv.append(str(min(135 - x, x - 45)))
                if count == 3:
                    txt.append('Дан треугольник ' + str(a) + str(b) + str(c) + ' с прямым углом ' + str(b) +
                          '. Биссектриса этого угла образует с гипотенузой '
                          '∠' + str(b) + str(d) + str(a) + ' = ' + str(x) + '. '
                                                                            'Найдите больший острый угол треугольника.')
                    otv.append(str(max(135 - x, x - 45)))
                if count == 4:
                    txt.append('Дан треугольник ' + str(a) + str(b) + str(c) + ' с прямым углом ' + str(b) +
                          '. Биссектриса этого угла образует с гипотенузой '
                          '∠' + str(b) + str(d) + str(a) + ' = ' + str(x) + '. '
                                                                            'Найдите меньший острый угол треугольника.')
                    otv.append(str(min(135 - x, x - 45)))


                count = randint(1, 3)
                a, b, c = sample(alph, 3)
                mass = [50, 52, 54, 56, 60, 63, 64, 66, 68, 70, 72, 75, 76, 78, 80, 81, 84, 88, 90, 92, 96, 98, 99,
                        100, 102, 104, 105,
                        108, 110, 112, 114, 116, 117, 120, 124, 126, 128, 130, 132, 135, 136, 138]
                t1 = randint(1, len(mass) - 1)
                t = mass[t1]
                mass2 = []
                for i in range(2, t - 1):
                    if t % i == 0:
                        mass2.append(i)
                count2 = randint(0, len(mass2) - 1)
                if count == 1:
                    x = mass2[count2]
                    y = randint(2, t // x)
                    txt.append('Дан треугольник ' + str(a) + str(b) + str(c) + '. Сторона ' + str(b) + str(c) +
                               ' равна ' + str(t) + ', а сторона ' + str(a) + str(b) + ' меньше неё в ' +
                               str(x) + ' раз(a), сторона ' + str(a) + str(c) + ' на ' + str(y) +
                               ' меньше ' + str(b) + str(c) + '. Найти периметр треугольника.')
                    otv.append(str(t + (t // x) + t - y))
                if count == 2:
                    x = randint(2, 3)
                    y = randint((t * x - t), t * x - t + 50)
                    txt.append('Дан треугольник ' + str(a) + str(b) + str(c) + '. Сторона ' + str(b) + str(c) +
                               ' равна ' + str(t) + ', а сторона ' + str(a) + str(b) + ' больше неё в ' +
                               str(x) + ' раз(a), сторона ' + str(a) + str(c) + ' на ' + str(y) +
                               ' больше ' + str(b) + str(c) + '. Найти периметр треугольника.')
                    otv.append(str(t + (t * x) + t + y))
                if count == 3:
                    x = mass2[count2]
                    y = randint(1, t // x)
                    txt.append('Дан треугольник ' + str(a) + str(b) + str(c) + '. Сторона ' + str(b) + str(c) +
                               ' равна ' + str(t) + ', а сторона ' + str(a) + str(b) + ' меньше неё в ' +
                               str(x) + ' раз(a), сторона ' + str(a) + str(c) + ' на ' + str(y) +
                               ' больше ' + str(b) + str(c) + '. Найти периметр треугольника.')
                    otv.append(str(t + (t // x) + t + y))


                # конец генерации стартовой для 8


                # начало генерации стартовой для 9 класса
            if tema == '9start':
                count = randint(1, 2)
                a, b, c = sample(alph, 3)
                x = randrange(40, 120, 2)
                if count == 1:
                    txt.append('В равнобедренном треугольнике ' + str(a) + str(b) + str(c) +
                               ' с основанием ' + str(a) + str(c) + ' угол ' + str(b) + ' равен ' + str(x) +' градусов. '
                               'Найдите величину угла ' + str(a) + '.')
                    otv.append(str((180 - x) // 2))
                if count == 2:
                    txt.append('В равнобедренном треугольнике ' + str(a) + str(b) + str(c) +
                               ' с основанием ' + str(a) + str(c) + ' угол ' + str(b) + ' равен ' + str(x) +' градусов. '
                               'Найдите величину угла ' + str(c) + '.')
                    otv.append(str((180 - x) // 2))


                count = randint(1, 8)
                count2 = 2
                count3 = randint(1, 2)
                x, y = piffTr[count][0] * count2, piffTr[count][1] * count2
                a, b, c, d = sample(alph, 4)
                if count3 == 1:
                    txt.append('В ромбе ' + str(a) + str(b) + str(c) + str(d) + ' диагональ ' + str(a) + str(c) +
                               ' равна ' + str(y) + ', a диагональ ' + str(b) + str(d) + ' равна ' + str(x) +
                               '. Найдите сторону ромба.')
                    otv.append(str(piffTr[count][2]))
                elif count3 == 2:
                    txt.append('В ромбе ' + str(a) + str(b) + str(c) + str(d) + ' диагональ ' + str(a) + str(c) +
                               ' равна ' + str(y) + ', a диагональ ' + str(b) + str(d) + ' равна ' + str(x) +
                               '. Найдите площадь ромба.')
                    otv.append(str((x * y) // 2))


                count = randint(1, 4)
                a, b, c, d, k = sample(alph, 5)
                x, y  = randint(10, 50), randint(25, 60)
                if count == 1:
                    txt.append('В параллелограмме ' + str(a) + str(b) + str(c) + str(d) + ' провели биссектрису '
                               'угла ' + str(a) + ' так, что ' + str(c) + str(k) + ' = ' + str(x) +
                               ' и ' + str(k) + str(b) + ' = ' + str(y) +
                               ', найдите периметр ' + str(a) + str(b) + str(c) + str(d) + '.')
                    otv.append(str((y * 2 + x) * 2))
                if count == 2:
                    txt.append('В параллелограмме ' + str(a) + str(b) + str(c) + str(d) + ' провели биссектрису '
                               'угла ' + str(b) + ' так, что ' + str(d) + str(k) + ' = ' + str(x) +
                               ' и ' + str(k) + str(a) + ' = ' + str(y) +
                               ', найдите периметр ' + str(a) + str(b) + str(c) + str(d) + '.')
                    otv.append(str((y * 2 + x) * 2))
                if count == 3:
                    txt.append('В параллелограмме ' + str(a) + str(b) + str(c) + str(d) + ' провели биссектрису '
                               'угла ' + str(c) + ' так, что ' + str(a) + str(k) + ' = ' + str(x) +
                               ' и ' + str(k) + str(d) + ' = ' + str(y) +
                               ', найдите периметр ' + str(a) + str(b) + str(c) + str(d) + '.')
                    otv.append(str((y * 2 + x) * 2))
                if count == 4:
                    txt.append('В параллелограмме ' + str(a) + str(b) + str(c) + str(d) + ' провели биссектрису '
                               'угла ' + str(d) + ' так, что ' + str(b) + str(k) + ' = ' + str(x) +
                               ' и ' + str(k) + str(c) + ' = ' + str(y) +
                               ', найдите периметр ' + str(a) + str(b) + str(c) + str(d) + '.')
                    otv.append(str((y * 2 + x) * 2))


                count = randint(1, 4)
                a, b, c, d = sample(alph, 4)
                x, y = randrange(40, 80, 2), randrange(82, 120, 2)
                if count == 1:
                    txt.append('Дана равнобедренная трапеция ' + str(a) + str(b) + str(c) + str(d) +
                               '. Меньшее основание ' + str(b) + str(c) + ' равно ' + str(x) + ', а основание '
                               + str(a) + str(d) + ' равно ' + str(y) + ', '
                               'угол ' + str(b) + ' равен 120. Найдите ' + str(a) + str(b) + '.')
                    otv.append(str((y - x) // 2 * 2))
                elif count == 2:
                    txt.append('Дана равнобедренная трапеция ' + str(a) + str(b) + str(c) + str(d) +
                               '. Меньшее основание ' + str(b) + str(c) + ' равно ' + str(x) + ', а основание '
                               + str(a) + str(d) + ' равно ' + str(y) + ', '
                               'угол ' + str(c) + ' равен 120. Найдите ' + str(a) + str(b) + '.')
                    otv.append(str((y - x) // 2 * 2))
                elif count == 3:
                    txt.append('Дана равнобедренная трапеция ' + str(a) + str(b) + str(c) + str(d) +
                               '. Меньшее основание ' + str(b) + str(c) + ' равно ' + str(x) + ', а основание '
                               + str(a) + str(d) + ' равно ' + str(y) + ', '
                               'угол ' + str(b) + ' равен 120. Найдите ' + str(c) + str(d) + '.')
                    otv.append(str((y - x) // 2 * 2))
                elif count == 4:
                    txt.append('Дана равнобедренная трапеция ' + str(a) + str(b) + str(c) + str(d) +
                               '. Меньшее основание ' + str(b) + str(c) + ' равно ' + str(x) + ', а основание '
                               + str(a) + str(d) + ' равно ' + str(y) + ', '
                               'угол ' + str(c) + ' равен 120. Найдите ' + str(c) + str(d) + '.')
                    otv.append(str((y - x) // 2 * 2))


                count = randint(1, 8)
                count2 = randint(2, 3)
                x, y = piffTr[count][2] * count2, piffTr[count][0] * count2
                txt.append('На высоте треугольника лежит центр описанной окружности, который делит её на отрезки, '
                           'равные ' + str(x) + ' и ' + str(y) + '. Найдите площадь этого треугольника.')
                otv.append(str((piffTr[count][1] * count2 * (x + y))))


                a, b, c, d = sample(alph, 4)
                x, k = randrange(100, 300, 4), randrange(150, 500, 4)
                y = randint((x + k) // 4, (x + k) // 2)
                txt.append('Четырёхугольник ' + str(a) + str(b) + str(c) + str(d) + ' описали вокруг окружности. ' +
                           str(a) + str(b) + ' = ' + str(x) + ', ' + str(a) + str(d) + ' = ' + str(y) +
                           ', ' + str(c) + str(d) + ' = ' + str(k) + '. Найдите ' + str(b) + str(c) + '.')
                otv.append(str(x + k - y))


                a, b, c, d, k = sample(alph, 5)
                number = '23456789'
                count = randint(1, 4)
                if count == 1:
                    x, y = sample(number, 2)
                    x, y = int(x), int(y)
                    w = y * x * randint(2, 10)
                    txt.append('Хорда ' + str(a) + str(b) + ' и хорда ' + str(c) + str(d) + ' пересекаются в точке ' +
                                str(k) + '. Найдите ' + str(a) + str(k) + ', если ' + str(k) + str(b) + ' = ' +
                                str(x) + ', ' + str(d) + str(k) + ' = ' + str(y) +
                               ', ' + str(c) + str(k) + ' = ' + str(w) + '.')
                    otv.append(str((w * y) // x))
                elif count == 2:
                    x, y = sample(number, 2)
                    x, y = int(x), int(y)
                    w = y * x * randint(2, 10)
                    txt.append('Хорда ' + str(a) + str(b) + ' и хорда ' + str(c) + str(d) + ' пересекаются в точке ' +
                                str(k) + '. Найдите ' + str(b) + str(k) + ', если ' + str(k) + str(a) + ' = ' +
                                str(x) + ', ' + str(d) + str(k) + ' = ' + str(y) +
                               ', ' + str(c) + str(k) + ' = ' + str(w) + '.')
                    otv.append(str((w * y) // x))
                elif count == 3:
                    w, y = sample(number, 2)
                    w, y = int(x), int(y)
                    x = y * w * randint(2, 5)
                    txt.append('Хорда ' + str(a) + str(b) + ' и хорда ' + str(c) + str(d) + ' пересекаются в точке ' +
                                str(k) + '. Найдите ' + str(c) + str(k) + ', если ' + str(k) + str(b) + ' = ' +
                                str(x) + ', ' + str(a) + str(k) + ' = ' + str(y) +
                               ', ' + str(d) + str(k) + ' = ' + str(w) + '.')
                    otv.append(str((x * y) // w))
                elif count == 4:
                    w, y = sample(number, 2)
                    w, y = int(x), int(y)
                    x = y * w * randint(2, 10)
                    txt.append('Хорда ' + str(a) + str(b) + ' и хорда ' + str(c) + str(d) + ' пересекаются в точке ' +
                                str(k) + '. Найдите ' + str(d) + str(k) + ', если ' + str(k) + str(b) + ' = ' +
                                str(x) + ', ' + str(a) + str(k) + ' = ' + str(y) +
                               ', ' + str(c) + str(k) + ' = ' + str(w) + '.')
                    otv.append(str((x * y) // w))

            # конец генерации работы для 9 класса

            # начало генерации стратовой работы для 10 класса
            if tema == '10start':
                a, b, c, d = sample(alph, 4)
                x = randrange(30, 60, 2)
                count = randint(1, 3)
                if count == 1:
                    txt.append('В треугольнике ' + str(a) + str(b) + str(c) + ', прямым углом в котором является угол ' +
                               str(b) + ', вписана окружность '
                               'с центром в точке ' + str(d) + '. Найдите угол ' + str(a) + str(d) + str(b) +
                               ', если угол ' + str(a) + str(c) + str(b) + ' равен ' + str(x) + '.')
                    otv.append(str(45 + (x // 2)))
                if count == 2:
                    txt.append('В треугольнике ' + str(a) + str(b) + str(c) + ', прямым углом в котором является угол ' +
                               str(a) + ', вписана окружность '
                               'с центром в точке ' + str(d) + '. Найдите угол ' + str(b) + str(d) + str(a) +
                               ', если угол ' + str(b) + str(c) + str(a) + ' равен ' + str(x) + '.')
                    otv.append(str(45 + (x // 2)))
                if count == 3:
                    txt.append('В треугольнике ' + str(a) + str(b) + str(c) + ', прямым углом в котором является угол ' +
                               str(c) + ', вписана окружность '
                               'с центром в точке ' + str(d) + '. Найдите угол ' + str(c) + str(d) + str(b) +
                               ', если угол ' + str(c) + str(a) + str(b) + ' равен ' + str(x) + '.')
                    otv.append(str(45 + (x // 2)))


                data = [30, 45, 60, 90, 120, 180]
                count = randint(0, 5)
                y = data[count]
                l = ''.join(sample(alph, 1))
                otvet = randrange(2, 16, 2)
                x = (otvet * (360 // y)) // 2
                txt.append('Пусть ' + str(l) + ' – длина дуги окружности радиусом ' + str(x) +
                           ', градусная мера которой равна ' + str(y) + '. '
                            'В ответе укажите величину ' + str(l) + '/pi')
                otv.append(str(otvet))


                count = randint(1, 4)
                a, d = sample(alph, 2)
                if count == 1:
                    x = randint(14, 37)
                    txt.append('Из точки ' + str(a) + ' проведены две касательные к окружности с центром в точке ' + str(d)
                               + '. Радиус окружности равен ' + str(x) + ' см, угол между касательными равен 60°. '
                               'Найти расстояние ' + str(a) + str(d) + '.')
                    otv.append(str(x * 2))
                if count == 2:
                    x = randrange(10, 40, 2)
                    txt.append('Из точки ' + str(a) + ' проведены две касательные к окружности с центром в точке ' + str(d)
                               + '. Диаметр окружности равен ' + str(x) + ' см, угол между касательными равен 60°. '
                               'Найти расстояние ' + str(a) + str(d) + '.')
                    otv.append(str(x))
                if count == 3:
                    x = randrange(10, 40, 2)
                    txt.append('Из точки ' + str(a) + ' проведены две касательные к окружности с центром в точке ' + str(d)
                               + '. Расстояние от точки ' + str(a) + ' до точки ' + str(d) + ' равно ' + str(x) +
                               ', угол между касательными равен 60°. Найдите радус окружности.')
                    otv.append(str(x // 2))
                if count == 4:
                    x = randrange(10, 40, 2)
                    txt.append('Из точки ' + str(a) + ' проведены две касательные к окружности с центром в точке ' + str(d)
                               + '. Расстояние от точки ' + str(a) + ' до точки ' + str(d) + ' равно ' + str(x) +
                               ', угол между касательными равен 60°. Найдите диаметр окружности.')
                    otv.append(str(x))


                count = randint(1, 4)
                a, b, c, d = sample(alph, 4)
                if count == 1:
                    x = randint(10, 23)
                    y = randint(25, 40)
                    z = x + randint(22, 31)
                    txt.append('Четырёхугольник ' + str(a) + str(b) + str(c) + str(d) +
                               ' описан около окружности. ' + str(c) + str(d) + '=' + str(x) +
                               ', ' + str(a) + str(d) + '=' + str(y) + ', ' + str(b) + str(c) + '=' + str(z) +
                               '. Найдите ' + str(a) + str(b) + '.')
                    otv.append(str(y + z - x))
                elif count == 2:
                    x = randint(10, 23)
                    y = randint(25, 40)
                    z = x + randint(22, 31)
                    txt.append('Четырёхугольник ' + str(a) + str(b) + str(c) + str(d) +
                               ' описан около окружности. ' + str(a) + str(b) + '=' + str(x) +
                               ', ' + str(a) + str(d) + '=' + str(y) + ', ' + str(b) + str(c) + '=' + str(z) +
                               '. Найдите ' + str(c) + str(d) + '.')
                    otv.append(str(y + z - x))
                elif count == 3:
                    x = randint(10, 23)
                    y = randint(25, 40)
                    z = x + randint(22, 31)
                    txt.append('Четырёхугольник ' + str(a) + str(b) + str(c) + str(d) +
                               ' описан около окружности. ' + str(a) + str(d) + '=' + str(x) +
                               ', ' + str(a) + str(b) + '=' + str(y) + ', ' + str(d) + str(c) + '=' + str(z) +
                               '. Найдите ' + str(b) + str(c) + '.')
                    otv.append(str(y + z - x))
                elif count == 4:
                    x = randint(10, 23)
                    y = randint(25, 40)
                    z = x + randint(22, 31)
                    txt.append('Четырёхугольник ' + str(a) + str(b) + str(c) + str(d) +
                               ' описан около окружности. ' + str(b) + str(c) + '=' + str(x) +
                               ', ' + str(a) + str(b) + '=' + str(y) + ', ' + str(d) + str(c) + '=' + str(z) +
                               '. Найдите ' + str(a) + str(d) + '.')
                    otv.append(str(y + z - x))


                a, b, c, d = sample(alph, 4)
                v_a, v_b, v_c, v_d = (randint(1, 4), randint(1, 3)), (randint(2, 5), randint(1, 2)), \
                                     (randint(1, 2), randint(3, 6)), (randint(1, 7), randint(4, 6))
                x = v_a[0] * v_b[0] * v_c[0] * v_d[0]
                y =  v_a[1] * v_b[1] * v_c[1] * v_d[1]
                otvet = x + y
                txt.append('На плоскости даны точки ' + str(a) + str(v_a) + ', ' + str(b) + str(v_b) + ', ' +
                           str(d) + str(v_d) + ', ' + str(c) + str(v_c) + '. Найдите скалярное произведение векторов.')
                otv.append(str(otvet))


                a, b, c = sample(alph, 3)
                nums = '012345678'
                count = randint(1, 3)
                if count == 1:
                    count1, count2, count3 = sample(nums, 3)
                    count1, count2, count3 = int(count1), int(count2), int(count3)
                    v_a, v_b, v_c = (piffTr[count1][1], piffTr[count1][0]), \
                                    (piffTr[count2][0], piffTr[count2][1]), \
                                    (piffTr[count3][1], piffTr[count3][0])
                    txt.append('Даны векторы ' + str(a) + str(v_a) + ', ' + str(b) + str(v_b) +
                               ' и ' + str(c) + str(v_c) + '. '
                               'Найдите длину вектора ' + str(a) + ' + ' + str(b) + ' + ' + str(c) + '.')
                    otv.append(str(piffTr[count1][2] + piffTr[count2][2] + piffTr[count3][2]))
                elif count == 2:
                    nums1 = '012'
                    nums2 = '345'
                    nums3 = '78'
                    count1 = ''.join(sample(nums1, 1))
                    count2 = ''.join(sample(nums3, 1))
                    count3 = ''.join(sample(nums2, 1))
                    count1, count2, count3 = int(count1), int(count2), int(count3)
                    v_a, v_b, v_c = (piffTr[count1][1], piffTr[count1][0]), \
                                    (piffTr[count2][0], piffTr[count2][1]), \
                                    (piffTr[count3][1], piffTr[count3][0])
                    txt.append('Даны векторы ' + str(a) + str(v_a) + ', ' + str(b) + str(v_b) +
                               ' и ' + str(c) + str(v_c) + '. '
                                                                 'Найдите длину вектора ' + str(a) + ' + ' + str(
                        b) + ' - ' + str(c) + '.')
                    otv.append(str(piffTr[count1][2] + piffTr[count2][2] - piffTr[count3][2]))
                elif count == 3:
                    nums1 = '012'
                    nums2 = '345'
                    nums3 = '678'
                    count1 = ''.join(sample(nums3, 1))
                    count2 = ''.join(sample(nums2, 1))
                    count3 = ''.join(sample(nums1, 1))
                    count1, count2, count3 = int(count1), int(count2), int(count3)
                    v_a, v_b, v_c = (piffTr[count1][1], piffTr[count1][0]), \
                                    (piffTr[count2][0], piffTr[count2][1]), \
                                    (piffTr[count3][1], piffTr[count3][0])
                    txt.append('Даны векторы ' + str(a) + str(v_a) + ', ' + str(b) + str(v_b) +
                               ' и ' + str(c) + str(v_c) + '. '
                                                                 'Найдите длину вектора ' + str(a) + ' - ' + str(
                        b) + ' + ' + str(c) + '.')
                    otv.append(str(piffTr[count1][2] - piffTr[count2][2] + piffTr[count3][2]))


            tx = '${!$%^'.join(txt)
            ot = '${!$%^'.join(otv)
            tems = {'7start': 'Стартовая работа для 7 класса',
                    '8start': 'Стартовая работа для 8 класса',
                    '9start': 'Стартовая работа для 9 класса',
                    '10start': 'Стартовая работа для 10 класса'
                    }


            TasksAkt(teacherId=teacher_id, pole1=tx,
                     pole2=ot, pole3=dates, pole6=work_name,
                     pole4=counter, pole7=request.user.first_name,
                     pole8=work_password, pole12=tems[tema]
                     ).save()
            passwords.append(str(len(passwords) + 1) + '. ' + str(work_password))
        teacher = request.user.first_name.split('{^@$')
        name, surname, patr = teacher[0], teacher[1], teacher[-1]
        mass = TeachersAkt.objects.get(idTeacher=teacher_id)
        email = mass.email
        try:
            send_mail(
                'Оповещение для учителя платформы GeoTutor!',
                'Здравствуйте, ' + name + ' ' + patr + '! Вы успешно создали работу.\n' +
                'Название: ' + str(work_name) + '\n' + 'Тема: ' + str(tems[tema]) + '\n' +
                'Кол-во вариантов: ' + str(
                    counter) + '\n' +
                '\n' + 'Пароли:\n' + '\n'.join(passwords) + '\n' +
                '\n' + '\n' + 'Дата и время начала: ' + str(start_date) + '\n' +
                'Дата и время окончания: ' + str(end_date) + '\n' + 'Время на работу: ' + str(time) + ' минут' + '\n' +
                '\n' + 'Перейти на сайт: geotutor.ru',
                'geometrix2023_2024@mail.ru',
                [email],
                fail_silently=False,
            )
        except Exception as e:
            mess = 'Ошибка при отправке письма...'
            return render(request, 'main/error.html', {'mess': mess})
        username = teacher_id
        chat_id = 914614230
        message_text = 'Пользователь ' + username + ' создал работу!:\nНазвание: ' + work_name + \
                       '\nТема: ' + str(tems[tema]) + '\nФИО: ' + \
                       surname + ' ' + name + '\nEmail: ' + email + '\nКол-во вариантов: ' + counter
        send_telegram_message(chat_id, message_text)
        return render(request, 'main/workCreated.html')
    return render(request, 'main/createWork.html')


def check_prost(num):
    mass = []
    for i in range(1, num + 1):
        if num % i == 0:
            mass.append(i)
    if len(mass) > 2:
        return True
    else:
        return False


def change_password(request):
    username = TeachersAkt.objects.get(idTeacher=request.user.username)
    u = User.objects.get(username=username)
    answer = request.GET
    if 'intlg' in answer:
        last_password = answer['last_password']
        new_password = answer['new_password']
        new_password2 = answer['new_password2']
        if new_password == new_password2 and len(new_password) > 2 \
                and username.pole3 == last_password:
            u.set_password(new_password)
            username.pole3 = new_password
            u.save()
            username.save()
            user_name = request.user.username
            teacher = request.user.first_name.split('{^@$')
            name, surname, patr = teacher[0], teacher[1], teacher[-1]
            email = username.email
            try:
                send_mail(
                    'Оповещение для учителя платформы GeoTutor!',
                    'Здравствуйте, ' + name + ' ' + patr + '! Изменён пароль вашей учётной записи!',
                    'geometrix2023_2024@mail.ru',
                    [email],
                    fail_silently=False,
                )
            except Exception as e:
                mess = 'Ошибка при отправке письма, ваш пароль изменён!'
                return render(request, 'main/error.html', {'mess': mess})
            return redirect('teacherReg')
        else:
            return render(request, 'main/view_message1.html')
    return render(request, 'main/change_password.html')


def StartToCheck(request):
    answer = request.GET
    if 'check' in answer:
        request.session['password2'] = answer['password']
        return redirect('TeacherCheckStat')
    return render(request, 'main/StartToCheck.html')


def startToCheck2(request):
    answer = request.GET
    username = request.user.username
    lst = TasksAkt.objects.filter(teacherId=username)
    data = []
    for i in lst:
        if i.pole6 not in data:
            data.append(i.pole6)
    if 'check' in answer:
        request.session['name_of_work'] = answer['name_of_work']
        return redirect('summary_of_work')
    return render(request, 'main/startToCheck2.html', {'data': data})


def TeacherCheckStat(request):
    answer = request.GET
    password = request.session['password2']
    data = TasksAkt.objects.get(pole8=password)
    zada4i = data.pole1.split('${!$%^')
    true_answers = data.pole2.split('${!$%^')

    if data.pole5 == '0':
        mess = 'Эту работу ещё не начинали выполнять!'
        return render(request, 'main/workStatus.html', {'mess': mess})
    elif data.pole5 == '1':
        mess = 'Работа в процессе выполнения, подождите..!'
        return render(request, 'main/workStatus.html', {'mess': mess})

    student_answers = data.pole10.split('$%&^')
    mass = []
    prav = 0

    for i in range(len(zada4i)):
        if student_answers[i] == '':
            mass.append([i + 1, zada4i[i], true_answers[i], 'Ответа нет!'])
        else:
            if student_answers[i] == true_answers[i]:
                prav += 1
            mass.append([i + 1, zada4i[i], true_answers[i], student_answers[i]])

    work_name = data.pole6
    student = data.studentId.split('{#{%%')[0] + ' ' + data.studentId.split('{#{%%')[1]
    itog = int((prav / len(zada4i)) * 100)

    return render(request, 'main/TeacherCheckStat.html', {'data': mass, 'work_name': work_name, 'itog': itog,
                                                          'student': student})





def send_mail_to_user(request, email):
    subject = 'Оповещение для учителя платформы GeoTutor!'
    message = 'Добро пожаловать! Мы рады приветствовать вас на нашей платформе)'
    sender = 'geometrix2023_2024@mail.ru'
    recipients = [email]  # To whom the email should be sent
    send_mail(subject, message, sender, recipients)
    return render(request, 'teacherReg.html')




# def send_mail_to_user(email):
#     subject = 'This email is from django'
#     message = 'This is test email'
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list = [email]
#
#     send_mail(subject, message, from_email, recipient_list)
#
#     return redirect('/')


def caesar_cipher(text, shift):
    encrypted_text = ""

    for char in text:
        if char.isalpha():
            if char.isupper():
                encrypted_text += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                encrypted_text += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        else:
            encrypted_text += char

    return encrypted_text


def caesar_decipher(text, shift):
    decrypted_text = ""

    for char in text:
        if char.isalpha():
            if char.isupper():
                decrypted_text += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                decrypted_text += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
        else:
            decrypted_text += char

    return decrypted_text


def caesar_cipher_rus(text, shift):
    encrypted_text = ""

    for char in text:
        if char.isalpha():
            if char.isupper():
                encrypted_text += chr((ord(char) - ord('А') + shift) % 33 + ord('А'))
            else:
                encrypted_text += chr((ord(char) - ord('а') + shift) % 33 + ord('а'))
        else:
            encrypted_text += char

    return encrypted_text


def caesar_decipher_rus(text, shift):
    decrypted_text = ""

    for char in text:
        if char.isalpha():
            if char.isupper():
                decrypted_text += chr((ord(char) - ord('А') - shift) % 33 + ord('А'))
            else:
                decrypted_text += chr((ord(char) - ord('а') - shift) % 33 + ord('а'))
        else:
            decrypted_text += char

    return decrypted_text


#  mas1 = [i for i in
#       Polzakt.objects.filter(scores__gt='').order_by('-pole3').values_list('pole3', '')]