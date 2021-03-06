# Auto Trade

## ENV

```bash
# Anaconda installed
pip install pandas
pip install numpy
pip install matplotlib
pip install mplfinance

pip install pandas_readdata
pip install tushare
pip install beautifulsoup4

pip install sklearn
pip install tensorflow # 2.2.0
# pip install tensorflow-gpu
pip install keras  # 2.3.1

pip install jupytor
pip install scipy
pip install scikit-learn

```

### anaconda

```bash
source /usr/local/anaconda3/bin/activate
conda activate py38
```
### install PostgresSQL
- Mac postgresapp

https://postgresapp.com/downloads.html

- Mac PgAdmin4 

https://www.postgresql.org/ftp/pgadmin/pgadmin4/

### Kubernetes

- Linux
- Docker
- Kubernetes
- Helm
- Terraform

### Postgres

- PostgreSQL
- PostGIS
- TimescaleDB
- Greenplum
- Redis
- Clickhouse
- Neo4j

### Python

- Python, Django, Numpy, Pandas, Matplotlib, pyplot, pyecharts
- Git, VSCode, Anaconda, Jupyter Notebook, JupyterLab
- 正则表达式
- ML 机器学习
- DL 深度学习
- RL 强化学习
- CNN, LSTM, NLP, Transformer, Attention 。。。


## 参考资料

- 《并行大数据处理：基于Python与PostgreSQL》：https://mp.weixin.qq.com/s/yuO4D2ySzL4FbbHc9BBArw

- 《深入浅出 Python 量化交易实战》，京东读书App

## 3.1 资料清单


以下各项中，第5、7、15项未标明出版社，因为它们是相关工具的手册，可到官网下载PDF版。

### 3.1.1 Python

#### 3.1.1.1 Python编程

[1] Allen B.Downey（著）, 赵普明（译）. 像计算机科学家一样思考Python（第2版）[M]. 人民邮电出版社, 2013.

[2] Mark Lutz（著），秦鹤，林明（译）. PYTHON学习手册（第5版）[M]. 机械工业出版社, 2014.

[3] Mark Lutz（著），邹晓，瞿乔，任发科等（译）. Python编程（第4版套装上下册）[M]. 中国电力出版社, 2014. 

[4] Giancarlo Zaccone（著），张龙，宋秉金（译）. Python并行编程参考手册[M].电子工业出版社, 2018.

[5] Python Tutorial Release, 3.9.2rc1，2021.

#### 3.1.1.2 Python数据分析

[6] Wes McKinney（著），徐敬一（译）. 利用Python进行数据分析（第2版）[M]. 机械工业出版社, 2018.

[7] pandas: powerful Python data analysis toolkit Release, 1.2.1，2021.

[8] Yves Hilpisch（著），姚军（译）. PYTHON金融大数据分析（第2版）[M]. 人民邮电出版社, 2020.

#### 3.1.1.3 Python机器学习

[9] Michael Bowles（著），沙嬴，李鹏（译）. Python机器学习预测分析核心算法[M].人民邮电出版社, 2016.

[10] Aurelien Geron（著），宋能辉，李娴（译）. 机器学习实战基于Scikit-Learn和TensorFlow [M]. 机械工业出版社, 2020.

#### 3.1.1.4 Python量化经济学（宏观、微观理论经济学方向）

Sargent 2015年有一本书，书名是《Quantitative Economics with Python》，其后一直都有更新。有配套网站（https://python.quantecon.org/intro.html）的，好像所有代码也都挂在Github上了。

### 3.1.2 PostgreSQL

[11] Ebola Ahmed（著），范翊，彭煜玮，唐成（译）. PostgreSQL 9X之巅（第2版）[M]. 机械工业出版社, 2018.

[12] Hironobu Suzuki（著）,冯若航，刘阳明，张文升（译）. PostgreSQL指南内幕探索[M]. 电子工业出版社, 2019.

[13] 唐成（著）. PostgreSQL修炼之道:从小工到专家（第2版）[M]. 机械工业出版社, 2020.

[14] 张树杰（著）. PostgreSQL技术内幕：查询优化深度探索[M].电子工业出版社, 2018.

[15] PostgreSQL 13.1 Documentation.

### 3.1.3 正则表达式

[16]Jeffrey E.F. Friedl（著），余晟（译）. 精通正则表达式（第3版）[M]. 电子工业出版社, 2012.

### 3.1.4. Docker与Kubernetes

[17] Sean，P.Kane，Karl，Matthias（著），安道（译）. Docker即学即用（第2版）[M]. 中国电力出版社, 2019.

[18] Kelsey Hightower，Brendan Burns，Joe Beda（著），韩波（译）. Kubernetes即学即用[M]. 中国电力出版社, 2018.

### 3.1.5 运维

[19] Betsy Beyer，Chris Jones，Jennifer Petoff，Niall Murphy （著），孙宇聪 （译）. Google运维解密[M].电子工业出版社，2016. 

[20] Betsy Beyer，Niall Murphy 等 （著），钟诚、刘征（译）. Google SRE工作手册[M].电子工业出版社，2020. 

## QA

## GitHub's file size limit of 100.00 MB解决办法

```bash
brew install git-lfs

git lfs install

find ./ -size +100M

git lfs track "name_of_a_giant_file"
#example:
git lfs track ".//examples/py_quant/aistudio/ml/svm1/work/cnews.train.txt"

git add path_of_a_giant_file
#example:
git add .//examples/py_quant/aistudio/ml/svm1/work/cnews.train.txt
```

- 删除某个文件的push

```bash
find ./ -size +10M

git filter-branch --force --index-filter "git rm --cached --ignore-unmatch app_zhongli_agent/android/java_pid93576.hprof"  --prune-empty --tag-name-filter cat -- --all

git commit --amend

git push
```