import os
import sys
import logging
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # move to modules 
from _fmw.fmw_utils import *
from _fmw.fmw_classes import BusinessException
from classes.robot_date import RobotDate
from process_scripts._base_process_class import ProcessBase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

class levantarNavegador(ProcessBase):

    def __init__(self, config:dict):
        ProcessBase.__init__(self, config=config) 
        self.state_name = self.state_name = type(self).__name__ # Get the class name, do not change     
        # workflow parameters 
        self.template_parameter_1 = self.config_env["ENV_PARAM_1"]
        self.template_parameter_2 = self.config_global["GLOBAL_PARAM_1"]
        #self.urlJira = "https://portafolio-claro.atlassian.net/"
        self.urlJira = self.config_env["URL_JIRA"]
        self.urlDirectaJira = self.config_env["URL_JIRA_UNITARIO"]
        print(self.urlJira)
        self.driver = webdriver.Chrome()
        self.filtro = "https://portafolio-claro.atlassian.net/issues/?filter=34564"
        self.contador=2
        self.listaJira = []
        #userJira="te.repggdd.bot34@clarochile.cl",contraJira="yEIZ@$uGB1j"
        self.userJira="te.repggdd.bot34@clarochile.cl"
        self.contraJira="yEIZ@$uGB1j"
        self.jefeAsignado = 'Francisco Ormeño'
        self.comentarioJefe = 'Junto con saludar, se ha creado requerimiento, por favor asignar Jefe de Proyectos, debe atender de acuerdo a la disponibilidad de recursos en el área, indicando tiempo estimado de ejecución.'

    def iniciarBrowser(self):
        logging.info('iniciar url')
        self.driver.get(self.urlJira)
        logging.info('maximizar window')
        self.driver.maximize_window()
        time.sleep(5)
    
    def login(self):
        logging.info('user')
        usernameJira = self.driver.find_element(By.CLASS_NAME, 'css-1cab8vv')
        usernameJira.send_keys(self.userJira)
        logging.info('pass')
        buttonContinuar = self.driver.find_element(By.CLASS_NAME, 'css-178ag6o')
        buttonContinuar.click()
        time.sleep(10)
        passwordJira = self.driver.find_element(By.CLASS_NAME, 'css-1cab8vv')
        passwordJira.send_keys(self.contraJira)
        time.sleep(5)
        buttonLogin = self.driver.find_element(By.CLASS_NAME, 'css-178ag6o')
        buttonLogin.click()
        time.sleep(15)

    #navega hasta el filtro directamente
    def navegarFiltro(self):
        self.driver.get(self.filtro)
        time.sleep(10)
    
    #lee los datos en la página de filtro para ver si existen jiras por avanzar
    #si encuentra uno copia el numero de jira y lo navega por medio de una url directamente
    def leerDatos(self):
        time.sleep(10)
        table = self.driver.find_element(By.TAG_NAME, 'table')
        data = []
        rows = table.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td') or row.find_elements(By.TAG_NAME, 'th')
            row_data = [cell.text for cell in cells]
            data.append(row_data)
        columnas = len(rows)
        if columnas>1:
            print(data[1][2])
            jira = data[1][2]
            self.driver.get(self.urlDirectaJira+jira)
            time.sleep(10)
            self.listaJira.append(jira)
        print(columnas)
        return columnas
    
    #avanza el jira al estado para aprobarlo desde validar el gestor
    def validaGestorGdd(self):
        clickpendiente = self.driver.find_element(By.ID, 'issue.fields.status-view.status-button')
        clickpendiente.click()
        time.sleep(5)
        clickpendiente = self.driver.find_element(By.ID, 'react-select-2-option-0')
        clickpendiente.click()
        time.sleep(5)

    #navegacion y llenado de formulario aprobar por ggdd
    def aprobarPorGdd(self):

        clickpendiente = self.driver.find_element(By.ID, 'issue.fields.status-view.status-button')
        clickpendiente.click()
        time.sleep(10)
        clickpendiente = self.driver.find_element(By.ID, 'react-select-2-option-1')
        clickpendiente.click()
        time.sleep(5)

        #Dropbox TIPO DE REQUERIMIENTO SI
        dropdown = Select(self.driver.find_element(By.ID, 'customfield_11023'))
        #id de la opcion ROBOTIZACIÓN
        dropdown.select_by_value('19758')

        #asignando responsable
        nombreAsignadoGDD = self.driver.find_element(By.ID, 'customfield_16515')
        nombreAsignadoGDD.send_keys('te.repggdd.bot34')
        #nombreAsignadoGDD.send_keys(Keys.ENTER yad)
        time.sleep(5)
        clickpendiente = self.driver.find_element(By.CLASS_NAME, 'yad')
        clickpendiente.click()
        time.sleep(5)

        #Radio button PRIORIDAD PORTAFOLIO
        clickpendiente = self.driver.find_element(By.ID, 'customfield_16300-1')
        clickpendiente.click()
        time.sleep(5)

        #Dropbox COMPLEJIDAD
        dropdown = Select(self.driver.find_element(By.ID, 'customfield_11006'))
        #id de la opcion MEDIANO customfield_10700
        dropdown.select_by_value('10625')
        time.sleep(10)

        #Dopbox SISTEMA INVOLUCRADO
        dropdown = Select(self.driver.find_element(By.ID, 'customfield_10700'))
        #id de la opcion NO APLICA
        dropdown.select_by_value('19449')
        time.sleep(5)

        #click en el radio button CATALOGO ANDES
        clickpendiente = self.driver.find_element(By.ID, 'customfield_13700-27')
        clickpendiente.click()
        time.sleep(5)

        print('eje estrategico')
        #Dopbox EJE ESTRATEGICO
        dropdown = Select(self.driver.find_element(By.ID, 'customfield_16487'))
        #id de la opcion TIME TO MARKET
        dropdown.select_by_value('19157')
        time.sleep(5)
        print('version fnp')
        #Dopbox VERSION FNP
        dropdown = Select(self.driver.find_element(By.ID, 'customfield_16519'))
        #id de la opcion NO APLICA (0 19168) (1 19169)
        dropdown.select_by_value('19169')
        time.sleep(5)
        #Dopbox SISTEMA DNP 
        dropdown = Select(self.driver.find_element(By.ID, 'customfield_16522'))
        #id de la opcion NO APLICA
        dropdown.select_by_value('19216')
        time.sleep(5)
        clickpendiente = self.driver.find_element(By.ID, 'issue-workflow-transition-submit')
        clickpendiente.click()
        time.sleep(30)
        
    def inicioCicloDesarrollo(self):

        clickpendiente = self.driver.find_element(By.ID, 'issue.fields.status-view.status-button')
        clickpendiente.click()
        time.sleep(5)
        clickpendiente = self.driver.find_element(By.ID, 'react-select-2-option-1')
        clickpendiente.click()
        time.sleep(5)

    def vincularIncidencia(self):
        
        time.sleep(10)               
        boton = self.driver.find_element(By.CSS_SELECTOR, 'body>div>div>div>div>div>div>div>main>div>div>div>div>div>div>div>div>div>div>span>div>button>span>span')
        boton.click()
        time.sleep(5)
        clickpendiente = self.driver.find_element(By.CSS_SELECTOR, 'body>div>div>div>div>div>div>div>main>div>div>div>div>div>div>div>div>div>div>span>div>div>div>button')
        clickpendiente.click()
        #ds--dropdown--3562df29
        time.sleep(5)
        clickpendiente = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="issue.views.issue-base.content.issue-links.add.create-linked-issue-button.create-linked-issue-button"]')
        clickpendiente.click()
        time.sleep(10)

        try:
            #Dropbox PROYECTO
            dropdown = Select(self.driver.find_element(By.ID, 'project-field'))
            #id de la opcion ROBOTIZACIÓN
            dropdown.select_by_value('11700')
            time.sleep(10)
        except Exception as e:
            print({e})
        
        #Dropbox PROYECTO
        dropdown = Select(self.driver.find_element(By.ID, 'issuelinks-linktype'))
        #id de la opcion ROBOTIZACIÓN
        dropdown.select_by_value('is caused by')
        time.sleep(10)
        #create-issue-submit
        clickpendiente = self.driver.find_element(By.ID, 'create-issue-submit')
        clickpendiente.click()
        time.sleep(15)
        clickpendiente = self.driver.find_element(By.CSS_SELECTOR,'a[data-testid="issue.issue-view.views.common.issue-line-card.issue-line-card-view.key"]')
        clickpendiente.click()
        time.sleep(10)

    def asignarJefe(self):
        #css-5z308y
        clickpendiente = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="issue.views.issue-base.foundation.status.actions-wrapper"]')
        clickpendiente.click()
        time.sleep(5)
        clickpendiente = self.driver.find_element(By.CSS_SELECTOR, 'body>div>div>div>div>div>div>div>button')
        clickpendiente.click()
        time.sleep(15)
        clickpendiente = self.driver.find_element(By.ID, 'customfield_16481-1')
        clickpendiente.click()
        time.sleep(5)
        dropdown = Select(self.driver.find_element(By.ID, 'customfield_16625'))
        #id de la opcion NO APLICA (0 19168) (1 19169)
        dropdown.select_by_value('20586')
        time.sleep(5)
        clickpendiente = self.driver.find_element(By.ID, 'customfield_16430')
        clickpendiente.send_keys(self.jefeAsignado)
        time.sleep(5)
        clickpendiente = self.driver.find_element(By.CLASS_NAME, 'yad')
        clickpendiente.click()
        time.sleep(5)
        clickpendiente = self.driver.find_element(By.ID, 'comment')
        clickpendiente.send_keys(self.comentarioJefe)
        time.sleep(5)
        clickpendiente = self.driver.find_element(By.ID, 'issue-workflow-transition-submit')
        clickpendiente.click()
        time.sleep(10)
        #issue-workflow-transition-submit


    def run_workflow(self):
        logging.info(f"----- Starting state: {self.state_name} -----")
        try: # Add workflow in try block bellow
            self.iniciarBrowser()
            self.login()
            while self.contador>1:
                self.navegarFiltro()
                jira = self.leerDatos()
                if (self.leerDatos())==1:
                    print('no existen registros')
                    break
                else:
                    print(self.listaJira)
                    self.validaGestorGdd()
                    self.aprobarPorGdd()
                    self.inicioCicloDesarrollo()
                    self.vincularIncidencia()
                    self.asignarJefe()
        except BusinessException as error:
            self._build_business_exception(error)
            raise error
        except Exception as error:
            raise error  
        logging.info(f"Finished state: {self.state_name}")


if __name__ == "__main__":
    start_logging(logs_level="DEBUG", show_console_logs=True, save_logs=False)
    config = read_config()
    logging.info(f"--------- Script {os.path.basename(__file__)} started ---------")    
    state = levantarNavegador(config=config)
    state.run_workflow()
    #state.script_function_1()
    logging.info(f"--------- Script {os.path.basename(__file__)} finished ---------")     