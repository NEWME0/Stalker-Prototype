
__all__ = ('FileOgf')


import struct
import numpy as np


CHUNK_HEADER          = 1
CHUNK_TEXTURE         = 2
CHUNK_VERTICES        = 3
CHUNK_INDICES         = 4
CHUNK_P_MAP           = 5
CHUNK_SWIDATA         = 6
CHUNK_VCONTAINER      = 7
CHUNK_ICONTAINER      = 8
CHUNK_CHILDREN        = 9
CHUNK_CHILDREN_L      = 10
CHUNK_LODDEF2         = 11
CHUNK_TREEDEF2        = 12
CHUNK_S_BONE_NAMES    = 13
CHUNK_S_MOTIONS       = 14
CHUNK_S_SMPARAMS      = 15
CHUNK_S_IKDATA        = 16
CHUNK_S_USERDATA      = 17
CHUNK_S_DESC          = 18
CHUNK_S_MOTION_REFS_0 = 19
CHUNK_SWICONTAINER    = 20
CHUNK_GCONTAINER      = 21
CHUNK_FASTPATH        = 22
CHUNK_S_LODS          = 23
CHUNK_S_MOTION_REFS_1 = 24

CHUNK_ALL = (
    CHUNK_HEADER,
    CHUNK_TEXTURE,
    CHUNK_VERTICES,
    CHUNK_INDICES,
    CHUNK_P_MAP,
    CHUNK_SWIDATA,
    CHUNK_VCONTAINER,
    CHUNK_ICONTAINER,
    CHUNK_CHILDREN,
    CHUNK_CHILDREN_L,
    CHUNK_LODDEF2,
    CHUNK_TREEDEF2,
    CHUNK_S_BONE_NAMES,
    CHUNK_S_MOTIONS,
    CHUNK_S_SMPARAMS,
    CHUNK_S_IKDATA,
    CHUNK_S_USERDATA,
    CHUNK_S_DESC,
    CHUNK_S_MOTION_REFS_0,
    CHUNK_SWICONTAINER,
    CHUNK_GCONTAINER,
    CHUNK_FASTPATH,
    CHUNK_S_LODS,
    CHUNK_S_MOTION_REFS_1,
)


DT_SWI = np.dtype([
    ('offset', np.uint32),
    ('num_tris', np.uint16),
    ('num_verts', np.uint16),
])

DT_LOD_VERTEX = np.dtype([
    ('v', (np.float32, 3)),
    ('t', (np.float32, 3)),
    ('c_rgb_hemi', (np.uint8, 4)),
    ('c_sun', np.uint8),
    ('pad', (np.uint8, 3)),
])

DT_LOD_FACE = np.dtype([
    ('a', DT_LOD_VERTEX),
    ('b', DT_LOD_VERTEX),
    ('c', DT_LOD_VERTEX),
    ('d', DT_LOD_VERTEX),
])

DT_COLOR5 = np.dtype([
    ('rgb', (np.float32, 3)),
    ('hemi', np.float32),
    ('sun',  np.float32),
])

DT_FMATRIX44 = np.dtype([
    ('mm', (np.float32, 16)),
])

DT_TREEDEF2 = np.dtype([
   ('tree_xform', DT_COLOR5),
   ('c_scale',    DT_COLOR5),
   ('c_bias',     DT_FMATRIX44),
])

"""

struct ogf4_5color {
    fvector3    rgb;
    float       hemi;
    float       sun;
};

// level mesh LOD definitions (billboards)
struct ogf4_lod_vertex {
    fvector3    v;
    fvector2    t;
    rgba32      c_rgb_hemi;
    uint8_t     c_sun;
    uint8_t     pad[3];
};

// on-disk format!!!
struct ogf4_lod_face {
    ogf4_lod_vertex v[4];
};

"""


