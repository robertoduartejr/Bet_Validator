from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from excelwriter import create_file

times = []

driver = webdriver.Chrome()
driver.get("https://www.flashscore.com.br/jogo/8tl9nPF5/#/resumo-de-jogo")
times.append(driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[2]/div[3]/div[2]/a').text)
times.append(driver.find_element(By.XPATH, '//*[@id="detail"]/div[5]/div[4]/div[3]/div[1]/a').text)
validator = [True, True, True, True, True, True] #posição 1 - jogos 0x0, posição 2 - paises, posição 3 - se é copa, #posição 4 - over 2.5, posição 5 - media de gols. posição 6 - a definir
erro = ""
#até aqui já tem nos métodos.



mediagols_times = []
mediagols_jogos = []
mediagols_casa = []
mediagols_fora = []

#code to click on classificação
try:
    url = "#/classificacao"
    button4 = driver.find_element(By.XPATH, '//a[@href="'+url+'"]')
    driver.execute_script("arguments[0].click();", button4)
    #code click on under/over

    #getting goals data
    time.sleep(5)
    classification = driver.find_element(By.XPATH, '//*[@id="tournament-table-tabs-and-content"]')
    html_content3 = classification.get_attribute('outerHTML')
    soup3 = BeautifulSoup(html_content3, 'html.parser')

    times_gols = soup3.find_all('span', class_='table__cell--score')  #get all names
    times_jogos = soup3.find_all('span', class_='table__cell table__cell--value')  # get all games
    times_nomes = soup3.find_all('div', class_='tableCellParticipant')  # get all names

    for i in range(len(times_nomes)):
        mediagols_times.append(times_nomes[i].get_text())
        mediagols_jogos.append(float(times_jogos[i].get_text()))
        mediagols_casa.append(float(times_gols[i].get_text().split(':')[0])) #using split to split home and out goals split by :
        mediagols_fora.append(float(times_gols[i].get_text().split(':')[1]))

   # over25_jogos = mediagols_jogos #deletar essa linha depois, utilizando so pra teste
    #Tive que usar os jogos obtidos

    print(mediagols_times,mediagols_jogos,mediagols_casa,mediagols_fora)

    # for time_gols in times_gols:
    #     gols = time_gols.get_text()
    #     gols_casa_fora = gols.split(':')
    #     print(gols_casa_fora)



    # # #passing all values to lists
    # for i in range(len(times_gols)):
    #     over25_times.append(times_nomes[i].get_text())
    #     over25_jogos.append(float(times_jogos[i].get_text()))
    #     over25_over.append(float(times_jogos_over[i].get_text()))
    #
    # position_time1 = over25_times.index(times[0])
    # position_time2 = over25_times.index(times[1])
    #
    # #validators
    # time1_validator = over25_over[position_time1] / over25_jogos[position_time1]
    # time2_validator = over25_over[position_time2] / over25_jogos[position_time2]
    #
    # if time1_validator <= 0.65 or time2_validator < 0.5:
    #     validator[3] = False
    #     print("não passou na analise de over 2.5")
    # else:
    #     print("passou")


except:
    erro = erro + " " + "Não é liga |"
    validator[3] = False
    print("nao é liga")
