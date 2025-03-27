from abc import ABC, abstractmethod
import os

class DataHandler(ABC):
    """数据操作抽象基类"""
    def __init__(self, connection_params):
        self.conn_params = connection_params
        self.repo_name = self._get_repo_name()

    def _get_repo_name(self):
        """智能生成默认数据仓库名，同时允许用户自定义文件名"""

        if 'repo_name' in self.conn_params:
            return self.conn_params['repo_name']

        current_path = os.path.dirname(os.path.abspath(__file__))
        current_folder_name = os.path.basename(current_path)
        return current_folder_name
    
    @abstractmethod
    def load_repository(self):
        raise NotImplementedError
    
    @abstractmethod
    def append_data(self, data: list):
        raise NotImplementedError
    
    @abstractmethod
    def save_data(self):
        raise NotImplementedError

    @abstractmethod
    def close_repository(self):
        raise NotImplementedError

class ExcelHandler(DataHandler):  # todo: pd也能导出csv
    """Excel文件处理器"""
    def __init__(self, connection_params):  # 这里为什么又是None了，下面的 or {}又是什么意思
        super().__init__(connection_params or {})
        self.repo_name = f"{self.repo_name}.xlsx"
        self.repo = self.load_repository()

    def load_repository(self):
        """动态选择加载方法"""
        load_method = getattr(self, '_load_openpyxl', self._load_pandas)
        return load_method()

    # def _load_openpyxl(self):
    #     """openpyxl实现（注释本方法则自动切换pandas）"""
    #     from openpyxl import load_workbook, Workbook
    #     # 判断文件是否存在
    #     if os.path.exists(self.repo_name):
    #         # 如果存在，使用 openpyxl 读取
    #         wb = load_workbook(self.repo_name)
    #         ws = wb.active

    #         print(f"文件 {self.repo_name} 已导入，内容如下：")
    #         for row in ws.iter_rows(min_row=1, max_row=6, values_only=True):
    #             print(row)
    #     else:
    #         # 创建新的 Excel 文件
    #         wb = Workbook()
    #         ws = wb.active
    #         # 写入标题行
    #         ws.append(self.conn_params["columns"])  # todo

    #         # 如果 index 为 True，插入索引列
    #         if index:  # todo: index 和 index_col_name
    #             columns.insert(0, index_col_name)
    #         # 保存文件
    #         wb.save(self.repo_name)

    #         print(f"文件 {self.repo_name} 不存在，已创建空文件。")

    #     return wb

    def _load_pandas(self):
        """pandas默认实现"""
        import pandas as pd
        # 判断文件是否存在
        if os.path.exists(self.repo_name):
            # 如果存在，使用 Pandas 读取
            df = pd.read_excel(self.repo_name)
            # # 如果 index 为 True，设置 index_name 列为索引
            # if index:  # todo: index 和 index_col_name
            #     df.set_index(index_name, inplace=True)
                
            print(f"文件 {self.repo_name} 已导入，内容如下：")
            print(df.head())  # 显示前几行数据
        else:
            # 创建空的 DataFrame
            df = pd.DataFrame(columns=self.conn_params["columns"])  # todo

            # # 如果 index 为 True，新增 index_name 索引列
            # if index:  # todo: index 和 index_col_name
            #     df.insert(0, index_name, value='')
            #     df.set_index(index_name, inplace=True)
            # # todo: 提示语句

        return df

    def append_data(self, data: list):
        """动态选择添加数据方法"""
        append_method = getattr(self, "_append_openxyl", self._append_pandas)
        append_method(data)

    # def _append_openxyl(self, data):
    #     """openpyxl添加数据实现"""
    #     # data[#] = re.sub(r'[\x00-\x1F\x7F]', '', data[#])  # 需要处理 HTML 编码的话取消注释
    #     self.repo.active.append(data)
    
    def _append_pandas(self, data):
        """pandas添加数据实现"""
        # data[#] = re.sub(r'[\x00-\x1F\x7F]', '', data[#])  # 需要处理 HTML 编码的话取消注释
        self.repo.loc[len(self.repo)] = data

    def save_data(self):
        """动态选择保存方法"""
        save_method = getattr(self, '_save_openpyxl', self._save_pandas)
        save_method()

    # def _save_openpyxl(self):
    #     """openpyxl保存实现"""
    #     self.repo.save(self.repo_name)
    #     print(f"数据已保存至 {self.repo_name}")

    def _save_pandas(self):
        """pandas保存实现"""
        self.repo.to_excel(self.repo_name, index=False)
        print(f"数据已保存至 {self.repo_name}")

    def close_repository(self):
        if hasattr(self.repo, 'close') and self.repo is not None:  # 处理 openpyxl 的 Workbook 对象
            self.repo.close()
        else:  # Pandas DataFrame 无需关闭
            pass

