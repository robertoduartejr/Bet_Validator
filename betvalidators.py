from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from excelwriter import create_file, writeondb

def betvalidator():

    driver = webdriver.Chrome()

    #opening the site and getting all the next games
    driver.get("https://www.flashscore.com.br/")
    time.sleep(5)
    tab_proximos_jogos = driver.find_element(By.XPATH, '//*[@id="live-table"]/div[1]/div[1]/div[5]')
    tab_proximos_jogos.click()
    time.sleep(0.1)


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


        resultados_game = soup.find_all('div', class_='h2h__row')


        validator = [True, True, True, True, True, True] #posição 1 - jogos 0x0, posição 2 - paises, posição 3 - se é copa, #posição 4 - over 2.5, posição 5 - media de gols. posição 6 - a definir
        sum_of_goals = 0

        #VALIDAR 0 A 0 NOS ULTIMOS JOGOS
        try:
            for i in range(10):
                gol1 = resultados_game[i].get_text()[-2]
                gol2 = resultados_game[i].get_text()[-3]
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
                erro = erro + " " + "Numero de jogos mínimo NOK |"


            if time1_over25_validator <= media_casa_over25 or time2_over25_validator < media_fora_over25:
                validator[3] = False


            # validator de media de gols
            time1_mediagols_validator = ((mediagols_favor[position_time1] / over25_jogos[position_time1]) + (
                        mediagols_contra[position_time1] / over25_jogos[position_time1])) / 2
            time2_mediagols_validator = ((mediagols_favor[position_time2] / over25_jogos[position_time2]) + (
                        mediagols_contra[position_time2] / over25_jogos[position_time2])) / 2

            if time1_mediagols_validator < mediagols_limiar or time2_mediagols_validator < mediagols_limiar:
                validator[4] = False

        except:
            erro = erro + " " + "Não é liga |"
            validator[3] = False


        ########################################VALIDADOR 2 E 3 FIM

        # seguda validação
        liga = driver.find_element(By.XPATH, '//*[@id="detail"]/div[4]/div/span[3]').text.split("-")[0]
        for pais in lista_proibidos:
            if pais in liga:
                validator[1] = False
                break

        if "COPA" in liga:
            validator[2] = False

        if False in validator:
            if validator[0] == False:
                erro = "Teve 0a0 recentemente |"
            if validator[1] == False:
                erro = erro + " " + "Liga sem Padrão |"
            if validator[2] == False:
                erro = erro + " " + "Não é liga |"
            if validator[3] == False:
                erro = erro + " " + "Baixa frequencia de jogos ocm muitos gols |"
            if validator[4] == False:
                erro = erro + " " + "Media de gols por jogo baixa |"
            if validator[5] == False:
                erro = erro + " " + "a definir |"

            jogos_validos = [times[0], times[1], liga, False, sum_of_goals, erro]
        else:
            jogos_validos = [times[0], times[1], liga, True,sum_of_goals, "Aprovado"]
            pass  # colocar aqui que é um jogo valido no excel, os nomes do time, competição

        return jogos_validos


    #function to define the games to bet according to method 3
    def game_analysis_improved():
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


        resultados_game = soup.find_all('div', class_='h2h__row')

        validator = [True, True, True, True, True, True] #posição 1 - jogos 0x0, posição 2 - paises, posição 3 - se é copa, #posição 4 - over 2.5, posição 5 - media de gols. posição 6 - a definir
        sum_of_goals = 0
        games_less_than_2 = 0
        try:
            for i in range(10):
                gol1 = resultados_game[i].get_text()[-2]
                gol2 = resultados_game[i].get_text()[-3]
                sum_of_goals = sum_of_goals + int(gol1) + int(gol2)  # getting the sum of last fibe games
                if gol1 == "0" and gol2 == "0": #improved the method not to accept games with less than 2 goals in the last five games
                    validator[0] = False
                    break
                if (gol1 == "1" and gol2 == "0") or (gol1 == "0" and gol2 == "1"):
                    games_less_than_2 = games_less_than_2 + 1
                if games_less_than_2 > 1:
                    validator[0] = False
                    erro = erro + " " + "Muitos jogos de 1x0 recentemente |"
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
                mediagols_favor.append(float(times_gols[i].get_text().split(':')[0]))  # using split to split home and out goals split by : GOLS IN FAVOR
                mediagols_contra.append(float(times_gols[i].get_text().split(':')[1]))  # using split to split home and out goals split by : GOLS AGAINST

            position_time1 = over25_times.index(times[0])
            position_time2 = over25_times.index(times[1])

            # validators de under 2.5
            time1_over25_validator = over25_over[position_time1] / over25_jogos[position_time1]
            time2_over25_validator = over25_over[position_time2] / over25_jogos[position_time2]

            # validar número minimo de jogos
            if over25_jogos[position_time1] < num_jogos or over25_jogos[position_time2] < num_jogos:
                validator[3] = False
                erro = erro + " " + "Numero de jogos mínimo NOK |"


            if time1_over25_validator <= media_casa_over25 or time2_over25_validator < media_fora_over25:
                validator[3] = False


            # validator de media de gols

            #VALIDADOR DE MEDIA CRUZADA PRA EVITAR PROBLEMAS DE CONFRONTO DE DOIS TIMES QUE NÃO FAZEM MUITO GOLS OU DOIS QUE NÇAO TOMAM MUITO GOL
            mediacruzada1_mediagols_validator = ((mediagols_favor[position_time1] / over25_jogos[position_time1]) + (mediagols_favor[position_time2] / over25_jogos[position_time2])) / 2
            mediacruzada2_mediagols_validator = ((mediagols_contra[position_time1] / over25_jogos[position_time1]) + (mediagols_contra[position_time2] / over25_jogos[position_time2])) / 2

            if mediacruzada1_mediagols_validator < mediagols_limiar or mediacruzada2_mediagols_validator < mediagols_limiar:
                validator[4] = False

                media_especial1 = ((mediagols_favor[position_time1] / over25_jogos[position_time1]) + (mediagols_contra[position_time2] / over25_jogos[position_time2]))/2
                #media_especial2 = ((mediagols_favor[position_time2] / over25_jogos[position_time2]) + (mediagols_contra[position_time1] / over25_jogos[position_time1]))/2
                #condicional abaixo valida jogos em que a média de gols de um time é alta e a média de gols tomado do outro time é alta, pq a tendenci é q o jogo tenha mto gol.
                if media_especial1 >= mediagols_limiar: #media especial apenas se o time goleador jogar em casa
                    validator[4] = True


        except:
            erro = erro + " " + "Não é liga |"
            validator[3] = False

        ########################################VALIDADOR 2 E 3 FIM




        # seguda validação
        liga = driver.find_element(By.XPATH, '//*[@id="detail"]/div[4]/div/span[3]').text.split("-")[0]
        for pais in lista_proibidos:
            if pais in liga:
                validator[1] = False
                break

        if "COPA" in liga:
            validator[2] = False

        if False in validator:
            if validator[0] == False:
                erro = "Teve 0a0 recentemente |"
            if validator[1] == False:
                erro = erro + " " + "Liga sem Padrão |"
            if validator[2] == False:
                erro = erro + " " + "Não é liga |"
            if validator[3] == False:
                erro = erro + " " + "Baixa frequencia de jogos ocm muitos gols |"
            if validator[4] == False:
                erro = erro + " " + "Media de gols por jogo baixa |"
            if validator[5] == False:
                erro = erro + " " + "a definir |"
            jogos_validos = [times[0], times[1], liga, False, sum_of_goals, erro]
        else:
            jogos_validos = [times[0], times[1], liga, True,sum_of_goals, "Aprovado"]
            pass  # colocar aqui que é um jogo valido no excel, os nomes do time, competição

        return jogos_validos



    i = True
    time.sleep(1)
    accept = driver.find_element(By.XPATH,f'//*[@id="onetrust-pc-btn-handler"]') #accept cookies 1
    accept.click()
    time.sleep(1)
    accept2 = driver.find_element(By.XPATH,'//*[@id="onetrust-pc-sdk"]/div[3]/div[1]/button[2]') #accept cookies 2
    accept2.click()
    time.sleep(1)
    #laço para abrir todos os jogos escondidos.
    while i:
        try:
            teste = driver.find_element(By.XPATH,"//*[@title='Exibir todos os jogos desta competição!']")
            teste.click()
        except:
            break

    #after open hidden games I can open all games below

    #pegando os dados apos recarregar a pagina com novos jogos
    div_allgames = driver.find_element(By.XPATH, '//*[@id="fsbody"]')
    html_content = div_allgames.get_attribute('outerHTML')
    soup = BeautifulSoup(html_content,'html.parser')

    #all games
    allgames = soup.find_all('div',class_='event__match--scheduled')

    original_window = driver.current_window_handle #define the fist google chrome window so that I can make control
    assert len(driver.window_handles) == 1

    #loop to open all game pages
    count = 1
    for game in allgames:
        try:
            print(count,"/",len(allgames))
            caminho = game.get('id')
            button = driver.find_element(By.XPATH, f'//*[@id="{caminho}"]') #click in each game
            driver.execute_script("arguments[0].click();", button) #a different way I found to click without geteting an error

            #loop to change the window
            for window_handle in driver.window_handles:
                if window_handle != original_window:
                    driver.switch_to.window(window_handle)
                    break

            #clicar no h2h
            url2 = "#/h2h"
            button4 = driver.find_element(By.XPATH, '//a[@href="' + url2 + '"]')
            driver.execute_script("arguments[0].click();", button4)


            time.sleep(0.5)
            jogos_validos.append(game_analysis()) #define which method to use
            #time.sleep(3)

            driver.close() #closing new open window
            driver.switch_to.window(original_window)  #returning to the original window
        except:
            pass
        count = count + 1
    #calling function to create excel file and open it
    create_file(jogos_validos)
    writeondb(jogos_validos)