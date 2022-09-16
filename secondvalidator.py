from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from excelwriter import create_file

times = []

driver = webdriver.Chrome()
driver.get("https://www.flashscore.com.br/jogo/OEgTOJQh/#/resumo-de-jogo")
times.append(driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[2]/div[3]/div[2]/a').text)
times.append(driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[4]/div[3]/div[1]/a').text)
validator = [True, True, True, True, True, True] #posição 1 - jogos 0x0, posição 2 - paises, posição 3 - se é copa, #posição 4 - over 2.5, posição 5 - media de gols. posição 6 - a definir
erro = ""
#até aqui já tem nos métodos.



over25_times = []
over25_jogos = []
over25_over = []
mediagols_favor = []
mediagols_contra = []

#code to click on classificação
try:
    url = "#/classificacao"
    button4 = driver.find_element(By.XPATH, '//a[@href="'+url+'"]')
    driver.execute_script("arguments[0].click();", button4)
    #code click on under/over

    time.sleep(0.5)
    url2 = "#/classificacao/over_under"
    button5 = driver.find_element(By.XPATH, '//a[@href="' + url2 + '"]')
    driver.execute_script("arguments[0].click();", button5)


    #getting over and under data
    time.sleep(2)
    over_under = driver.find_element(By.XPATH, '//*[@id="tournament-table-tabs-and-content"]')
    html_content2 = over_under.get_attribute('outerHTML')
    soup2 = BeautifulSoup(html_content2, 'html.parser')


    times_nomes = soup2.find_all('div', class_='tableCellParticipant')  #get all names
    times_jogos = soup2.find_all('span', class_='table__cell table__cell--value') #get all games
    times_jogos_over = soup2.find_all('span', class_='table__cell--over') #get all games over 2.5 goals
    times_gols = soup2.find_all('span', class_='table__cell--score')  # get all names


    #passing all values to lists
    for i in range(len(times_nomes)):
        over25_times.append(times_nomes[i].get_text())
        over25_jogos.append(float(times_jogos[i].get_text()))
        over25_over.append(float(times_jogos_over[i].get_text()))
        mediagols_favor.append(float(times_gols[i].get_text().split(':')[0]))  # using split to split home and out goals split by : GOLS IN FAVOR
        mediagols_contra.append(float(times_gols[i].get_text().split(':')[1]))  # using split to split home and out goals split by : GOLS AGAINST


    position_time1 = over25_times.index(times[0])
    position_time2 = over25_times.index(times[1])

    #validators de under 2.5
    time1_over25_validator = over25_over[position_time1] / over25_jogos[position_time1]
    time2_over25_validator = over25_over[position_time2] / over25_jogos[position_time2]

    if time1_over25_validator <= 0.65 or time2_over25_validator < 0.5:
        validator[3] = False
        print("não passou na analise de over 2.5")
    else:
        print("passou no over 2.5")

    #validator de media de gols
    time1_mediagols_validator = ((mediagols_favor[position_time1] / over25_jogos[position_time1]) + (mediagols_contra[position_time1] / over25_jogos[position_time1]))/2
    time2_mediagols_validator = ((mediagols_favor[position_time2] / over25_jogos[position_time2]) + (mediagols_contra[position_time2] / over25_jogos[position_time2])) / 2
    print(time1_mediagols_validator,time2_mediagols_validator)
    if time1_mediagols_validator < 1.5 or time1_mediagols_validator < 1.5:
        validator[4] = False
        print("não passou na analise de media de gols")
    else:
        print("passou no over 2.5")


    # #VALIDADOR DE MEDIA CRUZADA PRA EVITAR PROBLEMAS DE CONFRONTO DE DOIS TIMES QUE NÃO FAZEM MUITO GOLS OU DOIS QUE NÇAO TOMAM MUITO GOL
    # mediacruzada1_mediagols_validator = ((mediagols_favor[position_time1] / over25_jogos[position_time1]) + (mediagols_favor[position_time2] / over25_jogos[position_time2])) / 2
    # mediacruzada2_mediagols_validator = ((mediagols_contra[position_time1] / over25_jogos[position_time1]) + (mediagols_contra[position_time2] / over25_jogos[position_time2])) / 2
    # print(mediacruzada1_mediagols_validator, mediacruzada2_mediagols_validator)
    # if mediacruzada1_mediagols_validator < 1.5 or mediacruzada2_mediagols_validator < 1.5:
    #     validator[4] = False
    #     print("não passou na analise de media de gols cruzada")
    # else:
    #     print("passou na media de gols cruzada")






except:
    erro = erro + " " + "Não é liga |"
    validator[3] = False
    print("nao é liga")
