# tools — исходники и инструменты

- `validate_pack.py` — проверка пакета перед публикацией: `python3 tools/validate_pack.py packs/pack-003.json`.
- `content/banks.py`, `content/gen.py` — банки предложений и генератор pack-002 (образец для следующих пакетов; пути внутри рассчитаны на /home/claude).
- `app.js`, `app.src.html`, `build/build.py`, `level-v1.json` — исходники приложения. Для публикации нового пакета пересобирать приложение НЕ нужно: достаточно положить JSON в `packs/` и дописать `packs/index.json`.
