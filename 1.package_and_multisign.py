import zipfile
import re
import os
import time
import subprocess
import shutil
import glob
import sys 

try:
    command = "taskkill /IM java.exe /F"
    subprocess.run(command, check=True, shell=True)
except:
    pass
    
# Função para renomear o arquivo
def rename_file(option):
    # Caminho da pasta dist
    dist_path = 'dist'
    # Padrão para encontrar o arquivo
    file_pattern = os.path.join(dist_path, '*-0.0.1.aab')

    # Busca o arquivo original
    original_files = glob.glob(file_pattern)
    
    if not original_files:
        print("Arquivo original não encontrado!")
        return

    # Pega o nome do primeiro arquivo encontrado
    original_file_path = original_files[0]

    # Define o novo nome do arquivo com base na opção
    if option == '1':
        new_file_name = original_file_path.replace('-0.0.1.aab', '-mt.st.0.0.1.aab')
    elif option == '2':
        new_file_name = original_file_path.replace('-0.0.1.aab', '-mf.sf.0.0.2.aab')
    elif option == '3':
        new_file_name = original_file_path.replace('-0.0.1.aab', '-mt.sf.0.0.3.aab')
    elif option == '4':
        new_file_name = original_file_path.replace('-0.0.1.aab', '-mf.st.0.0.4.aab')
    else:
        print("Opção inválida!")
        return
    
    # Verifica se o novo nome já existe e incrementa o sufixo se necessário
    counter = 1
    base_name, ext = os.path.splitext(new_file_name)
    
    while os.path.exists(new_file_name):
        new_file_name = f"{base_name}-{counter}{ext}"
        counter += 1

    # Renomeia o arquivo
    os.rename(original_file_path, new_file_name)
    print(f"Arquivo renomeado para: {os.path.basename(new_file_name)}")  
    return new_file_name
    



# Função para esperar até o arquivo ser criado
def wait_for_file(file_path):
    while not os.path.exists(file_path):
        print(f"Aguardando a criação do arquivo: {file_path}...")
        caminho_atual = os.getcwd()

        # Extrai o nome da pasta
        nome_pasta = os.path.basename(caminho_atual)

        # Imprime o nome da pasta
        print(nome_pasta)
        time.sleep(1)  # Espera 1 segundo antes de verificar novamente
        
if os.path.exists('build'):
    # Remove a pasta e todo seu conteúdo
    shutil.rmtree('build')
subprocess.run(["briefcase", "build", "android"], check=True)

# Caminho do seu arquivo build.gradle
app_build = os.path.basename(os.getcwd())
file_path = rf'build\{app_build}\android\gradle\app\build.gradle'

wait_for_file(file_path)


# Função para executar o briefcase build android
def execute_briefcase_build():
    print("Executando briefcase build android...")
    print("Briefcase build concluído.")

# Espera até que o arquivo exista

# Lê o conteúdo do arquivo
with open(file_path, 'r') as file:
    content = file.read()

def apply_default_config(option, content):
    # Expressão regular para encontrar a seção defaultConfig
    pattern = r'(defaultConfig\s*\{)(.*?)(\})'
    
    def replacement_func(match):
        default_config_header = match.group(1)
        default_config_footer = match.group(3)

        if option == '1':
            new_version_code = "100"
            new_version_name = "\"0.0.1\""
        elif option == '2':
            new_version_code = "200"
            new_version_name = "\"0.0.2\""
        elif option == '3':
            new_version_code = "300"
            new_version_name = "\"0.0.3\""
        elif option == '4':
            new_version_code = "400"
            new_version_name = "\"0.0.4\""
        else:
            return match.group(0)  # Retorna o original se a opção não for válida
        
        inner_content = match.group(2)
        updated_content = re.sub(r'versionCode \d+', f'versionCode {new_version_code}', inner_content)
        updated_content = re.sub(r'versionName ".*?"', f'versionName {new_version_name}', updated_content)

        return f"{default_config_header}{updated_content}{default_config_footer}"

    new_content = re.sub(pattern, replacement_func, content, flags=re.DOTALL)
    return new_content

