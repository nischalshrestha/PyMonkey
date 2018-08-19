
class ParserTracer:

    trace_level = 0
    trace_ident_placeholder = "\t"

    def ident_level(self):
        return self.trace_ident_placeholder * (self.trace_level-1)

    def trace_print(self, fs):
        print("{}{}\n".format(self.ident_level(), fs))

    def inc_ident(self):
        self.trace_level = self.trace_level + 1

    def dec_ident(self):
        self.trace_level = self.trace_level - 1

    def trace(self, msg):
        self.inc_ident()
        self.trace_print("BEGIN " + msg)
        return msg

    def untrace(self, msg):
        self.trace_print("END " + msg)
        self.dec_ident()
