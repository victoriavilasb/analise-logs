# Projeto análise de logs
Projeto de análise de logs

## Sobre
Esse projeto está contido no nanodegree de FullStack Developer da Udacity, e diz respeito a um banco de dados de uma espécie de blog, com alguns artigos publicados e autores. Para a resolução do problema é necessário responder três perguntas que dizem respeito aos logs, aos artigos e aos autores. 

1) Quais são os três artigos mais populares de todos os tempos? 
2) Quem são os autores de artigos mais populares de todos os tempos? 
3) Em quais dias mais de 1% das requisições resultaram em erros? 

## Como instalar
- Python2: Acesse ao site oficial do python e faça download da versão 2.7, no seguinte link: https://www.python.org/download/releases/2.7/
- Vagrant: Faça download do vagrant no seguinte link: https://www.vagrantup.com/downloads.html
- VirtualBox: Faça download do virtual box no seguinte link: https://www.virtualbox.org/wiki/Downloads
- Banco de dados: Faça download do banco em questão no seguinte link: https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip


## Para rodar
- Python2
- Vagrant
- VirtualBox

Vá ao terminal, depois de instalar os programas acima, e rode as seguintes linhas de comando:
```
vagrant up
vagrant ssh
```

Em seguida, importe o banco de dados news com o seguinte comando:
```
psql -d news -f newsdata.sql
```
Em seguinte, arraste o database para dentro da sua pasta vagrant, e rode as views abaixo no banco de dados
```
psql news
```
## Para criar as Views utilizadas para consulta ao banco

a) Artigos mais populares
```sql
CREATE OR REPLACE VIEW articles_top3 as 
 select articles.title, count(log.path) as views 
 from log join articles on replace(log.path,'/article/','')=articles.slug 
 where log.path<>'/' 
 group by articles.title 
 order by views desc limit 3;
```

b) Autores mais populares
```sql
CREATE OR REPLACE VIEW popular_authors as 
 select authors.name, count(log.ip) as views
 from articles join authors 
 on articles.author=authors.id 
 join log on replace(log.path,'/article/','')=articles.slug 
 group by authors.name 
 order by views DESC;
 ``` 
c) Dias de requisição com porcentagem de erro maior que 1%
```sql
CREATE OR REPLACE VIEW dia_maior_porc as
 select * from 
 (select erros.data as data, erros.err::decimal / ok.oks * 100 as porcentagem from
    (select date(log.time) as data, count(time) as
     err from log where status!='200 OK' 
     group by date(time) 
     order by date(time) DESC) 
     as erros,
    (select date(log.time) as data, count(time) 
     as oks from log 
     group by date(time) 
     order by date(time) DESC) as ok

     where erros.data = ok.data
     order by porcentagem desc
 ) as consulta 
where porcentagem > 1;
```

Por ultimo, rode o código **index.py** com o seguinte comando:
```
python index.py
```
