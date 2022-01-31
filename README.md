**test_engine():**
  функция устраивает турнир движков стокфиш и майя с разными рейтингами. Возвращает двумерную таблицу, заполненную 0 и 1. 
  00 - стокфиш проиграл майе и за белых, и за черных
  01 - стокфиш проиграл майе за белых, выиграл за черных
  10 - стокфиш проиграл майе за черных, выиграл за белых
  11 - стокфиш выиграл у майи за белых и черных
  0.5 - ничья 

**def print_pgn(moves_list):**
  из списка ходов печатает pgn трансляцию партии
  
**def play_game(engine):**
  вызывается движок и играет сам с собой из указанной позиции
  
**def check_move(right_moves, right_position, engine):**
  есть шахматная задача, для нее пишется список правильных ходов. Данная функция проверяет, делает ли движок правильный ход в каждой позиции. Возвращает массив из TrueFalse для каждого из ходов
  
**def play_dual_game(engine1, engine2, first_starts=True):**
  вызывает два движка играть друг против друга


**def analyse_users_engine(moves, positions):**
  возвращает два массива соответствующие совпадающим ходам майи и стокфиша с разным рейтингом. Первый для ходов белого игрока, второй для черного игрока. В массиве ходов на первых 5 местах информация о партии - id партии, имя игроков и их рейтинг
  
 
 **def make_fen_from_movelist(movelist):**
 генерирует позиции по списку ходов
 
 **def take_moves_from_pgn(pgn):**
 парсит пгн партии в нормальный список ходов, запускает генерацию позиций и анализ партии движками. Возвращает датафрейм
