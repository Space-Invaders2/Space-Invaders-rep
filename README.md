# Projeto de MAC0413/5714 - Tópicos Avançados de Programação Orientada a Objetos :100:



# Space Invaders :space_invader:
Space Invaders é um vídeo game Arcade da década de 60 e um dos primeiros jogos de tiro criados, utilizou famosos filmes de ficção científica como inspiração, como [A Guerra dos mundos](https://pt.wikipedia.org/wiki/A_Guerra_dos_Mundos) e [Star wars](https://pt.wikipedia.org/wiki/Star_Wars).

# Objetivo do projeto :checkered_flag:
Este projeto visa desenvolver uma versão aprimorada e contemporânea do clássico jogo **[Space Invaders](https://en.wikipedia.org/wiki/Space_Invaders)** em **[Python](https://python.org)** por meio da biblioteca **[Pygame](https://www.pygame.org)**.

Ao incorporar elementos de [Bullet Hell](https://en.wikipedia.org/wiki/Bullet_hell) como itens, teremos uma jogabilidade desafiadora e variada. Os jogadores enfrentarão ondas de projéteis que necessitam de precisão e reações rápidas, assim como uma variedade de inimigos, obstáculos e itens que mudam a cada sessão de jogo.

Além disso, poderão fazer uso de obstáculos e powerups para avançar ao longo dos níveis, com objetivo final de escalar para a primeira posição do leaderboard.



# Autores

|Nome|NUSP|Usuário|
|-|-|-|
|Arthur Teixeira Magalhaes|4876102|@kignarthur|
|Gustavo Akio Honda|12543395|@gustavo_honda|
|Martin Mayer|15044014|@martin.mayer3|

# Conteúdo
1. [O que já foi feito](#O que já foi feito)
2. [Bugs a serem consertados](#Bugs a serem consertados)
3. [Jogabilidade](#Jogabilidade)
4. [Modelagem do projeto](#Modelagem do projeto)
5. [Design patterns](#Design Patterns)
6. [Implementações](#Implementações)
7. [Detalhes do Desenvolvimento](#Detalhes do Desenvolvimento)
8. [Como Rodar](#Como Rodar)
9. [Referências](#Referências)

# O que já foi feito :feet:

- **7 Níveis Implementados** :milky_way:
- **4 Aliens implementados** :alien:
- **1 Espaço nave do player implementada**:rocket:
- **5 Obstáculos implementados**:shield:
- **Controles funcionando**:joystick:
- **Movimento das entidades implementado**:runner:
- **Som do jogo implementado**:sound:
- **Interface de armas para aliens e players criada**:gun:
- **Colisões entre as entidades funcionando**:boom:
- **Tela de fim do Jogo implementadas**:skull:
- **Utilização de Imagens**:art:
- **Interface para powerups criada**:pill:
- **Lógica de loop do Jogo implementada**:loop:
- **Várias iterações de refatoração**:wrench:
- **Interface de usuário para settings do jogo implementada**:level_slider:
- **Arquivo que armazena diferentes configurações de variáveis do jogo implementadas** :gear:
- **5 powerups funcionando** :fire:

# Looks and Feels :lipstick:
Ao implementar o padrão Abstract Factory, exploraremos **diferentes estilos visuais**, conhecidos como "Looks & Feels". Os estilos incluirão opções como "Retrô", "Moderno" e uma combinação de ambos, proporcionando aos jogadores uma experiência visual personalizável e única.

# Bugs a serem consertados :bug:

- Aparente problema de colisão dos aliens com a parede :no_entry:
- Se os lasers forem muito rápidos há problema de colisão com obstáculos :no_entry:
- Queda do FPS caso centenas de tiros sejam criado de uma só vez :no_entry:
- Refatorar organização de módulos do jogo


# Jogabilidade :video_game:
## Menus
### Menu principal e jogo
| Função | Botão |
| ------ | ------ |
| Ver Highscores | H |
| Iniciar o jogo | Enter |
| Mover para esquerda | Seta esquerda |
| Mover para direita | Seta direita |
| Atirar | Barra de espaço |
|   Pausar     |    P     |
| Menu de configurações | P > S |
| Terminar a pausa     | Enter |
| Sair do jogo | P > Q |


### Configurações
| Função | Botão |
| ------ | ------ |
| Fechar configurações | S |
| Mudar desenho | D |
| Mudar dificuldade | Setas 1 - 5 |
| Ordem dos níveis | O |
| Ordem dos itens | P |
| Menu de configurações de som | A |

### Configurações de som
| Função | Botão |
| ------ | ------ |
| Fechar configurações de som | A |
| Ligar/Desligar música* | M |
| Definir o volume da música | Seta para cima / baixo |
| Ligar/Desligar sons | N |
| Definir o volume do som | V / B |

*Nota: A música depende do desenho nas configurações

### Fim do Jogo
| Função | Botão |
| ------ | ------ |
| Ver Highscores | H |
| Configurações | S |
| Tela inicial | 0 |

Se você fiquou entre os dez primeiros, pode inserir seu nome no fim do jogo. Você pode digitar seu nome novamente se comete um erro, mas ele só pode ser salvado uma vez

| Função | Botão |
| ------ | ------ |
| Inserir / Reinserir nome | E |
| Confirmar nome | Enter |
| Salvar nome | G |

## Mecânicas do jogo

### Alteração de Níveis
Após eliminar todos os aliens o próximo nível é carregado, como temos poucos níveis decidimos deixá-los em looping.

### Condição de Derrota
O player tem 5 vidas iniciais, antes que as perca, o player deverá conseguir o máximo de ponto antes que os lasers dos aliens acabem com todas as 5 vidas ou que o tempo acabe !

### Dificuldade do jogo
Os powerups são criados em lugares aleatórios, dependendo da dificuldade a quantidade de powerups criados é alterada e a acessibilidade é dificultada.

### Powerups de vida
Os dois power-ups relacionados a saúde do jogador o torna imune por um determinado período de tempo ou lhe dá uma vida extra. O jogador começa com 5 vidas e a quantidade máxima é 7.

### Diferentes tiros
Os três powerups relacionados a modificação da arma do jogador são: um tiro triplo, tiros mais frequentes e uma arma com laser duplo de velocidade mais lenta.

### Diferentes tipos de aliens
Existem 4 tipos de aliens com recompensas diferentes  por ordem de valor temos: vermelhos, verdes, amarelos e azuis que são os mais valoroso e dificeis de se acertar.

# Modelagem do projeto :open_file_folder:
Faremos um UML do projeto utilizado como base para visualizarmos as diferenças na implementação do código antes e depois da implementação:

Link para modelo: [Modelo do Tutorial UML](https://drive.google.com/file/d/1GXVy3ALOeCqvek3Zk6BwkmDtzCn8YvvO/view?usp=sharing)

Inicialmente fizemos um modelo em UML para nortear a refatoração que fariamos e esclarecer quais serão as divisões de modúlos, classes, métodos e atributos que utilizariamos no nosso projeto.

Link para modelo: [Modelo de referência UML](https://drive.google.com/file/d/16A1o2KsL9HRicJUy64CX809FY0magus4/view?usp=sharing)


Após um processo de refatoração das partes que envolvem o projeto, estamos implementando um modelo mais atualizado que visa descrever como a modelagem do projeto está em tempo real, utilizamos um mapa de cores para descrever quando implementamos cada parte do sistema.
Obs: por alterarmos frequentemente o sistema, as variávei e methodos das classes talvez não estejam totalmente corretos ou em seus devidos lugares

Link para modelo: [Modelo Descritivo UML](https://drive.google.com/file/d/14jP3LvyDQXnAXiKt9OiG0mOtJFOhZCsM/view?usp=sharing).



# Design Patterns :paintbrush:
Utilizamos padrões de projeto para melhorar a clareza do código, para facilitar sua evolução, desacoplá-lo, deixá-lo mais coeso e assegurar seu correto funcionamento.

Listamos os padrões utilizados nesse projeto e como são implementados:

## Stategy Design Pattern :mahjong:
Usamos o **Padrão Strategy** para **criar diferentes formações de alien** para tornar o jogo mais variado e conseguir controlar a **dificuldade do jogo**. Devido ao **polimorfismo** do POO, somente **a mesma função é chamada** para criar a estratégia dos aliens e somente a estratégia é alterada.

## Decorator Design Pattern :tanabata_tree:
O **Padrão Decorator** é usado para adicionar novas funcionalidades na arma do jogador de maneira dinâmica, sem alterar sua estrutura básica. Isso permite **combinar diferentes upgrades** de forma dinâmica.

## Singleton Design Pattern :point_up:
As **configurações e definições**, bem como o design, **devem ser chamados de maneira uniforme** por todas as classes do jogo. Como diferentes classes têm acesso a eles ao mesmo tempo. Para garantir que todas as classes acessem a mesma instância ao mesmo tempo, usamos o **Padrão Singleton**.

## Factory Design Pattern :factory:
Implementamos o padrão "Design Fabric" no módulo graphics para podermos utilizar **diferentes desenhos para o jogo**. O código pode **ser facilmente ampliado** para implementar outros designs.
As imagens podem ser chamadas por meio de uma classe especial que implementa a interface, de modo que apenas uma instância da classe precisa ser referenciada no restante do código

## Visitor Pattern :wave:
Usamos o **Padrão Visitor** no módulo change_design nas classes Visitor, DesignUpdater e ComponentToBeUpdated. Os objetos do jogo têm uma imagem que é definida durante a inicialização e é repintada a cada iteração. Todas essas instâncias implementam a interface ComponentToBeUpdated com a **função accept(Visitor)** para atualizar a imagem quando o usuário altera o design nas configurações. Dessa forma, os objetos só precisam de uma função para aceitar a imagem e o resto do código é externalizado.

# Implementações :calendar: :paperclip: - :pushpin:

## Próximas metas :dart:
- Adicionar mais testes de unidade e integração :wrench:
- Consertar bugs atuais :hammer:
- Criar mais tipos de aliens :alien:
- Adicionar mais trilhas sonoras :musical_note:
- *Boss Fight* :space_invader:
- *Behaviour Tree* para padrões mais complexos de comportamento de entidades e do sistema :deciduous_tree:

## Futuras Implementações :clipboard:
- Sistema para salvar o progresso do jogo :floppy_disk:
- Implementar tiros que explodem :bomb:
- *Grid Collision* para diminuir a complexidade de processamento de colisões e aumentar a performance :hash:

## Ideias de futuras Implementações :bulb: :writing_hand:
- Criação de uma IA para jogar o Space Invaders :robot:
- Utilização de padrão observer para atualização de eventos do jogo :eyes:
- Utilizar ray casting para detectar trajetória de tiros velozes para interceptar obstáculos :high_brightness:


# Detalhes do Desenvolvimento

## Utilização de Tutorial :arrow_forward:
Como nenhum integrante do grupo sabia como fazer jogos, para nos familiarizarmos com o pygame e a dinâmica de desenvolvimento de jogos com bibliotecas e engines, utilizamos este tutorial do youtube como [base para nosso projeto](https://www.youtube.com/watch?v=o-6pADy5Mdg&authuser=0) e seu respectivo [repositório](https://github.com/clear-code-projects), esse projeto tem como [**Licensa de uso CC0**](https://creativecommons.org/publicdomain/zero/1.0/deed.pt-br) que permite copiar, modificar, distribuir e executar o trabalho, mesmo para fins comerciais, tudo sem pedir autorização, além disso os direitos de patente ou marca registrada de qualquer pessoa não são afetados pela CC0, nem os direitos que outras pessoas possam ter sobre o trabalho ou sobre como o trabalho é usado, como publicidade ou direitos de privacidade.

## Utilização de Branches
Inicialmente separamos as branches por features e cada membro da equipe atuava em uma branch para o desenvolvimento de uma feature específica.

Entretanto como estavamos em uma fase inicial do projeto, o código apresentava alto acoplamento e, então, o processo de merge das features era muito complicado e demorado. Por isso decidimos utilizar uma branch única para o desenvolvimento do código - **[Branch Refactor](https://gitlab.com/psato/tapoo/-/tree/Refactor?ref_type=heads)** - e outra para guardar versões estáveis do jogo - **[Branch main](https://gitlab.com/psato/tapoo/-/tree/main?ref_type=heads)**

Antes de cada entrega de trabalho estamos fazendo [merge da branch Refactor na Main](https://gitlab.com/psato/tapoo/-/merge_requests/9/commits).

## Mudança de Godot para Pygame :arrows_counterclockwise:
Começamos a implementar o jogo básico para nos familiarizarmos com o ambiente de desenvolvimento Godot.

Durante as etapas iniciais do desenvolvimento do jogo,percebemos que devido a GUI do Godot ter muitas funcionalidades, vários padrões de projeto que utilizaríamos não seriam necessários já que a própria interface supria essas necessidades, a framework , tivemos dificuldade de nos adaptar a nova linguagem [gdscript](https://docs.godotengine.org/pt-br/4.x/tutorials/scripting/gdscript/gdscript_basics.html) específica do Godot Engine.

Portanto, iniciamos novamente o projeto utilizando a biblioteca [Pygame](https://www.pygame.org/docs/) para não sofrermos com essa restrição no futuro.

## Redução da equipe :arrow_down:
Durante o desenvolvimento do projeto Pedro Rabello Sato parou de cursar a matéria, agora estamos desenvolvendo esse projeto com **3 membros na equipe**.

# Como Rodar :gear:

## Pré-requisitos
Python 3.9 instalado e no `$PATH`.
## Clonar Repositório
```
git clone 'https://gitlab.com/psato/tapoo'
cd tapoo
```
## Instalar Requisitos

```
python3.9 -m venv .venv
source .venv/bin/activate
pip install -r SpaceInvadersPygame/requirements.txt
```
Foi criado um [ambiente virtual](https://docs.python.org/3.9/library/venv.html) para instalar nada no seu sistema.
### Rodar o jogo
Para rodarmos o jogo também há a opção de utilizarmos arquivos de configurações diferentes para o jogo, alterando a requencia de tiro,o tamanha, a velocidade, a posição de outras entidades e outras variáveis relacionadas a mecânica do jogo.

A escolha desse arquivo pode ser encontrada em **Config.py** com o nome **DEV_FILE** .

```
SpaceInvadersPygame$ make run
```
# Desenvolvimento :hammer:
## Pre-commit
Instalar o [pre-commit](https://pre-commit.com/) na versão do python 3.9.\
Basta rodar o pre-commit uma vez para adicionar os ganchos no git do repositório do projeto, recomenda-se utilizar o virtualenv criado para instalar o projeto.
```
cd $REPODIR
pre-commit install
```
## Executar testes

```
SpaceInvadersPygame$ make all_tests
```
## Verificar Cobertura de testes

```
SpaceInvadersPygame$ make test_cov
```

## Formatar Código

```
SpaceInvadersPygame$ make format

```

## Pre-commit

```
SpaceInvadersPygame$ make precommit
```

# Referências
## Conhecimento
[Design Patterns guide](https://refactoring.guru/design-patterns/catalog) \
[Pygame Documentation](https://www.pygame.org/docs/) \
[Tutorial pygame](https://www.youtube.com/watch?v=o-6pADy5Mdg&authuser=0)
[Repositório do tutorial](https://github.com/clear-code-projects/Space-invaders)\
[Sound effects and images for classic design](https://github.com/clear-code-projects/Space-invaders/tree/main)\
[Behavior tree](https://docs.unrealengine.com/4.27/en-US/InteractiveExperiences/ArtificialIntelligence/BehaviorTrees/BehaviorTreesOverview/)

## Imagens
[Images classic design](https://github.com/clear-code-projects/Space-invaders/tree/main/graphics) (excluding powerups)\
[Images classic design - Powerups](https://kyrise.itch.io/kyrises-free-16x16-rpg-icon-pack)\
[Images modern design](https://kenney.nl/assets/space-shooter-extension) (excluding powerups)\
[Images modern design - Powerups](https://kenney.nl/assets/space-shooter-redux)\
[Images black white design](https://kenney.nl/assets/simple-space) (including powerups) \
[Images christmas](https://asymmetric.itch.io/christmas-pixel-art-icon-pack?download) \
[Image background](https://www.youtube.com/watch?v=mM5LBBiDRts)

## Efeitos sonoros
### Músicas
[Design Classic](https://github.com/clear-code-projects/Space-invaders/tree/main/audio)\
[Design Modern\[Lounge Drum and Bass - ComaStudio\]](https://pixabay.com/de/music/schlagzeug-und-bass-lounge-drum-and-bass-108785/)\
[Black white Design [Cruising Down 8bit Lane - Monument_Music]](https://pixabay.com/de/music/videospiele-cruising-down-8bit-lane-159615/)
### Laser
[Pixabay - Laser](https://pixabay.com/de/sound-effects/laser-45816/)
### Explosões
[Explosion: [Pixaby - Pop2]]\
(https://pixabay.com/de/sound-effects/pop2-84862/)
