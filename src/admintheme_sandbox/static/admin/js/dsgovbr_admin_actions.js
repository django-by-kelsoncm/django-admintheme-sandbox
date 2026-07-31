// dsgovbr_admin_actions.js
window.dsgovbrAdminActionsTogglerInit = function() {
    function getToggler() {
        return document.querySelector('#action-toggle');
    }

    function getSelectedBar() {
        return document.querySelector('.selected-bar');
    }

    function getCheckboxes() {
        return document.querySelectorAll('input.action-select');
    }

    function getCheckboxesChecked() {
        return document.querySelectorAll('input.action-select:checked').length;
    }

    function getActionCounter() {
        var selectedBar = getSelectedBar();
        return selectedBar ? selectedBar.querySelector('span.action-counter-fixed') : null;
    }

    function updateSelectedBarCount() {
        // Atualização do contador de selecionados na selected-bar
        var selectedBar = getSelectedBar();
        var actionCounter = getActionCounter();
        if (selectedBar && actionCounter) {
            var checked = getCheckboxesChecked();
            if (checked > 0) {
                actionCounter.textContent = checked + ' selecionado' + (checked > 1 ? 's' : '');
                selectedBar.style.display = 'flex';
            } else {
                actionCounter.textContent = '';
                selectedBar.style.display = 'none';
            }
        }
    }

    function toggleCheckbox(cb) {
        if (cb.checked !== toggler.checked) {
            cb.checked = toggler.checked;
            var event = new Event('change', { bubbles: true });
            cb.dispatchEvent(event);
        }
    }

    function checkboxChanged() {
        updateSelectedBarCount();
    }

    var toggler = getToggler();
    if (toggler) {
        toggler.addEventListener('change', function(e) {
            getCheckboxes().forEach(toggleCheckbox);
            updateSelectedBarCount();
        });
    }

    // Escuta mudanças apenas nos checkboxes de seleção
    getCheckboxes().forEach(function(cb) {
        cb.addEventListener('change', checkboxChanged);
    });
    // Atualiza ao carregar a página
    updateSelectedBarCount();

};

window.dsgovbrAdminActionsRunnerInit = function() {

    // Actions da selected-bar
    var actionButtons = document.querySelectorAll('.selected-bar .action-select-btn');
    actionButtons.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            var actionValue = btn.getAttribute('data-action-value');
            var form = document.getElementById('changelist-form') || document.querySelector('form[action]');
            if (!form) return;
            var select = form.querySelector('select[name="action"]');
            if (select) {
                select.value = actionValue;
            } else {
                var hidden = form.querySelector('input[type="hidden"][name="action"]');
                if (!hidden) {
                    hidden = document.createElement('input');
                    hidden.type = 'hidden';
                    hidden.name = 'action';
                    form.appendChild(hidden);
                }
                hidden.value = actionValue;
            }
            form.submit();
        });
    });
};

// Inicializa automaticamente ao carregar o script
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', window.dsgovbrAdminActionsTogglerInit);
    document.addEventListener('DOMContentLoaded', window.dsgovbrAdminActionsRunnerInit);
} else {
    window.dsgovbrAdminActionsTogglerInit();
    window.dsgovbrAdminActionsRunnerInit();
}
