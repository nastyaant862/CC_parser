all_marks_without3: int = 4+5+4+4+4+5 + 5+5+5+5+5+4+5 + 5+5+4+4+5 + 5+5+4+5+5 + 35 + 20 + 5+5+4+5+5
cnt_without3 = 6+7+5+5+7+4+5


def if_new_mark(n, m, a1, a2):
    av_without3 = all_marks_without3 / cnt_without3
    print('Текущий средний балл без тройки:', av_without3)
    av_without3 = (all_marks_without3+n+m+a1+a2)/(cnt_without3+4)
    print('Если за пересдачу и курсач', n, 'и', m, ', то средний балл без тройки =', av_without3, '\n')


if_new_mark(4, 5, 5, 5)
print('Всего оценок:', cnt_without3+4)

