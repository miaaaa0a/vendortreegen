import os

# https://thispointer.com/python-search-strings-in-a-file-and-get-line-numbers-of-lines-containing-the-string/
def search_string_in_file(file_name, string_to_search):
	"""Search for the given string in file and return lines containing that string,
	along with line numbers"""
	line_number = 0
	list_of_results = []
	# Open the file in read only mode
	with open(file_name, 'r') as read_obj:
		# Read all lines in the file one by one
		for line in read_obj:
			# For each line, check if line contains the string
			line_number += 1
			if string_to_search in line:
				# If yes, then add the line number & line as a tuple in the list
				list_of_results.append((line_number, line.rstrip()))
	# Return list of tuples containing line numbers and lines where string is found
	return list_of_results

# i like my bools all lowercase
true = True
false = False

# defining some variables
# phone info
phonevendor	 = ""
phonemodel	  = ""
# manual phone info input
manualphoneinfo = ""

# check if inputs are there
if not os.path.isdir("./input/system"):
	assert "system folder not found!"
if not os.path.isfile("./input/proprietary-files.txt"):
	assert "proprietary-files.txt not found!"

# get phone name and model
# check if build.prop exists
if not os.path.isfile("./input/system/build.prop"):
	print("build.prop not found.")
	print("please enter phone vendor and model manually (example: samsung,a50):")
	# .replace fix, incase the user inputs vendor and model with space after the comma
	phonevendor, phonemodel = input("> ").replace(" ", "").lower().split(",")
else:
	with open("./input/system/build.prop") as f:
		# scraping info about the phone
		vendoroccur = search_string_in_file("./input/system/build.prop", "ro.product.brand=")
		modeloccur  = search_string_in_file("./input/system/build.prop",  "ro.product.name=")
		phonevendor = vendoroccur[0][1].strip("ro.product.brand=")
		phonemodel  = modeloccur[0][1].strip( "ro.product.name=")
		print(phonevendor, phonemodel)
		
		# ask if scraped info is correct
		print(f"is this the correct vendor and model?\n> {phonevendor} {phonemodel}")
		manualphoneinfo = input("(Y/N) ")
		# wow, an if statement in an if statement
		if [lambda: false, lambda: true][manualphoneinfo.lower() == "n"]():
			print("please enter phone vendor and model manually (example: samsung,a50):")
			phonevendor, phonemodel = input("> ").replace(" ", "").lower().split(",")
		# read the print statement
		print("creating core files...")
		os.mkdir(f"./output/android_vendor_{phonevendor}_{phonemodel}")
		with open(f"./output/android_vendor_{phonevendor}_{phonemodel}/{phonemodel}-vendor.mk", "w") as f:
			f.write(f"$(call inherit-product, vendor/{phonevendor}/{phonemodel}/{phonemodel}-vendor-blobs.mk)")
		with open(f"./output/android_vendor_{phonevendor}_{phonemodel}/{phonemodel}-vendor-blobs.mk", "w") as f:
			f.write("")
		# some values here need to be scraped from build.prop too but im too lazy lol
		with open(f"./output/android_vendor_{phonevendor}_{phonemodel}/Android.mk", "w") as f:
			f.write(f"LOCAL_PATH := $(call my-dir)\nifneq ($(filter {phonemodel}, $(TARGET_DEVICE)),)\n\n\ninclude $(CLEAR_VARS)\nLOCAL_MODULE := libdpframework\nLOCAL_MODULE_OWNER := mtk\nLOCAL_SRC_FILES := proprietary/lib/libdpframework.so\nLOCAL_MODULE_TAGS := optional\nLOCAL_MODULE_SUFFIX := .so\nLOCAL_MODULE_CLASS := SHARED_LIBRARIES\nLOCAL_MODULE_PATH := $(TARGET_OUT_SHARED_LIBRARIES)\ninclude $(BUILD_PREBUILT)\n\nendif")
		os.mkdir(f"./output/android_vendor_{phonevendor}_{phonemodel}/proprietary")
			
