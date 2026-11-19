import sys
import os
import glob

class Parser:
    def __init__(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            self.lines = []
            for line in f:
                clean = line.split('//')[0].strip()
                if clean:
                    self.lines.append(clean)
        self.current_idx = -1
        self.current_cmd = ""

    def has_more_commands(self):
        return self.current_idx + 1 < len(self.lines)

    def advance(self):
        self.current_idx += 1
        self.current_cmd = self.lines[self.current_idx]

    def command_type(self):
        cmd = self.current_cmd.split()[0]
        cmd_map = {
            'push': 'C_PUSH',
            'pop': 'C_POP',
            'label': 'C_LABEL',
            'goto': 'C_GOTO',
            'if-goto': 'C_IF',
            'function': 'C_FUNCTION',
            'return': 'C_RETURN',
            'call': 'C_CALL'
        }
        return cmd_map.get(cmd, 'C_ARITHMETIC')

    def arg1(self):
        parts = self.current_cmd.split()
        if self.command_type() == 'C_ARITHMETIC':
            return parts[0]
        return parts[1]

    def arg2(self):
        return int(self.current_cmd.split()[2])


class CodeWriter:
    def __init__(self, out_filepath):
        self.out = open(out_filepath, 'w', encoding='utf-8')
        self.filename = ""
        self.current_func = "null"
        self.label_id = 0
        self.ret_id = 0

    def set_file_name(self, filepath):
        self.filename = os.path.splitext(os.path.basename(filepath))[0]

    def write_lines(self, asm_list):
        for line in asm_list:
            self.out.write(line + '\n')

    def write_init(self):
        self.write_lines(['// Bootstrap code', '@256', 'D=A', '@SP', 'M=D'])
        self.write_call('Sys.init', 0)

    def write_arithmetic(self, cmd):
        self.write_lines([f'// {cmd}'])
        if cmd in ('add', 'sub', 'and', 'or'):
            op_map = {'add': 'M=D+M', 'sub': 'M=M-D', 'and': 'M=D&M', 'or': 'M=D|M'}
            self.write_lines(['@SP', 'AM=M-1', 'D=M', 'A=A-1', op_map[cmd]])
        elif cmd in ('neg', 'not'):
            op_map = {'neg': 'M=-M', 'not': 'M=!M'}
            self.write_lines(['@SP', 'A=M-1', op_map[cmd]])
        elif cmd in ('eq', 'gt', 'lt'):
            self.label_id += 1
            jmp_map = {'eq': 'JEQ', 'gt': 'JGT', 'lt': 'JLT'}
            t_lbl = f'TRUE_{self.label_id}'
            e_lbl = f'END_{self.label_id}'
            self.write_lines([
                '@SP', 'AM=M-1', 'D=M', 'A=A-1', 'D=M-D',
                f'@{t_lbl}', f'D;{jmp_map[cmd]}',
                '@SP', 'A=M-1', 'M=0',
                f'@{e_lbl}', '0;JMP',
                f'({t_lbl})', '@SP', 'A=M-1', 'M=-1',
                f'({e_lbl})'
            ])

    def write_push_pop(self, cmd_type, segment, index):
        self.write_lines([f'// {cmd_type} {segment} {index}'])
        seg_map = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT'}
        
        if cmd_type == 'C_PUSH':
            if segment == 'constant':
                self.write_lines([f'@{index}', 'D=A'])
            elif segment in seg_map:
                self.write_lines([f'@{index}', 'D=A', f'@{seg_map[segment]}', 'A=D+M', 'D=M'])
            elif segment == 'temp':
                self.write_lines([f'@{5 + index}', 'D=M'])
            elif segment == 'pointer':
                target = 'THIS' if index == 0 else 'THAT'
                self.write_lines([f'@{target}', 'D=M'])
            elif segment == 'static':
                self.write_lines([f'@{self.filename}.{index}', 'D=M'])
            self.write_lines(['@SP', 'A=M', 'M=D', '@SP', 'M=M+1'])

        elif cmd_type == 'C_POP':
            if segment in seg_map:
                self.write_lines([
                    f'@{index}', 'D=A', f'@{seg_map[segment]}', 'D=D+M',
                    '@R13', 'M=D', '@SP', 'AM=M-1', 'D=M', '@R13', 'A=M', 'M=D'
                ])
            elif segment == 'temp':
                self.write_lines(['@SP', 'AM=M-1', 'D=M', f'@{5 + index}', 'M=D'])
            elif segment == 'pointer':
                target = 'THIS' if index == 0 else 'THAT'
                self.write_lines(['@SP', 'AM=M-1', 'D=M', f'@{target}', 'M=D'])
            elif segment == 'static':
                self.write_lines(['@SP', 'AM=M-1', 'D=M', f'@{self.filename}.{index}', 'M=D'])

    def write_label(self, label):
        self.write_lines([f'// label {label}', f'({self.current_func}${label})'])

    def write_goto(self, label):
        self.write_lines([f'// goto {label}', f'@{self.current_func}${label}', '0;JMP'])

    def write_if(self, label):
        self.write_lines([
            f'// if-goto {label}',
            '@SP', 'AM=M-1', 'D=M',
            f'@{self.current_func}${label}', 'D;JNE'
        ])

    def write_function(self, func_name, num_vars):
        self.current_func = func_name
        self.write_lines([f'// function {func_name} {num_vars}', f'({func_name})'])
        for _ in range(num_vars):
            self.write_push_pop('C_PUSH', 'constant', 0)

    def write_call(self, func_name, num_args):
        self.ret_id += 1
        ret_label = f'{func_name}$ret.{self.ret_id}'
        self.write_lines([f'// call {func_name} {num_args}'])
        # 1. push return-address
        self.write_lines([f'@{ret_label}', 'D=A', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1'])
        # 2. push LCL, ARG, THIS, THAT
        for seg in ('LCL', 'ARG', 'THIS', 'THAT'):
            self.write_lines([f'@{seg}', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1'])
        # 3. ARG = SP - 5 - nArgs
        self.write_lines([
            '@SP', 'D=M', f'@{5 + num_args}', 'D=D-A', '@ARG', 'M=D'
        ])
        # 4. LCL = SP
        self.write_lines(['@SP', 'D=M', '@LCL', 'M=D'])
        # 5. goto func_name
        self.write_lines([f'@{func_name}', '0;JMP', f'({ret_label})'])

    def write_return(self):
        self.write_lines([
            '// return',
            '@LCL', 'D=M', '@R13', 'M=D',          # R13 = FRAME = LCL
            '@5', 'A=D-A', 'D=M', '@R14', 'M=D',    # R14 = RET = *(FRAME - 5)
            '@SP', 'AM=M-1', 'D=M', '@ARG', 'A=M', 'M=D',  # *ARG = pop()
            '@ARG', 'D=M+1', '@SP', 'M=D',          # SP = ARG + 1
        ])
        for offset, seg in enumerate(['THAT', 'THIS', 'ARG', 'LCL'], start=1):
            self.write_lines([
                '@R13', 'D=M', f'@{offset}', 'A=D-A', 'D=M', f'@{seg}', 'M=D'
            ])
        self.write_lines(['@R14', 'A=M', '0;JMP'])

    def close(self):
        self.out.close()


def main():
    in_path = os.path.normpath(sys.argv[1])
    is_dir = os.path.isdir(in_path)

    if is_dir:
        vm_files = sorted(glob.glob(os.path.join(in_path, '*.vm')))
        dir_name = os.path.basename(in_path)
        out_path = os.path.join(in_path, f'{dir_name}.asm')
    else:
        vm_files = [in_path]
        out_path = os.path.splitext(in_path)[0] + '.asm'

    writer = CodeWriter(out_path)
    if is_dir:
        writer.write_init()

    for vm_file in vm_files:
        writer.set_file_name(vm_file)
        parser = Parser(vm_file)
        while parser.has_more_commands():
            parser.advance()
            ctype = parser.command_type()
            if ctype == 'C_ARITHMETIC':
                writer.write_arithmetic(parser.arg1())
            elif ctype in ('C_PUSH', 'C_POP'):
                writer.write_push_pop(ctype, parser.arg1(), parser.arg2())
            elif ctype == 'C_LABEL':
                writer.write_label(parser.arg1())
            elif ctype == 'C_GOTO':
                writer.write_goto(parser.arg1())
            elif ctype == 'C_IF':
                writer.write_if(parser.arg1())
            elif ctype == 'C_FUNCTION':
                writer.write_function(parser.arg1(), parser.arg2())
            elif ctype == 'C_CALL':
                writer.write_call(parser.arg1(), parser.arg2())
            elif ctype == 'C_RETURN':
                writer.write_return()

    writer.close()

if __name__ == '__main__':
    main()