from collections import defaultdict
import csv
from os import listdir
from os.path import isfile, join

import networkx as nx

class Graph:

    def __init__(self, edge_list_path, node_property_list, delimiter='\t'):
        self._edge_list_path = edge_list_path
        self._node_property_list = node_property_list
        self._delimiter = delimiter
        self.graph = None
        self._attributes = defaultdict(set)
        self._edges_by_label = defaultdict()

        self._create_graph()
        self._set_attributes()

    def _create_graph(self):
        """ read edge_list to creat graph
        """
        self.graph = nx.read_edgelist(self._edge_list_path)

    def _set_attributes(self):
        """ read node attributes from file and set to graph
        """
        with open(self._node_property_list, 'rb') as csvfile:
            property_reader = csv.reader(csvfile, delimiter=self._delimiter)
            attr_types = property_reader.next()
            for i, attr_row in enumerate(property_reader):
                for j, attr_type in enumerate(attr_types):
                    self.graph.add_node(str(i+1), {attr_type: attr_row[j]})
                    self._attributes[attr_type].add(attr_row[j])

    def _set_edges_by_label(self, attr_type):
        """group by label
        """
        edges_by_label = defaultdict(int)
        for i, j in self.graph.edges_iter():
            edges_by_label[self.graph.node[i][attr_type], \
                           self.graph.node[j][attr_type]] += 1

        self._edges_by_label[attr_type] = dict(edges_by_label)

    def _euv(self, attr_type, u, v):
        try:
            euv = float(self._edges_by_label[attr_type][u, v]) / \
                  float(self.graph.number_of_edges())
        except:
            euv = 0

        return euv

    def _au(self, attr_type, u):
        sum = float(0)
        for v in self._attributes[attr_type]:
            try:
                val_uv = float(self._edges_by_label[attr_type][u, v]) / \
                         float(self.graph.number_of_edges())
                if u != v:
                    sum += val_uv / 2.0
                else:
                    sum += val_uv
            except:
                sum += 0

            try:
                val_vu = float(self._edges_by_label[attr_type][v, u]) / \
                         float(self.graph.number_of_edges())
                if u != v:
                    sum += val_vu / 2.0
                else:
                    sum += val_vu
            except:
                sum += 0
        try:
            val_uu = float(self._edges_by_label[attr_type][u, u]) / \
                     float(self.graph.number_of_edges())
        except:
            val_uu = 0
        sum -= val_uu

        return sum

    def _sub_modularity(self, attr_type, u, v):
        euv = self._euv(attr_type, u, v)
        au = self._au(attr_type, u)

        if euv == 0:
            return 0
        else:
            return euv - au**2

    def modularity(self, attr_type):
        """ calc graph modularity Q
        func: Q = sigma_u (euu - au**2)
        """
        self._set_edges_by_label(attr_type)
        q = 0.0
        for label in self._attributes[attr_type]:
            q += self._sub_modularity(attr_type, label, label)

        return q


def files(path):
    only_files = [f for f in listdir(path) if isfile(join(path, f))]
    edge_lists = [f for f in only_files if not f.endswith('_attr.txt')]
    attr_lists = [f for f in only_files if f.endswith('_attr.txt')]

    #FIXME
    return [f.replace("_attr.txt","") for f in attr_lists]

def job(name):
    print ">>>Begin:", name
    try:
        e = 'facebook100txt/' + name + '.txt'
        a = 'facebook100txt/' + name + '_attr.txt'
        g = Graph(e, a)
        attrs = ['status', 'major', 'gender']
        with open('result/'+name+'_mod.txt', "w") as f:
            writer = csv.writer(f, delimiter=',')
            for attr in attrs:
                output = attr, g.modularity(attr)
                writer.writerow(output)
        print "<<<Done", name
    except e:
        print "<<<DERR:", name


if __name__=="__main__":
    """
    edge_list_path = "sample/Cal65.txt"
    node_properties_path = "sample/Cal65_attr.txt"
    g = Graph(edge_list_path, node_properties_path)
    for key in g._attributes.keys():
        print key, g.modularity(key)
    """
    from multiprocessing import Pool
    from os import mkdir
    from os.path import isdir
    from shutil import rmtree


    p = Pool(4)
    root_path = 'facebook100txt'
    result_path = 'result'

    if isdir(result_path):
        rmtree(result_path)
    mkdir(result_path)

    pathes = files(root_path)
    p.map(job, pathes)
