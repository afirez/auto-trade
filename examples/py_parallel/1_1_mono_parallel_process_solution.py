#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 21:57:15 2021

@author: wangjianxiong
"""

import pandas as pd
from   pandas import DataFrame

import gc   # garbage collector

import time





import psycopg2     # 该库用于在 python 中调用 postgreSQL

from  multiprocessing import Pool      # 用于控制并行执行的包



# 添加python搜索路径， 后续搜索导入的库包时，就会从该路径导入
# path = "/Users/wangjianxiong/Desktop/《并行大数据处理：基于Python、PostgreSQL及其他》/1_书稿_ing/2_各章图表、示例代码及附加资料/CH09_分布式并行处理/2_代码/"
path = f"/Users/afirez/studio/python/auto-trade/examples/py_parallel/"
import sys
sys.path.append(path)


import parallel_process_postgres as ppp   # 导入该模块，该模块专为分析裁判文书而写。





#####################
# 0. 准备工作



#    0.1 创建数据库连接

#  创建数据库 股票分析数据库 的连接 
conn, curs, engine = ppp.creat_conn_with_pg(dbname='stock_data_for_test')

#  创建数据库 stock_data 的连接 
conn2, curs2, engine2 = ppp.creat_conn_with_pg(dbname='stock_data')




#    0.2 给出并行执行进程数

parallel_procedure_number = 3



#    0.3 给出当前日期

time_local           = time.localtime()       # 提取本地时间
date_of_today        = time.strftime("%Y-%m-%d", time_local)   # 转为表示日期的字符串




#####################
# 1. 在数据库中创建数据表 a_1_4_日度股票交易情况统计表 ，用于存储计算结果

try:
    #   4.1 为了避免出现已存在错误，先删除
    curs.execute("""DROP TABLE a_1_4_日度股票交易情况统计表;""")
    conn.commit()
except:
    conn.rollback()
    
try:
    #   4.2 建数日度股票交易情况统计表
    curs.execute("""CREATE TABLE a_1_4_日度股票交易情况统计表
                           (交易日期           date           NOT NULL,
                            
                            全部成交量         numeric(20,0)  DEFAULT -1,
                            全部成交额         numeric(20,0)  DEFAULT -1,
                            
                            上证主板成交量     numeric(20,0)  DEFAULT -1,
                            上证主板成交额     numeric(20,0)  DEFAULT -1,
                            
                            深证主板成交量     numeric(20,0)  DEFAULT -1,
                            深证主板成交额     numeric(20,0)  DEFAULT -1,
                            
                            中小板成交量       numeric(20,0)  DEFAULT -1,
                            中小板成交额       numeric(20,0)  DEFAULT -1,
                            
                            创业板成交量       numeric(20,0)  DEFAULT -1,
                            创业板成交额       numeric(20,0)  DEFAULT -1,
                            
                            科创板成交量       numeric(20,0)  DEFAULT -1,
                            科创板成交额       numeric(20,0)  DEFAULT -1
                            );""")

    #   4.3 添加索引
    curs.execute("""CREATE INDEX a_1_4_交易日期 ON a_1_4_日度股票交易情况统计表 (交易日期);"""
                 )
                            
    conn.commit()
    
    print('a_1_4_日度股票交易情况统计表 创建成功')
    
except Exception as e:
    print(e)
    conn.rollback()
    print('a_1_4_日度股票交易情况统计表 创建失败')





#  1.2 在数据库中创建任务分配表，用于存储分组信息及分组处理进度信息




#    1.2.1 创建 parallel_tool_并行任务分配信息表    

    
# 读入交易日期列表
df = pd.read_sql_query("""SELECT *
                                   FROM   a_1_0_交易日期表;""",
                        con = engine2)


# 仅保留所需变量
df = df[['交易日期',
         ]]

# 增加处理状态标记变量
df['处理状态'] = 0



#    1.2.2 写入数据库   

df.to_sql('parallel_tool_并行任务分配信息表',
          engine,
          index     = False,
          if_exists = 'replace')    # 写入数据库  还有一个参数是  append，那是附加在表后

# 添加索引
curs.execute("""CREATE  INDEX parallel_tool_1      ON  parallel_tool_并行任务分配信息表  (交易日期); 
                CREATE  INDEX parallel_tool_2      ON  parallel_tool_并行任务分配信息表  (处理状态);"""
            )
conn.commit()


#####################
# 2. 基于“分组”，进行并行计算


#    2.0 准备工作：清空分组处理记录，以便重新开始

# 如果首次执行，则执行以下操作：将所有处理记录归零
curs.execute("""UPDATE     parallel_tool_并行任务分配信息表
                   SET     处理状态     = %s;""", 
               (0,
                ))
conn.commit()







#    2.1 创建并行执行函数
def foo(i, process_num):
  
    
    #  创建数据库 股票分析数据库 的连接 
    conn, curs, engine = ppp.creat_conn_with_pg(dbname='stock_data_for_test')
    
    #  创建数据库 stock_data 的连接 
    conn2, curs2, engine2 = ppp.creat_conn_with_pg(dbname='stock_data')
    
    
    count_bat = 0
    while True:
        
        
        
        ##########################
        #   2.1.0 设定退出条件：如果所有分组数据都被处理，则退出
        
        df  = pd.read_sql_query("""SELECT   *
                                              FROM parallel_tool_并行任务分配信息表 
                                                WHERE 处理状态  = 0          --  未被处理
                                                --LIMIT(1000)                              -- 不能仅仅取一部分，应该全部都要取出来，不然会出错！！！（因为每次取到的，是同一批？）
                                                ;""",    
                                 con    = engine)  # 读取数据
        
        # 如果满足条件的小组不存在，则跳出循环：此时，已经处理完毕
        if len(df) == 0:
            conn.close()         # 断了数据库连接
            conn2.close()         # 断了数据库连接
            break
        
        

        ##########################
        #   2.1.1 导入待处理数据          
        
        #      2.1.1.0 准备阶段
        
        # 给出需要导入数据的“日期”：根据哈希运算结果，取一个
        df['hash_num']    = df['交易日期'].apply(hash)                       # 原理：先做哈希运算，再通过取余数分组，并将“余数等于子进程编号相同”的组留下）   
        # df['process_num'] = df['hash_num'].apply(lambda x: x%100000)
        # df['process_num'] = df['process_num'].apply(lambda x: x%process_num)        # 先对一个大数求余，再继续求余，就能获得一个均衡的结果！
        df['process_num'] = df['hash_num'].apply(lambda x: x%process_num)        # 先对一个大数求余，再继续求余，就能获得一个均衡的结果！
        
        
        """
        方案缺陷说明：
            本方案无法完成全部数据的处理，因为上述通过Python的内置哈希函数hash()进行任务分配的机制，在多进程环境下，会导致部分数据始终不会被处理。     
        
        具体原因在于：
            尽管哈希函数仅需要传入一个字符串作为参数，但其实每个进程在打开的时候，已经自动设定了一个跟该进程绑定的参数作为随机种子。
            故而即使是同一个字符串，在不同进程中，经哈希运算后得到的结果是不同的。故而，通过哈希运算来分配任务，并不能进行完备划分。 
        
        """
        
        
        
        
        print(len(df),'进程编号为 {}'.format(i))
            
        date_list = list(df[df['process_num'] == i]['交易日期'])
        
        if len(date_list) > 0:              # 也有可能目前这一批取出来的，都没有满足条件的，那就暂停3秒，再取下一批（暂停3秒，是防止一直读数据库，增加服务器压力）
            date      = date_list[0]
        else:
            print('本轮未取到合适的，暂停3秒，等下一批')
            time.sleep(3)
            continue





        #      2.1.1.1 正式导入数据
        
        
        # 读入全部市场当日的股票成交量和成交额到 total_num_df 
        total_num_df = pd.read_sql_query("""SELECT
                                                    SUM(成交量)   AS   全部成交量, 
                                                    SUM(成交额)   AS   全部成交额
                                         
                                            FROM          a_1_个股日度数据表
                                            WHERE            交易日期 = %s;""",
                                          con = engine2,
                                          params = (date,))
        
        # 读入上证主板当日的股票成交量和成交额到 shangHai_main_num_df 
        shangHai_main_num_df = pd.read_sql_query("""SELECT
                                                            SUM(成交量)   AS 上证主板成交量, 
                                                            SUM(成交额)   AS 上证主板成交额
                                       
                                                    FROM             a_1_个股日度数据表
                                                    WHERE          交易日期 = %s;""",
                                                  con = engine2,
                                                  params = (date,))
        
        # 读入深证主板当日的股票成交量和成交额到szse_num_df 
        shenZhen_main_num_df = pd.read_sql_query("""SELECT
                                                            SUM(成交量)  AS 深证主板成交量, 
                                                            SUM(成交额)  AS 深证主板成交额
                                        
                                                     FROM            a_1_个股日度数据表
                                                    WHERE            证券代码  LIKE   '000%%'
                                                      AND            交易日期 = %s;""",
                                                  con = engine2,
                                                  params = (date,))
        
        # 读入中小板当日的股票成交量和成交额到 sme_board_num_df 
        sme_board_num_df = pd.read_sql_query("""SELECT 
                                                        SUM(成交量)   AS    中小板成交量, 
                                                        SUM(成交额)    AS   中小板成交额
                                       
                                                 FROM                a_1_个股日度数据表
                                                WHERE                证券代码 LIKE  '002%%'
                                                  AND                交易日期 = %s;""",
                                              con = engine2,
                                              params = (date,))
        
        # 读入创业板当日的股票成交量和成交额到 gem_board_num_df 
        gem_board_num_df = pd.read_sql_query("""SELECT
                                                        SUM(成交量)    AS    创业板成交量, 
                                                        SUM(成交额)    AS    创业板成交额
                                       
                                                 FROM               a_1_个股日度数据表
                                                WHERE               市场类型 = 16
                                                  AND               交易日期 = %s;""",
                                              con = engine2,
                                              params = (date,))
        
        # 读入科创板当日的股票成交量和成交额到 sci_tech_board_num_df 
        sci_tech_board_num_df = pd.read_sql_query("""SELECT
                                                             SUM(成交量)   AS  科创板成交量, 
                                                             SUM(成交额)   AS  科创板成交额
                                            
                                                      FROM              a_1_个股日度数据表
                                                     WHERE              市场类型 = 32
                                                       AND              交易日期 = %s;""",
                                                   con = engine2,
                                                   params = (date,))
        
        
        
        
        ##########################
        #      2.1.2 合并数据

        table_num_list = [total_num_df, shangHai_main_num_df, shenZhen_main_num_df, sme_board_num_df, gem_board_num_df, sci_tech_board_num_df]
        
        total_nums_df = DataFrame({'交易日期':[]})
        
        # 遍历合并
        for table_num_df in table_num_list:
            
            table_num_df['交易日期'] = date
            total_nums_df = pd.merge(total_nums_df,table_num_df, how = 'outer', on='交易日期')
        
        
        # 缺失值填充：将 total_num_df 中的 Nan值 填入 默认值 -1 
        total_nums_df.fillna(-1, inplace = True)
        
        
        
        
        
        ##########################
        #      2.1.3 写入数据库
            
            
        # 给出待写入数据 
        columns_str = total_nums_df.columns        # 列名组合
        nums = total_nums_df.values                # 各列内容
        
        
        # 写入数据
        sql = f"insert into {'a_1_4_日度股票交易情况统计表'}({','.join(columns_str)}) values %s;"
        
        try:
            
            # 使用psycopg2包将数据插入至数据表中
            psycopg2.extras.execute_values(curs,sql,nums)
            conn.commit()
            
        except Exception as e:
            print(e)
            conn.rollback()
                
        
        # 手动删除对象，释放内存
        del (total_num_df,
             shangHai_main_num_df, 
             shenZhen_main_num_df, 
             sme_board_num_df, 
             gem_board_num_df, 
             sci_tech_board_num_df, 
             total_nums_df)
                
        
        
        
        
        ##########################
        #   2.1.Final 更新数据处理进度

        
        
        # 在数据库中标记：该小组已经处理完毕
        curs.execute("""UPDATE      parallel_tool_并行任务分配信息表
                            SET     处理状态              = %s   
                            WHERE   交易日期              = %s;""", 
                       (1,                                   # 用 1 表示该小组已经处理完毕
                        date,
                        ))
        conn.commit()
        
        
        
        # 给出未被处理的小组，以供进度显示所需
        df  = pd.read_sql_query("""SELECT   *
                                              FROM parallel_tool_并行任务分配信息表 
                                                WHERE 处理状态  = 0          --  未被处理
                                                      ;""",    
                                 con    = engine)  # 读取数据
        
        
        # 累计并显示进度        
        count_bat += 1  
        if count_bat%1 == 0:
            print('代码文件 1_1_单机版_分布式并行计算方案_*.py 的第2步-->>> 第 {} 个子进程工作进度：已完成第 {} 组的数据处理，还有 {} 组数据等待处理 '.format(i, count_bat, len(df)))
 
    
        del df  # 手动删对象
        
        # 清理内存
        if count_bat%10 == 0:
            gc.collect()
            

    return None



#    2.2 调用并行执行函数         (MacOS上的新版 Spyder，并行也只能在“__name__ == '__main__'”在进行了？)

if __name__ == '__main__':
    
                
    t_start=time.time()
    pool = Pool(parallel_procedure_number) # parallel_procedure_number 给出了并行执行的进程数
    
    for i in range(parallel_procedure_number):
        time.sleep(10)    # 缺省值设成了 0.1，实际运行设高一点，以免各个进程在查询数据库时相互竞争...
        print('提醒：正在开启第 {} 个并行子进程'.format(i))
        pool.apply_async(foo, (i, parallel_procedure_number))
    pool.close()
    pool.join()  # 进程池中进程执行完毕后再关闭，如果注释，那么程序直接关闭。
    
    # 给出当前日期、时间信息
    time_local    = time.localtime()       # 提取本地时间
    date_now      = time.strftime("%Y-%m-%d", time_local)   # 转为表示日期的字符串
    time_now      = time.strftime("%H时%M分", time_local)   # 转为表示小时和分钟的字符串
    print('现在是 {} ，本次数据处理已执行完毕'.format(time_now))    
    
    
    
    
    
        
             
    #######################################        
            
    # Final. 做最后处理，并断开主进程的数据库连接
    
    
    
    
    # 删除任务分配表        
    curs.execute("""
                    DROP     table parallel_tool_并行任务分配信息表;
                    """)   
    conn.commit()   
    
    
    
    
    
    # 断开主进程的数据库连接
    conn.close()
    conn2.close()
