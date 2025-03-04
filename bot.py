def bot_move(values, o, x):
    # 1. Проверяем, может ли бот выиграть этим ходом
    for combo in [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]:
        count_bot = sum(1 for i in combo if values[i] == o)
        count_empty = sum(1 for i in combo if values[i] == ';3')
        if count_bot == 2 and count_empty == 1:
            win_index = next(i for i in combo if values[i] == ';3')
            values[win_index] = o
            return values

    # 2. Проверяем, может ли игрок выиграть этим ходом (блокируем)
    for combo in [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]:
        count_player = sum(1 for i in combo if values[i] == x)
        count_empty = sum(1 for i in combo if values[i] == ';3')
        if count_player == 2 and count_empty == 1:
            block_index = next(i for i in combo if values[i] == ';3')
            values[block_index] = o
            return values

    # 3. Если нет угроз, ходим в первую свободную клетку
    for i in range(9):
        if values[i] == ';3':
            values[i] = o
            return values

    return None  # Если ходить некуда