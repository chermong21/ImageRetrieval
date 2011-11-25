Program:	ImageRetieval.py

NO WARRANTY OF THIS PROGRAM!

1	Prerequisites:

	*Python 2.6 or Python 2.7
	Extra library:
		*BeautifulSoup
		*PIL
		
2 Usage
	
	python ImageRetrieval.py url [image-width] [image-height] [folder-to-save]
	
	You can specify the image-width and image-height as you wish. When you do this, 
	the images will be downloaded if and only if both of their width and heigth are 
	larger than the values specified above.
	
	For example, 
	# all images in google webpage will be downloaded to current directory
	python ImageRetrieval.py http://www.google.com	
	
	#only larger than 200x200 images will be downloaded from the specified website to current directory
	python ImageRetrieval.py http://list.image.baidu.com/t/image_category/image_women_stars1.html 200 200
	 
	#download pictures to c:/images folder
	python ImageRetrieval.py http://list.image.baidu.com/t/image_category/image_women_stars1.html 200 200 c:/images