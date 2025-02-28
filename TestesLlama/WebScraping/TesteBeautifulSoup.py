import requests
from bs4 import BeautifulSoup

link = "https://www.planalto.gov.br/ccivil_03/leis/l9492.htm"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"}

requisicao = requests.get(link, headers=headers)
site = BeautifulSoup(requisicao.text, "html.parser")

print(requisicao)

#cotacao_dolar = site.find("p", class_="SwHCTb")
#print(cotacao_dolar.get_text())
#print(cotacao_dolar["data-value"])


# Verificando se a requisição foi bem-sucedida
if requisicao.status_code == 200:
    site = BeautifulSoup(requisicao.text, "html.parser")
    
    # Extraindo os parágrafos da página
    conteudo = site.find_all("p")
    for texto in conteudo[:5]:  # Exibir apenas os 5 primeiros para não poluir o terminal
        print(texto.get_text(strip=True))
    
    print("\nLinks encontrados na página:")
    
    # Extraindo os links da página
    links = site.find_all("a")
    for link in links:
        try:
            print(link["href"])
        except KeyError:
            pass  # Ignora links sem o atributo 'href'
else:
    print(f"Erro ao acessar a página. Código de status: {requisicao.status_code}")
