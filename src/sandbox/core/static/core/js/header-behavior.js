document.addEventListener('DOMContentLoaded', () => {
  const headerComponent = document.querySelector('.br-header');

  if (headerComponent) {
    // Instancia o comportamento do Header (Busca expansível, dropdown de login)
    // Assumindo que a biblioteca core.js do dsgovbr está acessível globalmente como `core`
    if (typeof core !== 'undefined' && core.BRHeader) {
      new core.BRHeader('br-header', headerComponent);
    }

    // Eventos customizados pro Sandbox (Ex: Atalho rápido de QA Orchestrator na busca)
    const searchInput = headerComponent.querySelector('#searchbox');
    if (searchInput) {
      searchInput.addEventListener('focus', () => console.log('Busca do DSGovBR ativada no Sandbox'));
    }
  }
});
