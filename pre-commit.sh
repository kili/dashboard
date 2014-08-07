# pre-commit.sh
git stash -q --keep-index

./run_tests.sh -V
RESULT=$?
git stash pop -q
[ $RESULT -ne 0 ] && exit 1
exit 0