import requests
from bs4 import BeautifulSoup
import re

def extrairTexto(link, headers):
    requisicao = requests.get(link, headers=headers)
    print(requisicao)

    textoRetorno = ""
    #cotacao_dolar = site.find("p", class_="SwHCTb")
    #print(cotacao_dolar.get_text())
    #print(cotacao_dolar["data-value"])

    # Verificando se a requisição foi bem-sucedida
    if requisicao.status_code == 200:
        site = BeautifulSoup(requisicao.text, "html.parser")

        # Filtrando os parágrafos que não possuem a tag <strike> dentro deles
        paragrafos_filtrados = []

        for p in site.find_all("p"):
            if not p.find("strike"):
                paragrafos_filtrados.append(p)
        
        for texto in paragrafos_filtrados:
            paragrafo = texto.get_text()
            texto_limpo = re.sub(r'\s+', ' ', paragrafo.replace("\n", " ")).strip()
            if texto_limpo and "(VETADO)" not in texto_limpo:
                textoRetorno += "\n"+texto_limpo
        
    else:
        print(f"Erro ao acessar a página. Código de status: {requisicao.status_code}")
    
    return textoRetorno

def extrairLinks(link, headers, tipoExtracao):
    '''
        Método retorna um array com os diferentes links encontrados, não retorna links repetidos.

        tipos de extração:
        1 - qualquer <a> presente na página
        2 - os <a> dentro de listas <li>, considerando apenas as <li> mais internas. (Usado no código de normas)
    '''

    requisicao = requests.get(link, headers=headers)
    print(requisicao)

    linksRetorno = []

    # Verificando se a requisição foi bem-sucedida
    if requisicao.status_code == 200:
        site = BeautifulSoup(requisicao.text, "html.parser")

        if tipoExtracao == 1: 
            # Extraindo os links da página
            links = site.find_all("a")
            for link in links:
                try:
                    linksRetorno.append(link["href"])
                except KeyError:
                    pass  # Ignora links sem o atributo 'href'
        
        elif tipoExtracao == 2:
            # Extraindo os links da página

            for li in site.find_all("li"):
                if not li.find("li") and not li.find("ul"):
                    #print(li)
                    link = li.find("a", href=True)
                    if link and "http" in link["href"]:
                        linksRetorno.append(link["href"])

    else:
        print(f"Erro ao acessar a página. Código de status: {requisicao.status_code}")

    return linksRetorno

if __name__ == "__main__":
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"}

    link_lei_9492_protestos = "https://www.planalto.gov.br/ccivil_03/leis/l9492.htm"
    link_codigo_normas = "https://www.tjsc.jus.br/web/codigo-de-normas/indice"
    link_lei_8935_cartorios = "https://www.planalto.gov.br/ccivil_03/leis/l8935.htm"

    #print(extrairTexto(link, headers, False))
    print(extrairLinks(link, headers, 2))