class FileOgf:
    def __init__(self):
        self.chunks = None

    @staticmethod
    def _iter_chunks(fp, start=None, end=None):
        if not start:
            start = 0

        if not end:
            fp.seek(0, 2)
            end = fp.tell()

        fp.seek(start, 0)

        while True:
            chtype, chsize = struct.unpack('2I', fp.read(8))

            pos = fp.tell()
            yield chtype, chsize
            fp.seek(pos + chsize, 0)

            if fp.tell() >= end:
                return

    def load(self, fp, start=None, end=None, chunks_to_load=CHUNK_ALL):
        self.chunks = list()

        for chtype, chsize in self._iter_chunks(fp, start, end):
            self.chunks.append(chtype)

            if not chtype in chunks_to_load:
                continue

            loader = {
                1:  self._load_header,
                2:  self._load_texture,
                3:  self._load_vertices,
                4:  self._load_indices,
                5:  self._load_p_map,
                6:  self._load_swidata,
                7:  self._load_vcontainer,
                8:  self._load_icontainer,
                9:  self._load_children,
                10: self._load_children_l,
                11: self._load_loddef2,
                12: self._load_treedef2,
                13: self._load_s_bone_names,
                14: self._load_s_motions,
                15: self._load_s_smparams,
                16: self._load_s_ikdata,
                17: self._load_s_userdata,
                18: self._load_s_desc,
                19: self._load_s_motion_refs_0,
                20: self._load_swicontainer,
                21: self._load_gcontainer,
                22: self._load_fastpath,
                23: self._load_s_lods,
                24: self._load_s_motion_refs_1,
            }.get(chtype, None)

            if loader == None:
                raise ValueError("Unknown chunk type " + str(chtype))

            loader(fp, chtype, chsize)

    def _load_header(self, fp, chtype, chsize):
        assert chtype == 1, ValueError("Wrong chunk type " + str(chtype))
        assert chsize == 44, ValueError("Wrong chunk size " + str(chsize))

        (
            self.version,
            self.modeltype,
            self.shaderid,
            self.bbox_min_x,
            self.bbox_min_y,
            self.bbox_min_z,
            self.bbox_max_x,
            self.bbox_max_y,
            self.bbox_max_z,
            self.bsphere_origin_x,
            self.bsphere_origin_y,
            self.bsphere_origin_z,
            self.bsphere_radius,
        ) = struct.unpack('=2BH10f', fp.read(44))

    def _load_texture(self, fp, chtype, chsize):
        NotImplemented

    def _load_vertices(self, fp, chtype, chsize):
        NotImplemented

    def _load_indices(self, fp, chtype, chsize):
        NotImplemented

    def _load_p_map(self, fp, chtype, chsize):
        NotImplemented

    def _load_swidata(self, fp, chtype, chsize):
        assert chtype == 6, ValueError("Wrong chunk type " + str(chtype))
        assert (chsize - 20) % 8 == 0, ValueError("Wrong chunk size " + str(chsize))

        (
            self.swi_reserved_0,
            self.swi_reserved_1,
            self.swi_reserved_2,
            self.swi_reserved_3,
            self.swi_len,
        ) = struct.unpack('5I', fp.read(20))

        self.swi_buf = np.frombuffer(fp.read(chsize - 20), DT_SWI)

        assert len(self.swi_buf) == self.swi_len, "Wrong swi len"

    def _load_vcontainer(self, fp, chtype, chsize):
        NotImplemented

    def _load_icontainer(self, fp, chtype, chsize):
        NotImplemented

    def _load_children(self, fp, chtype, chsize):
        NotImplemented

    def _load_children_l(self, fp, chtype, chsize):
        assert chtype == 10, ValueError("Wrong chunk type " + str(chtype))
        assert chsize % 4 == 0, ValueError("Wrong chunk size " + str(chsize))

        temp = struct.unpack('I' * (chsize // 4), fp.read(chsize))

        self.child_len = temp[0]
        self.child_ids = temp[1:]

        assert len(self.child_ids) == self.child_len, "Wrong child len"

    def _load_loddef2(self, fp, chtype, chsize):
        self.loddef = np.frombuffer(fp.read(chsize), DT_LOD_FACE)

    def _load_treedef2(self, fp, chtype, chsize):
        self.treedef = np.frombuffer(fp.read(chsize), DT_TREEDEF2)

    def _load_s_bone_names(self, fp, chtype, chsize):
        NotImplemented

    def _load_s_motions(self, fp, chtype, chsize):
        NotImplemented

    def _load_s_smparams(self, fp, chtype, chsize):
        NotImplemented

    def _load_s_ikdata(self, fp, chtype, chsize):
        NotImplemented

    def _load_s_userdata(self, fp, chtype, chsize):
        NotImplemented

    def _load_s_desc(self, fp, chtype, chsize):
        NotImplemented

    def _load_s_motion_refs_0(self, fp, chtype, chsize):
        NotImplemented

    def _load_swicontainer(self, fp, chtype, chsize):
        assert chtype == 20, ValueError("Wrong chunk type " + str(chtype))
        assert chsize == 4, ValueError("Wrong chunk size " + str(chsize))

        self.m_ext_swib_index = struct.unpack('I', fp.read(4))

    def _load_gcontainer(self, fp, chtype, chsize):
        assert chtype == 21, ValueError("Wrong chunk type " + str(chtype))
        assert chsize == 24, ValueError("Wrong chunk size " + str(chsize))

        (
            self.vb_index,
            self.vb_offset,
            self.vb_size,
            self.ib_index,
            self.ib_offset,
            self.ib_size,
        ) = struct.unpack('6I', fp.read(chsize))

    def _load_fastpath(self, fp, chtype, chsize):
        start = fp.tell()
        end = start + chsize
        self.fastpath = FileOgf()
        self.fastpath.load(fp, start, end)

    def _load_s_lods(self, fp, chtype, chsize):
        NotImplemented

    def _load_s_motion_refs_1(self, fp, chtype, chsize):
        NotImplemented


    def save(self, fp):
        NotImplemented



"""

(21, 6, 22, 1)
(21, 1)
(21, 22, 1)
(21, 12, 1, 20)
(1, 10, 11)
(21, 12, 1)
(21, 6, 1)
(1, 10)

1, 6, 10, 11, 12, 20, 21, 22

"""
