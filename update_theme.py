"""
update_theme.py
全HTMLのtheme-colorを暗い青に更新するスクリプト。
リポジトリのルートで実行してください。
"""

import os
import re

HTML_FILES = [
    'index.html',
    'AVCtyping.html',
    'Ultimate_255.html',
    'balloon_hangman.html',
    'dictationNT1&2.html',
    'dragon-english.html',
    'parts_quiz.html',
    'worddefender.html',
    '中学連語一問一答.html',
    '発音記号一問一答.html',
    '瞬間英作文basic.html',
    '瞬間英作文（仮定法).html',
    '瞬間英作文（受動態）.html',
]

OLD_COLOR = '#c0392b'
NEW_COLOR = '#1a3a5c'

updated = 0
for filename in HTML_FILES:
    if not os.path.exists(filename):
        print(f'⚠  スキップ（ファイルなし）: {filename}')
        continue

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content.replace(OLD_COLOR, NEW_COLOR)

    if new_content != content:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'✅ 更新完了: {filename}')
        updated += 1
    else:
        print(f'－ 変更なし: {filename}')

print(f'\n完了: {updated}件更新')