class SQLAlchemyHandler(DataHandler):
    """关系型数据库处理器 (支持SQLAlchemy)"""
    def __init__(self, connection_params):
        super().__init__(connection_params)
        from sqlalchemy import create_engine
        from sqlalchemy.orm import Session
        self.engine = create_engine(
            connection_params['url'],
            # connect_args={
            #     'charset': 'utf8mb4',
            #     'use_unicode': True,
            #     'collation': 'utf8mb4_unicode_ci',
            #     'init_command': "SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci"
            # }
        )
        self.session = Session(self.engine)
        # self.inspector = inspect(self.engine)  # todo: 是否删除包括import
        self.table = self.load_repository()

    def load_repository(self):
        from sqlalchemy import inspect

        table_is_exist = inspect(self.engine).has_table(self.repo_name)
        # 判断表是否存在
        if not table_is_exist:
            
            # # 定义标题行
            # columns = [
            # ]
            # # 创建空的 DataFrame，指定列名
            # df = pd.DataFrame(columns=columns)

            # # 如果 index 为 True，新增 index_name 索引列
            # if index:  # todo: index 和 index_col_name
            #     df.insert(0, index_name, value='')
            #     df.set_index(index_name, inplace=True)
            # # todo: 提示语句
            
            # 创建新表的逻辑
            from sqlalchemy import Column, Integer, String, Text, Float
            from sqlalchemy.ext.declarative import declarative_base
            Base = declarative_base()
            
            class HouseInfo(Base):  # todo
                __tablename__ = self.repo_name
                id = Column(Integer, primary_key=True, autoincrement=True)
                title = Column(String(200))
                layout = Column(String(50))
                head_ing = Column(String(10))
                price = Column(Float)
                unit_price = Column(Float)
                area = Column(Float)
                floor = Column(String(20))
                build_year = Column(String(10))
                building_type = Column(String(10))
                distinct  = Column(String(20))
                sq = Column(String(20))
                community_name = Column(String(20))
                address = Column(String(100))
                imgs_url = Column(Text)
                tag = Column(Text)
                url = Column(String(100))
                # ... 其他字段定义
                
            Base.metadata.create_all(self.engine)
            print(f"[SQL] 已创建新表 {self.repo_name}")

        from sqlalchemy.ext.automap import automap_base
        base = automap_base()
        base.prepare(self.engine, reflect=True)
        # 如果存在，使用 SQLAlchemy ORM 读取，支持异步
        table = base.classes[self.repo_name]  # todo: 如果对象表名变了

        # # todo: 如果存在，使用 SQLAlchemy Core 读取，检索速度更快
        # from sqlalchemy import Table, MetaData
        # table = Table(self.repo_name, MetaData(), autoload=True, autoload_with=self.engine)
        # # 如果 index 为 True，设置 index_name 列为索引
        # if index:
        #     df.set_index(index_name, inplace=True)
        
        if table_is_exist:
            print(f"表 {self.repo_name} 已导入，内容如下：")
            columns = [c.name for c in table.__table__.columns]
            results = self.session.query(table).limit(5).all()
            print(columns)
            for row in results:
                print([getattr(row, c) for c in columns])
            # for i, row in enumerate(results, 1):
            #     values = [str(getattr(row, col)) for col in columns]
            #     print(f"Row {i}: {' | '.join(values)}")

        return table

    def append_data(self, data: list):
        """使用 SQLAlchemy ORM 插入数据"""
        try:
            # 获取表的列名列表
            columns = [c.name for c in self.table.__table__.columns if c.name != 'id']
            
            # 创建数据字典（排除自增主键）
            data_dict = dict(zip(columns, data))
            
            # 创建 ORM 对象实例
            new_record = self.table(**data_dict)
            
            # 仅添加不提交
            self.session.add(new_record)
            print(f"[SQL] 数据已暂存至表 {self.repo_name}")
            
        except Exception as e:
            self.session.rollback()
            print(f"[SQL 错误] 写入失败: {str(e)}")

    def save_data(self):
        """提交事务到数据库"""
        try:
            self.session.commit()
            print(f"[SQL] 事务已提交到表 {self.repo_name}")
        except Exception as e:
            self.session.rollback()
            print(f"[SQL 错误] 提交失败: {str(e)}")

    def close_repository(self):
        """关闭会话前自动提交"""
        if self.session.is_active:
            self.save_data()
        self.session.close()

class RedisHandler(DataHandler):
    """Redis数据库处理器"""
    def __init__(self, connection_params):
        super().__init__(connection_params)
        import redis
        self.client = redis.Redis(
            host=connection_params.get('host', 'localhost'),
            port=connection_params.get('port', 6379),
            db=connection_params.get('db', 0)
        )
    
    def append_data(self, data: list):
        """暂存数据到内存列表"""
        if not hasattr(self, '_temp_data'):
            self._temp_data = []
        self._temp_data.append(data)
        print(f"[Redis] 数据已暂存到内存列表 {self.repo_name}")

    def save_data(self):
        """批量写入Redis"""
        try:
            import json
            if hasattr(self, '_temp_data'):
                # 批量插入数据
                pipe = self.client.pipeline()
                for data in self._temp_data:
                    pipe.rpush(self.repo_name, json.dumps(data))
                pipe.execute()
                
                print(f"[Redis] 已提交 {len(self._temp_data)} 条数据到列表 {self.repo_name}")
                del self._temp_data
        except Exception as e:
            print(f"[Redis 错误] 写入失败: {str(e)}")

    def close_repository(self):
        """关闭前自动保存"""
        self.save_data()
        self.client.close()

# 工厂方法
def get_handler(handler_type: str, **kwargs):  # todo: 通过get_handler.xxx方式调用
    handlers = {
        'excel': ExcelHandler,
        # 支持 ORM 的数据库调用 SQLAlchemyHandler
        'mysql': SQLAlchemyHandler,
        # 其他数据库处理器
        'redis': RedisHandler,
    }
    return handlers[handler_type](kwargs)