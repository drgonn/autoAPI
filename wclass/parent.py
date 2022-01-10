import os
from tools import  name_convert

# 表里一列




class Parent(object):
    def __init__(self, name, index, post, put, list,  mean, show):
        self.Name = name
        self.index = index
        self.post = post
        self.put = put
        self.list = list
        self.mean = mean
        self.show = show

        self.name = name_convert(name)
        self.names = self.name + "s"

        # 注释当中标注是否必须的str
        self.commit_need_str = "require" if self.post == 2 else "optional"

    def format_str(self, fm, tab_num):
        t = "    "
        s = ""
        if fm == "list_commit":
            if self.list:
                s = f"{t*tab_num}{self.name}_id (int optional): {self.mean}主键ID\n"
        elif fm == "return_commit":
            s = f"{t*tab_num}{self.name} ({self.type} optional): {self.mean}\n"        
        elif fm == "post_commit":
            if self.post:
                commit_need_str = "require" if self.post == 2 else "optional"
                s = f"{t*tab_num}{self.name}_id (int, {commit_need_str}): {self.mean}主键ID\n"
        elif fm == "commit_table":
            s += f"{t*tab_num}{self.name}_id: 父表{self.names}的ID\n"
            s += f"{t*tab_num}{self.name}: 父表{self.names}对象\n"

        elif fm == "flask_api_post_equal":
            if self.post:
                s = f"{t*tab_num}{self.name}_id={self.name}.id,\n"
            elif self.Name == 'User':
                s = f"{t*tab_num}user=g.current_user,\n"
                
        elif fm == "flask_api_post_verify":
            if self.post:
                s += f"\n{t}{self.name}_{self.index} = request.json.get('{self.name}_id')\n"
                if self.post == 2:
                    s += f"{t}{self.name} = {self.Name}.query.filter_by({self.index}={self.name}_{self.index}).first()\n"
                    s += f"{t}if {self.name} is None:\n"
                    s += f"{t}{t}return jsonify({{'success': False, 'error_code': -1, 'errmsg': '{self.name}不存在'}})\n"

        elif fm == "flask_model_detail":
            s += f"{t}{self.name}_id = db.Column(db.Integer, db.ForeignKey('{self.name}s.id'))\n"
            s += f"{t}{self.name} = db.relationship('{self.Name}', backref=db.backref('{self.table_name}s', lazy='dynamic'))\n"
        elif fm == "flask_model_to_json":
            if self.show is not None:
                for sho in self.show:
                    s_name = sho['name']
                    s += f"{t*tab_num}'{self.name}_{s_name}': self.{self.name}.{s_name} if self.{self.name} else None,\n"
                    s += f"{t*tab_num}'{self.name}_id': self.{self.name}.id if self.{self.name} else None,\n"
   

        return s    


