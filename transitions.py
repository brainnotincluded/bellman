from config import Config


class Transitions:
    """
    Это "матрица" допустимых переходов:
        s1 --a--> s2,
        где:
            s1 - исходное состояние
            a  - действие
            s2 - следующее состояние
    Жизнь робота есть цепь состояний и действий:
        S0  --a0-->  S1  --a1-->  S2  --a0-->  S3  --a2-->  S4  -- ... -->  Sn

    В каком то смысле это модель законов физики для робота, в терминах "что можно" и "что невозможно".
    """
    def __init__(self):
        # подготовим для каждой ориентации соответствуее изменение координат i, j в случае движения вперёд.
        self._orientations = [
            (1, 0),   # 'f' - т.е. если ориентация 'вперед', и действие двигаться вперед то i += 1
            (0, 1),   # 'r' - т.е. если ориентация 'вправо', и действие двигаться вперед то j += 1
            (-1, 0),  # 'b' - т.е. если ориентация 'назад', и действие двигаться вперед то  i -= 1
            (0, -1)   # 'l' - т.е. если ориентация 'влево', и действие двигаться вперед то  j -= 1
        ]  # i - соответствует буквенной координате, а j числовой

    def run(self, s, a):
        """
        Эта функция, для заданного состояния и действия, вычисляет следующее состояние.
        :param s:
            исходное состояние есть тупль (i, j, o), где
                i - 0,1,2,3,4,5,6 соответствуют буквенным координатам 'abcdefg'
                j - 0,1,2,3,4 соответствуют численным координатам '12345'
                o - 0,1,2,3 соответствуют ориентациям 'frbl' т.е. 'f'='вперед', 'r'='вправо', 'b'='назад', 'l'='влево'.
        :param a:
            действие может быть 0,1,2 что соответствует 'frl' т.е.
                'f'='вперед', 'r' - 'повернуться по часовой стрелке', 'l' - 'повернуться против часовой стрелке'
        :return:
            новое состояние есть тоже тупль (i, j, o)
        """
        i, j, o = s
        if a == 0:  # действие 'f' - 'движение вперед'
            di, dj = self._orientations[o]
            # меняем координаты
            i, j = i + di, j + dj
        elif a == 1:  # действие 'r' - 'поворот по часовой стрелке' ('поворот вправо')
            # меняем ориентацию
            o = (o + 1) % 4
        elif a == 2:  # действие 'l' - 'поворот против часовой стрелке' ('поворот влево')
            # меняем ориентацию
            o = (o - 1) % 4
        else:
            raise ValueError("Неизвестное действие: " + str(a))

        # если позиция оказалась за пределами поля то возвращаем None -- т.е. невозможное состояние
        if not (0 <= i < len(Config.letters)):  # за пределами по буквенной координате
            return None
        if not (0 <= j < len(Config.numbers)):  # за пределами по численной координате
            return None

        s1 = (i, j, o)
        return s1
