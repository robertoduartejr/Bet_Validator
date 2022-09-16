from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from excelwriter import create_file

driver = webdriver.Chrome()

#opening the site and getting all the next games
driver.get("https://www.flashscore.com.br/")
time.sleep(0.5)
tab_proximos_jogos = driver.find_element(By.XPATH, '//*[@id="live-table"]/div[1]/div[1]/div[5]')
tab_proximos_jogos.click()
time.sleep(0.5)


div_allgames = driver.find_element(By.XPATH, '//*[@id="fsbody"]')
html_content = div_allgames.get_attribute('outerHTML')
soup = BeautifulSoup(html_content,'html.parser')
jogos_validos = []

#function to define the games to bet according to method 1
def game_analysis():
    times = []
    lista_proibidos = ["ARGÉLIA", "ARGENTINA", "ALBÂNIA", "BIELORÚSSIA", "GRÉCIA", "ISRAEL", "IRÃ", "MARROCOS",
                       "RÚSSIA", "TAILÂNDIA", "ARGELIA", "ALBANIA", "BIELORUSSIA", "GRECIA", "RUSSIA",
                       "TAILANDIA","SUB-19","SUB-18","SUB-20","SUB-17","Sub-19","Sub-18","Sub-20","Sub-17","Cup","cup","CUP","JUVENIL"]
    erro = ""
    mediagols_limiar = 1.5
    num_jogos = 3
    media_casa_over25 = 0.65
    media_fora_over25 = 0.5

    div_5games = driver.find_element(By.XPATH, '/html/body/div[1]')
    html_content = div_5games.get_attribute('outerHTML')
    soup = BeautifulSoup(html_content, 'html.parser')

    #print(soup.prettify())
    resultados_game = soup.find_all('div', class_='h2h__row')
    #print(len(resultados_game))

    validator = [True, True, True, True, True, True] #posição 1 - jogos 0x0, posição 2 - paises, posição 3 - se é copa, #posição 4 - over 2.5, posição 5 - media de gols. posição 6 - a definir
    sum_of_goals = 0

    #VALIDAR 0 A 0 NOS ULTIMOS JOGOS
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

    ########################################VALIDADOR 2 E 3 INICIO

    over25_times = []
    over25_jogos = []
    over25_over = []
    mediagols_favor = []
    mediagols_contra = []

    # code to click on classificação
    try:
        times.append(driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[2]/div[3]/div[2]/a').text)
        times.append(driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[4]/div[3]/div[1]/a').text)
        url = "#/classificacao"
        button4 = driver.find_element(By.XPATH, '//a[@href="' + url + '"]')
        driver.execute_script("arguments[0].click();", button4)
        # code to click on under/over

        time.sleep(0.5)
        url2 = "#/classificacao/over_under"
        button5 = driver.find_element(By.XPATH, '//a[@href="' + url2 + '"]')
        driver.execute_script("arguments[0].click();", button5)

        # getting over and under data
        time.sleep(1)
        over_under = driver.find_element(By.XPATH, '//*[@id="tournament-table-tabs-and-content"]')
        html_content2 = over_under.get_attribute('outerHTML')
        soup2 = BeautifulSoup(html_content2, 'html.parser')

        times_nomes = soup2.find_all('div', class_='tableCellParticipant')  # get all names
        times_jogos = soup2.find_all('span', class_='table__cell table__cell--value')  # get all games
        times_jogos_over = soup2.find_all('span', class_='table__cell--over')  # get all games over 2.5 goals
        times_gols = soup2.find_all('span', class_='table__cell--score')  # get all names

        # passing all values to lists
        for i in range(len(times_nomes)):
            over25_times.append(times_nomes[i].get_text())
            over25_jogos.append(float(times_jogos[i].get_text()))
            over25_over.append(float(times_jogos_over[i].get_text()))
            mediagols_favor.append(float(times_gols[i].get_text().split(':')[
                                             0]))  # using split to split home and out goals split by : GOLS IN FAVOR
            mediagols_contra.append(float(times_gols[i].get_text().split(':')[
                                              1]))  # using split to split home and out goals split by : GOLS AGAINST

        position_time1 = over25_times.index(times[0])
        position_time2 = over25_times.index(times[1])

        # validators de under 2.5
        time1_over25_validator = over25_over[position_time1] / over25_jogos[position_time1]
        time2_over25_validator = over25_over[position_time2] / over25_jogos[position_time2]

        #validar número minimo de jogos
        if over25_jogos[position_time1] < num_jogos or over25_jogos[position_time2] < num_jogos:
            validator[3] = False
            print("não passou no numero de jogos minimo")
            erro = erro + " " + "Numero de jogos NOK |"
        else:
            print("numero de jogos ok")


        if time1_over25_validator <= media_casa_over25 or time2_over25_validator < media_fora_over25:
            validator[3] = False
            print("não passou na analise de over 2.5")
        else:
            print("passou no over 2.5")

        # validator de media de gols
        time1_mediagols_validator = ((mediagols_favor[position_time1] / over25_jogos[position_time1]) + (
                    mediagols_contra[position_time1] / over25_jogos[position_time1])) / 2
        time2_mediagols_validator = ((mediagols_favor[position_time2] / over25_jogos[position_time2]) + (
                    mediagols_contra[position_time2] / over25_jogos[position_time2])) / 2
        print(time1_mediagols_validator, time2_mediagols_validator)
        if time1_mediagols_validator < mediagols_limiar or time2_mediagols_validator < mediagols_limiar:
            validator[4] = False
            print(f"não passou na analise de media de gols. MEDIA TIME 1:{time1_mediagols_validator} TIME 2: {time2_mediagols_validator}")
        else:
            print("Passou na média de gols")


    except:
        erro = erro + " " + "Não é liga |"
        validator[3] = False
        print("nao é liga")


    ########################################VALIDADOR 2 E 3 FIM

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
            erro = "0a0 |"
        if validator[1] == False:
            #print("Liga proibida")
            erro = erro + " " + "Liga proibida |"
        if validator[2] == False:
            #print("Competição é copa")
            erro = erro + " " + "É Copa |"
        if validator[3] == False:
            erro = erro + " " + "Over 2.5 fraco |"
        if validator[4] == False:
            erro = erro + " " + "Media abaixo |"
        if validator[5] == False:
            erro = erro + " " + "a definir |"

        jogos_validos = [times[0], times[1], liga, False, sum_of_goals, erro]
    else:
        jogos_validos = [times[0], times[1], liga, True,sum_of_goals, "Passou"]
        pass  # colocar aqui que é um jogo valido no excel, os nomes do time, competição

    return jogos_validos

#function to define the games to bet according to method 2
def game_analysis_improved_max():
    times = []
    lista_proibidos = ["ARGÉLIA", "ARGENTINA", "ALBÂNIA", "BIELORÚSSIA", "GRÉCIA", "ISRAEL", "IRÃ", "MARROCOS",
                       "RÚSSIA", "TAILÂNDIA", "ARGELIA", "ALBANIA", "BIELORUSSIA", "GRECIA", "RUSSIA",
                       "TAILANDIA","SUB-19","SUB-18","SUB-20","SUB-17","Sub-19","Sub-18","Sub-20","Sub-17","Cup","cup","CUP","JUVENIL"]
    erro = ""


    div_5games = driver.find_element(By.XPATH, '/html/body/div[1]')
    html_content = div_5games.get_attribute('outerHTML')
    soup = BeautifulSoup(html_content, 'html.parser')

    #print(soup.prettify())
    resultados_game = soup.find_all('div', class_='h2h__row')
    #print(len(resultados_game))

    validator = [True, True, True, True, True, True] #posição 1 - jogos 0x0, posição 2 - paises, posição 3 - se é copa, #posição 4 - over 2.5, posição 5 - media de gols. posição 6 - a definir
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
        # print("não passou nas etapas")
        if validator[0] == False:
            # print("Teve 0 a 0 em algum dos ultimos 5 jogos")
            erro = "0a0 |"
        if validator[1] == False:
            # print("Liga proibida")
            erro = erro + " " + "Liga proibida |"
        if validator[2] == False:
            # print("Competição é copa")
            erro = erro + " " + "É Copa |"
        if validator[3] == False:
            erro = erro + " " + "Over 2.5 fraco |"
        if validator[4] == False:
            erro = erro + " " + "Media abaixo |"
        if validator[5] == False:
            erro = erro + " " + "a definir |"
        jogos_validos = [times[0], times[1], liga, False, sum_of_goals, erro]
    else:
        jogos_validos = [times[0], times[1], liga, True,sum_of_goals, "Passou"]
        pass  # colocar aqui que é um jogo valido no excel, os nomes do time, competição

    #print(jogos_validos)
    return jogos_validos

#function to define the games to bet according to method 3
def game_analysis_improved():
    times = []
    lista_proibidos = ["ARGÉLIA", "ARGENTINA", "ALBÂNIA", "BIELORÚSSIA", "GRÉCIA", "ISRAEL", "IRÃ", "MARROCOS",
                       "RÚSSIA", "TAILÂNDIA", "ARGELIA", "ALBANIA", "BIELORUSSIA", "GRECIA", "RUSSIA",
                       "TAILANDIA","SUB-19","SUB-18","SUB-20","SUB-17","Sub-19","Sub-18","Sub-20","Sub-17","Cup","cup","CUP","JUVENIL"]
    erro = ""


    div_5games = driver.find_element(By.XPATH, '/html/body/div[1]')
    html_content = div_5games.get_attribute('outerHTML')
    soup = BeautifulSoup(html_content, 'html.parser')

    #print(soup.prettify())
    resultados_game = soup.find_all('div', class_='h2h__row')
    #print(len(resultados_game))

    validator = [True, True, True, True, True, True] #posição 1 - jogos 0x0, posição 2 - paises, posição 3 - se é copa, #posição 4 - over 2.5, posição 5 - media de gols. posição 6 - a definir
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
        # print("não passou nas etapas")
        if validator[0] == False:
            # print("Teve 0 a 0 em algum dos ultimos 5 jogos")
            erro = "0a0 |"
        if validator[1] == False:
            # print("Liga proibida")
            erro = erro + " " + "Liga proibida |"
        if validator[2] == False:
            # print("Competição é copa")
            erro = erro + " " + "É Copa |"
        if validator[3] == False:
            erro = erro + " " + "Over 2.5 fraco |"
        if validator[4] == False:
            erro = erro + " " + "Media abaixo |"
        if validator[5] == False:
            erro = erro + " " + "a definir |"
        jogos_validos = [times[0], times[1], liga, False, sum_of_goals, erro]
    else:
        jogos_validos = [times[0], times[1], liga, True,sum_of_goals, "Passou"]
        pass  # colocar aqui que é um jogo valido no excel, os nomes do time, competição

    #print(jogos_validos)
    return jogos_validos


#all games
allgames = soup.find_all('div',class_='event__match--scheduled')

original_window = driver.current_window_handle #define the fist google chrome window so that I can make control
assert len(driver.window_handles) == 1

#loop to open all game pages
for game in allgames:
    caminho = game.get('id')
    button = driver.find_element(By.XPATH, f'//*[@id="{caminho}"]') #click in each game
    driver.execute_script("arguments[0].click();", button) #a different way I found to click without geteting an error

    #loop to change the window
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
    jogos_validos.append(game_analysis()) #define which method to use
    #time.sleep(3)

    driver.close() #closing new open window
    driver.switch_to.window(original_window)  #returning to the original window

#calling function to create excel file and open it
create_file(jogos_validos)