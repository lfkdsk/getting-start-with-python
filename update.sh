echo "removing useless files..."

rm -rf .git
rm *~
rm *.log

echo "reinitialize git repository..."

git init
git remote add origin https://github.com/lfkdsk/getting-start-with-python.git

git status

echo "committing changes..."

git add *
git add .gitignore
git stage *
git commit -a -m "refresh"

echo "status..."

git status

echo "git gc..."

git gc

echo "pushing, please wait..."

git push --force origin HEAD
git status

echo "all tasks done."