def apply_build_option(option, content):
    # Expressão regular para encontrar a seção buildTypes
    pattern = r'(buildTypes\s*\{)(.*?)(\s*\})'  # Captura o fechamento correto

    def replacement_func(match):
        build_types_header = match.group(1)
        build_types_footer = match.group(3)

        # Define a nova configuração com base na opção
        if option == '1':
            new_release = (
                "\n\t\trelease {\n"  # Note que aqui não é uma f-string
                "\t\t\tminifyEnabled true\n"
                "\t\t\tshrinkResources true\n"
                "\t\t\tproguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'\n"
                "\t\t\tndk {\n"
                "\t\t\t\tdebugSymbolLevel = \"FULL\" // ou \"SYMBOL_TABLE\", dependendo da sua necessidade\n"
                "\t\t\t}\n"  # Fechamento do bloco ndk
                "\t\t}\n"  # Fechamento do bloco release
            )
        elif option == '2':
            new_release = (
                f"\n\t\trelease {{\n"
                f"\t\t\tminifyEnabled false\n"
                f"\t\t\tshrinkResources false\n"
                "\t\t\tndk {\n"
                "\t\t\t\tdebugSymbolLevel = \"FULL\" // ou \"SYMBOL_TABLE\", dependendo da sua necessidade\n"
                "\t\t\t}\n"  # Fechamento do bloco ndk
                "\t\t}\n"  # Fechamento do bloco release
            )
        elif option == '3':
            new_release = (
                f"\n\t\trelease {{\n"
                f"\t\t\tminifyEnabled true\n"
                f"\t\t\tshrinkResources false\n"
                f"\t\t\tproguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'\n"
                "\t\t\tndk {\n"
                "\t\t\t\tdebugSymbolLevel = \"FULL\" // ou \"SYMBOL_TABLE\", dependendo da sua necessidade\n"
                "\t\t\t}\n"  # Fechamento do bloco ndk
                "\t\t}\n"  # Fechamento do bloco release
            )
        elif option == '4':
            new_release = (
                f"\n\t\trelease {{\n"
                f"\t\t\tminifyEnabled false\n"
                f"\t\t\tshrinkResources true\n"
                "\t\t\tndk {\n"
                "\t\t\t\tdebugSymbolLevel = \"FULL\" // ou \"SYMBOL_TABLE\", dependendo da sua necessidade\n"
                "\t\t\t}\n"  # Fechamento do bloco ndk
                "\t\t}\n"  # Fechamento do bloco release
            )
        
        # Retorna a nova configuração sem duplicar chaves
        return f"{build_types_header}{new_release}"

    # Aplica a substituição, garantindo que o fechamento da seção seja mantido corretamente
    new_content = re.sub(pattern, replacement_func, content, flags=re.DOTALL)

    return new_content

# Pergunta ao usuário qual configuração ele deseja usar 
print("Escolha uma opção:")
print("1: Maxima Compactação - release")
print("2: Mantem formato Original - release")
print("3: Compactação Moderada com minificação - release")
print("4: Compactação Moderada com redução de recursos - release")
print("\n") 
print("Descrição de Itens") 
print("1: Ativa a minificação e a redução de recursos, usando ProGuard para ofuscação.")
print("2: Desativa a minificação e a redução de recursos, mantendo tudo como está.")
print("3: Ativa a minificação, mas desativa a redução de recursos.")
print("4: Desativa a minificação, mas ativa a redução de recursos.")
print("\n")

# Explicações adicionais
print("Minificação: É o processo de remover partes desnecessárias do código fonte, como espaços em branco, comentários.")
print("Redução de Recursos: É o processo de identificar e remover recursos não utilizados (imagens, layouts, etc.) do APK")


if len(sys.argv) > 1:
    # Usa o argumento passado como opção
    opcao = sys.argv[1]
else:
    # Caso contrário, pede ao usuário para inserir uma opção
    opcao = input("Digite o número da opção escolhida: ")

# Verifica se a opção é válida
if opcao in ['1', '2', '3', '4']:
    # Aplica a opção escolhida para defaultConfig
    new_content1 = apply_default_config(opcao, content)
    
    # Aplica a opção escolhida para buildTypes
    final_content = apply_build_option(opcao, new_content1)

    # Escreve o conteúdo final no arquivo
    with open(file_path, 'w') as file:
        file.write(final_content)

    print("Alteração concluída com sucesso.")
else:
    print("Opção inválida.")


