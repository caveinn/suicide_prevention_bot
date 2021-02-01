## Pre requisites
- Have `pipenv` installed
- Have an installed chromedriver and have the driver location added to PATH. Chrome drivers and the matching chrome version they work on can be found [here](https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json). Go to your chrome version and download the chromedriver version matching your os. 
## Set Up
- Clone repo   
`git clone https://github.com/caveinn/suicide_prevention_bot.git`
- Cd into repo
- Update .env with valid credentials
- Install requirements  
`pipenv sync`
- Initialize env shell  
`pipenv shell`
- Run code  
`python main.py`