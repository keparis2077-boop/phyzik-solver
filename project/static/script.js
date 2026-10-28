// Переключение тёмной/светлой темы с сохранением в localStorage
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

// Перерисовка формул MathJax после загрузки (на всякий случай)
document.addEventListener('DOMContentLoaded', () => {
    if (window.MathJax && window.MathJax.typesetPromise) {
        window.MathJax.typesetPromise();
    }
});