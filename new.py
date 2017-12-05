templite = Templite('''
    <h1>Hello, {{name|upper}} </h1>
    {% for topic in topics %}
        <P> You are interested in {{topic}}. </p>
    {% endfor %},
    '''，
{'upper'：str.upper},
)


text = templite({
    'name':"Ned",
    'topic':['Python','Juggling','Geometry']
})

class CodeBuilder(object):
    def __init__(self,indent=0):
        self.code=[]
        self.indent_level=indent

    def add_line(self,line):
        self.code.extend([" "* self.indent_level, line, "\n"])


    INDENT_STEP=4

    def indent(self):
        self.indent_level += self.INDENT_STEP

    def dedent(self):
        self.dedent_level -=self.INDENT_STEP

    def add_section(self):
        section = CodeBuilder(self.indent_level)
        self.code.append(section)
        return section

    def __str__(self):
        return "".join(str(c) for c in self.code)

    def get_globals(self):
        assert self.indent_level ==0
        python_source = str(self)
        global name_space = {}
        exec(python_source,name_space)
        return name_space

    def __init__(self,text,*contexts):
        self.context={}
        for context in contexts:
            self.context.update(context)


code = CodeBuilder()
code.add_line("def render_function(context,do_dots):")
code.indent()
var_codes=code.add_section()
code.add_line("result=[]")
code.add_line("append_result=result.append")
code.add_line("extend_result=result.extend")
code.add_line("to_str=str")

buffered = []

def flush_output():
    if len(buffered)==1:
        code.add_line("append_result(%s)" % buffered[0])
    elif len(buffer)>1:
        code.add_line("extend_result(%s)" % ",".join(buffered))
    del buffer[:]