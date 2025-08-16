import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np  # <--- 1. ЯВНО ИМПОРТИРУЕМ NUMPY

# 1. Создаем "игрушечные" данные, похожие на наши
# (DataFrame - это специальная таблица из библиотеки pandas)
data = {
    'rating': ['G']*50 + ['PG']*50 + ['R']*50 + ['NC-17']*50,
    'length': [
        # Фильмы 'G' - стабильные, короткие
        # --- 2. ИСПОЛЬЗУЕМ np НАПРЯМУЮ ---
        *np.random.normal(80, 10, 50),
        # Фильмы 'PG' - чуть длиннее
        *np.random.normal(110, 15, 50),
        # Фильмы 'R' - большой разброс
        *np.random.normal(120, 25, 50),
        # Фильмы 'NC-17' - с выбросами
        *np.random.normal(115, 20, 48), 180, 185
    ]
}
df = pd.DataFrame(data)

# 2. Создаем "полотно" для рисования
plt.figure(figsize=(10, 6))

# 3. Строим Box Plot с помощью Seaborn (это делается одной строкой!)
sns.boxplot(x='rating', y='length', data=df)

# 4. Настраиваем внешний вид
plt.title('Пример Box Plot: Распределение длины фильмов по рейтингам', fontsize=16)
plt.xlabel('Рейтинг', fontsize=12)
plt.ylabel('Продолжительность (мин)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 5. Сохраняем и показываем
plt.savefig('example_boxplot.png')
plt.show()
