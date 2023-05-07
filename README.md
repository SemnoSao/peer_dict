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
Este será um sistema cliente/servidor. O servidor é responsável por armazenar os dados e executar as operações de busca. O cliente é responsável por enviar os comandos para o servidor e receber os resultados. Ao lado do cliente teremos o componente de interface e do lado do servidor teremos o componente de processamento e dados. Dessa forma, descrevemos as seguintes ações:
- o usuário inicia uma conexão com o servidor através da interface, o servidor então inicia uma thread que ficara em escuta de mensagens dessa conexão
- uma vez em modo de escuta o usuário pode enviar comandos para o servidor através da interface
- ao enviar uma entrada para ser armazenada o servidor recebe e armazena, retornando a confirmação para o usuário
- ao iniciar uma busca o servidor recebe e realiza a busca, retornando o resultado para o usuário
- o administrador pode iniciar um processo de remoção informando a senha no inicio da mensagem, o servidor recebe, valida a senha e remove a entrada, retornando a confirmação para o usuário

### Mensagem
a mensagem passada para o servidor tem o seguinte formato:
```
[comando] [chave] [tamanho do corpo]
[corpo]
```
os comandos possíveis são: search, insert, remove. A chave é o termo de referência e o tamnho do corpo é o tamanho do corpo na linha de baixo que pode ser o valor da chave ou a senha de administração, tudo em texto UTF-8. Queremos que o tamanho do cabeçalho caiba em um único receive de 1024 bytes, dessa forma temos o campo comando com 5 bytes, e escolhemos o campo tamanho do corpo com 6 bytes, unicamente por simetria, dessa forma com os espaços e quebra de linha totalizando 14 bytes, portanto a chave pode ter um total de 1024-14=1010 bytes. O corpo tem um tamanho total de 99999 bytes. O tamanho do corpo é necessário para que o servidor saiba quantos bytes deve receber para completar a mensagem.
 




