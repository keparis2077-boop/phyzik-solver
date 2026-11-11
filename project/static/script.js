// ============================================
// ФИЗИК — Интерактивный решебник
// ============================================

// ---------- Тёмная/светлая тема с плавным переходом ----------
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

// ---------- Горячие клавиши ----------
(function () {
    // Ctrl+Enter для отправки форм
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const form = document.activeElement.closest('form');
            if (form) {
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) submitBtn.click();
            }
        }
    });
    
    // Escape для закрытия модалок (если будут)
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const modal = document.querySelector('.modal-overlay');
            if (modal) modal.style.display = 'none';
        }
    });
})();

// ---------- Подсветка активного поля при фокусе ----------
(function () {
    document.querySelectorAll('.form-group input, .form-group select').forEach(input => {
        input.addEventListener('focus', function() {
            this.closest('.form-group').style.borderColor = 'var(--primary)';
        });
        input.addEventListener('blur', function() {
            this.closest('.form-group').style.borderColor = '';
        });
    });
})();

// ---------- Анимация появления элементов ----------
(function () {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.lesson-card, .task-panel, .reference-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(el);
    });
})();
