from yattag import Doc
from graphviz import Digraph


class GraphvizGenerator:
    @staticmethod
    def generate(states):
        g = Digraph(node_attr={'shape': 'Mrecord'})
        count = 0
        for state in states:
            doc, tag, text = Doc().tagtext()
            with tag('table', border='0',
                cellborder='0',
                cellpadding='3'
                ):
                for item in state.items:
                    with tag('tr'):
                        with tag('td'):
                            text(str(item))
            g.node(str(count), label='<' + doc.getvalue() + '>')
            count += 1
        g.view()