codigo_log = """
    afterEvaluate { 
        logger.lifecycle("Configuração do projeto: ${project.name}")
        logger.lifecycle("SDK de compilação: ${compileSdkVersion}")
        logger.lifecycle("Versão do aplicativo: ${defaultConfig.versionName} (Código: ${defaultConfig.versionCode})")
        
        // Ajuste para minSdkVersion e targetSdkVersion (usando `getApiLevel`)
        logger.lifecycle("Min SDK: ${defaultConfig.minSdkVersion.getApiLevel()}, Target SDK: ${defaultConfig.targetSdkVersion.getApiLevel()}")
        
        // Mensagens de diferentes níveis
        logger.info("Processo de build iniciado.")
        logger.warn("Certifique-se de que a versão do Gradle está atualizada.")
        
        // Verificação do NDK (agora acessando corretamente a configuração do Android)
        if (!android.hasProperty('ndkVersion') || android.ndkVersion == null) {
            logger.error("Erro: Não foi possível configurar o NDK corretamente. Verifique a versão do NDK no projeto.")
        } else {
            logger.lifecycle("NDK configurado corretamente: ${android.ndkVersion}")
        }
        
        // Usando debug e trace
        logger.debug("Detalhes do build: ${project.allprojects}")
        logger.trace("Rastreamento completo das dependências do projeto.")
    }
"""


def add_ndk_version_to_gradle(file_path):
    # Ler o conteúdo do arquivo build.gradle
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Criar uma nova lista para armazenar as linhas modificadas
    new_lines = []
    for line in lines:
        new_lines.append(line)
        # Verificar se a linha contém compileSdkVersion 34
        if 'compileSdkVersion 34' in line:
            new_lines.append('    ndkVersion "27.0.12077973"\n')  # Adicionar a linha do NDK

    # Escrever as linhas modificadas de volta ao arquivo
    with open(file_path, 'w') as file:
        file.writelines(new_lines)
        
def insert_after_source_sets_code(file_path, code_to_insert):
    # Ler o conteúdo do arquivo
    with open(file_path, 'r') as file:
        content = file.read()

    if "afterEvaluate" in content:
        print("O bloco afterEvaluate já existe. Nenhuma alteração foi feita.")
        return
    # Padrão para encontrar o fechamento do bloco sourceSets
    pattern = r'(sourceSets\s*\{.*?})(\s*})'  # Captura o bloco sourceSets e sua chave de fechamento
    new_content_log = re.sub(pattern, r'\1\2\n\n' + code_to_insert, content, flags=re.DOTALL)

    # Gravar as alterações de volta no arquivo
    with open(file_path, 'w') as file:
        file.write(new_content_log)

    print("Código inserido com sucesso.")

# Chamar a função para inserir o código
add_ndk_version_to_gradle(file_path)
insert_after_source_sets_code(file_path, codigo_log)
 
file_path_gradle_properties = rf'build\{app_build}\android\gradle\gradle.properties'

# Linha a ser adicionada no arquivo gradle.properties 
line_to_add = "android.ndkHome=d:\\ndk\\android-ndk-r27"

# Verificando se o arquivo existe 
if os.path.exists(file_path_gradle_properties):
    # Abrindo o arquivo para leitura e escrita (modo r+)
    with open(file_path_gradle_properties, 'r+') as file:
        # Lendo o conteúdo do arquivo
        content = file.read()
        
        # Checando se a linha já existe no conteúdo do arquivo
        if line_to_add not in content:
            # Posiciona o ponteiro de volta para o final do arquivo e escreve a linha
            file.seek(0, os.SEEK_END)  # Garante que estamos no final do arquivo
            file.write(f"\n{line_to_add}\n")
            print(f"Adicionada a linha: {line_to_add}")
        else:
            print("A linha já existe no arquivo.")
else:
    print(f"O arquivo {file_path_gradle_properties} não existe.")


# Após a modificação do arquivo, execute briefcase package android
print("Executando briefcase package android...")
subprocess.run(["briefcase", "package", "android"], check=True)
print("Empacotamento concluído.")

#nome_final_do_arquivo = os.path.basename(rename_file(opcao))
nome_final_do_arquivo = rename_file(opcao)

# Caminho de origem (ajuste conforme necessário) 
origem_simbolos = os.path.join('build', app_build, 'android', 'gradle', 'app', 'build', 'intermediates', 'merged_native_libs', 'release', 'out', 'lib')
if opcao == '1':
    nomepasta = '-mt.st.0.0.1.aab'
elif opcao == '2':
    nomepasta = '-mf.sf.0.0.2.aab'
elif opcao == '3':
    nomepasta = '-mt.sf.0.0.3.aab'
elif opcao == '4':
    nomepasta = '-mf.st.0.0.4.aab'
# Caminho de destino
destino_simbolos = os.path.join('dist', f'simbolos{nomepasta}')

