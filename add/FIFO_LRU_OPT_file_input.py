def is_page_uploaded():
    """ Функция, проверяющая загружена ли текущая страница в ОП.

            Запускаем цикл, проходящий по кадрам в ОП.
            Если текущая страница нашлась в каком-то кадре ОП, возвращаем соответствующее сообщение
            процессу[пользователю], выводим текущее состояние ОП и None.
            Если же страница не была обнаружена, то запускаем Загрузчик страниц.

            """
    i = m - 1
    while i > -1:
        if frames_op_memory[i][0] == page_number:
            output_data.write('Page %s already uploaded!\n' % page_number)
            for i in range(len(frames_op_memory)):
                output_data.write("%s " % frames_op_memory[i][0])
            output_data.write('\n')
            return None
        i -= 1
    return page_uploader()


def page_uploader():
    """Загрузчик страниц

            Проверяем наличие свободных кадров в ОП при помощи функции are_any_free_frames(), если хотя бы один такой
            имеется - загружаем в него текущую страницу, используя "Загрузка в пустой кадр", если таких нет - идём к
            "Выбору алгоритма замещения".

            """
    global all_frame_usage_counter, frame_rewrites_count_opt, frame_rewrites_count_fifo, frame_rewrites_count_lru
    if algorithm == 'FIFO':
        frame_rewrites_count_fifo += 1
    elif algorithm == 'LRU':
        frame_rewrites_count_lru += 1
    else:
        frame_rewrites_count_opt += 1
    all_frame_usage_counter += 1
    free_frame_number = are_any_free_frames()
    if free_frame_number != -1:
        upload_to_free_frame(free_frame_number)
    else:
        replacement_choice()


def are_any_free_frames():
    """Проверка на свободный кадр в ОП

            Бродя по кадрам ОП, ищем кадр с загруженной в него "0" страницей - последовательность запрашиваемых процессом
            страниц от 1 до n , а "0" страница означает незанятость этого кадра. Если таковой найдется - возвращаем его
            номер в ОП, иначе вернём -1.

            """
    for i in range(m):
        if frames_op_memory[i][0] == 0:
            return i
    return -1


def upload_to_free_frame(free_frame_number):
    """Загрузка в пустой кадр

            Загружаем в пустой кадр (изначально свободный/очищенный одним из алгоритмов замещения) текущую страницу, выводим
            соответствующее сообщение процессу[пользователю] и показываем текущее состояние ОП.

            """
    frames_op_memory[free_frame_number][0] = page_number
    if algorithm == 'FIFO':
        frames_op_memory[free_frame_number][1] = all_frame_usage_counter
    output_data.write('Page %s uploaded to ' % page_number)
    output_data.write('%s frame\n' % free_frame_number)
    for i in range(len(frames_op_memory)):
        output_data.write("%s " % frames_op_memory[i][0])
    output_data.write('\n')


def replacement_choice():
    """Выбор алгоритма замещения.

            В зависимости от текущего значения параметра "algorithm", то есть от текущего выбранного алгоритма замещения,
            запускаем один из них - FIFO, LRU или OPT.

            """
    if algorithm == 'FIFO':
        frame_clear((all_frame_usage_counter - 1) % m)
    elif algorithm == 'LRU':
        clearing_of_frame_lru()
    else:
        clearing_of_frame_opt()


def clearing_of_frame_lru():
    """Алгоритм замещения LRU.

            Ищем среди кадров, а вернее, загруженных в них страниц, ту, к которой не обращались последние (длина ОП - 1)
            шага; найдя, запускаем "Очистку кадра".

            """
    for i in range(len(frames_op_memory)):
        if frames_op_memory[i][0] not in recent_page_uses:
            replaceable_page = i
            break
    frame_clear(replaceable_page)


