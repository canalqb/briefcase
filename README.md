# Python 3.8 + BeeWare + Toga - Upando Seus aplicativos no Google Play Console

Galera, se esse script ajudar você de alguma forma, não se esqueça de seguir o [youtube.com/@canalqb](https://youtube.com/@canalqb).
Sempre com uma novidade em Script e soluções de problemas para você.
Vá no canal, e comente uma duvida, estou disposto a solucionar.
Obrigado.

Video passo a passo:.
[![Em caso de dúvidas assista esse vídeo](https://www.youtube.com/img/desktop/yt_1200.png)](https://youtu.be/1Xh_d6cEXyc)


## Arquivos Disponíveis

- `1. R8/proguard e Symbol.py`  

## 1. R8/proguard e Symbol.py

*Deixe este script na raiz do projeto, na mesma pasta que o `pyproject.toml`.*

Como já sabemos o Google Console Play existe o SDK atualizado, no momento deste post, estamos falando do 34 (atualize no **pyproject.toml**)
Vamos ao Script.

Usando o **briefcase build android** vamos criar a pasta build, podemos fazer as modificações necessárias.
Usando o **briefcase package android** vamos criar o aab para postar no google play

Então usando o comando
O Script vai parar qualquer java.exe em execução, simplesmente encerrando o processo.
no seu Script ele vai deletar a pasta Build, para criar uma nova, toda vez.

`if os.path.exists('build'):`

`    #Remove a pasta e todo seu conteúdo`

`    shutil.rmtree('build')`

O script simplesmente irá tratar 2 arquivos
gradle\app\build.gradle e o gradle\gradle.properties

Modificações dos 2 arquivos:
- `Instalar o NDK 27`
- `Alterar versões de arquivo AAB para tornar mais facil a visualização.`
- `Criar e editar o minifyEnabled, shrinkResources para ser possivel realizar a ofuscação`
- `Incluir o debugSymbolLevel para ser possivel a extração dos Symbol do seu aplicativo.`
- `E criar alguns logs.`

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
- `'1': new_version_code = "100"` | `new_version_name = "0.0.1"`
- `'2': new_version_code = "200"` | `new_version_name = "0.0.2"`
- `'3': new_version_code = "300"` | `new_version_name = "0.0.3"`
- `'4': new_version_code = "400"` | `new_version_name = "0.0.4"`

Você vai precisar o NDK atualizado, procure em https://developer.android.com/ndk/downloads

Indico utilizar o OpenJava 17 que está configurado dentro do Beeware, para gerar as Keystore.

C:\\Users\\**{seuperfil}**\\AppData\\Local\\BeeWare\\briefcase\\Cache\\tools\\java17\\bin


Também devemos usar o android_sdk da mesma versão que o Google Play Console exige, neste momento é o 34, disponivel dentro do beeware.

C:\\Users\\**{seuperfil}**\\AppData\\Local\\BeeWare\\briefcase\\Cache\\tools\\android_sdk\\build-tools\\34.0.0'


Eu utilizei a versão 1.16 do bundletool: https://github.com/google/bundletool/releases/download/1.16.0/bundletool-all-1.16.0.jar
O arquivo pem e o pepk.jar, você precisa pegar no Google Play Console 

### Vamos aos comandos:

`keytool -genkeypair -v -keystore "alias.keystore" -alias "suaalias" -keyalg RSA -keysize 2048 -validity 10000 -storepass "xxxxxx" -dname "CN=canalqb, OU=canalqb, O=canalqb, L=Sao Paulo, ST=Sao Paulo, C=BR"`

`java -jar bundletool-all-1.16.0.jar validate --bundle "**arquivo.aab**"`

`apksigner sign --ks "**keystore**" --ks-pass pass:**senha_keystore** --min-sdk-version 34 "**arquivo.aab**"`

Após concluir a criação do seu .aab, vamos usar os comandos abaixo para certificar para o Google Play Store

`java -jar "pepk.jar" --keystore="**keystore**" --alias="**suaalias**" --output=output.zip --include-cert --rsa-aes-encryption --encryption-key-path="encryption_public_key.pem" --keystore-pass="xxxxxx"`



