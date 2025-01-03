export REPO_ROOT=`pwd`
echo $REPO_ROOT
if [ $# -ne 0 ]; then
    export CONTENT=`cat $1`
fi
echo $CONTENT
TMP_FILE=$REPO_ROOT/patch/diff_tmp.log
repo forall -c '
    REPO_PATH=$(pwd| sed "s|^${REPO_ROOT}/||")
    echo $REPO_PATH
    apply=1
    if [ -z "$CONTENT" ];then
	echo "CONTENT is None"
    else
	echo "CONTENT is $CONTENT"
	if echo "$CONTENT" | grep -q "$REPO_PATH";then
            echo "$REPO_PATH is in $CONTENT"
	else
            echo "$REPO_PATH is not in $CONTENT"
            apply=0
        fi
    fi
    if [ "$apply" -eq 0 ];then
	echo "Skip $REPO_PATH"
    else
        patch_path=$REPO_ROOT/patch/$REPO_PATH.patch
        mkdir -p $(dirname "$patch_path")
        diff=`git diff HEAD`
	if [ -z "$diff" ];then
	    echo "$REPO_PATH is empty."
        else
	    echo "Start to diff" $patch_path
            echo $diff > $patch_path
        fi
    fi
' > $TMP_FILE

grep "Start to" $TMP_FILE
echo ""
grep "is empty" $TMP_FILE
