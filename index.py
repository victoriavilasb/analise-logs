#!/usr/bin/env python
import psycopg2

def popularArticles():
    cursor.execute("select * from articles_top3") 
    artigos = cursor.fetchall()
    for artigo in artigos: 
        print("%s - %s"%(artigo[0],artigo[1]))

def popularAuthors():
    cursor.execute("select * from popular_authors")
    authors = cursor.fetchall()
    for author in authors:
        print("%s - %s"%(author[0],author[1]))

def dayOfErrorRequest(): 
    cursor.execute("select * from dia_maior_porc")
    dias = cursor.fetchall()
    for dia in dias:
        print("%s - %s"%(dia[0],dia[1]))

def main():
    try: 
        conn = psycopg2.connect("dbname=news")
        global cursor 
        cursor = conn.cursor()

        print('-------- 3 artigos mais populares --------')
        popularArticles()
        print('\n')

        print('-------- Autores populares --------')
        popularAuthors()
        print('\n')

        print('-------- Mais requisicoes com erro --------')
        dayOfErrorRequest()

        conn.close()
    except psycopg2.Error as e:
        print('Nao foi possivel conectar com o banco de dados')
        
if __name__ == "__main__":
    main()



