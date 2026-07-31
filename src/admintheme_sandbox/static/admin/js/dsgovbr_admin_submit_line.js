
window.dsgovbrAdminSubmitLineInit = function() {

    var iconBtn = document.getElementById('saveDropdownIconBtn');
    var menu = iconBtn && iconBtn.nextElementSibling;

    if (iconBtn && menu) {
        iconBtn.addEventListener('click', function(e) {
            e.preventDefault();
            menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
        });
        document.addEventListener('click', function(e) {
            if (!iconBtn.contains(e.target) && !menu.contains(e.target)) {
                menu.style.display = 'none';
            }
        });
    }
}

// Inicializa automaticamente ao carregar o script
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', window.dsgovbrAdminSubmitLineInit);
} else {
    window.dsgovbrAdminSubmitLineInit();
}