# Função para copiar arquivos e pastas
def copy_files(src, dest):
    try:
        # Verifica se o diretório de origem existe
        if not os.path.exists(src):
            print(f"Diretório de origem não encontrado: {src}")
            return
        
        # Cria o diretório de destino, se não existir
        if not os.path.exists(dest):
            os.makedirs(dest)
            print(f"Criando diretório: {dest}")
        
        # Copia os arquivos e subdiretórios recursivamente
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dest, item)
            if os.path.isdir(s):
                # Se for um diretório, copia recursivamente
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                # Se for um arquivo, copia normalmente
                shutil.copy2(s, d)
        
        print(f"Arquivos copiados de {src} para {dest} com sucesso.")
    
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Chama a função para copiar os arquivos
copy_files(origem_simbolos, destino_simbolos)

#------------------------------------------------------------------------
print(f'Descomprimindo {os.path.basename(nome_final_do_arquivo)}')
 
# Caminho do arquivo ZIP e destino da extração
arquivo_zip = nome_final_do_arquivo

# Definir o diretório de destino (criando um diretório específico para extração)
diretorio_destino = os.path.splitext(arquivo_zip)[0]  # Remove a extensão .aab para usar como pasta

# Verificar se o diretório de destino existe, se não, criar
if not os.path.exists(diretorio_destino):
    os.makedirs(diretorio_destino)

# Abrir o arquivo ZIP
with zipfile.ZipFile(arquivo_zip, 'r') as zip_ref:
    # Extrair todos os arquivos para o diretório de destino
    zip_ref.extractall(diretorio_destino)

print(f'Arquivo {arquivo_zip} descompactado com sucesso em {diretorio_destino}')

#------------------------------------------------------------------------
print('Transferindo symbols')
 

# Definir o novo diretório para onde os arquivos serão copiados
diretorio_destino = os.path.join(os.path.splitext(arquivo_zip)[0], 'BUNDLE-METADATA', 'com.android.tools.build.debugsymbols')

# Criar o diretório com.android.tools.build.debugsymbols, se não existir
if not os.path.exists(diretorio_destino):
    os.makedirs(diretorio_destino)
    print(f'Diretório criado: {diretorio_destino}')

# Verificar se o diretório de origem existe
if os.path.exists(destino_simbolos):
    # Copiar todo o conteúdo do diretório de origem para o novo diretório
    for item in os.listdir(destino_simbolos):
        origem_item = os.path.join(destino_simbolos, item)
        destino_item = os.path.join(diretorio_destino, item)
        
        if os.path.isdir(origem_item):
            # Se for um diretório, copiamos recursivamente
            shutil.copytree(origem_item, destino_item)
            print(f'Pasta copiada: {origem_item} para {destino_item}')
        else:
            # Se for um arquivo, copiamos diretamente
            shutil.copy2(origem_item, destino_item)
            print(f'Arquivo copiado: {origem_item} para {destino_item}')
else:
    print(f'Erro: O diretório de origem não existe: {destino_simbolos}')

#------------------------------------------------------------------------ 
# Diretório que você deseja compactar
diretorio_para_compactar = os.path.splitext(nome_final_do_arquivo)[0]  # Remove a extensão .aab para usar o nome da pasta

# Definindo o nome da pasta corretamente
nome_da_pasta = os.path.basename(diretorio_para_compactar)  # Extrai o nome da pasta

# Construir o nome do arquivo .abb, combinando o nome da pasta e 'symbol' (exemplo: symbolCanalQb - Puzzle.abb)
arquivo_abb = os.path.join(os.path.dirname(diretorio_para_compactar), f'{nome_da_pasta}_symbol.aab')

# Verifique se o diretório existe
if os.path.exists(diretorio_para_compactar):
    # Compactar o diretório em formato .zip temporariamente
    shutil.make_archive(diretorio_para_compactar, 'zip', diretorio_para_compactar)
    
    # Renomear o arquivo .zip para .abb com o nome correto
    if os.path.exists(f'{diretorio_para_compactar}.zip'):
        os.rename(f'{diretorio_para_compactar}.zip', arquivo_abb)
        print(f'Diretório {diretorio_para_compactar} compactado e salvo com sucesso como {arquivo_abb}')
        
        # Deletar o diretório após a compactação
        shutil.rmtree(diretorio_para_compactar)
        print(f'Diretório {diretorio_para_compactar} deletado com sucesso.')
    else:
        print('Erro ao criar o arquivo .zip.')
else:
    print(f'Erro: O diretório {diretorio_para_compactar} não existe.')
