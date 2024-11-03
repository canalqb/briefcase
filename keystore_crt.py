import os
import subprocess
import shutil
import time
import requests

# Função para executar comandos
def run_command(command):
    result = subprocess.run(command, shell=True, check=True, text=True)
    return result

# Limpar a tela
os.system('cls' if os.name == 'nt' else 'clear')
# Importa o certificado para o cacerts do Java
java_home = os.environ.get('JAVA_HOME') 
cacerts_path = os.path.join(java_home, 'lib', 'security', 'cacerts') 

# Solicitar informações do usuário
alias_keystore = input("Informe sua alias da keystore: ")
senha_keystore = input("Informe sua senha de keystore: ")
senha_key = input("Informe sua senha de key: ")

# Navegar para o diretório 'dist'
os.chdir('dist')

# Verifica se o diretório de backup existe, se não, cria
backup_dir = os.path.join('..', 'backup')
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

# Copia os arquivos .aab para o diretório de backup
for file in os.listdir('.'):
    if file.endswith('.aab'):
        shutil.copy(file, backup_dir)

# Delete existing keystore and certificate if they exist
for file in [f"{alias_keystore}.keystore", f"{alias_keystore}_cert.crt", "output.zip"]:
    if os.path.exists(file):
        os.remove(file)

# Gera um novo keystore e keypair
run_command(f'keytool -genkeypair -v -keystore "{alias_keystore}.keystore" -alias {alias_keystore} -keyalg RSA -keysize 2048 -validity 10000 -storepass {senha_keystore} -dname "CN={alias_keystore}, OU={alias_keystore}, O={alias_keystore}, L=Sao Paulo, ST=Sao Paulo, C=BR"')

# Exporta o certificado
run_command(f'keytool -export -alias {alias_keystore} -keystore "{alias_keystore}.keystore" -file "{alias_keystore}.crt" -storepass {senha_keystore}')

# Assina e verifica cada arquivo .aab
for file in os.listdir('.'):
    if file.endswith('.aab'):
        run_command(f'jarsigner -sigalg SHA384withRSA -digestalg SHA-256 -keystore "{alias_keystore}.keystore" -tsa http://timestamp.digicert.com "{file}" "{alias_keystore}" -storepass "{senha_keystore}"')
        run_command(f'jarsigner -verify  -certs "{file}"')



while True:
    if 'encryption_public_key.pem' in os.listdir('.'):
        pepk_url = "https://github.com/canalqb/briefcase/raw/refs/heads/main/pepk.jar"
        response = requests.get(pepk_url)
        with open('pepk.jar', 'wb') as file:
            file.write(response.content)
            
        # O arquivo existe, executa o comando
        run_command(f'java -jar "pepk.jar" --keystore="{alias_keystore}.keystore" --alias="{alias_keystore}" --output="output.zip" --include-cert --rsa-aes-encryption --encryption-key-path="encryption_public_key.pem" --keystore-pass="{senha_keystore}" --key-pass="{senha_key}"')
        print("Criado arquivo output.zip, envie para o Google Play Console, em 'Exportar e fazer upload de uma chave de um keystore Java\n'")
        print(f"Salve {alias_keystore}.keystore + {alias_keystore}.crt + alias e senha do senha_keystore e senha_key\nEm algum local seguro")

        break
    else:
        # O arquivo não existe, imprime a mensagem e aguarda 2 segundos
        print("Acesse o Google Play Console para baixar sua pem atual, entre em Exportar e fazer upload de uma chave de um keystore Java, e baixe eu .pem nesta pasta dist\n")
        print("Se este é sua segunda publicação, você pode usar a keystore original na opção 'Usar a mesma chave de outro app desta conta de desenvolvedor'")
        time.sleep(2)
