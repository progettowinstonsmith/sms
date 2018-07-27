
1. Installare MINICONDA

ad es 

wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod a+x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh

premi return o yes a tutte le risposte
esci e rientra dall'utente

fai which python
e dovrebbe essere qualcosa come

/home/exedre/miniconda3/bin/python

altrimenti fai:

export PATH=~/miniconda3/bin:$PATH

2. Creare un environment per tnt

conda create -n tnt python pip mysql-connector-python

3. Attiva l'environment

source activate tnt



4. Estrai il progetto da github

git clone https://github.com/progettowinstonsmith/sms.git tnt-work

5. Crea i prerequisiti

cd tnt-work
pip install --upgrade pip
pip install -r requirement.txt

6. Attiva il package

flit instal -s

7. Scarica il db di tnt

wget ...

8. Crea il db per tnt

mysqladmin create tnt2 -uroot -ppassword

7. sposta lo script nella directory bin

    cp script/make_forum.sh ~/miniconda3/envs/tnt/bin
    
8. carica l'elenco degli utenti "buoni" nella dir ~/.tnt

mkdir ~/.tnt
wget ... ~/.tnt/good-users.map

9. spostati in una directory di lavoro estrai le tabelle di base

mkdir ../tnt-export
cd ../tnt-export

user_groups
categories

users 
user_groups
categories
foums

ognuna di questa genera un file sql che puoi importare in torrentpier









users 
groups
user_groups
categories

forums

messages

moderators

posts
releases
topics
