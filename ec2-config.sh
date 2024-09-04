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