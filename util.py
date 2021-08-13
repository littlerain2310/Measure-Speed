from glob import glob

def image_files_from_folder(folder,upper=True):
	extensions = ['jpg','jpeg','png']
	img_files  = []
	for ext in extensions:
		img_files += glob('%s/*.%s' % (folder,ext))
		if upper:
			img_files += glob('%s/*.%s' % (folder,ext.upper()))
	return img_files
def bbox_to_centroid(bbox):
    """
    Computes centroid of bbox in format [xmin, xmax, ymin, ymax]
    :param bbox: (array) bounding box
    :return: (tuple) centroid x_center, y_center
    """
    # use the bounding box coordinates to derive the centroid
    cX = int((bbox[0] + bbox[2]) / 2.0)
    cY = int((bbox[1] + bbox[3]) / 2.0)

    return cX, cY