import sys
import os

class Parser:
    def __init__(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            self.lines = []
            for line in f:
                # 去除註解與前後空白
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
        parts = self.current_cmd.split()
        if parts[0] == 'push':
            return 'C_PUSH'
        elif parts[0] == 'pop':
            return 'C_POP'
        else:
            return 'C_ARITHMETIC'

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
        self.filename = os.path.splitext(os.path.basename(out_filepath))[0]
        self.label_id = 0

    def write_lines(self, asm_list):
        for line in asm_list:
            self.out.write(line + '\n')

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
            # 統一推入堆疊
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

    def close(self):
        self.out.close()


def main():
    in_path = sys.argv[1]
    out_path = os.path.splitext(in_path)[0] + '.asm'
    parser = Parser(in_path)
    writer = CodeWriter(out_path)

    while parser.has_more_commands():
        parser.advance()
        ctype = parser.command_type()
        if ctype == 'C_ARITHMETIC':
            writer.write_arithmetic(parser.arg1())
        elif ctype in ('C_PUSH', 'C_POP'):
            writer.write_push_pop(ctype, parser.arg1(), parser.arg2())

    writer.close()

if __name__ == '__main__':
    main()