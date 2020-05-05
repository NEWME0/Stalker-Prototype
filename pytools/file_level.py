


__all__ = ('FileLevel', 
	'CHUNK_HEADER', 'CHUNK_SHADERS', 'CHUNK_VISUALS', 'CHUNK_PORTALS', 
	'CHUNK_DLIGHTS', 'CHUNK_GLOWS', 'CHUNK_SECTORS', 'CHUNK_ALL')


import struct
from file_ogf import FileOgf


CHUNK_HEADER  = 1
CHUNK_SHADERS = 2
CHUNK_VISUALS = 3
CHUNK_PORTALS = 4
CHUNK_DLIGHTS = 6
CHUNK_GLOWS   = 7
CHUNK_SECTORS = 8

CHUNK_ALL = (
	CHUNK_HEADER,
	CHUNK_SHADERS,
	CHUNK_VISUALS,
	CHUNK_PORTALS,
	CHUNK_DLIGHTS,
	CHUNK_GLOWS,
	CHUNK_SECTORS,
)


class FileLevel:
	def __init__(self):
		self.version = None
		self.quality = None
		self.shaders = None
		self.visuals = None

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

	def load(self, fp, chunks_to_load=()):
		for chtype, chsize in self._iter_chunks(fp):
			if not chtype in chunks_to_load:
				continue

			loader = {
				1: self._load_header,
				2: self._load_shaders,
				3: self._load_visuals,
				4: self._load_portals,
				6: self._load_dlights,
				7: self._load_glows,
				8: self._load_sectors,
			}.get(chtype, None)

			if loader == None:
				raise ValueError("Unknown chunk type " + str(chtype))

			loader(fp, chtype, chsize)

	def save(self, fp):
		NotImplemented

	def _load_header(self, fp, chtype, chsize):
		assert chtype == 1, ValueError("Wrong chunk type " + str(chtype))
		assert chsize == 4, ValueError("Wrong chunk size " + str(chsize))

		(
			self.version,
			self.quality,
		) = struct.unpack('2H', fp.read(4))

	def _load_shaders(self, fp, chtype, chsize):
		assert chtype == 2, ValueError("Wrong chunk type " + str(chtype))

		num = struct.unpack('I', fp.read(4))[0]

		self.shaders = fp.read(chsize - 4).decode('utf-8').split('\x00')[:-1]

		assert len(self.shaders) == num, ValueError("Wrong shaders num")

	def _load_visuals(self, fp, chtype, chsize):
		assert chtype == 3, ValueError("Wrong chunk type " + str(chtype))

		start = fp.tell()
		end = start + chsize

		self.visuals = list()

		for chtype, chsize in self._iter_chunks(fp, start, end):
			start = fp.tell()
			end = start + chsize
			ogf = FileOgf()
			ogf.load(fp, start, end)
			self.visuals.append(ogf)

	def _load_portals(self, fp, chtype, chsize):
		NotImplemented

	def _load_dlights(self, fp, chtype, chsize):
		NotImplemented

	def _load_glows(self, fp, chtype, chsize):
		NotImplemented

	def _load_sectors(self, fp, chtype, chsize):
		NotImplemented
