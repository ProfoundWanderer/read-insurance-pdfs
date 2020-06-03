# standard imports
import time
import sys
# third party imports
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
# local imports
import config


def update_insurance(dot_or_mc, dot_mc_number, insurance_dict):
    # go to login page and login
    geckodriver_path = './geckodriver-v0.26.0-win64/geckodriver.exe'
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(executable_path=geckodriver_path, firefox_options=options)
    driver.get('https://bedrocklogistics.com/login')

    if driver.title != 'Login - Bedrock':
        raise Exception('Unable to load google page!')

    # login to website
    driver.find_element_by_id('loginButton').click()

    username_field = driver.find_element_by_id('username')
    username_field.send_keys(config.username)
    password_field = driver.find_element_by_id('password')
    password_field.send_keys(config.password)

    driver.find_element_by_id('postTeamLogin').click()

    # input auto insurance information
    if 'automobile_liability' in insurance_dict:
        def input_auto():
            # go to search page
            driver.get('https://bedrocklogistics.com/carrierSearch')

            # input information based on if it was a DOT or MC
            if dot_or_mc.upper() == 'DOT':
                driver.find_element_by_id('dotNumber').send_keys(dot_mc_number)
            elif dot_or_mc.upper() == 'MC':
                driver.find_element_by_id('docketNumber').send_keys(dot_mc_number)
            else:
                print('Unable to input information.')
                return

            # open insurance dialogue box
            driver.find_element_by_id('carrierSearchBtn').click()
            driver.find_element_by_id('3').click()
            driver.find_element_by_id('addInsurance').click()

            try:
                driver.find_element_by_id('agentName').send_keys(insurance_dict['contact_info']['producer'])
            except:
                try:
                    driver.find_element_by_id('agentName').send_keys(insurance_dict['contact_info']['contact_name'])
                except:
                    agent_name_field = driver.find_element_by_id('agentName')
                    agent_name_field.send_keys('Customer Service')

            try:
                driver.find_element_by_id('agentPhone').send_keys(insurance_dict['contact_info']['phone'])
            except:
                agent_phone_field = driver.find_element_by_id('agentPhone')
                agent_phone_field.send_keys('')

            try:
                driver.find_element_by_id('agentFax').send_keys(insurance_dict['contact_info']['fax'])
            except:
                agent_phone_field = driver.find_element_by_id('agentFax')
                agent_phone_field.send_keys('')

            try:
                driver.find_element_by_id('agentEmail').send_keys(insurance_dict['contact_info']['insurance_email'])
            except:
                agent_phone_field = driver.find_element_by_id('agentEmail')
                agent_phone_field.send_keys('')

            try:
                driver.find_element_by_id('policyNumber').send_keys(
                    insurance_dict['automobile_liability']['policy_number'])
            except:
                print('Unable to find policy number.')
                return

            try:
                driver.find_element_by_id('coverageAmount').send_keys(
                    insurance_dict['automobile_liability']['coverage_amount'])
            except:
                print('Unable to find coverage amount.')
                return

            try:
                driver.find_element_by_id('certificateLevel').send_keys(Keys.TAB)
                eff_date = driver.find_element_by_id('effectiveDateInsurance')
                ActionChains(driver).move_to_element(eff_date).send_keys(
                    insurance_dict['automobile_liability']['effective_date']).perform()
            except:
                print('Unable to find automobile liability insurance effective date.')
                return

            try:
                driver.find_element_by_id('certificateLevel').send_keys(Keys.TAB * 5)
                exp_date = driver.find_element_by_id('expirationDateInsurance')
                ActionChains(driver).move_to_element(exp_date).send_keys(
                    insurance_dict['automobile_liability']['expiration_date']).perform()
            except:
                print('Unable to find automobile liability insurance expiration date.')
                return

            driver.find_element_by_id('saveInsurance').click()

        input_auto()

    # input cargo insurance information
    if 'cargo' in insurance_dict:
        def input_cargo():
            # go to search page
            driver.get('https://bedrocklogistics.com/carrierSearch')

            # input information based on if it was a DOT or MC
            if dot_or_mc.upper() == 'DOT':
                driver.find_element_by_id('dotNumber').send_keys(dot_mc_number)
            elif dot_or_mc.upper() == 'MC':
                driver.find_element_by_id('docketNumber').send_keys(dot_mc_number)
            else:
                print('Unable to input information.')
                return

            # open insurance dialogue box
            driver.find_element_by_id('carrierSearchBtn').click()
            driver.find_element_by_id('3').click()
            driver.find_element_by_id('addInsurance').click()

            try:
                driver.find_element_by_id('agentName').send_keys(insurance_dict['contact_info']['producer'])
            except:
                try:
                    driver.find_element_by_id('agentName').send_keys(insurance_dict['contact_info']['contact_name'])
                except:
                    agent_name_field = driver.find_element_by_id('agentName')
                    agent_name_field.send_keys('Customer Service')

            try:
                driver.find_element_by_id('agentPhone').send_keys(insurance_dict['contact_info']['phone'])
            except:
                agent_phone_field = driver.find_element_by_id('agentPhone')
                agent_phone_field.send_keys('')

            try:
                driver.find_element_by_id('agentFax').send_keys(insurance_dict['contact_info']['fax'])
            except:
                agent_phone_field = driver.find_element_by_id('agentFax')
                agent_phone_field.send_keys('')

            try:
                driver.find_element_by_id('agentEmail').send_keys(insurance_dict['contact_info']['insurance_email'])
            except:
                agent_phone_field = driver.find_element_by_id('agentEmail')
                agent_phone_field.send_keys('')

            try:
                driver.find_element_by_id('policyNumber').send_keys(insurance_dict['cargo']['policy_number'])
            except:
                print('Unable to find policy number.')
                return

            try:
                driver.find_element_by_id('coverageAmount').send_keys(insurance_dict['cargo']['coverage_amount'])
            except:
                print('Unable to find coverage amount.')
                return

            try:
                driver.find_element_by_id('certificateLevel').send_keys(Keys.TAB)
                eff_date = driver.find_element_by_id('effectiveDateInsurance')
                ActionChains(driver).move_to_element(eff_date).send_keys(
                    insurance_dict['cargo']['effective_date']).perform()
            except:
                print('Unable to find cargo insurance effective date.')
                return

            try:
                driver.find_element_by_id('certificateLevel').send_keys(Keys.TAB * 5)
                exp_date = driver.find_element_by_id('expirationDateInsurance')
                ActionChains(driver).move_to_element(exp_date).send_keys(
                    insurance_dict['cargo']['expiration_date']).perform()
            except:
                print('Unable to find cargo insurance expiration date.')
                return

            driver.find_element_by_id('saveInsurance').click()

        input_cargo()

    driver.save_screenshot('./test/after_input.png')

    driver.quit()


if __name__ == '__main__':
    update_insurance('DOT', '2731803', {})
