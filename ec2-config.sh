# Good luck running this without copy/paste lmao

# install git
sudo yum update -y
sudo yum install git -y
git --version
git config --global user.name "mckinlde"
git config --global user.email "douglas.e.mckinley@gmail.com"
# make an ssh key
ssh-keygen -t ed25519 -C "douglas.e.mckinley@gmail.com"
# clone the repo
cat ~/ec2-ssh-key.pub >> ~/.ssh/authorized_keys
git clone git@github.com:mckinlde/clBot.git

# Installing Node 
#   https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/setting-up-node-on-ec2-instance.html
# install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
# load nvm
source ~/.bashrc
# use nvm to install latest Node.js LTS (this includes NPM)
nvm install --lts
# test that node is installed
node -e "console.log('Running Node.js ' + process.version)"

# https://preethamdpg.medium.com/running-selenium-webdriver-with-python-on-an-aws-ec2-instance-be9780c97d47
# Install Chrome (browser first, then webdriver to match browser version)
cd ../../
cd tmp
sudo wget https://chromedriver.storage.googleapis.com/80.0.3987.106/chromedriver_linux64.zip
sudo unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin/chromedriver
chromedriver --version
# ChromeDriver 80.0.3987.106 (f68069574609230cf9b635cd784cfb1bf81bb53a-refs/branch-heads/3987@{#882})

# Testing example_script
node clBot/example_script.spec.js
#start firstTest()
# Error: Unable to obtain browser driver.
#         For more information on how to install drivers see
#