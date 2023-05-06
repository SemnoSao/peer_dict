 # peer_dict
só mais um projeto de dicionário distribuído

# arquitetura
este projeto prevê o estilo arquitetural em camadas, definido como abaixo:
## componentes
1. interface de usuário
2. camada de processamento
3. camada de dados
## funcionalidades
### 1. interface de usuário
Prove a interface de usuário para o usuário interagir com o sistema. A interface de usuário é responsável por receber os comandos do usuário e enviar para a camada de processamento através da chamada de método.
Aqui também é onde o usuário pode visualizar os resultados das buscas. Valida as permissões do usuário para executar as operações.
### 2. camada de processamento
Recebe os comandos da interface de usuário e os processa. A camada de processamento é responsável por traduzir, checar e validar os comandos recebidos e enviar para a camada de dados através da chamada de método. Também é responsável por receber os resultados da camada de dados, traduzí-los e enviar para a interface de usuário.
### 3. camada de dados
Recebe os comandos da camada de processamento e realiza as buscas necessárias. A camada de dados é responsável por armazenar os dados e executar as operações de busca. Também é responsável por enviar os resultados para a camada de processamento.

## arquitetura de sistema
Este será um sistema par-a-par. Cada usuário tem um dicionário local, armazenado em arquivo onde pode realizar buscas, adicionar e remover entradas. Cada usuário também pode se conectar a outros usuários para compartilhar seus dicionários. Quando um usuário se conecta a outro, ele pode realizar buscas no dicionário do outro usuário. 
Dessa forma, um usuário pode começar uma instância local, onde terá um terminal com comandos para:
- adicionar uma entrada ao dicionário local
- remover uma entrada do dicionário local
- buscar uma entrada nos dicionários conectados
- conectar a outro usuário 

Assim, toda instancia do sistema funciona em todas as camadas e cabe a camada de processamento iniciar as buscas local e remotamente, reunindo a informação coletada e transmitindo à camada de aplicação. Descreve-se a busca, a operação de fato distribuída, da sefuinte forma:
1. o usuário inicia uma busca local através da camada de aplicação
2. a camada de aplicação envia a busca para a camada de processamento
3. a camada de processamento envia a busca para a camada de dados local e armazena, temporariamente, o resultado
4. a camada de processamento verifica se existem conexões ativas e envia a busca para as instancias remotas, e aguarda a resposta
5. uma instancia remota realiza o passo 3 e envia o resultado para a requisitante
6. a camada de processamento recebe o resultado, junta ao resultado do passo 3 e envia para a camada de aplicação
 




