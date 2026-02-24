// sidebar.js

document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('main-content');
    const sidebarCollapse = document.getElementById('sidebarCollapse'); // Botão Hamburguer no Navbar Base
    const sidebarCollapseClose = document.getElementById('sidebarCollapseClose'); // Botão fechar (Mobile)
    const sidebarToggleBtn = document.getElementById('sidebarToggleBtn'); // Botão interno da sidebar

    // Check if it's desktop (width > 768px)
    const isDesktop = () => window.innerWidth > 768;

    // Função para tratar o toggle em telas grandes
    function toggleSidebarDesktop() {
        sidebar.classList.toggle('collapsed');
    }

    // Função para tratar o toggle em telas pequenas (Mobile)
    function toggleSidebarMobile() {
        sidebar.classList.toggle('active');
    }

    // Adiciona listener ao botão de abrir/fechar o sidebar (Navbar base)
    if (sidebarCollapse) {
        sidebarCollapse.addEventListener('click', function () {
            if (isDesktop()) {
                toggleSidebarDesktop();
            } else {
                toggleSidebarMobile();
            }
        });
    }

    // Adiciona listener ao botão de toggle interno da sidebar
    if (sidebarToggleBtn) {
        sidebarToggleBtn.addEventListener('click', function () {
            if (isDesktop()) {
                toggleSidebarDesktop();
            }
        });
    }

    // Adiciona listener ao botão específico de fechar no mobile (X na sidebar)
    if (sidebarCollapseClose) {
        sidebarCollapseClose.addEventListener('click', function () {
            sidebar.classList.remove('active');
        });
    }

    // Fecha a sidebar se clicar fora dela no mobile
    document.addEventListener('click', function (event) {
        if (!isDesktop() && sidebar.classList.contains('active')) {
            const isClickInsideSidebar = sidebar.contains(event.target);
            const isClickOnToggle = sidebarCollapse && sidebarCollapse.contains(event.target);
            const isClickOnClose = sidebarCollapseClose && sidebarCollapseClose.contains(event.target);

            if (!isClickInsideSidebar && !isClickOnToggle && !isClickOnClose) {
                sidebar.classList.remove('active');
            }
        }
    });

    // Handle window resize gracefully
    window.addEventListener('resize', function () {
        if (isDesktop()) {
            sidebar.classList.remove('active'); // Remove a classe mobile

            // Para Desktop, comportamento padrão definido pelo HTML (+/- classes CSS)
            // Se redimensionou pra mobile e voltou, não precisa de forçar 'collapsed' porque o padrão agora é aberto.
        } else {
            sidebar.classList.remove('collapsed'); // Remove a classe desktop, senão no mobile fica 80px
        }
    });
});
