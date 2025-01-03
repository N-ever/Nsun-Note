export REPO_ROOT=`pwd`
echo $REPO_ROOT
if [ $# -ne 0 ]; then
    export CONTENT=`cat $1`
fi
echo $CONTENT
TMP_FILE=$REPO_ROOT/patch/patch_tmp.log
repo forall -c '
    REPO_PATH=$(pwd| sed "s|^${REPO_ROOT}/||")
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
        echo $patch_path
        if [ -s "$patch_path" ]; then
            echo "Start ot apply" $REPO_PATH
            git apply $patch_path
            if [ $? -ne 0 ]; then
                echo "Apply $patch_path failed !!!"
            else
                echo "Apply $patch_path successed!!!"
            fi
        fi
    fi
' > $TMP_FILE

grep "successed" $TMP_FILE
echo ""
grep "failed" $TMP_FILE
