# Requisitos

- Use o padrão caveman para anotar neste arquivo
- Nunca misture no mesmo arquivo CSS, HTML e JS.
- O projeto deve evitar o uso de CSS direto, priorizar CSS gerado a partir de SCSS
- No SCSS CSS nunca usar a cor, font family name, font size diretamente, usar variável
- Prefira uv ao pip
- É vedado fazer alterações nas subpastas de vendors.
- Ao gerar as mensagens de commit faça em português do Brasil, use formato conventional detalhado commits:
  tipo(escopo): [VERBO] descrição. Inclua impacto das mudanças, arquivos afetados e motivo. Mantenha
  imperativo. Os verbos são ADD=adição, FIX=correção, UPD=atualização, DEL=remoção, UPG=atualização de pacotes.
  Os tipos são: feat: novas funcionalidades, fix: correção de bugs, refactor: refatoração ou performances (sem impacto em
  lógica), style: estilo ou formatação de código (sem impacto em lógica), test: testes, doc: documentação no código
  ou do repositório, env: CI/CD ou settings, build: build ou dependências.
- Separação Estrita de Recursos: Nunca inclua CSS, HTML e JS no mesmo arquivo.
- Compilação via SCSS: Todo o estilo customizado deve ser escrito em SCSS e compilado pelo `django-compressor`.
- Apenas Variáveis: Nunca declare cores, famílias de fontes ou tamanhos de fontes diretamente no corpo das regras CSS/SCSS; use variáveis (ex: `$sandbox-border-color` ou referências do tema).
- Sem Templates Globais na Raiz: Os templates devem ser localizados estritamente dentro das pastas `<app>/templates/<app>/` para manter a modularidade e evitar conflitos globais fora do empacotamento.
