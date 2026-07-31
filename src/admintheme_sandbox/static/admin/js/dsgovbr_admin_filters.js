
window.dsgovbrAdminFiltersInit = function() {
    var filterBtn = document.getElementById('button-input-filter');
    var filterBar = document.getElementById('filter-bar');
    var filterDismissBtn = filterBar ? filterBar.querySelector('[data-dismiss="filter"]') : null;
    var tagsContainer = document.getElementById('filter-tags');
    var form = document.getElementById('changelist-form'); // Corrigido para o form correto

    if (tagsContainer) tagsContainer.style.display = 'flex';

    if (filterBtn && filterBar) {
        filterBtn.addEventListener('click', function() {
            filterBar.hidden = false;
            filterBar.classList.add('active');
            var searchBar = document.querySelector('.search-bar');
            if (searchBar) searchBar.hidden = true;
        });
    }
    if (filterDismissBtn && filterBar) {
        filterDismissBtn.addEventListener('click', function() {
            filterBar.hidden = true;
            filterBar.classList.remove('active');
        });
    }

    // Evita múltiplos event listeners
    if (filterBar && !filterBar._dsgovbrFilterListenerAdded) {
        filterBar.addEventListener('click', function(e) {
            var el = e.target;
            while (el && !el.classList.contains('filter_choice')) {
                if (el === filterBar) return;
                el = el.parentElement;
            }
            if (!el || !el.classList.contains('filter_choice')) return;
            e.preventDefault();
            var fieldName = el.getAttribute('data-field-name');
            var fieldTitle = el.getAttribute('data-field-title');
            var value = el.getAttribute('data-value');
            var display = el.getAttribute('data-display');
            if (!fieldName || !value) {
                return;
            }

            // Remove tag/input antigos para o mesmo filtro
            if (tagsContainer) {
                var oldTag = tagsContainer.querySelector('.br-tag[data-field-name="' + fieldName + '"]');
                if (oldTag) oldTag.remove();
            }
            if (form) {
                var oldInput = form.querySelector('input[name="' + fieldName + '"]');
                if (oldInput) oldInput.remove();
            }

            var tag = document.createElement('span');
            tag.className = 'br-tag interaction small';
            tag.setAttribute('data-field-name', fieldName);
            tag.setAttribute('style', "padding-right: 0;");

            var textSpan = document.createElement('span');
            textSpan.className = 'br-tag__text';
            textSpan.textContent = fieldTitle + ': ' + display;
            tag.appendChild(textSpan);

            var closeButton = document.createElement('button');
            closeButton.className = 'br-tag__close br-button inverted';
            closeButton.type = 'button';
            closeButton.setAttribute('aria-label', 'Fechar');

            var closeIcon = document.createElement('i');
            closeIcon.className = 'fas fa-times';
            closeIcon.setAttribute('aria-hidden', 'true');
            closeButton.appendChild(closeIcon);

            tag.appendChild(closeButton);

            if (tagsContainer) tagsContainer.appendChild(tag);

            var input = document.createElement('input');
            input.type = 'hidden';
            input.name = fieldName;
            input.value = value;
            if (form) form.appendChild(input);

            tag.querySelector('.br-tag__close').addEventListener('click', function() {
                tag.remove();
                input.remove();
            });
        });
        filterBar._dsgovbrFilterListenerAdded = true;
    }
}

// Inicializa automaticamente ao carregar o script
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', window.dsgovbrAdminFiltersInit);
} else {
    window.dsgovbrAdminFiltersInit();
}
