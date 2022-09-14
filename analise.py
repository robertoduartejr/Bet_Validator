
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support import expected_conditions as EC, wait

jogos_validos = []
times = []
lista_proibidos = ["ARGÉLIA","ARGENTINA","ALBÂNIA","BIELORÚSSIA","GRÉCIA","ISRAEL","IRÃ","MARROCOS","RÚSSIA","TAILÂNDIA","ARGELIA","ALBANIA","BIELORUSSIA","GRECIA","IRA","RUSSIA","TAILANDIA","MÉXICO"]
driver = webdriver.Chrome()
erro =""

driver.get("https://www.flashscore.com.br/jogo/Chq9qZeo/#/h2h/overall")
time.sleep(5)



div_5games = driver.find_element(By.XPATH, '/html/body/div[1]')
html_content = div_5games.get_attribute('outerHTML')
soup = BeautifulSoup(html_content,'html.parser')

print(soup.prettify())
resultados = soup.find_all('div',class_='h2h__row')
print(len(resultados))
resultado_time1 = []
resultado_time2 = []
validator = [True, True, True]

for i in range(10):
    print(resultados[i].get_text())
    gol1 = resultados[i].get_text()[-2]
    gol2 = resultados[i].get_text()[-3]
    print(gol1, gol2)
    if gol1 == "0" and gol2 == "0":
        validator[0] = False
        break


times.append(driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[2]/div[3]/div[2]/a').text)
times.append(driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[4]/div[3]/div[1]/a').text)

#seguda validação
liga = driver.find_element(By.XPATH, '//*[@id="detail"]/div[4]/div/span[3]').text
for pais in lista_proibidos:
    if pais in liga:
        validator[1] = False
        break

if "COPA" in liga:
    validator[3] = False

if False in validator:
    print("não passou nas etapas")
    if validator[0] == False:
        print("Teve 0 a 0 em algum dos ultimos 5 jogos")
        erro = "0a0"
    if validator[1] == False:
        print("Liga proibida")
        erro = erro+" "+"Liga proibida"
    if validator[2] == False:
        print("Competição é copa")
        erro = erro + " " + "É Copa"
    jogos_validos.append([times[0], times[1], liga, False, erro])
else:
    jogos_validos.append([times[0],times[1],liga, True, "Passou"])
    pass #colocar aqui que é um jogo valido no excel, os nomes do time, competição

print(jogos_validos)


# //*[@id="detail"]/div[8]/div[2]/div[1]/div[2]/div[1]
# //*[@id="detail"]/div[8]/div[2]/div[1]/div[2]/div[2]
# //*[@id="detail"]/div[8]/div[2]/div[1]/div[2]/div[3]
# //*[@id="detail"]/div[8]/div[2]/div[1]/div[2]/div[5]
# //*[@id="detail"]/div[8]/div[2]/div[2]/div[2]/div[1]
# //*[@id="detail"]/div[8]/div[2]/div[2]/div[2]/div[5]