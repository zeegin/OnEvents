import os
import yaml
from datetime import datetime
from pathlib import Path
from babel.dates import format_date

# Пути
EVENTS_DIR = Path("events")
TEMPLATE_FILE = Path("web/index.html")
OUTPUT_DIR = Path("site")
OUTPUT_FILE = OUTPUT_DIR / "index.html"

# Загружаем шаблон
template = TEMPLATE_FILE.read_text(encoding="utf-8")

# Список событий
events = []

for file in EVENTS_DIR.glob("*.yml"):
    with open(file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    event_date = datetime.strptime(data["date"], "%Y-%m-%d").date()
    if event_date >= datetime.today().date():
        events.append(data)

# Сортируем по дате
events.sort(key=lambda e: e["date"])

# Функция генерации карточки
def render_event(e):
    date_obj = datetime.strptime(e['date'], "%Y-%m-%d")
    date_str = date_str = format_date(date_obj, format="d MMMM y", locale="ru")  # 15 сентября 2025

    return f"""
    <article class="card" itemscope itemtype="https://schema.org/Event">
      <div class="card-header" style="display:flex; align-items:flex-start; gap:1em;">
        <img class="logo-img" alt="Логотип «{e['title']}»" 
             src="img/{e['icon']}" width="72" height="72" 
             style="border-radius:50%; object-fit:cover;">
        <div class="event-info">
          <h2 class="card-title" itemprop="name" style="margin:0 0 .25em 0;">{e['title']}</h2>
          <div class="meta-item">
            <span class="icon">📅</span>
            <time itemprop="startDate" datetime="{e['date']}">{date_str}</time>
          </div>
          <div class="meta-item">
            <span class="icon">📍</span>
            <span itemprop="location" itemscope itemtype="https://schema.org/Place">
              <span itemprop="addressLocality">{e['city']}, {e['address']}</span>
            </span>
          </div>
        </div>
      </div>
      <p>{e['description']}</p>
      <a href="{e['registration_url']}" role="button">Регистрация</a>
    </article>
    """

# Генерируем HTML
events_html = "\n".join(render_event(e) for e in events)

# Подставляем в шаблон
result_html = template.replace("{{ events }}", events_html)

# Создаем папку site при необходимости
OUTPUT_DIR.mkdir(exist_ok=True)

# Сохраняем результат
OUTPUT_FILE.write_text(result_html, encoding="utf-8")