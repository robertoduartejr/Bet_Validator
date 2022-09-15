
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from excelwriter import create_file
from selenium.webdriver.support import expected_conditions as EC, wait



driver = webdriver.Chrome()

driver.get("https://www.flashscore.com.br/")
time.sleep(0.5)
tab_proximos_jogos = driver.find_element(By.XPATH, '//*[@id="live-table"]/div[1]/div[1]/div[5]')
tab_proximos_jogos.click()
time.sleep(0.5)


div_allgames = driver.find_element(By.XPATH, '//*[@id="fsbody"]')
html_content = div_allgames.get_attribute('outerHTML')
soup = BeautifulSoup(html_content,'html.parser')
jogos_validos = []

def game_analysis():
    jogos_validos = []
    times = []
    lista_proibidos = ["ARGÉLIA", "ARGENTINA", "ALBÂNIA", "BIELORÚSSIA", "GRÉCIA", "ISRAEL", "IRÃ", "MARROCOS",
                       "RÚSSIA", "TAILÂNDIA", "ARGELIA", "ALBANIA", "BIELORUSSIA", "GRECIA", "IRA", "RUSSIA",
                       "TAILANDIA","SUB-19","SUB-18","SUB-20","SUB-17","Sub-19","Sub-18","Sub-20","Sub-17","Cup","cup","CUP","JUVENIL"]
    erro = ""


    div_5games = driver.find_element(By.XPATH, '/html/body/div[1]')
    html_content = div_5games.get_attribute('outerHTML')
    soup = BeautifulSoup(html_content, 'html.parser')

    #print(soup.prettify())
    resultados_game = soup.find_all('div', class_='h2h__row')
    #print(len(resultados_game))

    validator = [True, True, True]
    sum_of_goals = 0
    try:
        for i in range(10):
            #print(resultados_game[i].get_text())
            gol1 = resultados_game[i].get_text()[-2]
            gol2 = resultados_game[i].get_text()[-3]
            #print(gol1, gol2)
            sum_of_goals = sum_of_goals + int(gol1) + int(gol2)  # getting the sum of last fibe games
            if gol1 == "0" and gol2 == "0": #improved the method not to accept games with less than 2 goals in the last five games
                validator[0] = False
                break
    except:
        validator[0] = False


    times.append(driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[2]/div[3]/div[2]/a').text)
    times.append(driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[4]/div[3]/div[1]/a').text)

    # seguda validação
    liga = driver.find_element(By.XPATH, '//*[@id="detail"]/div[4]/div/span[3]').text
    for pais in lista_proibidos:
        if pais in liga:
            validator[1] = False
            break

    if "COPA" in liga:
        validator[2] = False

    if False in validator:
        #print("não passou nas etapas")
        if validator[0] == False:
            #print("Teve 0 a 0 em algum dos ultimos 5 jogos")
            erro = "0a0"
        if validator[1] == False:
            #print("Liga proibida")
            erro = erro + " " + "Liga proibida"
        if validator[2] == False:
            #print("Competição é copa")
            erro = erro + " " + "É Copa"
        jogos_validos = [times[0], times[1], liga, False, sum_of_goals, erro]
    else:
        jogos_validos = [times[0], times[1], liga, True,sum_of_goals, "Passou"]
        pass  # colocar aqui que é um jogo valido no excel, os nomes do time, competição

    return jogos_validos


def game_analysis_improved_max():
    jogos_validos = []
    times = []
    lista_proibidos = ["ARGÉLIA", "ARGENTINA", "ALBÂNIA", "BIELORÚSSIA", "GRÉCIA", "ISRAEL", "IRÃ", "MARROCOS",
                       "RÚSSIA", "TAILÂNDIA", "ARGELIA", "ALBANIA", "BIELORUSSIA", "GRECIA", "IRA", "RUSSIA",
                       "TAILANDIA","SUB-19","SUB-18","SUB-20","SUB-17","Sub-19","Sub-18","Sub-20","Sub-17","Cup","cup","CUP","JUVENIL"]
    erro = ""


    div_5games = driver.find_element(By.XPATH, '/html/body/div[1]')
    html_content = div_5games.get_attribute('outerHTML')
    soup = BeautifulSoup(html_content, 'html.parser')

    #print(soup.prettify())
    resultados_game = soup.find_all('div', class_='h2h__row')
    #print(len(resultados_game))

    validator = [True, True, True]
    sum_of_goals = 0
    try:
        for i in range(10):
            #print(resultados_game[i].get_text())
            #gol1 = resultados_game[i].get_text()[-2]
            #gol2 = resultados_game[i].get_text()[-3]
            #print(gol1, gol2)
            sum_of_goals = sum_of_goals + int(gol1) + int(gol2)  # getting the sum of last fibe games
            if (gol1 == "0" and gol2 == "0") or (gol1 == "1" and gol2 == "0") or (gol1 == "0" and gol2 == "1"): #improved the method not to accept games with less than 2 goals in the last five games
                validator[0] = False
                break
    except:
        validator[0] = False


    times.append(driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[2]/div[3]/div[2]/a').text)
    times.append(driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[4]/div[3]/div[1]/a').text)

    # seguda validação
    liga = driver.find_element(By.XPATH, '//*[@id="detail"]/div[4]/div/span[3]').text
    for pais in lista_proibidos:
        if pais in liga:
            validator[1] = False
            break

    if "COPA" in liga:
        validator[2] = False

    if False in validator:
        #print("não passou nas etapas")
        if validator[0] == False:
            #print("Teve 0 a 0 em algum dos ultimos 5 jogos")
            erro = "0a0"
        if validator[1] == False:
            #print("Liga proibida")
            erro = erro + " " + "Liga proibida"
        if validator[2] == False:
            #print("Competição é copa")
            erro = erro + " " + "É Copa"
        jogos_validos = [times[0], times[1], liga, False, sum_of_goals, erro]
    else:
        jogos_validos = [times[0], times[1], liga, True,sum_of_goals, "Passou"]
        pass  # colocar aqui que é um jogo valido no excel, os nomes do time, competição

    #print(jogos_validos)
    return jogos_validos


def game_analysis_improved():
    jogos_validos = []
    times = []
    lista_proibidos = ["ARGÉLIA", "ARGENTINA", "ALBÂNIA", "BIELORÚSSIA", "GRÉCIA", "ISRAEL", "IRÃ", "MARROCOS",
                       "RÚSSIA", "TAILÂNDIA", "ARGELIA", "ALBANIA", "BIELORUSSIA", "GRECIA", "IRA", "RUSSIA",
                       "TAILANDIA","SUB-19","SUB-18","SUB-20","SUB-17","Sub-19","Sub-18","Sub-20","Sub-17","Cup","cup","CUP","JUVENIL"]
    erro = ""


    div_5games = driver.find_element(By.XPATH, '/html/body/div[1]')
    html_content = div_5games.get_attribute('outerHTML')
    soup = BeautifulSoup(html_content, 'html.parser')

    #print(soup.prettify())
    resultados_game = soup.find_all('div', class_='h2h__row')
    #print(len(resultados_game))

    validator = [True, True, True]
    sum_of_goals = 0
    games_less_than_2 = 0
    try:
        for i in range(10):
            #print(resultados_game[i].get_text())
            gol1 = resultados_game[i].get_text()[-2]
            gol2 = resultados_game[i].get_text()[-3]
            #print(gol1, gol2)
            sum_of_goals = sum_of_goals + int(gol1) + int(gol2)  # getting the sum of last fibe games
            if gol1 == "0" and gol2 == "0": #improved the method not to accept games with less than 2 goals in the last five games
                validator[0] = False
                break
            if (gol1 == "1" and gol2 == "0") or (gol1 == "0" and gol2 == "1"):
                games_less_than_2 = games_less_than_2 + 1
            if games_less_than_2 > 1:
                validator[0] = False
    except:
        validator[0] = False


    times.append(driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[2]/div[3]/div[2]/a').text)
    times.append(driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[4]/div[3]/div[1]/a').text)

    # seguda validação
    liga = driver.find_element(By.XPATH, '//*[@id="detail"]/div[4]/div/span[3]').text
    for pais in lista_proibidos:
        if pais in liga:
            validator[1] = False
            break

    if "COPA" in liga:
        validator[2] = False

    if False in validator:
        #print("não passou nas etapas")
        if validator[0] == False:
            #print("Teve 0 a 0 em algum dos ultimos 5 jogos")
            erro = "0a0"
        if validator[1] == False:
            #print("Liga proibida")
            erro = erro + " " + "Liga proibida"
        if validator[2] == False:
            #print("Competição é copa")
            erro = erro + " " + "É Copa"
        jogos_validos = [times[0], times[1], liga, False, sum_of_goals, erro]
    else:
        jogos_validos = [times[0], times[1], liga, True,sum_of_goals, "Passou"]
        pass  # colocar aqui que é um jogo valido no excel, os nomes do time, competição

    #print(jogos_validos)
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
        try:
            try:
                button2 = driver.find_element(By.XPATH, '//*[@id="detail"]/div[6]/div/a[3]')
                driver.execute_script("arguments[0].click();", button2)
            except:
                button2 = driver.find_element(By.XPATH, '//*[@id="detail"]/div[6]/div/a[2]')
                driver.execute_script("arguments[0].click();", button2)
        except: #there's 2 different xpath for the same button. If not one is the another one.
            button2 = driver.find_element(By.XPATH, '//*[@id="detail"]/div[7]/div/a[3]')
            driver.execute_script("arguments[0].click();", button2)
    except:
        button2 = driver.find_element(By.XPATH, '//*[@id="detail"]/div[8]/div/a[3]')
        driver.execute_script("arguments[0].click();", button2)


    time.sleep(1)
    jogos_validos.append(game_analysis_improved_max()) #escolher qual método
    #time.sleep(3)

    driver.close() #closing new open page
    driver.switch_to.window(original_window)  #returning to the original page


    #print(jogos_validos)

create_file(jogos_validos)