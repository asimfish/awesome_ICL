# tools/

Gitignored tool repos used by this survey (clone on demand):

| Tool | Source | Used for |
|---|---|---|
| super_translate | https://github.com/asimfish/super_translate | PDF translation (scripts/translate_queue*.sh) |
| ppt-master | https://github.com/hugohe3/ppt-master | Slide narrative patterns |
| anti-defensive-writing | https://github.com/Kiterlin/anti-defensive-writing | Writing style checks |
| shuorenhua | https://github.com/MrGeDiao/shuorenhua | De-AI phrasing checks |
| PaperOrchestra | https://github.com/Ar9av/PaperOrchestra | Layout reference |
| beamer-skill | https://github.com/Noi1r/beamer-skill | Beamer slide skill (unused in final flow) |

Only `super_translate` is a hard dependency for reproducing translations; its venv is created automatically by `uv run` on first use.
