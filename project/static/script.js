// ============================================
// ФИЗИК — Интерактивный решебник
// ============================================

// ---------- Тёмная/светлая тема ----------
(function () {
    const root = document.documentElement;
    const btn  = document.getElementById('theme-toggle');
    const saved = localStorage.getItem('theme');

    if (saved) root.setAttribute('data-theme', saved);

    function updateIcon() {
        btn.textContent = root.getAttribute('data-theme') === 'dark' ? '☀️' : '🌙';
    }
    updateIcon();

    btn.addEventListener('click', () => {
        const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        root.setAttribute('data-theme', next);
        localStorage.setItem('theme', next);
        updateIcon();
    });
})();

// ---------- Фильтры по классам ----------
(function () {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const sections = document.querySelectorAll('.category-section');
    const cards = document.querySelectorAll('.lesson-card');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Обновляем активную кнопку
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filter = btn.dataset.filter;

            if (filter === 'all') {
                // Показываем все карточки и секции
                cards.forEach(card => card.style.display = '');
                sections.forEach(sec => sec.style.display = '');
            } else {
                // Показываем только карточки выбранного класса
                cards.forEach(card => {
                    card.style.display = card.dataset.class === filter ? '' : 'none';
                });
                // Скрываем пустые секции
                sections.forEach(sec => {
                    const visibleCards = sec.querySelectorAll('.lesson-card[style=""], .lesson-card:not([style])');
                    sec.style.display = visibleCards.length > 0 ? '' : 'none';
                });
            }
        });
    });
})();

// ---------- MathJax ----------
document.addEventListener('DOMContentLoaded', () => {
    if (window.MathJax && window.MathJax.typesetPromise) {
        window.MathJax.typesetPromise();
    }
});