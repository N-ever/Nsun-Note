<center>
    <h1>
        AOSP Make
    </h1>
</center>

## Get AOSP Code

### Install Git

```shell
sudo apt-get install git
git config --global user.email "evern@xxx.com"
git config --global user.name evern
```

### Install Python

```shell
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh > /tmp/Miniconda3-latest-Linux-x86_64.sh
bash /tmp/Miniconda3-latest-Linux-x86_64.sh
source ~/.zshrc
```

### Install Repo

```shell
sudo apt-get install curl

mkdir ~/usr/bin 											# 创建执行命令的目录，并将他放到PATH中。
echo "export PATH=~/usr/bin:\$PATH" >> ~/.zshrc 			# 如果使用的是bash就重定向到~/.bashrc
source ~/.zshrc 											# 同上如果是bash就source ~/.bashrc

curl https://mirrors.tuna.tsinghua.edu.cn/git/git-repo > ~/usr/bin/repo
chmod a+x ~/usr/bin/repo

echo "export REPO_URL='https://mirrors.tuna.tsinghua.edu.cn/git/git-repo/'" >> ~/.zshrc
source ~/.zshrc
```

### Get Platform Code

```shell
make -p ~/local/aosp
cd ~/local/aosp
repo init -u "https://android.googlesource.com/platform/manifest"
cd .repo/manifests
git pull
git branch -av 												# 查看所有分支，选取需要的Android版本分支
git checkout -b android-13.0.0_r9
cd ../..
repo sync -j4 												# 同步代码
```

## Make Code

### Install Java

```shell
sudo apt-get update
sudo apt-get install -y openjdk-8-jdk
```

### Make Init

```shell
source build/envsetup.sh 								# 初始化编译环境
lunch													# 选择编译版本

You're building on Linux

Lunch menu .. Here are the common combinations:
     1. aosp_arm-eng
     2. aosp_arm64-eng
     3. aosp_barbet-userdebug
     4. aosp_bluejay-userdebug
     5. aosp_bluejay_car-userdebug
     6. aosp_bramble-userdebug
     7. aosp_bramble_car-userdebug
     8. aosp_car_arm-userdebug
     9. aosp_car_arm64-userdebug
     10. aosp_car_x86-userdebug
     11. aosp_car_x86_64-userdebug
     12. aosp_cf_arm64_auto-userdebug
     13. aosp_cf_arm64_phone-userdebug
     14. aosp_cf_x86_64_foldable-userdebug
     15. aosp_cf_x86_64_only_auto-userdebug
     16. aosp_cf_x86_64_only_phone_hsum-userdebug
     17. aosp_cf_x86_64_pc-userdebug
     18. aosp_cf_x86_64_phone-userdebug
     19. aosp_cf_x86_64_tv-userdebug
     20. aosp_cf_x86_phone-userdebug
     21. aosp_cf_x86_tv-userdebug
     22. aosp_cheetah-userdebug
     23. aosp_cloudripper-userdebug
     24. aosp_coral-userdebug
     25. aosp_coral_car-userdebug
     26. aosp_flame-userdebug
     27. aosp_flame_car-userdebug
     28. aosp_oriole-userdebug
     29. aosp_oriole_car-userdebug
     30. aosp_panther-userdebug
     31. aosp_raven-userdebug
     32. aosp_raven_car-userdebug
     33. aosp_ravenclaw-userdebug
     34. aosp_redfin-userdebug
     35. aosp_redfin_car-userdebug
     36. aosp_redfin_vf-userdebug
     37. aosp_slider-userdebug
     38. aosp_sunfish-userdebug
     39. aosp_sunfish_car-userdebug
     40. aosp_trout_arm64-userdebug
     41. aosp_trout_x86-userdebug
     42. aosp_whitefin-userdebug
     43. aosp_x86-eng
     44. aosp_x86_64-eng
     45. arm_krait-eng
     46. arm_v7_v8-eng
     47. armv8-eng
     48. armv8_cortex_a55-eng
     49. armv8_kryo385-eng
     50. beagle_x15-userdebug
     51. beagle_x15_auto-userdebug
     52. car_ui_portrait-userdebug
     53. car_x86_64-userdebug
     54. db845c-userdebug
     55. gsi_car_arm64-userdebug
     56. gsi_car_x86_64-userdebug
     57. hikey-userdebug
     58. hikey64_only-userdebug
     59. hikey960-userdebug
     60. hikey960_tv-userdebug
     61. hikey_tv-userdebug
     62. poplar-eng
     63. poplar-user
     64. poplar-userdebug
     65. qemu_trusty_arm64-userdebug
     66. rb5-userdebug
     67. sdk_car_arm-userdebug
     68. sdk_car_arm64-userdebug
     69. sdk_car_md_x86_64-userdebug
     70. sdk_car_portrait_x86_64-userdebug
     71. sdk_car_x86-userdebug
     72. sdk_car_x86_64-userdebug
     73. sdk_pc_x86_64-userdebug
     74. silvermont-eng
     75. uml-userdebug
     76. yukawa-userdebug
     77. yukawa_sei510-userdebug

Which would you like? [aosp_arm-eng]
Pick from common choices above (e.g. 13) or specify your own (e.g. aosp_barbet-eng): aosp_x86_64-eng # 选择版本
# 这里想着使用windows上的模拟器进行运行，所以编译x86_64的版本，因为需要Debug所以编译eng的版本类型

Hint: next time you can simply run 'lunch aosp_x86_64-eng'

============================================
PLATFORM_VERSION_CODENAME=UpsideDownCake
PLATFORM_VERSION=UpsideDownCake
TARGET_PRODUCT=aosp_x86_64
TARGET_BUILD_VARIANT=eng
TARGET_ARCH=x86_64
TARGET_ARCH_VARIANT=x86_64
TARGET_2ND_ARCH=x86
TARGET_2ND_ARCH_VARIANT=x86_64
HOST_OS=linux
HOST_OS_EXTRA=Linux-5.10.16.3-microsoft-standard-WSL2-x86_64-Ubuntu-22.04.1-LTS
HOST_CROSS_OS=windows
BUILD_ID=AOSP.MASTER
OUT_DIR=out
============================================
```

### Start Make

```shell
make -j8 										# 以8线程进行编译
```

