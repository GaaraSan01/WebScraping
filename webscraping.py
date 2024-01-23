from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import time

# 1. Pegar o conteúdo HTML a partir da URL
url = 'https://thehustle.co/'

option = Options()
option.headless = True
driver = webdriver.Chrome(options=option)
driver.get(url)
driver.implicitly_wait(10)

lista_de_posts = []

link_blog = driver.find_elements(By.XPATH, '//h3[@class="blog-post-card-title"]')

for i, post_link in enumerate(link_blog):
    # Localiza novamente o elemento para evitar StaleElementReferenceException
    link_blog = driver.find_elements(By.XPATH, '//h3[@class="blog-post-card-title"]')
    
    # Clica no link específico
    link_blog[i].click()
    
    # Espera um pouco para garantir que a página seja carregada completamente
    time.sleep(2)

    content_titulo = driver.find_element(By.XPATH, '//h1[@class="blog-hustle-header-title"]')
    content_subtitulo = driver.find_element(By.XPATH, '//h2[@class="blog-hustle-header-subtitle"]')
    content_texto = driver.find_element(By.XPATH, '//span[@class="hs_cos_wrapper hs_cos_wrapper_meta_field hs_cos_wrapper_type_rich_text"]')

    html_content_texto = content_texto.get_attribute('outerHTML')
    
    soup = BeautifulSoup(html_content_texto, 'html.parser')
    posts = soup.find_all('p')
    image_post = soup.find_all('img')

    textos = [texto.get_text(strip=True) for texto in posts]
    imagens = [img['src'] for img in image_post]

    # 4. Transformar os Dados em um dicionário de dados próprio

    dados_dict = {
        "Titulo": content_titulo.text.strip(),
        "Subtitulo": content_subtitulo.text.strip(),
        "Imagens": imagens,
        "Textos": textos
    }

    lista_de_posts.append(dados_dict)

    # Volta para a página inicial
    driver.get(url)
    driver.implicitly_wait(10)

# Salva a lista de posts em um arquivo JSON
with open('posts.json', 'w', encoding='utf-8') as file:
    json.dump(lista_de_posts, file, ensure_ascii=False, indent=2)

txt_filename = "posts.txt"

with open(txt_filename, 'w', encoding='utf-8') as txt_file:
    
    for post in lista_de_posts:
        txt_file.write(f'Título: {post["Titulo"]}\n')
        txt_file.write(f'Subtítulo: {post["Subtitulo"]}\n')

        txt_file.write('Textos:\n')
        for texto in post["Textos"]:
            txt_file.write(f'  - {texto}\n')

        txt_file.write('\n' + '-'*50 + '\n')

driver.quit()
