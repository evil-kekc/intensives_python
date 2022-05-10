number = 100  # Загаданное число
count_of_attempts = 1  # Количество попыток

while True:  # Цикл событий
    try:
        answer = int(input('Введите число: '))  # Ответ пользователя

        if answer == number:  # Проверка соответствия ответа пользователя с загаданным числом
            print('Вы угадали!')
            print(f'Количество попыток: {count_of_attempts}')

            with open('high_score.txt', 'w+') as high_score:  # Запись лучшего результата в тестовый файл
                if len(high_score.read()) == 0:  # Проверка наличия в файле данных
                    high_score.write(f'{count_of_attempts}')
                    break
                if int(high_score.read()) < count_of_attempts:  # Проверка и запись нового лучшего результата
                    high_score.write(f'{count_of_attempts}')

        elif number < answer:  # Проверка соответствия ответа пользователя с загаданным числом
            print('Введенное число меньше загаданного\n')
            count_of_attempts += 1
        elif number > answer:  # Проверка соответствия ответа пользователя с загаданным числом
            print('Введенное число больше загаданного\n')
            count_of_attempts += 1

    except ValueError:  # Отлавливание ошибки ввода данных и инфомирование пользователя о ней
        print("\n['ERROR'] Данные должны иметь числовой тип данных\n")
