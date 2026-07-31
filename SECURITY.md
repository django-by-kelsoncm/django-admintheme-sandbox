# Security Policy

## Versões suportadas

As seguintes versões do `django-dsgovbr` recebem correções de segurança ativas:

| 6.0.x    | Sim       |
| <= 5.2.x | Não       |

> **Recomendação:** utilize sempre a versão mais recente publicada no [PyPI](https://pypi.org/project/django-dsgovbr/).

***

## Escopo de segurança

Este pacote é um **tema para o Django Admin** baseado no
[Design System do Governo Federal (DS Gov.br)](https://www.gov.br/ds/home). Por ser essencialmente um conjunto de
templates HTML, arquivos SASS/CSS e JavaScript, a superfície de ataque é limitada, mas não inexistente.

Vulnerabilidades consideradas **dentro do escopo**:

- Injeção de conteúdo via templates Jinja2/DTL (XSS em templates customizados)
- Dependências com CVEs conhecidos (`django-compressor`, `django-libsass`, `libsass`)
- Arquivos estáticos que introduzam scripts maliciosos ou payloads via CDN
- Problemas de Content Security Policy (CSP) introduzidos pelo tema
- Exposição inadvertida de informações sensíveis do admin Django

Vulnerabilidades **fora do escopo**:

- Vulnerabilidades no próprio Django (reporte ao [Django Security Team](https://www.djangoproject.com/foundation/teams/#security-team))
- Configurações incorretas feitas pela aplicação consumidora do pacote
- Ataques que dependem de acesso físico ou credenciais de superusuário já comprometidas

***

## Como reportar uma vulnerabilidade

**Não abra uma issue pública** para reportar vulnerabilidades de segurança — isso expõe os usuários antes que uma
correção esteja disponível.

### Canal preferencial

Envie um e-mail para **<kelsoncm@gmail.com>** com o assunto: `[SECURITY] django-dsgovbr - <descrição curta>`.

### Informações que devem constar no reporte

Por favor, inclua:

1. **Versão afetada** do pacote (ex: `6.0.0`)
2. **Ambiente** — versão do Python, versão do Django, sistema operacional
3. **Descrição detalhada** da vulnerabilidade
4. **Passos para reproduzir** (PoC mínimo reproduzível)
5. **Impacto estimado** (confidencialidade, integridade, disponibilidade)
6. **Sugestão de correção** (opcional, mas bem-vinda)

### Prazo de resposta

| Etapa                              | Prazo estimado |
|------------------------------------|----------------|
| Confirmação de recebimento         | 3 dias úteis   |
| Avaliação inicial da severidade    | 7 dias úteis   |
| Divulgação coordenada / patch      | 30–90 dias     |

Reportes de boa-fé serão tratados com respeito e confidencialidade. O nome do pesquisador poderá ser incluído nos
agradecimentos do release, caso desejado.

***

## Processo de divulgação

Este projeto adota o modelo de **Divulgação Coordenada de Vulnerabilidades (CVD)**:

1. Recebimento e triagem interna do reporte
2. Confirmação e atribuição de severidade (seguindo [CVSS v3.1](https://www.first.org/cvss/))
3. Desenvolvimento e teste do patch em branch privada
4. Publicação da versão corrigida no PyPI
5. Publicação de **Security Advisory** no GitHub
6. Atualização do `VERSIONS.md` com nota de segurança

***

## Dependências

Este pacote depende de:

| Dependência         | Versão mínima | Canal de reporte de segurança                            |
|---------------------|---------------|----------------------------------------------------------|
| `django`            | ≥ 6.0         | <https://www.djangoproject.com/security/>                |
| `django-compressor` | ≥ 4.4         | <https://github.com/django-compressor/django-compressor> |
| `django-libsass`    | ≥ 0.9         | <https://github.com/torchbox/django-libsass>             |
| `libsass`           | ≥ 0.23.0      | <https://github.com/sass/libsass-python>                 |

Recomenda-se o uso de ferramentas como [`pip-audit`](https://pypi.org/project/pip-audit/) ou
[Dependabot](https://docs.github.com/en/code-security/dependabot) para monitorar CVEs nas dependências.

***

## Boas práticas para quem usa este pacote

- Mantenha o pacote atualizado (`pip install --upgrade django-dsgovbr`)
- Habilite o [Django Security Middleware](https://docs.djangoproject.com/en/stable/ref/middleware/#security-middleware)
  (`SecurityMiddleware`)
- Configure uma **Content Security Policy (CSP)** rigorosa usando [`django-csp`](https://django-csp.readthedocs.io/)
- Restrinja o acesso ao Django Admin a redes internas ou via VPN
- Utilize HTTPS em produção e configure `SECURE_HSTS_SECONDS` adequadamente
- Ative `SECURE_CONTENT_TYPE_NOSNIFF` e `X_FRAME_OPTIONS = 'DENY'` no `settings.py`

***

## Referências

- [Django Security Releases](https://www.djangoproject.com/security/)
- [DS Gov.br — Design System do Governo Federal](https://www.gov.br/ds/home)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CVSSv3.1 Calculator](https://www.first.org/cvss/calculator/3.1)