class Many(object):
    def __init__(self, name,  w_model, add_api,  mean, prefix):
        self.Name = name
        self.w_model = w_model
        self.add_api = add_api
        self.mean = mean
        self.prefix = prefix

        self.name = name_convert(name)
        self.names = self.name + "s"

    def format_str(self, fm, tab_num):
        t = "    "
        s = ""
        if fm == "flask_model_map_table":
            if self.w_model:
                s += f"{self.table_name}_{self.prefix}{self.name} = db.Table(\n{t}'{self.table_name}_{self.prefix}{self.name}',\n"
                s += f"{t}db.Column('{self.table_name}_id', db.Integer, db.ForeignKey('{self.table_name}s.id')),\n"
                s += f"{t}db.Column('{self.name}_id', db.Integer, db.ForeignKey('{self.name}s.id'))\n)\n\n"
        elif fm == "flask_model_relation":
            if self.w_model:
                    s += f"\n{t}{self.prefix}{self.names} = db.relationship('{self.Name}',\n"
                    s += f"{t}{t}secondary={self.table_name}_{self.prefix}{self.name},\n"
                    s += f"{t}{t}backref=db.backref('{self.prefix}{self.table_name}', lazy='dynamic'),\n"
                    s += f"{t}{t}lazy='dynamic')\n"
        elif fm == "flask_api_post":
            s += f"{t*tab_num}{self.prefix}{self.name}_ids = request.json.get('{self.prefix}{self.name}_ids') or []\n"
            s += f"{t*tab_num}for {self.name}_id in {self.prefix}{self.name}_ids:\n"
            s += f"{t*tab_num}{t}{self.name} = {self.Name}.query.filter_by(id={self.name}_id).first()\n"
            s += f"{t*tab_num}{t}if {self.name} is None:\n"
            s += f"{t*tab_num}{t}{t}return jsonify({{'success':False, 'error_code':-1, 'errmsg':'{self.name}ID不存在'}})\n"
            s += f"{t*tab_num}{t}{self.table_name}.{self.prefix}{self.name}s.append({self.name})\n\n"
        elif fm == "flask_api_put":
            s += f"\n{t*tab_num}{self.prefix}{self.name}_ids = request.json.get('{self.prefix}{self.name}_ids')\n"
            s += f"{t*tab_num}if {self.prefix}{self.name}_ids is not None:\n"
            s += f"{t*tab_num}{t}original_ids = [i.id for i in {self.table_name}.{self.prefix}{self.names}]\n"
            s += f"{t*tab_num}{t}add_ids = list(set({self.prefix}{self.name}_ids).difference(set(original_ids)))\n"
            s += f"{t*tab_num}{t}remove_ids = list(set(original_ids).difference(set({self.prefix}{self.name}_ids)))\n"
            s += f"{t*tab_num}{t}for {self.name}_id in add_ids:\n"
            s += f"{t*tab_num}{t}{t}{self.name} = {self.Name}.query.filter_by(id={self.name}_id).first()\n"
            s += f"{t*tab_num}{t}{t}if {self.name} is None:\n"
            s += f"{t*tab_num}{t}{t}{t}return jsonify({{'success':False, 'error_code':-1, 'errmsg':'{self.name}ID不存在'}})\n"
            s += f"{t*tab_num}{t}{t}if {self.name}.{self.table_name}_id is not None:\n"
            s += f"{t*tab_num}{t}{t}{t}return jsonify({{'success':False, 'error_code':-1, 'errmsg':'{self.name} 已在其他分组'}})\n"
            s += f"{t*tab_num}{t}{t}{self.table_name}.{self.prefix}{self.name}s.append({self.name})\n"
            s += f"{t*tab_num}{t}for {self.name}_id in remove_ids:\n"
            s += f"{t*tab_num}{t}{t}{self.name} = {self.Name}.query.filter_by(id={self.name}_id).first()\n"
            s += f"{t*tab_num}{t}{t}{self.table_name}.{self.prefix}{self.name}s.remove({self.name})\n"
        elif fm == "flask_api_list":
            s += f"{t*tab_num}{self.prefix}{self.name}_id = request.args.get('{self.prefix}{self.name}_id')\n"
            s += f"{t*tab_num}if {self.prefix}{self.name}_id is not None:\n"
            s += f"{t*tab_num}{t}{self.name} = {self.Name}.query.filter_by(id={self.prefix}{self.name}_id).first()\n"
            s += f"{t*tab_num}{t}if {self.name} is None:\n"
            s += f"""{t*tab_num}{t}{t}return jsonify({{'success': False, 'error_code': -1, 'errmsg': f'{self.prefix}{self.name}: {{{self.prefix}{self.name}_id}}不存在'}})\n"""
            s += f"{t*tab_num}{t}else:\n"
            s += f"{t*tab_num}{t}{t}total_{self.table_name} = {self.name}.{self.table_name}s\n\n"
        return s



class Son(object):
    def __init__(self, name, to_json,add):
        self.Name = name
        self.to_json = to_json
        self.add = add   # 创建和修改中可以关联子表的功能

        self.name = name_convert(name)
        self.names = self.name + "s"

    # def make_mean(self,tabs):


