<center>
    <h1>
        Docker install Tensorflow
    </h1>
</center>

## 创建Tensorflow容器

创建使用最新cpu版本tensorflow创建docker容器，并测试tensorflow

安装文档[官网](https://www.tensorflow.org/install/docker)，这里默认安装的是cpu版本。

```shell
$ docker run -it --rm -p 10022:22 tensorflow/tensorflow \
   python -c "import tensorflow as tf; print(tf.reduce_sum(tf.random.normal([1000, 1000])))"
```