mkdir $1
mkdir $1.git
mkdir $1/data
mkdir $1/data/pages
mkdir $1/data/user
mkdir $1/underlay
mkdir $1/underlay/pages

cd $1.git
git init
cd ..
cp lib/config/git.config.sample $1.git/.git/config
cp lib/config/wikifarm_instance_config.py $1.py
