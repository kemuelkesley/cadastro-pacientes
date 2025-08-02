window.addEventListener('load', () => {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.style.opacity = '0';
        loader.style.transition = 'opacity 0.7s ease';
        setTimeout(() => loader.style.display = 'none', 700);
    }
});