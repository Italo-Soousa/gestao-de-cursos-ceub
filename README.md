# gestao-de-cursos-ceub
# Projeto de gestão de cursos
### Projeto de gestão de cursos feito pelo professor Gilberto Hiragi nas matérias de Pensamento Computacional e Banco de Dados. Tem como objetivo a criação de um sistema de gestão de cursos de monitoria, onde alunos podem se inscrever em cursos e os administradores podem gerenciar esses cursos, inscrições e perfis de usuários. O sistema utiliza MySQL como banco de dados para armazenar informações sobre os cursos, inscrições de alunos e o perfil dos usuários. A finalidade é facilitar a organização e o acompanhamento de cursos e suas respectivas inscrições.
### Tabelas do Banco de Dados
Este projeto utiliza 3 tabelas principais

1. Tabela cursos: armazena as informações sobre os cursos disponíveis para os alunos. Cada curso possui um id_curso, nome, carga_horaria, vagas, descricao. Exemplo de criação da tabela cursos:
CREATE TABLE `curso` (
  `id_curso` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(20) NOT NULL,
  `carga_horaria` int NOT NULL,
  `vagas` int NOT NULL,
  `descricao` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_curso`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb3

Campos:
id_curso: Identificador único do curso.
nome: Nome do curso.
carga_horaria: Duração do curso em horas.
descricao: Descrição detalhada do curso.
vagas: Número de vagas disponíveis.

2. Tabela perfis: armazena os dados dos usuários do sistema. Cada usuário pode ser um aluno ou administrador. Esta tabela inclui o id_perfis, nome, login, senha, email, tipo_usuario.

Exemplo de criação da tabela perfis:
CREATE TABLE `perfis` (
  `id_perfis` int NOT NULL AUTO_INCREMENT,
  `login` varchar(30) NOT NULL,
  `senha` varchar(30) NOT NULL,
  `email` varchar(50) NOT NULL,
  `tipo_usuario` varchar(50) NOT NULL,
  `nome` varchar(45) NOT NULL,
  PRIMARY KEY (`id_perfis`),
  UNIQUE KEY `login_UNIQUE` (`login`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3

Campos:
id_perfis: Identificador único dos perfis.
nome: Nome do usuário do perfil.
login: Email utilizado para fazer o login.
senha: Senha utilizada para fazer o login.
email: Email utilizado para fazer o login.
tipo_usuario: Tipo do usuário (aluno ou administrador)

3. Tabela inscricoes: armazena as inscrições dos alunos nos cursos. Cada inscrição está associada a um aluno, a um curso, a data de inscrição no curso, a nota final do aluno e sua presença.

Exemplo de criação da tabela inscricoes:
CREATE TABLE `inscricoes` (
  `id_inscricao` bigint unsigned NOT NULL AUTO_INCREMENT,
  `id_perfis` int NOT NULL,
  `id_cursos` int NOT NULL,
  `data_inscricao` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `nota_aluno` int DEFAULT NULL,
  `presenca_aluno` int DEFAULT NULL,
  PRIMARY KEY (`id_inscricao`),
  UNIQUE KEY `id_inscricao` (`id_inscricao`),
  KEY `id_perfis` (`id_perfis`),
  KEY `id_curso` (`id_curso`),
  CONSTRAINT `inscricoes_ibfk_1` FOREIGN KEY (`id_perfis`) REFERENCES `perfis` (`id_perfis`),
  CONSTRAINT `inscricoes_ibfk_2` FOREIGN KEY (`id_curso`) REFERENCES `curso` (`id_curso`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3

Campos:
id_inscricao: Identificador único da inscrição.
id_perfis: Identificador único do perfil.
id_cursos: Identificador único do curso.
data_inscricao: Data de inscrição no curso.
nota_aluno: Nota final do aluno no curso.
presenca_aluno: Presença do aluno durante as aulas


### Linguagens utilizadas no projeto: 

<div style="display: inline_block"><br/>
    <img align="center" alt="html5" src="https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white" />
    <img align="center" alt="html5" src="https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white" />
</div>
