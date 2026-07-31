import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.hashers import make_password
from django.utils import timezone

from accounts.models import CustomUser
from cadastro.models import Orgao, Servidor, Documento, Servico
from editorial.models import Categoria, Tag, Noticia, Comentario
from atendimento.models import Chamado
from eventos.models import Evento, InscricaoEvento
from public_forms.models import SolicitacaoServico
from media_library.models import Midia


class Command(BaseCommand):
    help = "Limpa e semeia o banco de dados do sandbox com perfis e massas de teste."

    def handle(self, *args, **options):
        self.stdout.write("Limpando dados existentes...")
        CustomUser.objects.all().delete()
        Documento.objects.all().delete()
        Servidor.objects.all().delete()
        Servico.objects.all().delete()
        Orgao.objects.all().delete()
        Comentario.objects.all().delete()
        Noticia.objects.all().delete()
        Tag.objects.all().delete()
        Categoria.objects.all().delete()
        Chamado.objects.all().delete()
        InscricaoEvento.objects.all().delete()
        Evento.objects.all().delete()
        SolicitacaoServico.objects.all().delete()
        Midia.objects.all().delete()
        Group.objects.all().delete()

        self.stdout.write("Criando órgãos iniciais para amarração...")
        mec = Orgao.objects.create(
            nome="Ministério da Educação",
            sigla="MEC",
            descricao="Órgão central de educação nacional",
            ativo=True,
        )
        saude = Orgao.objects.create(
            nome="Ministério da Saúde",
            sigla="MS",
            descricao="Gestão de saúde pública",
            ativo=True,
        )
        ifrn = Orgao.objects.create(
            nome="Instituto Federal do Rio Grande do Norte",
            sigla="IFRN",
            descricao="Ensino técnico e superior",
            ativo=True,
        )

        self.stdout.write("Criando grupos de permissão...")
        admin_global = Group.objects.create(name="Admin_Global")
        editorial_manager = Group.objects.create(name="Editorial_Manager")
        editorial_reader = Group.objects.create(name="Editorial_Reader")
        suporte = Group.objects.create(name="Suporte")
        eventos_manager = Group.objects.create(name="Eventos_Manager")
        cadastro_reader = Group.objects.create(name="Cadastro_Reader")

        # Função auxiliar para atribuir permissões a um grupo
        def grant_perms(
            group, app_label, model_name, actions=["add", "change", "delete", "view"]
        ):
            try:
                ct = ContentType.objects.get(app_label=app_label, model=model_name)
                for action in actions:
                    codename = f"{action}_{model_name}"
                    perm = Permission.objects.get(content_type=ct, codename=codename)
                    group.permissions.add(perm)
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(
                        f"Erro ao atribuir permissão {app_label}.{model_name}: {str(e)}"
                    )
                )

        # Configurando permissões por grupo
        for app in [
            "cadastro",
            "editorial",
            "atendimento",
            "eventos",
            "media_library",
            "public_forms",
        ]:
            ct_list = ContentType.objects.filter(app_label=app)
            for ct in ct_list:
                grant_perms(admin_global, app, ct.model)

        # Editorial Manager (full access in editorial)
        grant_perms(editorial_manager, "editorial", "categoria")
        grant_perms(editorial_manager, "editorial", "tag")
        grant_perms(editorial_manager, "editorial", "noticia")
        grant_perms(editorial_manager, "editorial", "comentario")

        # Editorial Reader (readonly)
        grant_perms(editorial_reader, "editorial", "categoria", ["view"])
        grant_perms(editorial_reader, "editorial", "tag", ["view"])
        grant_perms(editorial_reader, "editorial", "noticia", ["view"])
        grant_perms(editorial_reader, "editorial", "comentario", ["view"])

        # Suporte (add/change/view, no delete)
        grant_perms(suporte, "atendimento", "chamado", ["add", "change", "view"])

        # Eventos Manager (change/delete/view, no add)
        grant_perms(eventos_manager, "eventos", "evento", ["change", "delete", "view"])
        grant_perms(
            eventos_manager, "eventos", "inscricaoevento", ["change", "delete", "view"]
        )

        # Cadastro Reader (readonly)
        grant_perms(cadastro_reader, "cadastro", "orgao", ["view"])
        grant_perms(cadastro_reader, "cadastro", "servidor", ["view"])
        grant_perms(cadastro_reader, "cadastro", "documento", ["view"])

        self.stdout.write("Criando usuários de teste...")
        senha_hash = make_password("Senha123!")

        # 1. Superuser
        CustomUser.objects.create(
            username="superuser",
            email="superuser@gov.br",
            password=senha_hash,
            is_superuser=True,
            is_staff=True,
            is_active=True,
            first_name="Super",
            last_name="User",
            cargo="Diretor de TI",
            orgao=ifrn,
        )

        # 2. Staff Admin Total
        u_admin_total = CustomUser.objects.create(
            username="staff_admin_total",
            email="admin_total@gov.br",
            password=senha_hash,
            is_staff=True,
            is_active=True,
            first_name="Administrador",
            last_name="Global",
            cargo="Coordenador Geral",
            orgao=mec,
        )
        u_admin_total.groups.add(admin_global)

        # 3. Staff Editorial Full
        u_ed_full = CustomUser.objects.create(
            username="staff_editorial_full",
            email="ed_full@gov.br",
            password=senha_hash,
            is_staff=True,
            is_active=True,
            first_name="Gestor",
            last_name="Editorial",
            cargo="Editor-Chefe",
            orgao=mec,
        )
        u_ed_full.groups.add(editorial_manager)

        # 4. Staff Editorial Readonly
        u_ed_ro = CustomUser.objects.create(
            username="staff_editorial_readonly",
            email="ed_ro@gov.br",
            password=senha_hash,
            is_staff=True,
            is_active=True,
            first_name="Leitor",
            last_name="Editorial",
            cargo="Revisor",
            orgao=mec,
        )
        u_ed_ro.groups.add(editorial_reader)

        # 5. Staff Atendimento Sem Delete
        u_suporte = CustomUser.objects.create(
            username="staff_atendimento_sem_delete",
            email="suporte@gov.br",
            password=senha_hash,
            is_staff=True,
            is_active=True,
            first_name="Analista",
            last_name="Suporte",
            cargo="Técnico de Suporte",
            orgao=ifrn,
        )
        u_suporte.groups.add(suporte)

        # 6. Staff Eventos Sem Add
        u_eventos = CustomUser.objects.create(
            username="staff_eventos_sem_add",
            email="eventos@gov.br",
            password=senha_hash,
            is_staff=True,
            is_active=True,
            first_name="Coordenador",
            last_name="Eventos",
            cargo="Produtor de Eventos",
            orgao=saude,
        )
        u_eventos.groups.add(eventos_manager)

        # 7. Staff Cadastro View Only
        u_cad_ro = CustomUser.objects.create(
            username="staff_cadastro_view_only",
            email="cadastro_ro@gov.br",
            password=senha_hash,
            is_staff=True,
            is_active=True,
            first_name="Fiscal",
            last_name="Cadastro",
            cargo="Auditor",
            orgao=ifrn,
        )
        u_cad_ro.groups.add(cadastro_reader)

        # 8. User Autenticado Comum
        CustomUser.objects.create(
            username="user_autenticado_comum",
            email="cidadao@gov.br",
            password=senha_hash,
            is_staff=False,
            is_active=True,
            first_name="Cidadão",
            last_name="Comum",
            cargo="Cidadão",
        )

        # 9. User Inativo
        CustomUser.objects.create(
            username="user_inativo",
            email="inativo@gov.br",
            password=senha_hash,
            is_staff=False,
            is_active=False,
            first_name="Usuário",
            last_name="Bloqueado",
        )

        self.stdout.write("Semeando dados para Editorial...")
        cat_noticias = Categoria.objects.create(
            nome="Notícias Gerais", slug="noticias-gerais"
        )
        cat_editais = Categoria.objects.create(
            nome="Editais e Licitações", slug="editais-licitacoes"
        )

        tag_tech = Tag.objects.create(nome="Tecnologia")
        tag_educacao = Tag.objects.create(nome="Educação")
        # tag_saude = Tag.objects.create(nome="Saúde pública")

        n1 = Noticia.objects.create(
            titulo="Lançamento do Novo Portal de Acesso à Educação Técnica",
            slug="lancamento-novo-portal-educacao-tecnica",
            conteudo="O Ministério da Educação lança hoje o novo portal para acesso aos cursos técnicos integrados em todo o território nacional. A plataforma visa facilitar a matrícula e o acompanhamento dos alunos da rede federal.",
            categoria=cat_noticias,
            status="publicado",
            data_publicacao=timezone.now(),
        )
        n1.tags.add(tag_tech, tag_educacao)

        n2 = Noticia.objects.create(
            titulo="Processo Seletivo Simplificado para Professores Substitutos",
            slug="processo-seletivo-professores-substitutos",
            conteudo="Estão abertas as inscrições para o processo seletivo simplificado visando à contratação de docentes substitutos no campus central do IFRN. Veja o edital em anexo para mais informações.",
            categoria=cat_editais,
            status="rascunho",
        )
        n2.tags.add(tag_educacao)

        Comentario.objects.create(
            noticia=n1,
            autor="José da Silva",
            comentario="Parabéns pela iniciativa! Facilita muito nossa vida.",
        )
        Comentario.objects.create(
            noticia=n1,
            autor="Maria Santos",
            comentario="Gostaria de saber se o aplicativo mobile também receberá atualização.",
            aprovado=False,
        )

        self.stdout.write("Semeando dados para Cadastro (Órgãos & Servidores)...")
        # Criando alguns servidores para testar inlines e autocomplete
        s1 = Servidor.objects.create(
            orgao=ifrn,
            nome="Carlos Eduardo Medeiros",
            cpf="111.111.111-11",
            email="carlos.medeiros@ifrn.edu.br",
            cargo="Professor Titular",
            data_admissao=datetime.date(2015, 3, 10),
        )
        s2 = Servidor.objects.create(
            orgao=mec,
            nome="Ana Julia Barbosa",
            cpf="222.222.222-22",
            email="ana.barbosa@mec.gov.br",
            cargo="Analista Técnico Administrativo",
            data_admissao=datetime.date(2018, 6, 15),
        )
        # s3 = Servidor.objects.create(
        #     orgao=saude,
        #     nome="Roberto Carlos Souza",
        #     cpf="333.333.333-33",
        #     email="roberto.souza@saude.gov.br",
        #     cargo="Médico Clínico",
        #     data_admissao=datetime.date(2012, 1, 1),
        # )

        # Adicionando documentos de teste
        Documento.objects.create(servidor=s1, tipo="portaria")
        Documento.objects.create(servidor=s2, tipo="identidade")

        # Criando serviços públicos associados aos órgãos
        servico = Servico.objects.create(
            nome="Emissão de Diploma Digital",
            url_portal="https://www.gov.br/pt-br/servicos/emissao-diploma-digital",
            publico_alvo="Estudantes de graduação",
        )
        servico.orgaos_envolvidos.add(ifrn, mec)

        self.stdout.write("Semeando dados de Eventos...")
        e1 = Evento.objects.create(
            titulo="Seminário Nacional de Inovação Pública 2026",
            descricao="Seminário focado em inovação, ferramentas de IA e modernização do serviço público federal brasileiro.",
            data_inicio=datetime.date(2026, 9, 15),
            data_fim=datetime.date(2026, 9, 17),
            local="Auditório Principal do MEC - Brasília/DF",
            vagas=150,
            preco=50.00,
        )
        e2 = Evento.objects.create(
            titulo="Workshop de Acessibilidade Digital e UX GovBR",
            descricao="Workshop prático sobre eMAG, diretrizes visuais e aplicação de design systems em sistemas web ministeriais.",
            data_inicio=datetime.date(2026, 10, 5),
            data_fim=datetime.date(2026, 10, 6),
            local="Escola Nacional de Administração Pública - ENAP",
            vagas=80,
            preco=0.00,
        )

        InscricaoEvento.objects.create(
            evento=e1,
            nome_participante="Guilherme Moreira",
            email_participante="guilherme@gov.br",
            pago=True,
            valor_pago=50.00,
        )
        InscricaoEvento.objects.create(
            evento=e1,
            nome_participante="Fernanda Lima",
            email_participante="fernanda@gmail.com",
            pago=False,
        )
        InscricaoEvento.objects.create(
            evento=e2,
            nome_participante="Carlos Barbosa",
            email_participante="carlos@saude.gov.br",
            pago=True,
            valor_pago=0.00,
        )

        self.stdout.write("Semeando Chamados de Atendimento...")
        Chamado.objects.create(
            protocolo="CH-20260615-1234",
            assunto="Problema no acesso com certificado digital",
            descricao="Ao tentar logar no painel administrativo utilizando o e-CPF, o sistema retorna um erro 500 informando falha de parse dos campos do certificado.",
            prioridade="alta",
            status="em_atendimento",
            atendente=u_suporte,
        )
        Chamado.objects.create(
            protocolo="CH-20260615-5678",
            assunto="Dúvida sobre preenchimento de portaria de substituto",
            descricao="Gostaria de saber qual tipo de anexo devo enviar no cadastro de professor substituto do campus central.",
            prioridade="baixa",
            status="resolvido",
            atendente=u_suporte,
            resposta="Deve ser anexada a cópia da portaria de homologação em formato PDF contendo as assinaturas digitais.",
            resolvido_em=timezone.now(),
        )

        self.stdout.write("Semeando Solicitações de Serviços...")
        SolicitacaoServico.objects.create(
            nome="João Santos Souza",
            email="joao@gmail.com",
            telefone="(61) 98765-4321",
            tipo="duvida",
            descricao="Como solicito a segunda via do meu histórico acadêmico pelo portal?",
            concorda_termos=True,
        )
        SolicitacaoServico.objects.create(
            nome="Clara Mendes Reis",
            email="clara.reis@hotmail.com",
            telefone="(84) 99123-4567",
            tipo="reclamacao",
            descricao="A página de carregamento de anexo de diploma demorou mais de 5 minutos e depois deu timeout.",
            concorda_termos=True,
        )

        self.stdout.write(self.style.SUCCESS("Banco de dados semeado com sucesso!"))
