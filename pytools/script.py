import glob
from static import LEVEL_MAIN
from file_level import FileLevel


dataset = set()


for path in glob.glob(LEVEL_MAIN):

	with open(path, 'rb') as fp:
		print(path)
		lv = FileLevel()
		lv.load(fp, (1,2,3))

		dataset.update([tuple(ogf.chunks) for ogf in lv.visuals])

		print(lv.version, lv.quality, len(lv.shaders), len(lv.visuals))


print(*dataset, sep='\n')
