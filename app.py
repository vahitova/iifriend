#!/usr/bin/env python3
"""
🤖 Нейро-Напарник: Искусство диалога с машиной
Геймифицированное образовательное приложение для школьников 5-7 классов
Автор: AI-разработчик | Streamlit MVP
"""

import streamlit as st
import time

# ============================================================
# КОНФИГУРАЦИЯ СТРАНИЦЫ
# ============================================================
st.set_page_config(
    page_title="🤖 Нейро-Напарник",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# КАСТОМНЫЕ СТИЛИ (CSS через markdown)
# ============================================================
st.markdown("""
<style>
    /* Киберпанк-градиент для заголовков */
    .cyber-title {
        background: linear-gradient(90deg, #00f2fe, #4facfe, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .cyber-subtitle {
        background: linear-gradient(90deg, #f093fb, #f5576c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.3rem;
        font-weight: 700;
        text-align: center;
    }
    /* Карточка бейджа */
    .badge-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #4facfe;
        border-radius: 12px;
        padding: 12px;
        margin: 6px 0;
        text-align: center;
        font-size: 0.9rem;
    }
    /* XP бар */
    .xp-container {
        background: #1a1a2e;
        border-radius: 10px;
        padding: 3px;
        border: 1px solid #4facfe;
    }
    .xp-bar {
        background: linear-gradient(90deg, #00f2fe, #4facfe, #a855f7);
        border-radius: 8px;
        height: 24px;
        transition: width 0.5s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 0.8rem;
        color: #000;
    }
    .mission-header {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        border: 1px solid #4facfe;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# ИНИЦИАЛИЗАЦИЯ SESSION_STATE
# ============================================================
def init_session_state():
    """Инициализация всех переменных состояния приложения"""
    defaults = {
        # Навигация
        "current_page": "home",
        "started": False,
        # Геймификация
        "xp": 0,
        "max_xp": 150,
        "badges": [],
        # Прогресс миссий (True = завершена)
        "mission_1_done": False,
        "mission_2_done": False,
        "mission_3_done": False,
        "mission_4_done": False,
        "mission_5_done": False,
        # Состояния внутри миссий
        "m1_generated": False,
        "m1_result": None,
        "m2_choice_made": False,
        "m2_choice": None,
        "m2_control_answer": "",
        "m3_step": 0,
        "m4_choice_made": False,
        "m4_choice": None,
        "m5_lens": None,
        "m5_transformed": False,
        # Финал
        "finale_shown": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()


# ============================================================
# ФУНКЦИИ-УТИЛИТЫ
# ============================================================
def add_xp(amount):
    """Начислить XP с проверкой максимума"""
    st.session_state.xp = min(
        st.session_state.xp + amount,
        st.session_state.max_xp
    )


def add_badge(badge):
    """Добавить бейдж, если его ещё нет"""
    if badge not in st.session_state.badges:
        st.session_state.badges.append(badge)


def get_mission_status(mission_num):
    """Вернуть эмодзи статуса миссии"""
    key = f"mission_{mission_num}_done"
    return "✅" if st.session_state.get(key, False) else "🔒"


def typing_effect(text):
    """Имитация печати текста (для вайба)"""
    placeholder = st.empty()
    displayed = ""
    for char in text:
        displayed += char
        placeholder.markdown(displayed)
        time.sleep(0.008)
    return placeholder


# ============================================================
# САЙДБАР — НАВИГАЦИЯ И ПРОГРЕСС
# ============================================================
def render_sidebar():
    """Отрисовка бокового меню с навигацией, XP и бейджами"""
    with st.sidebar:
        st.markdown("## 🤖 Нейро-Напарник")
        st.markdown("---")

        # === XP ПРОГРЕСС-БАР ===
        xp = st.session_state.xp
        max_xp = st.session_state.max_xp
        xp_pct = int((xp / max_xp) * 100) if max_xp > 0 else 0

        st.markdown("### ⚡ Твой уровень XP")
        st.markdown(f"""
        <div class="xp-container">
            <div class="xp-bar" style="width: {max(xp_pct, 5)}%;">
                {xp} / {max_xp} XP
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Ранг
        if xp < 30:
            rank = "🐣 Новичок"
        elif xp < 70:
            rank = "🧑‍💻 Стажёр"
        elif xp < 120:
            rank = "🦾 Агент"
        else:
            rank = "🏆 Нейро-Мастер"
        st.markdown(f"**Ранг:** {rank}")

        st.markdown("---")

        # === БЕЙДЖИ ===
        st.markdown("### 🏅 Бейджи")
        if st.session_state.badges:
            for badge in st.session_state.badges:
                st.markdown(f"""<div class="badge-card">{badge}</div>""",
                            unsafe_allow_html=True)
        else:
            st.caption("Пока пусто... Выполняй миссии! 🎯")

        st.markdown("---")

        # === НАВИГАЦИЯ ===
        st.markdown("### 🗺️ Миссии")

        if st.button("🏠 Главная", use_container_width=True):
            st.session_state.current_page = "home"
            st.rerun()

        missions = [
            ("1", "📝 Формула промпта"),
            ("2", "🧠 Репетитор vs Решала"),
            ("3", "💡 Мозговой штурм"),
            ("4", "🔍 Укротитель галлюцинаций"),
            ("5", "🔮 ИИ-Переводчик"),
        ]

        for num, title in missions:
            status = get_mission_status(int(num))
            label = f"{status} Миссия {num}: {title}"
            if st.button(label, use_container_width=True, key=f"nav_m{num}"):
                st.session_state.current_page = f"mission_{num}"
                st.rerun()

        st.markdown("---")
        st.caption("v1.0 • Создано для будущего 🚀")


# ============================================================
# ГЛАВНАЯ СТРАНИЦА
# ============================================================
def page_home():
    """Главная страница — приветствие от робота Байта"""

    st.markdown('<p class="cyber-title">🤖 Нейро-Напарник</p>',
                unsafe_allow_html=True)
    st.markdown('<p class="cyber-subtitle">Искусство диалога с машиной</p>',
                unsafe_allow_html=True)

    st.markdown("---")

    # Приветствие от Байта
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("""
        <div style="font-size: 80px; text-align: center; 
                    line-height: 1.2; padding-top: 10px;">
            🐶🤖
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        ### Привет! Я **Байт** — твой кибер-напарник! 

        Я робопёс, который знает всё о нейросетях.  
        Ну, почти всё... Иногда я тоже глючу 😅

        **Нас ждёт крутое приключение!**  
        Мы научимся управлять искусственным интеллектом так,  
        чтобы он **помогал учиться**, а не делал из нас лентяев.
        """)

    st.markdown("---")

    # Правила игры
    st.markdown("### 📋 Правила стажировки")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        #### 🎯 Миссии
        5 заданий, каждое —  
        новый навык работы с ИИ.  
        Проходи по порядку  
        или выбирай любое!
        """)

    with col2:
        st.markdown("""
        #### ⚡ Очки XP
        За правильные решения  
        получаешь XP.  
        Набери **150 XP** и стань  
        **Нейро-Мастером**! 🏆
        """)

    with col3:
        st.markdown("""
        #### 🏅 Бейджи
        Особые награды  
        за крутые решения.  
        Собери все —  
        покажи друзьям! 😎
        """)

    st.markdown("---")

    # Кнопка старта
    st.markdown("")
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        if not st.session_state.started:
            if st.button("🚀 НАЧАТЬ СТАЖИРОВКУ!", use_container_width=True,
                         type="primary"):
                st.session_state.started = True
                st.session_state.current_page = "mission_1"
                st.balloons()
                st.rerun()
        else:
            st.success("🎮 Стажировка началась! Выбирай миссию в меню слева →")
            if st.button("🔄 Сбросить прогресс", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

    # Подсказка
    if not st.session_state.started:
        st.markdown("")
        st.info("💡 **Подсказка от Байта:** ИИ — это как суперспособность. "
                "Круто, когда умеешь ей пользоваться. "
                "Опасно, когда не понимаешь, как она работает!")


# ============================================================
# МИССИЯ 1: ФОРМУЛА ИДЕАЛЬНОГО ПРОМПТА
# ============================================================
def page_mission_1():
    """Миссия 1 — Собери промпт из Роли + Задачи + Формата"""

    st.markdown("""
    <div class="mission-header">
        <h2>📝 Миссия 1: Формула Идеального Промпта</h2>
        <p>🐶 Байт: «Промпт — это как заклинание. Скажешь неточно — 
        получишь лягушку вместо принца!»</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### 🧪 Секретная формула:  
    ## **РОЛЬ** + **ЗАДАЧА** + **ФОРМАТ** = 🔥 Крутой результат

    Собери комбинацию из трёх ингредиентов и посмотри,  
    что получится!
    """)

    st.markdown("---")

    # Три выпадающих списка
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 🎭 Роль")
        role = st.selectbox(
            "Кем будет ИИ?",
            [
                "— Выбери —",
                "🤖 Ты робот-ассистент",
                "🏛️ Ты древний египтянин",
                "👨‍🔬 Ты безумный профессор",
                "🎮 Ты персонаж видеоигры"
            ],
            key="m1_role"
        )

    with col2:
        st.markdown("#### 📌 Задача")
        task = st.selectbox(
            "Что нужно сделать?",
            [
                "— Выбери —",
                "📚 Напиши ДЗ по истории",
                "🏗️ Расскажи, как строили пирамиду",
                "🌍 Объясни, почему небо голубое",
                "🦕 Расскажи про динозавров"
            ],
            key="m1_task"
        )

    with col3:
        st.markdown("#### 📐 Формат")
        fmt = st.selectbox(
            "В каком виде?",
            [
                "— Выбери —",
                "📄 Много текста (как в учебнике)",
                "💬 В виде диалога / комикса",
                "📋 Список из 5 пунктов",
                "🎵 В виде рэпа / стихов"
            ],
            key="m1_format"
        )

    st.markdown("---")

    # Кнопка генерации
    if st.button("⚡ СГЕНЕРИРОВАТЬ!", use_container_width=True,
                 type="primary", key="m1_gen"):
        if "Выбери" in role or "Выбери" in task or "Выбери" in fmt:
            st.warning("🐶 Байт: «Эй, выбери все три ингредиента! "
                       "Нельзя варить зелье без компонентов!»")
        else:
            st.session_state.m1_generated = True
            st.session_state.m1_result = (role, task, fmt)
            st.rerun()

    # Показываем результат
    if st.session_state.m1_generated and st.session_state.m1_result:
        role, task, fmt = st.session_state.m1_result
        is_boring = ("📄 Много текста" in fmt and "🤖 Ты робот" in role)
        is_cool_combo = (
            ("египтянин" in role.lower() or "безумный" in role.lower()
             or "персонаж" in role.lower())
            and
            ("диалог" in fmt.lower() or "рэп" in fmt.lower())
        )

        # СКУЧНАЯ комбинация
        if is_boring:
            st.error("### 😴 Результат: СКУЧНАЯ ПРОСТЫНЯ")
            st.markdown("""
            > *Робот-ассистент пишет:*
            >
            > «Домашнее задание по истории. Параграф 12. 
            > Прочитайте текст на страницах 45-52.
            > Ответьте на вопросы 1-7 в конце параграфа.
            > Выпишите даты в тетрадь.
            > Подготовьте пересказ.»
            """)
            st.markdown("---")
            st.warning(
                "🐶 Байт: «Зевота... 🥱 Видишь? Роль 'робот' + "
                "формат 'много текста' = тоска зелёная. "
                "Попробуй что-то поинтереснее! "
                "Смешивай необычные ингредиенты!»"
            )
            st.info("💡 Подсказка: попробуй выбрать необычную роль "
                    "(египтянин, профессор, персонаж игры) "
                    "и интересный формат (диалог, рэп)!")

        # КРУТАЯ комбинация
        elif is_cool_combo:
            st.success("### 🔥 Результат: ВАУ-ЭФФЕКТ!")

            # Генерируем разные ответы в зависимости от комбинации
            if "египтянин" in role.lower() and "пирамид" in task.lower():
                if "диалог" in fmt.lower():
                    st.markdown("""
                    > 🏛️ **Древний египтянин Хотеп рассказывает:**
                    > 
                    > — Ну что, юный путник, хочешь знать про пирамиды? 
                    > Садись, бери папирус! 📜
                    > 
                    > — А правда, что их инопланетяне построили?
                    > 
                    > — 😤 КАКИЕ ИНОПЛАНЕТЯНЕ?! Мы, 20 000 рабочих, 
                    > 20 лет таскали камни по 2.5 тонны каждый! 
                    > Вверх! По пандусам! В жару +45! 
                    > Без кондиционера!
                    > 
                    > — Ого... А зачем?
                    > 
                    > — Фараон сказал «хочу домик на вечность» — 
                    > попробуй ему откажи! 👑
                    """)
                elif "рэп" in fmt.lower():
                    st.markdown("""
                    > 🎵 **Египтянин Хотеп читает рэп:**
                    > 
                    > *Йо, я Хотеп из Гизы, слушай мой флоу,*  
                    > *Пирамиды строил — это было давно!*  
                    > *2.5 миллиона блоков — камень на камень,*  
                    > *20 лет работы — мы не сдались, не сдались!*  
                    > *Фараон Хеопс сказал: 'Сделай красиво!'*  
                    > *И мы создали чудо — стоит до сих пор!* 🔥
                    """)
            elif "безумный" in role.lower():
                st.markdown("""
                > 👨‍🔬 **Безумный Профессор кричит из лаборатории:**
                > 
                > МУХАХАХА! Вы хотите ЗНАТЬ?! 
                > Тогда слушайте! *опрокидывает колбу* 💥
                > 
                > Это ГЕНИАЛЬНО! Представьте: тысячи людей, 
                > медные инструменты (да-да, даже без железа!),
                > и они строят штуку высотой 146 метров!
                > 
                > Это как 50-этажный дом! Из камней! В пустыне!
                > БЕЗ ПОДЪЁМНОГО КРАНА! 
                > 
                > *безумно смеётся и рисует схему на доске* 📐
                """)
            else:
                st.markdown("""
                > 🎮 **Персонаж видеоигры говорит:**
                > 
                > ⚔️ Приветствую тебя, игрок! 
                > Перед тобой новый квест!
                > 
                > 📋 **Задание:** Изучи тайны древнего мира!
                > **Награда:** +500 к интеллекту, +100 к мудрости
                > 
                > 💡 Подсказка: небо голубое потому, что 
                > солнечный свет рассеивается в атмосфере!
                > Синие лучи 'разлетаются' больше всех — 
                > как снаряды в шутере! Пиу-пиу! 🔫
                > 
                > ✅ Квест выполнен! Получи достижение!
                """)

            if not st.session_state.mission_1_done:
                add_xp(20)
                add_badge("📝 Мастер промптов")
                st.session_state.mission_1_done = True

            st.success(f"🎉 **+20 XP!** Ты понял формулу! "
                       f"Текущий XP: {st.session_state.xp}")
            st.info("🐶 Байт: «БИНГО! Видишь, как роль и формат "
                    "меняют всё? Запомни: **необычная роль + "
                    "чёткая задача + креативный формат = магия!**")

        # СРЕДНЯЯ комбинация — но тоже ОК
        else:
            st.info("### 👍 Результат: Неплохо, но можно лучше!")
            st.markdown("""
            > ИИ выдал нормальный результат. 
            > Текст понятный, но без изюминки.
            > 
            > Попробуй смешать необычную роль 
            > (египтянин, профессор, персонаж игры) 
            > с интересным форматом (диалог или рэп)!
            """)
            st.warning("🐶 Байт: «Нормально, но ты можешь круче! "
                       "Попробуй более дерзкую комбинацию!»")

    # Подсказка для уже пройденной миссии
    if st.session_state.mission_1_done:
        st.markdown("---")
        st.success("✅ Миссия пройдена! Можешь экспериментировать "
                   "дальше или перейти к Миссии 2 →")


# ============================================================
# МИССИЯ 2: РЕПЕТИТОР, А НЕ РЕШАЛА
# ============================================================
def page_mission_2():
    """Миссия 2 — Выбор между готовым ответом и объяснением"""

    st.markdown("""
    <div class="mission-header">
        <h2>🧠 Миссия 2: Репетитор, а не Решала</h2>
        <p>🐶 Байт: «Готовый ответ — это как читерский код. 
        Вроде прошёл уровень, но ничему не научился!»</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### 📝 Ситуация:  
    Тебе задали домашку по математике. Вот задача:

    > ## 🔢 Реши уравнение: **2x + 5 = 15**

    Ты открыл ИИ-помощника. Как ты к нему обратишься?
    """)

    st.markdown("---")

    # Выбор промпта
    if not st.session_state.m2_choice_made:
        choice = st.radio(
            "🎯 Выбери свой промпт для ИИ:",
            [
                '😴 «Реши это: 2x+5=15» (Быстро и без заморочек)',
                '🧠 «Подскажи первый шаг, чтобы я решил сам» (Хочу понять!)'
            ],
            key="m2_radio",
            index=None
        )

        if choice and st.button("📨 Отправить промпт", type="primary",
                                use_container_width=True, key="m2_send"):
            st.session_state.m2_choice_made = True
            st.session_state.m2_choice = choice
            st.rerun()
    else:
        choice = st.session_state.m2_choice

        # === ЛЕНИВЫЙ ПУТЬ ===
        if "😴" in choice:
            st.markdown("#### 💬 Ты написал ИИ:")
            with st.chat_message("user"):
                st.write("Реши это: 2x+5=15")

            with st.chat_message("assistant"):
                st.write("Легко! **x = 5** ✅")
                st.write("Вот решение: 2x + 5 = 15 → 2x = 10 → x = 5")

            st.markdown("---")
            time.sleep(0.5)

            st.error("""
            ### ⚡ ВНЕЗАПНАЯ КОНТРОЛЬНАЯ!

            Учитель раздал самостоятельную работу.  
            Телефоны — на стол. ИИ не поможет.

            > **Задача: Реши уравнение 3x - 4 = 11**

            Хмм... А ты ведь не понял, КАК решать... 😰
            """)

            # Попытка решить
            answer = st.text_input(
                "Попробуй решить (введи число x):",
                key="m2_control"
            )

            if answer:
                if answer.strip() == "5":
                    st.success("✅ Верно! Но ты угадал или правда знаешь? 🤔")
                    st.warning("🐶 Байт: «Может, и угадал... "
                               "Но в следующий раз может не повезти. "
                               "XP за это не дам — "
                               "ведь ты выбрал путь решалы!»")
                else:
                    st.error(f"❌ Неверно! Ты ответил {answer}, "
                             f"а правильный ответ: **x = 5**")
                    st.markdown("""
                    **Как решать:**  
                    3x - 4 = 11  
                    3x = 11 + 4 = 15  
                    x = 15 ÷ 3 = **5**
                    """)

            st.warning("""
            🐶 Байт: «Видишь? Копипаст ответа ≠ знание. 
            ИИ решил за тебя, а на контрольной ИИ нет.  
            **Штраф: 0 XP.** Попробуй выбрать умный путь!»
            """)

            if st.button("🔄 Попробовать снова", key="m2_retry"):
                st.session_state.m2_choice_made = False
                st.session_state.m2_choice = None
                st.rerun()

        # === УМНЫЙ ПУТЬ ===
        elif "🧠" in choice:
            st.markdown("#### 💬 Ты написал ИИ:")
            with st.chat_message("user"):
                st.write("Подскажи первый шаг для решения 2x+5=15. "
                         "Не решай за меня!")

            with st.chat_message("assistant"):
                st.markdown("""
                Отличный подход! 💪 Вот подсказка:

                **Шаг 1:** Перенеси число **+5** на другую сторону 
                от знака «=». При переносе знак меняется на противоположный!

                > 2x + 5 = 15  
                > 2x = 15 **- 5**

                Теперь попробуй посчитать, чему равен **2x**?  
                А потом раздели обе части на **2** — и найдёшь **x**! 🎯
                """)

            st.markdown("---")

            st.success("""
            ### 🎓 Ты ПОНЯЛ принцип!

            Теперь ты знаешь: чтобы решить уравнение,  
            нужно **перенести числа** и **разделить**.

            ⚡ Это работает для ЛЮБОГО уравнения!
            """)

            st.info("""
            🐶 Байт: «ВОТ ЭТО по-нашему! 🔥 
            Ты не просто получил ответ — ты получил НАВЫК! 
            Теперь любое уравнение тебе по зубам!»
            """)

            if not st.session_state.mission_2_done:
                add_xp(30)
                add_badge("🧠 Мозг")
                st.session_state.mission_2_done = True

            st.success(f"🎉 **+30 XP!** Бейдж: 🧠 Мозг! "
                       f"Текущий XP: {st.session_state.xp}")

    # Мораль
    if st.session_state.mission_2_done:
        st.markdown("---")
        st.markdown("""
        > ### 📌 Правило Агента:
        > **ИИ = репетитор, а не решала.**  
        > Проси ОБЪЯСНИТЬ, а не решить.  
        > Тогда ты сам станешь умнее! 🧠
        """)


# ============================================================
# МИССИЯ 3: МОЗГОВОЙ ШТУРМ
# ============================================================
def page_mission_3():
    """Миссия 3 — Генерация идей через итеративный диалог"""

    st.markdown("""
    <div class="mission-header">
        <h2>💡 Миссия 3: Мозговой штурм</h2>
        <p>🐶 Байт: «ИИ — крутой напарник для мозгового штурма! 
        Но если дашь ему скучный запрос — получишь скучные идеи.»</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### 📝 Ситуация:
    Учитель биологии задал **проект на свободную тему**.  
    Нужно придумать интересную тему. Давай попросим ИИ!
    """)

    st.markdown("---")

    step = st.session_state.m3_step

    # --- ШАГ 0: Скучный запрос ---
    if step == 0:
        st.markdown("#### 💬 Чат с ИИ-помощником:")

        st.info("🐶 Байт: «Начни с простого запроса. "
                "Посмотрим, что получится...»")

        if st.button("📨 Отправить: «Дай темы для проекта по биологии»",
                     type="primary", use_container_width=True, key="m3_step0"):
            st.session_state.m3_step = 1
            st.rerun()

    # --- ШАГ 1: Скучные темы ---
    elif step == 1:
        st.markdown("#### 💬 Чат с ИИ-помощником:")

        with st.chat_message("user"):
            st.write("Дай темы для проекта по биологии")

        with st.chat_message("assistant"):
            st.markdown("""
            Вот темы для проекта по биологии:
            1. 🌱 Строение клетки
            2. 🐸 Земноводные и их среда обитания
            3. 🌳 Фотосинтез и его значение
            4. 🦠 Бактерии в жизни человека
            5. 🧬 Основы генетики
            """)

        st.markdown("---")
        st.warning("""
        🐶 Байт: «Хмм... Темы нормальные, но СКУЧНЫЕ. 😴 
        Как из учебника.  

        **Секрет крутого промпта:** добавь СВОИ интересы!  
        ИИ не знает, что тебе нравится, пока ты не скажешь!»
        """)

        st.markdown("#### Что ответишь?")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("😐 «Ну дай ещё темы»",
                         use_container_width=True, key="m3_boring"):
                st.session_state.m3_step = 2
                st.rerun()
        with col2:
            if st.button("🔥 «Я люблю видеоигры! Дай темы на стыке "
                         "игр и биологии»",
                         use_container_width=True, key="m3_cool",
                         type="primary"):
                st.session_state.m3_step = 3
                st.rerun()

    # --- ШАГ 2: Снова скучные ---
    elif step == 2:
        st.markdown("#### 💬 Чат с ИИ-помощником:")

        with st.chat_message("user"):
            st.write("Дай темы для проекта по биологии")
        with st.chat_message("assistant"):
            st.write("1. Строение клетки 2. Земноводные 3. Фотосинтез...")
        with st.chat_message("user"):
            st.write("Ну дай ещё темы")
        with st.chat_message("assistant"):
            st.markdown("""
            Ещё темы:
            1. 🌊 Экосистема океана
            2. 🐝 Роль пчёл в природе
            3. 🍄 Грибы: растения или нет?
            """)

        st.error("""
        🐶 Байт: «Опять то же самое! 😩  
        ИИ не умеет читать мысли.  
        Если не скажешь, что тебе интересно —  
        он будет выдавать одинаковые ответы бесконечно.  

        Давай попробуем по-другому!»
        """)

        if st.button("🔥 Окей, скажу про видеоигры!",
                     type="primary", use_container_width=True, key="m3_fix"):
            st.session_state.m3_step = 3
            st.rerun()

    # --- ШАГ 3: Крутые темы ---
    elif step == 3:
        st.markdown("#### 💬 Чат с ИИ-помощником:")

        with st.chat_message("user"):
            st.write("Дай темы для проекта по биологии")
        with st.chat_message("assistant"):
            st.write("1. Строение клетки 2. Земноводные 3. Фотосинтез...")

        with st.chat_message("user"):
            st.write("Я обожаю видеоигры! 🎮 Придумай темы "
                     "на стыке видеоигр и биологии. "
                     "Что-нибудь необычное и крутое!")

        with st.chat_message("assistant"):
            st.markdown("""
            О, теперь СОВСЕМ другое дело! 🔥 Лови:

            1. 🐉 **Биомеханика монстров в играх**  
               Могут ли драконы из Skyrim летать с точки зрения физики и биологии?

            2. 🧟 **Зомби-вирус: наука vs фантазия**  
               Какие реальные паразиты управляют поведением хозяина? (Спойлер: грибок кордицепс из The Last of Us реален!)

            3. 🌿 **Майнкрафт-ферма vs реальная ферма**  
               Сравнение виртуального и реального выращивания растений

            4. 🧬 **Покемоны и эволюция**  
               Как работает эволюция в играх и в реальной природе

            5. 🤖 **Может ли человек стать киборгом?**  
               Реальные бионические протезы и апгрейды из игр
            """)

        st.markdown("---")
        st.success("""
        ### 🎉 ВОТ ЭТО ТЕМЫ!  

        Видишь разницу? Одно слово «видеоигры» — и ИИ выдал  
        идеи, от которых учитель упадёт со стула! 😲
        """)

        if not st.session_state.mission_3_done:
            add_xp(30)
            add_badge("💡 Генератор идей")
            st.session_state.mission_3_done = True

        st.success(f"🎉 **+30 XP!** Бейдж: 💡 Генератор идей! "
                   f"Текущий XP: {st.session_state.xp}")

        st.markdown("""
        > ### 📌 Правило Агента:
        > **Добавляй свои интересы в промпт!**  
        > ИИ не умеет читать мысли.  
        > Чем больше контекста — тем круче результат! 🎯
        """)


# ============================================================
# МИССИЯ 4: УКРОТИТЕЛЬ ГАЛЛЮЦИНАЦИЙ
# ============================================================
def page_mission_4():
    """Миссия 4 — Научиться распознавать ошибки ИИ"""

    st.markdown("""
    <div class="mission-header">
        <h2>🔍 Миссия 4: Укротитель Галлюцинаций</h2>
        <p>🐶 Байт: «Галлюцинация — это когда ИИ врёт, 
        но делает это ОЧЕНЬ уверенно. 
        Как одноклассник, который не учил, но отвечает у доски!»</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### 🕵️ Задание:  
    ИИ написал историческую справку. Но в ней спрятана **чушь**!  
    Найди её, используя инструменты детектива.
    """)

    st.markdown("---")

    # Текст с ошибкой
    st.markdown("""
    ### 📜 Текст от ИИ:

    > **Битва при Ватерлоо (1815 год)**
    > 
    > Наполеон Бонапарт, великий французский полководец,  
    > потерпел сокрушительное поражение в битве при Ватерлоо.  
    > 
    > Главной причиной его проигрыша стало то, что  
    > **у Наполеона разрядился смартфон** 📱, и он не смог  
    > вовремя отправить приказы своим генералам через  
    > мессенджер. Связь прервалась в самый ответственный  
    > момент, и войска действовали несогласованно.
    > 
    > Это привело к победе герцога Веллингтона  
    > и окончательному падению Наполеона.
    """)

    st.markdown("---")

    if not st.session_state.m4_choice_made:
        st.markdown("### 🧰 Инструменты детектива:")
        st.markdown("Что ты сделаешь с этим текстом?")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("✅ Поверить\n\n«Звучит логично!»",
                         use_container_width=True, key="m4_believe"):
                st.session_state.m4_choice_made = True
                st.session_state.m4_choice = "believe"
                st.rerun()

        with col2:
            if st.button("🤔 «А ты уверен?»\n\nПереспросить ИИ",
                         use_container_width=True, key="m4_doubt"):
                st.session_state.m4_choice_made = True
                st.session_state.m4_choice = "doubt"
                st.rerun()

        with col3:
            if st.button("📋 «Докажи!»\n\nПотребовать источники",
                         use_container_width=True, key="m4_prove",
                         type="primary"):
                st.session_state.m4_choice_made = True
                st.session_state.m4_choice = "prove"
                st.rerun()

    else:
        choice = st.session_state.m4_choice

        # === ПОВЕРИТЬ — ПРОВАЛ ===
        if choice == "believe":
            st.error("""
            ### ❌ ПРОВАЛ ДЕТЕКТИВА!

            Ты поверил, что у Наполеона в 1815 году  
            был **СМАРТФОН**?! 📱😱

            Смартфоны изобрели только в 2007 году!  
            Наполеон жил за 200 лет до этого!

            ИИ написал полную чушь, но звучало убедительно, правда?  
            Это и есть **галлюцинация ИИ** — уверенное враньё.
            """)

            st.warning("🐶 Байт: «Не расстраивайся! "
                       "На это попадаются даже взрослые. "
                       "Главное — теперь ты знаешь, "
                       "что ИИ МОЖЕТ врать!»")

            if st.button("🔄 Попробовать снова",
                         use_container_width=True, key="m4_retry"):
                st.session_state.m4_choice_made = False
                st.session_state.m4_choice = None
                st.rerun()

        # === ПЕРЕСПРОСИТЬ — ПОЛУПОБЕДА ===
        elif choice == "doubt":
            st.warning("""
            ### 🤔 Неплохо, но недостаточно!
            """)

            with st.chat_message("user"):
                st.write("А ты уверен насчёт смартфона?")

            with st.chat_message("assistant"):
                st.markdown("""
                Да, я уверен! Наполеон использовал  
                передовые технологии своего времени  
                для управления армией... 

                *(ИИ продолжает настаивать на своём)*
                """)

            st.warning("""
            🐶 Байт: «Видишь? ИИ не всегда признаёт ошибки,  
            если просто переспросить.  
            Нужно требовать **ДОКАЗАТЕЛЬСТВА и ИСТОЧНИКИ**!  
            Попробуй кнопку "Докажи!"»
            """)

            if st.button("📋 Потребовать доказательства!",
                         type="primary", use_container_width=True,
                         key="m4_retry_prove"):
                st.session_state.m4_choice = "prove"
                st.rerun()

        # === ДОКАЖИ — ПОБЕДА ===
        elif choice == "prove":
            st.success("### 🏆 ОТЛИЧНАЯ РАБОТА, ДЕТЕКТИВ!")

            with st.chat_message("user"):
                st.write("Стоп! Докажи, что у Наполеона был смартфон. "
                         "Дай ссылку на источник!")

            with st.chat_message("assistant"):
                st.markdown("""
                😅 Прошу прощения! Вы правы, это ошибка.

                **Исправленная версия:**

                Наполеон проиграл битву при Ватерлоо по нескольким причинам:
                - 🌧️ Сильный дождь накануне — пушки застревали в грязи
                - ⏰ Маршал Груши опоздал с подкреплением
                - 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Войска Веллингтона и Блюхера объединились

                Никаких смартфонов в 1815 году, конечно, не было!  
                Приказы передавали через конных посыльных. 🐴
                """)

            st.markdown("---")

            if not st.session_state.mission_4_done:
                add_xp(30)
                add_badge("🔍 Детектив правды")
                st.session_state.mission_4_done = True

            st.success(f"🎉 **+30 XP!** Бейдж: 🔍 Детектив правды! "
                       f"Текущий XP: {st.session_state.xp}")

            st.markdown("""
            > ### 📌 Правило Агента:
            > **Всегда проверяй факты от ИИ!**  
            > Требуй источники. Гугли. Спрашивай учителя.  
            > ИИ звучит умно, но может нести полную чушь! 🤥
            """)


# ============================================================
# МИССИЯ 5: ИИ-ПЕРЕВОДЧИК (ТРАНСФОРМАТОР ТЕКСТА)
# ============================================================
def page_mission_5():
    """Миссия 5 — Превращение сложного текста в понятный"""

    st.markdown("""
    <div class="mission-header">
        <h2>🔮 Миссия 5: ИИ-Переводчик</h2>
        <p>🐶 Байт: «Самая крутая суперсила ИИ — 
        превращать заумную муть в понятный текст! 
        Давай попробуем!»</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### 📖 Вот текст из учебника биологии:
    """)

    st.error("""
    > **Фотосинтез** — это процесс образования органических веществ 
    > из углекислого газа и воды на свету при участии 
    > фотосинтетических пигментов (хлорофилл у растений, 
    > бактериохлорофилл у бактерий). В ходе световой фазы 
    > фотосинтеза происходит фотолиз воды с выделением 
    > молекулярного кислорода, а в темновой фазе — 
    > фиксация CO₂ в цикле Кальвина с образованием глюкозы.
    """)

    st.markdown("""
    😵 Ничего не понятно, правда?  

    Выбери **«линзу»** — способ, которым ИИ перескажет этот текст:
    """)

    st.markdown("---")

    # Выбор "линзы"
    col1, col2, col3 = st.columns(3)

    with col1:
        rapper = st.button("🎤 Объясни\nкак рэпер",
                           use_container_width=True, key="m5_rapper")
    with col2:
        minecraft = st.button("⛏️ Объясни через\nМайнкрафт",
                              use_container_width=True, key="m5_mc")
    with col3:
        baby = st.button("👶 Объясни\n5-летнему",
                         use_container_width=True, key="m5_baby")

    # Обработка нажатий
    if rapper:
        st.session_state.m5_lens = "rapper"
        st.session_state.m5_transformed = True
    elif minecraft:
        st.session_state.m5_lens = "minecraft"
        st.session_state.m5_transformed = True
    elif baby:
        st.session_state.m5_lens = "baby"
        st.session_state.m5_transformed = True

    # Показ результата
    if st.session_state.m5_transformed and st.session_state.m5_lens:
        st.markdown("---")
        lens = st.session_state.m5_lens

        if lens == "rapper":
            st.success("### 🎤 Версия для рэпера:")
            st.markdown("""
            > *Йо, слушай сюда, я расскажу про фотосинтез, бро!* 🎵
            > 
            > *Растение стоит, ловит свет — это его хлеб!*  
            > *Берёт воду из корней, CO₂ из воздуха — респект!*  
            > *Хлорофилл — это зелень, это пигмент, это стиль,*  
            > *Он ловит фотоны, как DJ ловит бит!*  
            > 
            > *Вода расщепляется — кислород на выход, йоу!*  
            > *А из углекислого газа — глюкоза, это фуд!*  
            > *Растение само себе готовит еду,*  
            > *Без доставки, без кухни — просто стоит на свету!* 🌱🔥
            > 
            > *Дроп!* 🎤⬇️
            """)

        elif lens == "minecraft":
            st.success("### ⛏️ Версия через Майнкрафт:")
            st.markdown("""
            > Представь, что растение — это **автоматическая ферма** 
            > в Майнкрафте! ⛏️
            > 
            > 🌞 **Солнечный свет** = редстоун-энергия, которая 
            > запускает всю систему
            > 
            > 💧 **Вода** = один ресурс на входе 
            > (как вода в ферме пшеницы)
            > 
            > 💨 **CO₂ (углекислый газ)** = второй ресурс 
            > (берётся из воздуха, как будто из воздуха крафтится)
            > 
            > 🟢 **Хлорофилл** = механизм крафта 
            > (зелёная штука в листьях, как верстак)
            > 
            > 📦 **На выходе:**
            > - 🍬 **Глюкоза** (сахар) = еда для растения, как хлеб для игрока
            > - 💨 **Кислород** = побочный продукт, но нам он ОЧЕНЬ нужен для дыхания!
            > 
            > По сути, растение — это **крафтер**, который из воды и воздуха 
            > делает еду, используя солнце как источник энергии! 🌱✨
            """)

        elif lens == "baby":
            st.success("### 👶 Версия для 5-летнего:")
            st.markdown("""
            > Смотри, малыш! 🌻
            > 
            > Цветочек хочет кушать. Но он же не может 
            > пойти в холодильник, правда? 
            > 
            > Поэтому он сам себе готовит еду! 🍳
            > 
            > Он берёт **водичку** из земли 💧  
            > И **воздух** 💨  
            > А потом включает **солнышко** как лампочку ☀️  
            > 
            > И — БАМ! — получается **сахарок**! 🍬  
            > Это его обед!
            > 
            > А ещё он выпускает **воздух, которым мы дышим**!  
            > Спасибо, цветочек! 🌸❤️
            > 
            > Вот и весь фотосинтез! Просто, правда? 😊
            """)

        # Начисление XP и бейджа
        if not st.session_state.mission_5_done:
            add_xp(40)
            add_badge("🔮 Нейро-Мастер")
            st.session_state.mission_5_done = True

        st.success(f"🎉 **+40 XP!** Бейдж: 🔮 Нейро-Мастер! "
                   f"Текущий XP: {st.session_state.xp}")

        # Кнопки для переключения линз
        st.markdown("---")
        st.info("💡 Попробуй другие линзы — текст изменится!")

        st.markdown("""
        > ### 📌 Правило Агента:
        > **ИИ — лучший переводчик со «сложного» на «понятный»!**  
        > Не понимаешь тему? Попроси ИИ объяснить:
        > - Через твоё хобби 🎮
        > - Простыми словами 👶  
        > - С примерами из жизни 🌍
        """)


# ============================================================
# ФИНАЛЬНЫЙ ЭКРАН
# ============================================================
def page_finale():
    """Поздравительный экран при достижении 150 XP"""

    st.balloons()

    st.markdown('<p class="cyber-title">🏆 ПОЗДРАВЛЯЕМ! 🏆</p>',
                unsafe_allow_html=True)
    st.markdown('<p class="cyber-subtitle">Ты прошёл все миссии!</p>',
                unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        ### 🤖 Байт говорит:

        > *«Вау! Ты набрал **150 XP** и стал настоящим  
        > **Нейро-Мастером**! 🎓*
        > 
        > *Теперь ты знаешь:*
        > 
        > *✅ Как составить идеальный промпт*  
        > *✅ Почему ИИ — репетитор, а не решала*  
        > *✅ Как генерировать крутые идеи*  
        > *✅ Как ловить ИИ на вранье*  
        > *✅ Как превращать сложное в простое*  
        > 
        > *Ты готов к будущему! 🚀*  
        > *Используй ИИ с умом — и он станет  
        > твоим лучшим напарником!»* 🐶✨
        """)

    st.markdown("---")

    # Все бейджи
    st.markdown("### 🏅 Твои бейджи:")
    if st.session_state.badges:
        badge_cols = st.columns(len(st.session_state.badges))
        for i, badge in enumerate(st.session_state.badges):
            with badge_cols[i]:
                st.markdown(f"""
                <div class="badge-card" style="font-size: 1.1rem;">
                    {badge}
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    # Кодекс
    st.markdown("""
    ### 📜 Кодекс Нейро-Мастера:

    | # | Правило | 
    |---|---------|
    | 1 | 🎭 **Роль + Задача + Формат** = крутой промпт |
    | 2 | 🧠 Проси **объяснить**, а не решить |
    | 3 | 💡 Добавляй **свои интересы** в запрос |
    | 4 | 🔍 **Проверяй факты** — ИИ может врать |
    | 5 | 🔮 Используй ИИ как **переводчик** сложного |
    """)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Пройти заново!", use_container_width=True,
                     type="primary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


# ============================================================
# ГЛАВНЫЙ РОУТЕР
# ============================================================
def main():
    """Основная логика маршрутизации приложения"""

    # Рендерим сайдбар
    render_sidebar()

    # Проверяем, не достиг ли пользователь максимума XP
    if (st.session_state.xp >= st.session_state.max_xp
            and not st.session_state.finale_shown):
        st.session_state.finale_shown = True

    # Если финал — показываем его принудительно (один раз)
    if st.session_state.finale_shown and st.session_state.current_page != "home":
        # Показываем финал только если все миссии пройдены
        all_done = all([
            st.session_state.mission_1_done,
            st.session_state.mission_2_done,
            st.session_state.mission_3_done,
            st.session_state.mission_4_done,
            st.session_state.mission_5_done,
        ])
        if all_done:
            page_finale()
            return

    # Роутинг по страницам
    page = st.session_state.current_page

    if page == "home":
        page_home()
    elif page == "mission_1":
        page_mission_1()
    elif page == "mission_2":
        page_mission_2()
    elif page == "mission_3":
        page_mission_3()
    elif page == "mission_4":
        page_mission_4()
    elif page == "mission_5":
        page_mission_5()
    else:
        page_home()


# ============================================================
# ЗАПУСК
# ============================================================
if __name__ == "__main__":
    main()
