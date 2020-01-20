compress:
	cd items && zip -v -9 -r -o ../items.zip . && cd .. && mv "./items.zip" "./items/items-$$(date +%Y%m%d).zip"