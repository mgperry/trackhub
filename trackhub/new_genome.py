import os
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
from validate import ValidationError
from base import HubComponent


class NewGenome(HubComponent):
    def __init__(self, genome, twobit_fn, trackdb=None, genome_file_obj=None, genome_info=None):
        """
        Represents a 2-line genome stanza within a "genomes.txt" file.

        The file itself is represented by a :class:`GenomesFile` object.
        """
        HubComponent.__init__(self)
        self.genome = genome
        self.twobit_fn = twobit_fn
        self.trackdb = None
        if trackdb is not None:
            self.add_trackdb(trackdb)
        if genome_file_obj:
            self.add_parent(genome_file_obj)
        self.genome_info = dict()
        if genome_info:
            self.genome_info.update(genome_info)

    @property
    def genome_file_obj(self):
        try:
            return self.parent
        except AttributeError:
            return None

    def add_trackdb(self, trackdb):
        self.children = []
        self.add_child(trackdb)
        self.trackdb = self.children[0]

    def __str__(self):
        try:
            self.validate()
        except ValidationError:
            return "Unconfigured <Genome> object"
        s = []
        s.append('genome %s' % self.genome)
        trackdb_relpath = os.path.relpath(self.trackdb.local_fn,
                                          start = os.path.dirname(
                                                    self.parent.parent.local_fn)) #local_fn of hub file
        s.append('trackDb %s' % trackdb_relpath)
        twobit_relpath = os.path.relpath(self.twobit_fn,
                                          start = os.path.dirname(
                                                    self.parent.parent.local_fn)) #local_fn of hub file
        s.append('twoBitPath %s' % self.twobit_relpath)
        for k, v in self.genome_info.iteritems():
            s.append(str(k) + ' ' + str(v))
        return '\n'.join(s) + '\n'

    def validate(self):
        if len(self.children) == 0:
            raise ValidationError(
                "No TrackDb objects provided")
        if self.trackdb is None:
            raise ValidationError("No TrackDb objects provided")

    def _render(self):
        """
        No file is created from a Genome object -- only from its parent
        GenomesFile object.
        """
        pass