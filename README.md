# Projeto análise de logs
Projeto de análise de logs

## Sobre
Esse projeto está contido no nanodegree de FullStack Developer da Udacity, e diz respeito a um banco de dados de uma espécie de blog, com alguns artigos publicados e autores. Para a resolução do problema é necessário responder três perguntas que dizem respeito aos logs, aos artigos e aos autores. 

1) Quais são os três artigos mais populares de todos os tempos? 
2) Quem são os autores de artigos mais populares de todos os tempos? 
3) Em quais dias mais de 1% das requisições resultaram em erros? 

## Para rodar
- Python3
- Vagrant
- VirtualBox

## Para criar as Views utilizadas para consulta ao banco

a) Artigos mais populares
```sql
CREATE VIEW articles_top3 as 
 select articles.title, count(log.path) as views 
 from log join articles on replace(log.path,'/article/','')=articles.slug 
 where log.path<>'/' 
 group by articles.title 
 order by views desc limit 3;
```

b) Autores mais populares
```sql
CREATE VIEW popular_authors as 
 select authors.name, count(log.ip) as views
 from articles join authors 
 on articles.author=authors.id 
 join log on replace(log.path,'/article/','')=articles.slug 
 group by authors.name 
 order by views DESC;
 ``` 
c) Dias de requisição com porcentagem de erro maior que 1%
```sql
CREATE VIEW dia_maior_porc as
 select * from 
 (select erros.data as data, erros.err::decimal / ok.oks * 100 as porcentagem from
    (select date(log.time) as data, count(time) as
     err from log where status<>'200 OK' 
     group by date(time) 
     order by date(time) DESC) 
     as erros,
    (select date(log.time) as data, count(time) 
     as oks from log where status='200 OK' 
     group by date(time) 
     order by date(time) DESC) as ok

     where erros.data = ok.data
     order by porcentagem desc
 ) as consulta 
where porcentagem > 1;
```
