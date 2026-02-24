# Descrição

Este projeto consiste na criação de um servidor de aplicação na forma de uma API Rest.

Caso haja uma rota de definida para a chamada HTTP feita, retorna o resultado gerado pela função associada a esta chamada.

Porém, se a chamada for do tipo GET, e não houve uma rota espacífica para esta chamada, com o caminho indicado na roda, é executada uma função padrão que executa um CMS (gestor de conteúdo).

**Requisitos**

- **FastAPI** - toda gestão de requisições e definição de endpoint é feita com o módulo FastAPI
- **Pyrsing** - Todo conteúdo pode ser escrito diretamente em HTML ou em formato Markdown, que será convertido em HTML para ser exidido em navegadores. O módulo Pyrsing é o responsável por fazer a conversão de documentos Markdown em HTML.

# Projeto

O módulo Etomyte é estruturado para ser utilizado na forma de um projeto. Um projeto Etomyte, por sua vez, é basicamente um diretório. Um diretório onde os componentes (definições de rotas, configurações, e componentes do CMS) estão alocados.

Podemos criar um projeto manualmente, criando a estrutura de ficheiros e pastas, ou simplesmente utilizar o comando:

```bash
python -m etomyte "nome_do_projeto"
```

**Execução**

```bash
python -m etomyte run "caminho/para/pasta_do_projeto"
```

# CMS

O CMS funciona quando o servidor de aplicação recebe uma solicitação do tipo GET e não há uma rota já definida no framework para esta rota. Neste caso, é extraído o caminho (path) da URL, e os parametros.

O framework então busca por um conteúdo indicado pelo caminho da URL.

Se o conteúdo for encontrado, o CMS carrega o conteúdo e processa a resposta. Se não encontrar, faz redirecionamento para carregar o conteúdo padrão que representa o erro 404.

## Componentes do CMS

Os componentes que fazem parte do CMS são:

- **Conteúdo** - conteúdo retornado mediante ao path da URL solicitada.
- **Template** - páginas master onde os conteúdos são carregados. 
- **Snippets** - códigos modulares que podem ser utilizados em templates e conteúdos.

### Templates

Quando o usuário faz uma requisição para uma determinada URL, é buscado um template que exista no caminho indicado. Suponha-se que seja requisitado:

`GET /produtos/carros/modeloX`

Neste momento será buscado um template no caminho `/produtos/carros/modeloX`.

Caso não exista um template para o caminho indicado, sobe-se na hierarquia dos documentos e procura pelo template na parte do path anterior ao path requisitado, no caso, um template em _carros_: `/produtos/carros`.

É feito isso sucessivamente até buscar um template na raiz `/`, que é o **template padrão** do sistema, carregado quando o visitante acessa a raiz do sistema ou quando nenhum template **mais específico** a solicitaão é encontrado. 

Por _default_ o **template padrão** é armazenado com o nome `index`. Mas isso pode ser alterado nas configurações do CMS.

Templates, por tanto, são como páginas _master_ que retornar um "conteúdo" para a solicitação feita, sendo flexível o bastante para, caso não seja encontrado, retornar um template mas generalista, em um nível acima, ou até mesmo o template raiz.

Templates podem possuir em seu texto a marcação `{{content}}`. Esta marcação será substituída pelo conteúdo específico a URL, referente ao caminho solicitado inicialmente.

### Conteúdo

Enquanto templates são "conteúdos flexíveis", capazes de retornar uma resposta subindo na hierarquia do caminho requisitado, Conteúdos possuem uma resposta mais inflexível.

Se o usuário solicitar `GET /produtos/carros/modeloX`, é esperado que exista um conteúdo no caminho `/produtos/carros/modeloX`.

Caso não exista um conteúdo que case exatamente com a solicitação, uma resposta do tipo 404 é retornada.

Conteúdos são processados e anexados ao conteúdo do template para gerar a resposta. O conteúdo é processado e seu conteúdo é unido com o código do template para formar a resposta final. A marcação `{{content}}` é o local no template onde o conteúdo será adicionado.

Imagine que tenhamos o conteúdo `/produtos/carros/modeloX` e seu código seja:

```md
## Model X

O modelo Model X é o modelo com mais espaço fabricado pela Tesla.
```

E tenhamos o template `/produtos/carros/`:


```md
# Carros

{{content}}
```

O resultado final ao acessar o endereço seria `/produtos/carros/modeloX` basicamente o conteúdo referente aplicado sobre o template relativo (já que não havia um template mais específico para este caminho):

```md
# Carros

## Model X

O modelo Model X é o modelo com mais espaço fabricado pela Tesla.
```

Existem conteúdos padrão, que já acompanham o framework, que são usados para representar mensagens de sistema, como erros do tipo 404, 503, etc.

### Snippets

Snippets são marcações que podem ser adicionadas em templates e conteúdo que, durante o processamento, chamam a execução de códigos e, ao fim da execução, a marcação será substituída pelo resultado do processamento.

Snippets funcionam, por tanto, como módulos para reaproveitamento de código.

A marcação que indica um snippet são duas chaves que envolvem o nome do snippet `[[meu_snippet]]`.

Podemos passar parametros para a execução do snippet, de forma que ele pode ter respostas dinâmicas. Os parametros são passados no mesmo formato que passamos parametros por URLs. Veja o exemplo:

`[[meu_snippet?parametro1=valor1,parametro2=valor2,...]]`.

O resultado da execução do snippet deve ser armazenado obrigatóriamente em uma variável chamada `result`. É essa variável do snippet que terá seu conteúdo recuperado e adicionado no local da marcação original que chamou o snippet. 

Podemos ver a marcação ``{{content}}` (que carrega o conteúdo nos templates) como um snippet embutido no sistema.

# Execução

