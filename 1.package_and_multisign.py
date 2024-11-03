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

if os.path.exists('build'):
    # Remove a pasta e todo seu conteúdo
    shutil.rmtree('build')

# Função para esperar até o arquivo ser criado
def wait_for_file(file_path):
    while not os.path.exists(file_path):
        print(f"Aguardando a criação do arquivo: {file_path}...")
        time.sleep(1)  # Espera 1 segundo antes de verificar novamente

subprocess.run(["briefcase", "build", "android"], check=True)

# Caminho do seu arquivo build.gradle
file_path = r'build\canalqb\android\gradle\app\build.gradle'

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
                f"\n\t\trelease {{\n"
                f"\t\t\tminifyEnabled true\n"
                f"\t\t\tshrinkResources true\n"
                f"\t\t\tproguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'\n"
                f"\t\t}}"
            )
        elif option == '2':
            new_release = (
                f"\n\t\trelease {{\n"
                f"\t\t\tminifyEnabled false\n"
                f"\t\t\tshrinkResources false\n"
                f"\t\t}}"
            )
        elif option == '3':
            new_release = (
                f"\n\t\trelease {{\n"
                f"\t\t\tminifyEnabled true\n"
                f"\t\t\tshrinkResources false\n"
                f"\t\t\tproguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'\n"
                f"\t\t}}"
            )
        elif option == '4':
            new_release = (
                f"\n\t\trelease {{\n"
                f"\t\t\tminifyEnabled false\n"
                f"\t\t\tshrinkResources true\n"
                f"\t\t}}"
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
    # Exibe a opção escolhida
    print(f"Opção escolhida em linha b : {opcao}")
    print(type(opcao))
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

# Após a modificação do arquivo, execute briefcase package android
print("Executando briefcase package android...")
subprocess.run(["briefcase", "package", "android"], check=True)
print("Empacotamento concluído.")

rename_file(opcao)
