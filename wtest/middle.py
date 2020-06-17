import os
import random
import json
import string
import html

def single_str(zh,typezh,host,port,protocol,path,method,pjson,argaddr,bean):
    get_json = f"""
          <JSONPostProcessor guiclass="JSONPostProcessorGui" testclass="JSONPostProcessor" testname="JSON提取" enabled="true">
            <stringProp name="JSONPostProcessor.referenceNames">temparg</stringProp>
            <stringProp name="JSONPostProcessor.jsonPathExprs">{argaddr}</stringProp>
            <stringProp name="JSONPostProcessor.match_numbers"></stringProp>
            <stringProp name="JSONPostProcessor.defaultValues">null1</stringProp>
          </JSONPostProcessor>
          <hashTree/>
    """ if argaddr else ""
    beanshell = f"""
          <BeanShellPostProcessor guiclass="TestBeanGUI" testclass="BeanShellPostProcessor" testname="BeanShell 后置处理程序" enabled="true">
            <stringProp name="filename"></stringProp>
            <stringProp name="parameters"></stringProp>
            <boolProp name="resetInterpreter">false</boolProp>
            <stringProp name="script">${{__setProperty({bean},${{temparg}},)}}</stringProp>
          </BeanShellPostProcessor>
          <hashTree/>
    """ if bean else ""

    assertion = f"""
              <ResponseAssertion guiclass="AssertionGui" testclass="ResponseAssertion" testname="ret 为True" enabled="true">
                <collectionProp name="Asserion.test_strings">
                  <stringProp name="-1952278985">&quot;ret&quot;: true</stringProp>
                </collectionProp>
                <stringProp name="Assertion.custom_message"></stringProp>
                <stringProp name="Assertion.test_field">Assertion.response_data</stringProp>
                <boolProp name="Assertion.assume_success">false</boolProp>
                <intProp name="Assertion.test_type">2</intProp>
              </ResponseAssertion>
              <hashTree/>
        """
    testapi = f"""
            <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="{zh}{typezh}" enabled="true">
              <boolProp name="HTTPSampler.postBodyRaw">true</boolProp>
              <elementProp name="HTTPsampler.Arguments" elementType="Arguments">
                <collectionProp name="Arguments.arguments">
                  <elementProp name="" elementType="HTTPArgument">
                    <boolProp name="HTTPArgument.always_encode">false</boolProp>
                    <stringProp name="Argument.value">{pjson}</stringProp>
                    <stringProp name="Argument.metadata">=</stringProp>
                  </elementProp>
                </collectionProp>
              </elementProp>
              <stringProp name="HTTPSampler.domain">{host}</stringProp>
              <stringProp name="HTTPSampler.port">{port}</stringProp>
              <stringProp name="HTTPSampler.protocol">{protocol}</stringProp>
              <stringProp name="HTTPSampler.contentEncoding">utf-8</stringProp>
              <stringProp name="HTTPSampler.path">{path}?token=${{__property(newtoken)}}</stringProp>
              <stringProp name="HTTPSampler.method">{method}</stringProp>
              <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
              <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
              <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
              <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
              <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
              <stringProp name="HTTPSampler.connect_timeout"></stringProp>
              <stringProp name="HTTPSampler.response_timeout"></stringProp>
            </HTTPSamplerProxy>
            <hashTree>
    {assertion}
    {get_json}
    {beanshell}
            </hashTree>
        """
    return testapi

def random_arg(type):
    if type == 'str':
        return ''.join(random.sample(string.ascii_letters + string.digits, 8))
    elif type == "float":
        return round(random.uniform(1, 100),3)
    elif type == "bool":
        return random.randint(0,1)
    elif type == "int":
        return random.randint(0,3)




def write_middle(root,ojson):
    app = ojson.get('app')
    testdoc = os.path.join(root, f'{app}/jMeter/{app}_test.jmx')
    w = open(testdoc,'a')
    crud = [("创建","POST",'',False),
            ("列表","POST",'/list','$.data.records[-1].id'),
            ("单个获取","GET",'/<id>',False),
            ("修改","PUT",'/<id>',False),
            ]
    host=ojson.get("testhost")                             #
    port = ojson.get("testport")                                #
    protocol= ojson.get("testprotocol")                             #
    for table in ojson.get('databases'):
        if table.get('api'):
            zh = table.get('zh')
            tablename = table.get("table").lower()
            pjson = {}
            for typezh,method,p,argaddr in crud:
                path = f"/api/v1/order/{tablename}"
                bean = False
                if typezh == "创建":
                    for column in table.get('args'):
                        if column.get('need'):
                            argname = column.get('name')
                            argtype = column.get('type')
                            pjson[argname] = random_arg(argtype)
                    for column in table.get('parents'):
                        pclass = column.get('name')
                        if column.get('postmust') and column.get('name') != 'User':
                            argname = column.get('name').lower()+ "Id"
                            argtype = column.get('type')
                            pjson[argname] = f'${{__property({pclass}_id)}}'
                elif typezh == "列表":
                    pjson['pageindex'] = 10000
                    bean = f"{table.get('table')}_id"
                elif typezh == "修改":
                    pjson = {}
                    for column in table.get('args'):
                        if column.get('putneed'):
                            argname = column.get('name')
                            argtype = column.get('type')
                            pjson[argname] = random_arg(argtype)
                pjsonstr = json.dumps(pjson)
                pjsonstr = html.escape(pjsonstr)
                if p == '/<id>':
                    path+=f"/${{__property({table.get('table')}_id)}}"
                else:
                    path += p
                single_api = single_str(zh,typezh,host,port,protocol,path,method,pjsonstr,argaddr,bean)
                w.write(single_api)



    # crud = [("删除","DELETE",'/<id>',False)]
    # for table in ojson.get('databases')[::-1]:
    #     if table.get('api'):
    #         zh = table.get('zh')
    #         tablename = table.get("table").lower()
    #         pjson = {}
    #         for typezh,method,p,argaddr in crud:
    #             path = f"/api/v1/order/{tablename}"
    #             bean = False
    #             pjsonstr = json.dumps(pjson)
    #             pjsonstr = html.escape(pjsonstr)
    #             path+=f"/${{__property({table.get('table')}_id)}}"
    #             single_api = single_str(zh,typezh,host,port,protocol,path,method,pjsonstr,argaddr,bean)
    #             w.write(single_api)
    #

    w.close()




