const CACHE_NAME = 'eigo-apps-v1';

const ASSETS = [
  './index.html',
  './AVCtyping.html',
  './Ultimate_255.html',
  './balloon_hangman.html',
  './dictationNT1&2.html',
  './dragon-english.html',
  './parts_quiz.html',
  './worddefender.html',
  './中学連語一問一答.html',
  './発音記号一問一答.html',
  './瞬間英作文basic.html',
  './瞬間英作文（仮定法).html',
  './瞬間英作文（受動態）.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
  'https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@400;700;900&family=Lora:ital,wght@0,600;1,400&display=swap'
];

// インストール時：全アセットをキャッシュ
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      // 個別に追加して1つ失敗しても止まらないように
      return Promise.allSettled(ASSETS.map(url => cache.add(url)));
    })
  );
  self.skipWaiting();
});

// 古いキャッシュを削除
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      )
    )
  );
  self.clients.claim();
});

// フェッチ：キャッシュ優先、なければネット取得してキャッシュに追加
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;
      return fetch(event.request).then(response => {
        if (response && response.status === 200 && response.type !== 'opaque') {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        }
        return response;
      }).catch(() => cached);
    })
  );
});
