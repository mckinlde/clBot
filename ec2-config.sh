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
