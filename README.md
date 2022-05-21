
# Gomoku 

## TODO
### Юра
1. Настроить класс Gomoku для взаимодействия с gui, чтобы он принимал и оправлял сообщения о ходе игры.
2. Написать максимально абстрактно рабочий алгоритм mix-max, который может работать с любыми эвристиками. 
Для начала можно написать любую, которая ставит фишки просто рядом с существующими, чтобы появилась возможность 
дебажить на gui.
3. Разработка эвристик:
- вычисление рабочего поля, т.е. контур вокруг существующих фишек.
- вычисление ситуаций - https://arxiv.org/pdf/1912.05407.pdf

### Леша
1. ~~Доработать ситуацию с запрещенным ходом - `_BW.B_`, чтобы нельзя было поставить внутрь захвата белую фишку.~~
2. ~~Добавить подсказки ходов для игроков.~~
3. ~~Проработать ситуацию - если после выстраивания пяти в ряд, у соперника возможен захват.~~
4. ~~Проработать ситуацию - образование двойной тройки после захвата.~~
