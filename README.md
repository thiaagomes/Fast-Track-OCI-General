# 🚀 OCI Fast Track Hands-On
Este repositório contém um Lab prático de OCI, criado para demonstrar, de forma simples e progressiva, como provisionar uma arquitetura cloud com a fundação de inraestrutura, máquina virtual, banco de dados, storage, events service e functions. 

---

## 🎯 Objetivo

Ao final deste hands-on, você terá construído uma arquitetura funcional na OCI.

---

## 🛠️ Arquitetura Proposta
![alt text](image-1.png)



---

## ⚙️ Configuração

### 1. Oracle Cloud Infrastructure

1. Acesse [https://cloud.oracle.com/] e faça login
2. Acesse o canto superior direito "PROFILE" →  Identity Domain →  Compartments = "Create Compartment"
3. Criação de componentes de Redes: **Menu Principal → Networking →  Virtual Cloud Networks**
   - Actions: 'Start VCN Wizard'
   - Connection Type: 'Create VCN with Internet Connectivity'
   - Examples: VCN Name(vcn-fast-track), VCN IPv4 CIDR block(10.0.0.0/16), Public Subnet CIDR block(10.0.0.0/24), Private Subnet CIDR block(10.0.1.0/24)
4. Revisão e Criação VCN, Subnets, Route Table, Gateways e Security List

---
### 1.1 Máquina Virtual (VM)

1. Criação de Máquina Virtual: **Menu Principal → Compute → Instances**
   - Create Instance
   - Examples: instance-fast-track, Image And Shape (Flex), Networking(VCN e Subnet criadas no passo anterior), Add SSH keys (Generate a key pair for me) and Download private key & public key
   - Storage (Nesse Lab não é necessário criar Block volumes)
   - Review e Create
2. O acesso a VM será feito via **Canto Superior Direito ao Lado da Region → Developer Tools → Cloud Shell**
 - Com o Cloud Shell aberto, selecionar ícone de engrenagem "Cloud Shell Menu" e fazer o UPLOAD das duas chaves ssh(private e public)
 - Conferir se as chaves ssh estão aparecendo "ls -la"
 - Rodar comando "chmod 600 ~/{chave-privada.key}" Exemplo : chmod 600 ~/ssh-key-fast-track-private.key
 - Acesso VM, rode o comando ssh -i ~/{chave-privada.key} opc@<PUBLIC_IP_VM> Exemplo: ssh -i ~/ssh-key-fast-track-private.key opc@147.15.25.7
 - Atualize a VM com o comando : sudo dnf update -y
 - Instale os pacotes básicos : sudo dnf install -y git wget curl unzip vim nano jq tar firewalld python3 python3-pip python3-devel gcc mysql-server
 - Execute os comandos para liberação de algumas regras : 
   - sudo systemctl enable --now mysqld
   - sudo systemctl enable --now firewalld
   - sudo firewall-cmd --permanent --add-port=5000/tcp
   - sudo firewall-cmd --reload
- Valide se deu certo, executando os seguintes comandos :
   - sudo systemctl status mysqld
   - sudo systemctl status firewalld
   - sudo firewall-cmd --list-ports (O esperado nesse comando é 5000/tcp)

---
### 1.2 Object Storage (Bucket)
1. Criação de Object Storage **Menu Principal → Storage → Object Storage & Archive Storage → Bucket**
   - Create Bucket
   - Examples: Bucket Name (bucket-fast-track), Default Storage Tier (Standard), Create

---
### 1.3 MySQL(Database)
1. Criação do database MySQL **Menu Principal → Databases → MySQL HeatWave → DB systems**
   - Create DB system
   - Examples : Db Name (mysql-fast-track), Template (Development or testing), Create administrator credentials (salve as credenciais), Setup (Standalone)

---
### 1.4 Functions
Antes de criarmos a functions, será preciso gerar um Auth Token e Montar o comando de Login no OCIR

1. Geração Auth Token para login no OCIR 
Antes de fazer o deploy da Function, precisamos autenticar o Docker no OCIR, que é o Oracle Cloud Infrastructure Registry.

Criação Auth Token
![alt text](image.png)

- My profile → Tokens and keys
- Auth tokens → Generate token (Copie o token gerado e salve temporariamente, porque ele será exibido apenas uma vez)

Importante: esse token será usado como senha no docker login. Não use a senha da Console OCI.

2. Montar o comando de login no OCIR
O formato do login é: 

docker login -u '<NAMESPACE>/<IDENTITY_DOMAIN>/<USUARIO>' <REGION_KEY>.ocir.io

por exemplo: docker login -u 'idi1o0a010nx/OracleIdentityCloudService/thiago.gomes@oracle.com' gru.ocir.io

Para pegar os dados e montar url: 
![alt text](image-2.png)

- Governance & Administration → Account Management → Tenancy Details → Object storage namespace
- Profile → Identity & Security → Identity → Domains
- Para region seguir essa doc → https://docs.oracle.com/pt-br/iaas/Content/Registry/Concepts/registryprerequisites.htm?
   - Exemplo: gru.ocir.io, vcp.ocir.io e etc 

---
Após montar url e gravar token, vamos seguir o passo a passo abaixo:

3. Criação da Functions **Menu Principal → Developer Services → Functions → Applications **
   - Create application
   - Examples : Name(functions-fast-track), Compartment & VCN & Subnet(Public), Shape GENERIC_ARM
   - Selecionar Functions e Create in code editor

Após abrir o code editor, no terminal valide algumas ferramentas:
   - fn --version
   - docker --version
   - oci --version

Fazer Login no OCIR
   - docker login -u 'idi1o0a010nx/OracleIdentityCloudService/thiago.gomes@oracle.com' sa-saopaulo-1.ocir.io
   - Token 
   - retorno esperado ![alt text](image-3.png)
   - Crie uma pasta limpa para a Function : mkdir -p ~/oci-fast-track-functions
      - cd ~/oci-fast-track-functions
   - Crie a Functions: fn init --runtime python functions1-fast-track
   - Entre na pasta da Functions: cd functions1-fast-track
   - Liste os arquivos: ls -la
      - Retorno esperado: func.py, func.yaml, requirements.txt
   - Liste os contextos existentes: fn list context
      - crie o contexto da região, caso ainda não exista: fn create context sa-saopaulo-1 --provider oracle
      - use o contexto: fn use context sa-saopaulo-1
   - Atualizar o registry: fn update context registry sa-saopaulo-1.ocir.io/idi1o0a010nx/functions-fast-track
      - Confira se atualizou: ![alt text](image.png)
      - Valide o contexto completo: fn inspect context (veja se já existe o campo:oracle.compartment-id)
         - Se não estiver, rode : fn update context oracle.compartment-id <OCID_DO_COMPARTMENT>
   - Realize o Login novamente: docker login -u 'idi1o0a010nx/OracleIdentityCloudService/thiago.gomes@oracle.com' sa-saopaulo-1.ocir.io
   - Confirme o nome da Function no func.yaml : cat func.yaml
   - Agora rode o deploy usando o nome exato da sua Application: fn -v deploy --app functions-fast-track
      - ![alt text](image.png)
      - Valide : fn list functions functions-fast-track
   - Teste a function: fn invoke <NOME_DA_APPLICATION> <NOME_DA_FUNCTION>, por exemplo : fn invoke functions-fast-track functions1-fast-track
      - ![alt text](image.png)

---
### 1.5 Validação Conectividade da VM com o MySQL
Como a VM será usada para fazer o SELECT e expor uma página via browser, ela precisa conseguir se conectar ao MySQL