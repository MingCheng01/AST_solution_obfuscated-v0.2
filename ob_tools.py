import execjs
import tkinter as tk
from tkinter import scrolledtext
import tkinter.filedialog
from tkinter.messagebox import showinfo, showwarning, showerror
from tkinter import *


class ob_tools():

    def __init__(self):
        window = tk.Tk()
        window.title('AST解混淆工具-by:Uncle_Ming')
        window.geometry('760x720')
        self.js_code = ''
        self.compression = 0
        self.environment = 0
        L1 = tk.Label(window, text='AST还原', width=7, height=1, justify='left', anchor='w', font=("Times", 15, "bold"))
        L1.place(x=250, y=2)
        # AST处理窗口
        self.Process_scrolled = scrolledtext.ScrolledText(window, width=80, height=50, state=tk.DISABLED)
        self.Process_scrolled.place(x=10, y=30)

        b1 = tk.Button(window, text='  打开文件 ', command=self.open_read)
        b1.place(x=600, y=30)

        L2 = tk.Label(window, text='AST功能', width=7, height=1, justify='left', anchor='w', font=("Times", 15, "bold"),
                      fg="DarkBlue")
        L2.place(x=590, y=65)
        b2 = tk.Button(window, text='删除空语句', command=self.delete_the_empty_statement)
        b2.place(x=600, y=100)
        b3 = tk.Button(window, text='字符解混淆', command=self.character_deobfuscation)
        b3.place(x=680, y=100)
        b4 = tk.Button(window, text='return简化', command=self.return_simplified)
        b4.place(x=600, y=140)
        b5 = tk.Button(window, text='标识符简化', command=self.identifier_simplification)
        b5.place(x=680, y=140)
        b6 = tk.Button(window, text='大数组解密', command=self.array_obfuscation)
        b6.place(x=600, y=180)
        b7 = tk.Button(window, text='常量--计算', command=self.constants_calculations)
        b7.place(x=680, y=180)
        b8 = tk.Button(window, text='去除花指令', command=self.flower_instructions)
        b8.place(x=600, y=220)
        b9 = tk.Button(window, text='序列表达式', command=self.sequence_expressions)
        b9.place(x=680, y=220)
        b10 = tk.Button(window, text='控制平坦化', command=self.control_flattening)
        b10.place(x=600, y=260)
        b11 = tk.Button(window, text='三元表达式', command=self.ternary_expressions)
        b11.place(x=680, y=260)
        b12 = tk.Button(window, text=' 删除if的假', command=self.remove_if_fake)
        b12.place(x=600, y=300)
        b13 = tk.Button(window, text=' 数组--简化', command=self.arrays_simplified)
        b13.place(x=680, y=300)
        b14 = tk.Button(window, text='标识符删除', command=self.identifier_deletion)
        b14.place(x=600, y=340)
        b15 = tk.Button(window, text=' try—catch', command=self.try_catch_simplified)
        b15.place(x=680, y=340)
        b16 = tk.Button(window, text='自执行换参', command=self.self_executing_parameter_swapping)
        b16.place(x=600, y=380)
        b17 = tk.Button(window, text='删除debug', command=self.remove_distractions)
        b17.place(x=680, y=380)

        L3 = tk.Label(window, text='代码 压缩', width=7, height=1, justify='left', anchor='w', font=("Times", 15, "bold"),
                      fg="DarkBlue")
        L3.place(x=590, y=420)

        b18 = tk.Button(window, text=' 轻度-压缩 ', command=self.mild_compression)
        b18.place(x=600, y=460)
        b19 = tk.Button(window, text=' 重度-压缩 ', command=self.heavy_compression)
        b19.place(x=680, y=460)

        L4 = tk.Label(window, text='   其  它', width=7, height=1, justify='left', anchor='w', font=("Times", 15, "bold"),
                      fg="DarkBlue")
        L4.place(x=590, y=500)
        b20 = tk.Button(window, text='一键补环境', command=self.make_up_the_environment)
        b20.place(x=600, y=540)

        L5 = tk.Label(window, text='代码 保存', width=7, height=1, justify='left', anchor='w', font=("Times", 15, "bold"),
                      fg="DarkBlue")
        L5.place(x=590, y=580)

        b21 = tk.Button(window, text='  js另存为 ', command=self.file_save)
        b21.place(x=600, y=620)

        L6 = tk.Label(window, text='日志：', width=5, height=1, justify='left', anchor='w', font=("Times", 15, "bold"))
        L6.place(x=10, y=690)
        self.L7 = tk.Label(window, text='', width=45, height=1, justify='left', anchor='w', font=("Times", 15))
        self.L7.place(x=70, y=690)
        window.mainloop()

    def updata_text(self, text):
        self.Process_scrolled.config(state='normal')
        self.del_text()
        self.Process_scrolled.insert(END, text)
        self.Process_scrolled.config(state=tk.DISABLED)
        self.Process_scrolled.update()

    def pop_ups(self, type_, text):
        if type_ == 'info':
            showinfo(title="提示", message=text)
        elif type_ == 'warning':
            showwarning(title="警告", message=text)
        elif type_ == 'error':
            showerror(title="错误", message=text)
        else:
            showinfo(title="提示", message=text)

    def del_text(self):
        self.Process_scrolled.config(state='normal')
        self.Process_scrolled.delete(1.0, 'end')
        self.Process_scrolled.update()

    def open_read(self):
        path_ = tk.filedialog.askopenfilename()
        try:
            if path_.split('.')[-1] != 'js' and path_ != '':
                self.pop_ups('info', text='目前仅支持读取js文件！')
            elif path_ == '':
                pass
            else:
                with open(path_, 'r', encoding='utf-8') as f:
                    self.js_code = f.read()
                    self.del_text()
                    self.compression = 0
                    self.environment = 0
        except Exception as e:
            self.pop_ups(type_='error', text=str(e))

    def log_(self, text, type_):
        if type_ == 'success':
            self.L7.config(text=text, fg="chartreuse4")
            self.L7.update()
        else:
            self.L7.config(text=text, fg="DarkRed")
            self.L7.update()

    def open_ast_js(self, path_):
        try:
            with open(path_, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            self.pop_ups(type_='error', text="初始化AST_js文件出现问题: " + str(e))

    def delete_the_empty_statement(self):
        try:
            ast_code = self.open_ast_js(path_='./AST/AST_删除无效空语句.js')
            ast_code = execjs.compile(ast_code)
            self.js_code = ast_code.call('Delete_the_empty_statement', self.js_code)
            self.log_('删除无效空语句-成功！', type_='success')
            self.updata_text(self.js_code)
        except Exception as e:
            self.log_('删除无效空语句-失败！', type_='error')
            self.pop_ups(type_='error', text=str(e))

    def character_deobfuscation(self):
        try:
            ast_code = self.open_ast_js(path_='./AST/AST_字符串混淆.js')
            ast_code = execjs.compile(ast_code)
            self.js_code = ast_code.call('String_obfuscation', self.js_code)
            self.log_('字符串解混淆-成功！', type_='success')
            self.updata_text( self.js_code)
             
        except Exception as e:
            self.log_('字符串解混淆-失败！', type_='error')
            self.pop_ups(type_='error', text=str(e))

    def return_simplified(self):
        try:
            ast_code = self.open_ast_js(path_='./AST/AST_return函数简化.js')
            ast_code = execjs.compile(ast_code)
            self.js_code = ast_code.call('Simplify_return', self.js_code)
            self.log_('return函数简化-成功！', type_='success')
            self.updata_text( self.js_code)
             
        except Exception as e:
            self.log_('return函数简化-失败！', type_='error')
            self.pop_ups(type_='error', text=str(e))

    def identifier_simplification(self):
        try:
            ast_code = self.open_ast_js(path_='./AST/AST_标识符简化.js')
            ast_code = execjs.compile(ast_code)
            self.js_code = ast_code.call('Duplicate_assignment_of_identifiers', self.js_code)
            self.log_('标识符简化-成功！', type_='success')
            self.updata_text( self.js_code)
             
        except Exception as e:
            self.log_('标识符简化-失败！', type_='error')
            self.pop_ups(type_='error', text=str(e))

    def array_obfuscation(self):
        try:
            ast_code = self.open_ast_js(path_='./AST/AST_大数组加密解混淆.js')
            ast_code = execjs.compile(ast_code)
            self.js_code = ast_code.call('Large_array_encryption', self.js_code)
             
            self.log_('AST大数组加密解混淆-成功！', type_='success')
            self.updata_text( self.js_code)
        except Exception as e:
            self.log_('AST大数组加密解混淆-失败！', type_='error')
            self.pop_ups(type_='error', text=str(e))

    def constants_calculations(self):
        try:
            ast_code = self.open_ast_js(path_='./AST/AST_常量计算.js')
            ast_code = execjs.compile(ast_code)
            self.js_code = ast_code.call('Constant_calculations', self.js_code)
            self.log_('常量计算-成功！', type_='success')
            self.updata_text( self.js_code)
        except Exception as e:
            self.log_('常量计算-失败！', type_='error')
            self.pop_ups(type_='error', text=str(e))

    def flower_instructions(self):
        try:
            ast_code = self.open_ast_js(path_='./AST/AST_花指令剔除.js')
            ast_code = execjs.compile(ast_code)
            self.js_code = ast_code.call('Flower_instructions', self.js_code)
            self.log_('花指令剔除-成功！', type_='success')
            self.updata_text( self.js_code)
        except Exception as e:
            self.log_('花指令剔除-失败！', type_='error')
            self.pop_ups(type_='error', text=str(e))

    def sequence_expressions(self):
        try:
            ast_code = self.open_ast_js(path_='./AST/AST_序列表达式还原.js')
            ast_code = execjs.compile(ast_code)
            self.js_code = ast_code.call('Sequence_expression_restoration', self.js_code)
            self.log_('序列表达式还原-成功！', type_='success')
            self.updata_text( self.js_code)
        except Exception as e:
            self.log_('序列表达式还原-失败！', type_='error')
            self.pop_ups(type_='error', text=str(e))

    def control_flattening(self):
        try:
            ast_code = self.open_ast_js(path_='./AST/AST_控制流平坦化.js')
            ast_code = execjs.compile(ast_code)
            self.js_code = ast_code.call('Control_leveling', self.js_code)
            self.log_('控制平坦化-成功！', type_='success')
            self.updata_text( self.js_code)
        except Exception as e:
            self.log_('控制平坦化-失败！', type_='error')
            self.pop_ups(type_='error', text=str(e))

    def ternary_expressions(self):
        try:
            ast_code = self.open_ast_js(path_='./AST/AST_三元表达式转if.js')
            ast_code = execjs.compile(ast_code)
            self.js_code = ast_code.call('Ternary_expression', self.js_code)
            self.log_('三元表达式转if-成功！', type_='success')
            self.updata_text( self.js_code)
        except Exception as e:
            self.log_('三元表达式转if-失败！', type_='error')
            self.pop_ups(type_='error', text=str(e))

    def remove_if_fake(self):
        try:
            ast_code = self.open_ast_js(path_='./AST/AST_删除if假.js')
            ast_code = execjs.compile(ast_code)
            self.js_code = ast_code.call('Delete_fake', self.js_code)
            self.log_('删除if假-成功！', type_='success')
            self.updata_text( self.js_code)
        except Exception as e:
            self.log_('删除if假-失败！', type_='error')
            self.pop_ups(type_='error', text=str(e))

    def arrays_simplified(self):
        try:
            ast_code = self.open_ast_js(path_='./AST/AST_数组简化.js')
            ast_code = execjs.compile(ast_code)
            self.js_code = ast_code.call('Array_simplification', self.js_code)
            self.log_('数组简化-成功！', type_='success')
            self.updata_text( self.js_code)
        except Exception as e:
            self.log_('数组简化-失败！', type_='error')
            self.pop_ups(type_='error', text=str(e))

    def identifier_deletion(self):
        try:
            ast_code = self.open_ast_js(path_='./AST/AST_未使用标识符删除.js')
            ast_code = execjs.compile(ast_code)
            self.js_code = ast_code.call('Identifier_deletion', self.js_code)
            self.log_('未使用标识符删除-成功！', type_='success')
            self.updata_text( self.js_code)
        except Exception as e:
            self.log_('未使用标识符删除-失败！', type_='error')
            self.pop_ups(type_='error', text=str(e))

    def try_catch_simplified(self):
        try:
            ast_code = self.open_ast_js(path_='./AST/AST_try-catch简化.js')
            ast_code = execjs.compile(ast_code)
            self.js_code = ast_code.call('Try_catch_simplification', self.js_code)
            self.log_('try-catch简化-成功！', type_='success')
            self.updata_text( self.js_code)
        except Exception as e:
            self.log_('try-catch简化-失败！', type_='error')
            self.pop_ups(type_='error', text=str(e))

    def self_executing_parameter_swapping(self):
        try:
            ast_code = self.open_ast_js(path_='./AST/AST_自执行实参替换形参.js')
            ast_code = execjs.compile(ast_code)
            self.js_code = ast_code.call('Replace_formal_parameters', self.js_code)
            self.log_('自执行实参替换形参-成功！', type_='success')
            self.updata_text( self.js_code)
        except Exception as e:
            self.log_('自执行实参替换形参-失败！', type_='error')
            self.pop_ups(type_='error', text=str(e))

    def remove_distractions(self):
        try:
            ast_code = self.open_ast_js(path_='./AST/AST_删除Debugger_计时器_禁用console删减.js')
            ast_code = execjs.compile(ast_code)
            self.js_code = ast_code.call('Delete_', self.js_code)
            self.log_('删除Debugger_计时器_禁用console删减-成功！', type_='success')
            self.updata_text(self.js_code)
        except Exception as e:
            self.log_('删除Debugger_计时器_禁用console删减-失败！', type_='error')
            self.pop_ups(type_='error', text=str(e))

    def mild_compression(self):
        try:
            if self.compression == 1:
                self.updata_text(text='重度压缩后不支持再次轻度压缩！\n会出问题哒')
            else:
                ast_code = self.open_ast_js(path_='./AST/AST_轻度压缩.js')
                ast_code = execjs.compile(ast_code)
                self.js_code = ast_code.call('Mild_compression', self.js_code)
                self.updata_text( self.js_code)
        except Exception as e:
            self.pop_ups(type_='error', text=str(e))

    def heavy_compression(self):
        try:
            if self.compression == 1:
                self.updata_text(text='重度压缩了怎么还要再压缩？\n会出问题哒')
            else:
                ast_code = self.open_ast_js(path_='./AST/AST_重度压缩.js')
                ast_code = execjs.compile(ast_code)
                self.js_code = ast_code.call('Heavy_compression', self.js_code)
                self.updata_text(text='重度压缩显示会导致tk严重卡顿\n当您看到这句话时说明压缩已经结束，可以执行保存')
                self.compression = 1
        except Exception as e:
            self.pop_ups(type_='error', text=str(e))

    def file_save(self):
        try:
            path_ = tkinter.filedialog.asksaveasfilename(title='保存js', initialfile='out.js')
            if path_ != '':
                with open(path_, 'w', encoding='utf-8') as f:
                    f.write(self.js_code)
            else:
                pass
        except Exception as e:
            self.pop_ups(type_='error', text=str(e))

    def make_up_the_environment(self):
        str_ = "const jsdom=require('jsdom')\nconst { JSDOM } =jsdom\nconst dom=new JSDOM('<!doctype html><p> hello </p>')\nwindow=dom.window\ndocument=window.document\nnavigator=window.navigator\n"
        if self.js_code != '' and self.environment == 0:
            self.js_code = str_ + self.js_code
            self.updata_text( self.js_code)


tools = ob_tools()
