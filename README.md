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