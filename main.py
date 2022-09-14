
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support import expected_conditions as EC, wait



driver = webdriver.Chrome()

driver.get("https://www.flashscore.com.br/")
time.sleep(5)
tab_proximos_jogos = driver.find_element(By.XPATH, '//*[@id="live-table"]/div[1]/div[1]/div[5]')
tab_proximos_jogos.click()
time.sleep(2)


div_allgames = driver.find_element(By.XPATH, '//*[@id="fsbody"]')
html_content = div_allgames.get_attribute('outerHTML')
soup = BeautifulSoup(html_content,'html.parser')
jogos_validos = []

def game_analysis():
    jogos_validos = []
    times = []
    lista_proibidos = ["ARGÉLIA", "ARGENTINA", "ALBÂNIA", "BIELORÚSSIA", "GRÉCIA", "ISRAEL", "IRÃ", "MARROCOS",
                       "RÚSSIA", "TAILÂNDIA", "ARGELIA", "ALBANIA", "BIELORUSSIA", "GRECIA", "IRA", "RUSSIA",
                       "TAILANDIA", "MÉXICO","SUB-19","SUB-18","SUB-20","SUB-17","Sub-19","Sub-18","Sub-20","Sub-17"]
    erro = ""


    div_5games = driver.find_element(By.XPATH, '/html/body/div[1]')
    html_content = div_5games.get_attribute('outerHTML')
    soup = BeautifulSoup(html_content, 'html.parser')

    print(soup.prettify())
    resultados_game = soup.find_all('div', class_='h2h__row')
    print(len(resultados_game))

    validator = [True, True, True]

    for i in range(10):
        print(resultados_game[i].get_text())
        gol1 = resultados_game[i].get_text()[-2]
        gol2 = resultados_game[i].get_text()[-3]
        print(gol1, gol2)
        if gol1 == "0" and gol2 == "0":
            validator[0] = False
            break

    times.append(driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[2]/div[3]/div[2]/a').text)
    times.append(driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[4]/div[3]/div[1]/a').text)

    # seguda validação
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
            erro = erro + " " + "Liga proibida"
        if validator[2] == False:
            print("Competição é copa")
            erro = erro + " " + "É Copa"
        jogos_validos.append([times[0], times[1], liga, False, erro])
    else:
        jogos_validos.append([times[0], times[1], liga, True, "Passou"])
        pass  # colocar aqui que é um jogo valido no excel, os nomes do time, competição

    print(jogos_validos)
    return jogos_validos




#loop to open all game pages
allgames = soup.find_all('div',class_='event__match--scheduled')

original_window = driver.current_window_handle
assert len(driver.window_handles) == 1
for game in allgames:
    caminho = game.get('id')
    button = driver.find_element(By.XPATH, f'//*[@id="{caminho}"]')
    driver.execute_script("arguments[0].click();", button) #a different way I found to click without geteting an error

    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break
    try:
        button2 = driver.find_element(By.XPATH, '//*[@id="detail"]/div[6]/div/a[3]')
        driver.execute_script("arguments[0].click();", button2)
    except: #there's 2 different xpath for the same button. If not one is the another one.
        button2 = driver.find_element(By.XPATH, '//*[@id="detail"]/div[7]/div/a[3]')
        driver.execute_script("arguments[0].click();", button2)

    time.sleep(5)
    jogos_validos.append(game_analysis())
    time.sleep(10)

    driver.close() #closing new open page
    driver.switch_to.window(original_window)  #returning to the original page

for jogos in jogos_validos:
    print(jogos)
