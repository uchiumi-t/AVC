"""
inject_pwa.py
全HTMLファイルにPWA対応タグとSW登録コードを一括挿入するスクリプト。

使い方:
  1. このスクリプトをリポジトリのルートに置く
  2. python3 inject_pwa.py
  3. 各HTMLがその場で上書き更新される（バックアップは .bak で保存）
"""

import os
import re
import shutil

# ── 設定 ──────────────────────────────────────────
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

PWA_HEAD = '''\
  <!-- PWA -->
  <link rel="manifest" href="manifest.json">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="英語アプリ">
  <meta name="theme-color" content="#c0392b">
  <link rel="apple-touch-icon" href="icon-192.png">'''

PWA_SCRIPT = '''\
<script>
  // PWA: Service Worker 登録
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('./sw.js')
        .catch(err => console.warn('SW registration failed:', err));
    });
  }
</script>'''

SAFE_AREA_CSS = '''\
    /* iPhone ノッチ・ホームバー対応 */
    padding-top: env(safe-area-inset-top);
    padding-bottom: env(safe-area-inset-bottom);
    padding-left: env(safe-area-inset-left);
    padding-right: env(safe-area-inset-right);'''

# ── 処理 ──────────────────────────────────────────
def already_has_pwa(content):
    return 'rel="manifest"' in content

def inject_head(content):
    """<head>の直後にPWAタグを挿入"""
    return re.sub(r'(<head[^>]*>)', r'\1\n' + PWA_HEAD, content, count=1)

def inject_sw(content):
    """</body>の直前にSW登録スクリプトを挿入"""
    return re.sub(r'(</body>)', PWA_SCRIPT + r'\n\1', content, count=1, flags=re.IGNORECASE)

def patch_viewport(content):
    """viewport に viewport-fit=cover を追加（なければ）"""
    if 'viewport-fit=cover' in content:
        return content
    return re.sub(
        r'(content="width=device-width[^"]*)"',
        r'\1, viewport-fit=cover"',
        content, count=1
    )

def inject_safe_area(content):
    """html, body { ... } に safe-area-inset を追加（なければ）"""
    if 'safe-area-inset' in content:
        return content
    # min-height: 100vh; の行の後に挿入
    return re.sub(
        r'(min-height:\s*100vh;)',
        r'\1\n    min-height: 100dvh;' + SAFE_AREA_CSS,
        content, count=1
    )

processed = []
skipped = []

for filename in HTML_FILES:
    if not os.path.exists(filename):
        print(f'⚠  スキップ（ファイルなし）: {filename}')
        skipped.append(filename)
        continue

    with open(filename, 'r', encoding='utf-8') as f:
        original = f.read()

    if already_has_pwa(original):
        print(f'✓  既に対応済み: {filename}')
        skipped.append(filename)
        continue

    # バックアップ
    shutil.copy2(filename, filename + '.bak')

    content = original
    content = inject_head(content)
    content = inject_sw(content)
    content = patch_viewport(content)
    content = inject_safe_area(content)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'✅ 更新完了: {filename}')
    processed.append(filename)

print()
print(f'完了: {len(processed)}件更新 / {len(skipped)}件スキップ')
print('バックアップは各HTMLと同じ場所に .bak で保存されています。')
print('問題があれば .bak ファイルを元のファイル名に戻してください。')