def clearing_of_frame_opt():
    """Алгоритм замещения OPT.

            Действия этого алгоритма основаны на анализе следующих запрашиваемых процессом страниц - среди текущих страниц
            ищется либо та, к которой до конца последовательности запросов не будет обращений, либо та, которая дольше всего
            не будет использоваться среди всех, загруженных на данный момент в ОП. Найдя одну их двух, алгоритм запускает
            очистку кадра с соотвествующей страницей.

            """
    for i in range(len(frames_op_memory)):
        if remain_query_sequence.count(frames_op_memory[i][0]):
            frames_op_memory[i][1] = remain_query_sequence.index(frames_op_memory[i][0]) + 1
    for i in range(len(frames_op_memory)):
        if frames_op_memory[i][1] == 0:
            never_used_page_again = i
            frame_clear(never_used_page_again)
            for i in range(len(frames_op_memory)):
                frames_op_memory[i][1] = 0
            return None
    max_using_range = 0
    for i in frames_op_memory:
        if i[1] > max_using_range:
            max_using_range = i[1]
    for i in range(len(frames_op_memory)):
        if frames_op_memory[i][1] == max_using_range:
            longest_unused_page = i
            frame_clear(longest_unused_page)
            for i in range(len(frames_op_memory)):
                frames_op_memory[i][1] = 0
            return None


def frame_clear(replaceable_page):
    """Очистка кадра.

            Освобождаем кадр, где содержится 'replaceable_page' - заменяемая страница, изменив значение содержащейся в
            нём страницы на 0, - после чего выводим текущее состояние ОП и запускаем находящийся выше алгоритм "Загрузки
            в пустой кадр".

            """
    output_data.write('Free frame needed, clearing of %s frame in progress...\n' % replaceable_page)
    output_data.write('Page %s uploaded back from ' % frames_op_memory[replaceable_page][0])
    output_data.write('%s frame to External Media\n' % replaceable_page)
    frames_op_memory[replaceable_page][0] = 0
    for i in range(len(frames_op_memory)):
        output_data.write("%s " % frames_op_memory[i][0])
    output_data.write('\n')
    upload_to_free_frame(replaceable_page)


with open('Input.txt') as input_data:
    n, m = (int(k) for k in input_data.readline().split())
    query_sequence = []
    for temp_page in input_data:
        query_sequence.append(int(temp_page.strip()))
query_sequence.remove(0)
output_data = open('Logs_and_Output.txt', 'w')
output_data.write(str(n))
output_data.write(' ')
output_data.write(str(m))
output_data.write('\n')
for i in query_sequence:
    output_data.write("%s" % i)
    output_data.write('\n')
frames_op_memory = []
output_data.write('FIFO\n')
for i in range(m):
    frames_op_memory.append([0, 0])
for i in range(len(frames_op_memory)):
    output_data.write("%s " % frames_op_memory[i][0])
output_data.write('\n')
algorithm = 'FIFO'
all_frame_usage_counter = 0
frame_rewrites_count_fifo = 0
for i in query_sequence:
    page_number = i
    is_page_uploaded()
output_data.write("Frame rewrites by using FIFO: %s\n" % frame_rewrites_count_fifo)
output_data.write('LRU\n')
for i in range(len(frames_op_memory)):
    frames_op_memory[i] = [0, 0]
for i in range(len(frames_op_memory)):
    output_data.write("%s " % frames_op_memory[i][0])
output_data.write('\n')
algorithm = 'LRU'
frame_rewrites_count_lru = 0
recent_page_uses = []
for i in query_sequence:
    page_number = i
    if len(recent_page_uses) > m - 1:
        del recent_page_uses[0]
    recent_page_uses.append(page_number)
    is_page_uploaded()
output_data.write("Frame rewrites by using LRU: %s\n" % frame_rewrites_count_lru)
output_data.write('OPTIMAL\n')
for i in range(len(frames_op_memory)):
    frames_op_memory[i] = [0, 0]
for i in range(len(frames_op_memory)):
    output_data.write("%s " % frames_op_memory[i][0])
output_data.write('\n')
algorithm = 'OPT'
frame_rewrites_count_opt = 0
remain_query_sequence = query_sequence.copy()
for i in range(len(query_sequence)):
    page_number = query_sequence[i]
    del remain_query_sequence[0]
    is_page_uploaded()
output_data.write("Frame rewrites by using OPTIMAL: %s" % frame_rewrites_count_opt)
output_data.close()
