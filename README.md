# Ferramentas Desenvolvidas para Beeware + TOGA

Espero que estas ferramentas sejam úteis para você! Os scripts estão prontos para uso, e você está à vontade para modificá-los conforme necessário. Se estas ferramentas melhorarem sua experiência com o Beeware, considere se inscrever no meu canal no YouTube: [youtube.com/@canalqb](https://youtube.com/@canalqb).

## Arquivos Disponíveis

- `1.package_and_multisign.py`
- `2.keystore_crt.py`
- `pepk.jar`

## 1. package_and_multisign.py

*Deixe este script na raiz do projeto, na mesma pasta que o `pyproject.toml`.*

Este script automatiza o processo de construção do seu aplicativo Android, oferecendo as seguintes funcionalidades:

- **Criação da Pasta de Build**: Gera a pasta `build` do Android na raiz do seu projeto utilizando o comando `briefcase build android`.
- **Painel Interativo**: Apresenta um menu com quatro opções, permitindo que você escolha quais funcionalidades ativar. Você também pode passar um argumento para o script, por exemplo: `python 1.package_and_multisign.py 1`, para automatizar o processo.

### Funcionalidades

- **Minificação de Código**: 
  - `minifyEnabled`: Reduz o tamanho do código e ofusca partes não utilizadas.
  
- **Eliminação de Recursos Não Utilizados**: 
  - `shrinkResources`: Remove recursos desnecessários, como imagens e layouts, contribuindo para a redução do tamanho do APK.
  
- **Nível de Símbolos de Depuração**: 
  - Adiciona a configuração `debugSymbolLevel` para evitar mensagens de erro no Google Play Console sobre a falta de símbolos de depuração. Você pode escolher entre:
    - `FULL`: Inclui nomes de funções, arquivos e números de linha.
    - `SYMBOL_TABLE`: Inclui apenas nomes de funções.

- **Sufixos para Nomes de Arquivo**: 
  O script gera arquivos com os seguintes sufixos:
  - `-mt`: `minifyEnabled` true
  - `-mf`: `minifyEnabled` false
  - `-st`: `shrinkResources` true
  - `-sf`: `shrinkResources` false

  Exemplos de nomes gerados:
  - `SeuArquivo-mt.st.0.0.1.aab`
  - `SeuArquivo-mf.sf.0.0.2.aab`

- **exporta o symbols para a pasta dist**
  - Descompacta o arquivo aab criado sem assinatura
  - Copia os arquivos symbol para o aab
  - Cria o arquivo com terminação **_symbol.aab**
 
### Versionamento

Os arquivos são salvos com nomes internos de versão:
- `'1'`: `new_version_code = "100"` | `new_version_name = "0.0.1"`
- `'2'`: `new_version_code = "200"` | `new_version_name = "0.0.2"`
- `'3'`: `new_version_code = "300"` | `new_version_name = "0.0.3"`
- `'4'`: `new_version_code = "400"` | `new_version_name = "0.0.4"`

## 2. keystore_crt.py

*Deixe este script na raiz do projeto, na mesma pasta que o `pyproject.toml`.*

Este script é mais simples e executa as seguintes tarefas:

- Cria sua keystore.
- Extrai o certificado da keystore criada.
- Importa o certificado extraído para o `cacerts`.
- Insere a keystore em seus arquivos `.aab`.
- Cria um arquivo `output.zip` para o Google Play Console.

### Funções Utilizadas no Script

**Lembre-se de usar o OpenJDK em vez do Oracle JDK:**
**xxxxxx é sua senha pessoa, minino de 6 caracteres**

- **Criação da keystore**: keytool -genkeypair -v -keystore "canalqb.keystore" -alias canalqb -keyalg RSA -keysize 2048 -validity 10000 -storepass xxxxxx -dname "CN=canalqb, OU=canalqb, O=canalqb, L=Sao Paulo, ST=Sao Paulo, C=BR"
- **Extração do certificado**: keytool -export -alias canalqb -keystore "canalqb.keystore" -file "canalqb_cert.crt" -storepass xxxxxx
- **Listagem da keystore no cacerts**: keytool -list -keystore "c:\Program Files\Java\jdk-23\lib\security\cacerts" -storepass xxxxxx -alias canalqb
- **Remoção do alias da keystore**: keytool -delete -alias canalqb -keystore "c:\Program Files\Java\jdk-23\lib\security\cacerts" -storepass xxxxxx 
- **Importação do certificado para o cacerts**: keytool -import -alias canalqb -file "canalqb_cert.crt" -keystore "c:\Program Files\Java\jdk-23\lib\security\cacerts" -storepass xxxxxx 
- **Assinatura do arquivo .aab**: jarsigner -verbose -sigalg SHA384withRSA -digestalg SHA-256 -keystore "C:\Users\34630737\Desktop\teste\canalqbpuzzle67\dist\canalqb.keystore" -storepass xxxxxx "CanalQb - Puzzle - 67-mt.st.0.0.1.aab" canalqb  
- **Verificação da assinatura**: jarsigner -verify -verbose -certs "CanalQb - Puzzle - 67-mt.st.0.0.1.aab"
- **Criação do output.zip**: java -jar pepk.jar --keystore=canalqb.keystore --alias=canalqb --output=output.zip --include-cert --rsa-aes-encryption --encryption-key-path=encryption_public_key.pem


## pepk.jar

*Deixe este arquivo na pasta `dist`.*
Este é o arquivo fornecido pelo Google Play Console, extraído em novembro. Caso ocorra algum erro, pode ser necessário utilizar a versão diretamente do Google Play Console.


github: [canalqb] 


patreon: [canalqb]


opencollective: [canalqb]


paypal: [qrodrigob@gmail.com]


