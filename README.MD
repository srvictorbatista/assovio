#   ![Assovio](https://img.icons8.com/ios-filled/50/AAAAAA/whispering.png)      Assovio – Transcrição de Áudio  HTTP Request 
## Transcrição de Áudio em Português Brasileiro via HTTP (Oaut-opt)



[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)        [![GitHub Repository](https://img.shields.io/badge/github%20-%20Repository-%23D8B00??style=for-the-badge&logo=github&logoColor=white)](https://github.com/srvictorbatista/assovio)

**Made Withe:**

 ![Python Slin](https://img.shields.io/badge/python%20-%203%20Slin-%23F1BF7A??style=for-the-badge&logo=python&logoColor=white)        ![Docker-Compose](https://img.shields.io/badge/docker%20-%20Compose%20-%233776AB??style=for-the-badge&logo=docker&logoColor=white)      ![ApiKey](https://img.shields.io/badge/ApiKey%20-%20WEB%20Security%20-%23FC6D26??style=for-the-badge&logo=caddy&logoColor=white)       ![Json](https://img.shields.io/badge/json%20-%20Web%20Response%20-%231B1C30??style=for-the-badge&logo=json&logoColor=white)       ![RAW](https://img.shields.io/badge/RAW%20-%20IA%20Models%20-%237033FD??style=for-the-badge&logo=ray&logoColor=white)  ![FFMPEG](https://img.shields.io/badge/FFMPEG%20-%20Converter%20-%23007808??style=for-the-badge&logo=ffmpeg&logoColor=white)        

**RESTs exemples** (Oaut-opts):

![Python Slin](https://img.shields.io/badge/cURL%20-%20BASH-%23EEEEEE??style=for-the-badge&logo=curl&logoColor=white)         ![Insomnia](https://img.shields.io/badge/Insomnia-%23AD29B6??style=for-the-badge&logo=insomnia&logoColor=white)       ![Postman](https://img.shields.io/badge/Postman-%23FC6D26??style=for-the-badge&logo=postman&logoColor=white)              
![PHP All Versions](https://img.shields.io/badge/PHP%20-%20All%20Versions-%23777BB4??style=for-the-badge&logo=php&logoColor=white)               ![JS All Versions](https://img.shields.io/badge/javascript%20-%20All%20Versions-%23F7DF1E??style=for-the-badge&logo=javascript&logoColor=white)                          ![Python All Versions](https://img.shields.io/badge/python%20-%20All%20Versions-%23F1BF7A??style=for-the-badge&logo=python&logoColor=white)         ![Node.JS All Versions](https://img.shields.io/badge/node.Js%20-%20All%20Versions-%235FA04E??style=for-the-badge&logo=nodedotjs&logoColor=white)


## Índice

- [Descrição](#descrição)
- [Características Técnicas](#características-técnicas)
- [Inicio Rápido!](#inicio-rápido)
- [Exemplos de Uso](#exemplos-de-uso)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Vantagens](#vantagens)
- [Ambiente Docker Compose](#ambiente-docker-compose)
- [Como Executar](#como-executar)
- [Casos de Uso](#casos-de-uso)
- [Segurança](#segurança)
- [Limpeza de Arquivos Temporários](#limpeza-de-arquivos-temporários)
- [Considerações Finais](#considerações-finais)
- [Nota Técnica](#nota-técnica-expandir)
- [Licença](#licença)
- [Destaques e Aplicações](#destaques-e-aplicações)

---

## Descrição

**Assovio** é um microserviço RESTful em Python para transcrição automática de arquivos de áudio em português brasileiro. Utiliza o reconhecimento de voz **Vosk** com modelos offline para garantir privacidade e independência da internet. Pode aplicar correção textual com base em frequência via **SymSpell**, aumentando a qualidade do texto final.

Oferece uma rota única HTTP (`/escutar`) que aceita arquivos via `multipart/form-data` e retorna a transcrição em JSON.

---

## Características Técnicas

- Reconhecimento offline com modelos locais **Vosk**.
- Suporte a múltiplos formatos, transcodificando automaticamente para `.wav` com **FFmpeg**.
- Correção textual opcional usando **SymSpellPy** e dicionário de alta qualidade.
- Processamento concorrente com `ThreadPoolExecutor`.
- Validação do tamanho máximo do arquivo, configurável via variáveis de ambiente.
- Autenticação via chave de API para controle de acesso.
- Documentação e exemplos para diversos ambientes (curl, PHP, Python, Node.js).
- Respostas consistentes no formato `application/json`.

---

## Inicio Rápido!

**Rodando com Docker Compose:**

```bash
docker-compose up --build
```

----------

## Exemplos de Uso


### Usando `cURL` (com autenticação)

```bash
curl -X POST -H "apikey: XXXXXXXXXX" -F "audio=@seuarquivo.wav" http://localhost:55507/escutar

```

### Usando `cURL` (sem autenticação)

```bash
curl -X POST -F "audio=@seuarquivo.wav" http://localhost:55507/escutar

```

<p> &nbsp</p>
Claro! Que não poderia faltar exemplos de uso simples que fazem a requisição para o endpoint `/escutar` do Assovio, incluindo o envio do arquivo de áudio e o cabeçalho de autenticação `apikey`:

----------

### Exemplo em PHP (usando cURL)

```php
<?php

$apikey = "XXXXXXXXXX";
$audioFile = "seuarquivo.wav";
$url = "http://localhost:55507/escutar";

$curl = curl_init();

curl_setopt_array($curl, [
    CURLOPT_URL => $url,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST => true,
    CURLOPT_HTTPHEADER => [
        "apikey: $apikey",
    ],
    CURLOPT_POSTFIELDS => [
        'audio' => new CURLFile($audioFile)
    ],
]);

$response = curl_exec($curl);

if (curl_errno($curl)) {
    echo 'Erro: ' . curl_error($curl);
} else {
    $decoded = json_decode($response, true);
    print_r($decoded);
}

curl_close($curl);

```

----------

### Exemplo em JavaScript

```javascript
const url = "http://localhost:55507/escutar";
const apikey = "XXXXXXXXXX";

// Seleciona o arquivo de um input do tipo file (exemplo)
const inputFile = document.querySelector('input[type="file"]');

inputFile.addEventListener('change', () => {
  const file = inputFile.files[0];
  if (!file) {
    console.error('Nenhum arquivo selecionado.');
    return;
  }

  const formData = new FormData();
  formData.append('audio', file);

  fetch(url, {
    method: 'POST',
    headers: {
      'apikey': apikey
      // Note que não definimos Content-Type aqui, o fetch faz automaticamente para FormData
    },
    body: formData
  })
  .then(response => {
    if (!response.ok) throw new Error('Erro na requisição: ' + response.status);
    return response.json();
  })
  .then(data => {
    console.log('Transcrição:', data);
  })
  .catch(err => {
    console.error(err);
  });
});
```


### Exemplo em Python

```python
import requests

url = "http://localhost:55507/escutar"
headers = {"apikey": "XXXXXXXXXX"}
files = {"audio": open("seuarquivo.wav", "rb")}

response = requests.post(url, headers=headers, files=files)
print(response.json())

```

### Exemplo em Node.js com axios e form-data

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const form = new FormData();
form.append('audio', fs.createReadStream('seuarquivo.wav'));

axios.post('http://localhost:55507/escutar', form, {
  headers: {
    ...form.getHeaders(),
    'apikey': 'XXXXXXXXXX'
  }
}).then(res => {
  console.log(res.data);
}).catch(console.error);

```



## Variáveis de Ambiente

| Variável                 | Tipo    | Padrão                                   | Descrição                                                                                                                                         |
|--------------------------|---------|------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| `INTERNAL_PORT`          | inteiro  | `55507`                                  | Porta onde o serviço ficará disponível.                                                                                                           |
| `MODEL_NAME`             | string  | `vosk-model-pt-fb-v0.1.1-20220516_2113`  | Nome do modelo Vosk na pasta `modelos/`. Use o modelo menor (`vosk-model-small-pt-0.3`) para mais velocidade e menor precisão, ou o maior para mais assertividade e maior latência. |
| `AUTHENTICATION_API_KEY`| string  | `XXXXXXXXXX`                             | Chave de API para autenticação do endpoint. Se vazio (`""`), a autenticação é desabilitada.                                                      |
| `INTERNAL_LIMIT`         | inteiro | `10`                                     | Limite máximo para envio de arquivos de áudio (em MB).                                                                                           |
| `DICIONARIO_DE_FREQUENCIA`| string | `NAO`                                    | Ativa (`SIM`, `1`, `S`, `sim`) ou desativa (`NAO`, `0`, `N`, `nao`) a correção via dicionário SymSpell. Aumenta a acurácia o que pode aumentar o consumo de processamento. |
| `WORKERS`                | inteiro | `1`                                      | Número de processadores físicos dedicados ao processamento.                                                                                       |
| `THREADS`                | inteiro | `4`                                      | Número de núcleos virtuais (threads) utilizados. Influencia o uso de cache e memória.                                                            |




## Vantagens

-   Reconhecimento 100% offline, garantindo privacidade total.
    
-   Correção textual com dicionário de frequência de alta qualidade.
    
-   Arquitetura escalável para uso pessoal e corporativo.
    
-   Suporte a múltiplos formatos com transcodificação via FFmpeg.
    
-   Baixa latência e alta eficiência.

- Alta disponibilidade com baixo consumo.
    
-   Autenticação integrada e validações robustas.
    
-   Limpeza automática de arquivos temporários.
    

----------

## Ambiente Docker Compose

Estrutura de pastas do repositório:

```
assovio/
├── README.md
├── docker-compose.yml
├── audio.ogg               # Áudio para demonstração
├── audio.mp3               # Áudio para demonstração
├── Dockerfiles/
│   ├── assovio             # Dockerfile principal
│   ├── assovio.py          # Script Python dentro do container
│   ├── assovio.sh          # Script de inicialização
│   └── assovio_dicionario_de_frequancia.py  # Script para buildar o dicionário interno

```

----------

## Como Executar

1.  Com **docker** e **docker-compose** instalado em seu ambiente. Execute: 
`docker-compose up --build -d` 
    
2.  Pronto! Agora é só desfrutar do serviço.

3. Uma das formas mais simples de usar este serviço, assim que erguido. É enviando uma requisição cURL:
```bash
curl -X POST -H "apikey: XXXXXXXXXX" -F "audio=@seuarquivo.wav" http://localhost:55507/escutar
```

Sendo **``seuarquivo.wav``**  o arquivo de áudio que você deseja transcrever e **``XXXXXXXXXX``** a chave-api definida no arquivo **``docker-compose.yml``**.



----------

## Casos de Uso

-   Sistemas de atendimento automatizado (URA).
    
-   Transcrição de entrevistas, reuniões, podcasts e vídeos.
    
-   Comandos de voz para automação industrial e residencial.
    
-   Processamento para análises jurídicas e acadêmicas.
    
-   Ferramentas de acessibilidade para deficientes auditivos.
    

----------

## Segurança

Se configurada, a variável `AUTHENTICATION_API_KEY` requer que as requisições incluam o cabeçalho:

```
apikey: XXXXXXXXXX
```
Protegendo o serviço contra acessos não autorizados.
É altamente recomendado que você **substitua a serie de "XXXXXXXXXX" por sua apikey única**. 
<br>
 Uma forma **simples e pratica** de gerar sua própria apikey única. É executando o seguinte comando **a partir de um terminal BASH** (o que inclui o próprio container, se preferir):
 
**``` clear && printf "\n\nSua apikey: \033[1;37;44m %s \033[0m\n\n\n\n" "$(tr -dc 'A-Z0-9' </dev/urandom | head -c10)"```**
Onde "-c" corresponde ao total de caracteres desejados. Neste exemplo, 10.

_Os áudios recebidos, são **imediatamente excluídos** do servidor, assim que transcritos. **Não restando dados remanescentes** da operação._ 

Além disto. O serviço é fornecido em um **ambiente docker**, o que já garante seu **isolamento por padrão**. E ao mesmo tempo, a **conectividade necessária para desfrutar** do serviço com segurança e controles de acesso isoladamente.

----------

## Limpeza de Arquivos Temporários

Arquivos gerados durante o processamento são removidos automaticamente após cada requisição, garantindo segurança e economia de espaço.

----------

## Considerações Finais

Assovio é uma solução robusta e eficiente para transcrição de áudio em português, com foco em privacidade, desempenho e escalabilidade. Seu design modular facilita adaptações para diversos ambientes, do pessoal ao corporativo.

O **dicionário interno** é buildado a partir de um índice amostral de 200 mil palavras classificadas e indexadas por [**WordFrequency**](https://www.wordfrequency.info/portuguese.asp) com base na frequancia de ocorrencia na lingua portufuesa, no período de 2012 a 2019. Obtido em https://www.wordfrequency.info/portuguese.asp neste projeto inclui um script de automação que baixa esta amotra e constroi um dicionário interno com base nesta amostra. Segundo a fonte, os dados são baseados em palavras obtidas e analisadas do [**corpus Web/Dialects**](https://www.corpusdoportugues.org/web-dial/) do Corpus do Português.
Para quem gosta deste tipo de pesquisa/analise estatística, vale am pena dar uma olhada em [**jusText**](https://pypi.org/project/jusText). Trata-se da ferramenta em python usada pela **Web/Dialects** para limpeza durante a catalogação dos dados (webScrap) e você pode [ver mais sobre ela aqui](https://code.google.com/archive/p/justext). Como dados tecncos e uma [amostra](https://nlp.fi.muni.cz/projects/justext) de uso online. Sendo uma poderosa e útil ferramenta para criação de recursos linguísticos.







## [Nota Técnica (expandir)](#nota-tecnica-expandir)
<details>

###  &nbsp; <a href="#nota-tecnica-expandir" target="_blank">Aspectos Importantes</a>
 &nbsp; &nbsp; <summary id="several-resume"><em>Este projeto foi testado e revisado por pares, antes da sua primeira publicação.</em></summary>


<br>

### DICIONÁRIOS LINGUÍSTICOS

O uso de **dicionários linguísticos** para suporte a modelos longos em **motores autohospedados** tem se revelado uma estratégia altamente eficaz para ampliar a **assertividade analítica em tempo real**. Entretanto, essa abordagem incorre em **custos computacionais e impactos diretos no tempo de resposta**, aspectos que precisam ser criteriosamente avaliados de acordo com as condições de infraestrutura, o nível de exposição e os objetivos do ambiente em questão.

### DIMENSIONAMENTO E ALOCAÇÃO DE RECURSOS

Em cenários com infraestrutura limitada, em universos amostrais reduzidos ou em contextos em que **a agilidade operacional seja mais importante que a precisão linguística**, **não recomendo a adoção de dicionários de frequência linguística**, tampouco de modelos extensos. Em diversos testes realizados, a inclusão desses componentes **não apresentou ganhos significativos na qualidade dos resultados**. Pelo contrário — observou-se, em alguns casos, **um aumento no tempo de resposta** e **degradação da qualidade léxica e sintática**, quando comparado ao uso corretamente dimensionado desses mesmos recursos.

Como exemplo prático de **dimensionamento eficiente**, menciono requisições contendo áudios superiores a 3 minutos que foram processadas com extremo sucesso em **frações de segundo**, utilizando apenas um núcleo físico (3.0 GHz) e 4 threads (configuração padrão). Importante destacar que tais resultados foram obtidos **sem o uso de dicionários linguísticos**, operando com um **modelo longo de 14 bilhões de parâmetros**, previamente ajustado para **execução simultânea em ambientes de produção com múltiplas requisições concorrentes**.

Diante disso, **recomendo fortemente a realização de testes controlados e ajustes finos nos parâmetros**, considerando as características específicas de cada aplicação. Estou convicto de que **os resultados obtidos — mesmo com infraestrutura modesta — podem ser comparáveis (ou superiores)** aos oferecidos por soluções comerciais de grande porte e alto custo.

Adicionalmente, destaco que **a crescente vilanização de serviços externos** (como clouds e plataformas SaaS) — muitas vezes criticados por seus custos elevados, tráfego excessivo ou uso intensivo de processamento — tem motivado a busca por **alternativas autônomas, mais eficientes e economicamente viáveis**. Esta proposta foi concebida justamente com esse propósito: **oferecer performance de alto nível, com independência operacional e controle total sobre os recursos disponibilizados**.

</details>


----------



&nbsp;



## [Licença](#licenca)
<details>
 &nbsp; <summary id="licenca">Este projeto está licenciado sob a Licença MIT</summary>

## &nbsp; &nbsp; <a href="https://opensource.org/licenses/MIT" target="_blank">Licença MIT - Open Source</a>

É concedida permissão, gratuitamente, a qualquer pessoa que obtenha uma cópia deste software e dos arquivos de documentação associados (o “Software”), para negociar o Software sem restrições, incluindo, sem limitação, os direitos de usar, copiar, modificar, mesclar , publicar, distribuir, sublicenciar e/ou vender cópias do Software e permitir que as pessoas a quem o Software seja fornecido o façam, sujeito às seguintes condições:

O aviso de direitos autorais acima e este aviso de permissão serão incluídos em todas as cópias ou partes substanciais do Software.

<STRONG> O SOFTWARE É FORNECIDO “NO ESTADO EM QUE SE ENCONTRA”, SEM GARANTIA DE QUALQUER TIPO, EXPRESSA OU IMPLÍCITA, INCLUINDO, MAS NÃO SE LIMITANDO ÀS GARANTIAS DE COMERCIALIZAÇÃO, ADEQUAÇÃO A UM DETERMINADO FIM E NÃO VIOLAÇÃO. EM HIPÓTESE ALGUMA OS AUTORES OU DETENTORES DE DIREITOS AUTORAIS SERÃO RESPONSÁVEIS POR QUALQUER RECLAMAÇÃO, DANOS OU OUTRA RESPONSABILIDADE, SEJA EM UMA AÇÃO DE CONTRATO, ATO ILÍCITO OU DE OUTRA FORMA, DECORRENTE DE, OU EM CONEXÃO COM O SOFTWARE OU O USO OU OUTRAS NEGOCIAÇÕES NO PROGRAMA.</STRONG>


A Licença MIT é uma licença de software de código aberto que permite aos usuários utilizar, modificar, distribuir e sublicenciar o software sem restrições significativas, desde que a notificação de direitos autorais e a licença sejam incluídas em todas as cópias ou partes substanciais do software.

A Licença MIT é conhecida por sua simplicidade e permissividade. Ela permite que os usuários façam praticamente qualquer coisa com o software, incluindo o uso comercial, sem a necessidade de compartilhar as modificações ou melhorias que façam no código-fonte.

Principais características da Licença MIT:
- **Permissiva**: A Licença MIT é considerada uma das licenças mais permissivas em termos de uso de software. Ela permite que os usuários façam quase tudo o que quiserem com o software, incluindo o uso comercial, sem muitas restrições.
- **Requisitos mínimos**: A licença é muito curta e simples, com requisitos mínimos para o uso e redistribuição do software. Geralmente, exige apenas a inclusão do aviso de direitos autorais e da licença em todas as cópias do software.
- **Compatibilidade**: A Licença MIT é compatível com muitas outras licenças de código aberto, permitindo que o software licenciado sob a MIT seja combinado e distribuído com software licenciado sob outras licenças de código aberto.

A Licença MIT é uma escolha popular para projetos de software de código aberto devido à sua simplicidade e permissividade, permitindo que os desenvolvedores compartilhem e usem software com poucas restrições.

</details>


<BR><BR>


### Autor: Sr. Victor Batista -  t.me/LevyMac 
| [<img src="https://avatars.githubusercontent.com/u/131806887?v=4" width=85><br><sup>Sr. Victor Batista</sup>](https://github.com/srvictorbatista) |
| :---: |

##### CONTATO: 
[![Contact|Solid](https://img.shields.io/badge/contact%20%5BPT--BR%5D-@levymac-9cf?labelColor=brightgrey&style=for-the-badge&logo=telegram)](https://t.me/levymac)




----------

## Destaques e Aplicações

-   Domino e privacidade total (100% offline).
    
-   Baixo custo operacional sem dependência de serviços pagos na nuvem.
    
-   Integração simples e instantânea, via API REST.
    
-   Alta performance em hardware modesto. 

-   Alta portabilidade com baixa latência (self-hosted).

-   Extremamente escalável, em ambientes de produção.
    
-   Aplicações educacionais, jurídicas, industriais, e mais.
    
-   Fácil customização para novos idiomas, modelos e usos.
    

    
----------

# Obrigado por assoviar também! 😙🚀



