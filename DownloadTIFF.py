import pandas as pd
import os
import urllib
import time

#Read csvFile that consists indices of files to be downloaded
filepath = "C:\DevStagePred\datasets\Lund\metadata.csv"
metadata = pd.read_csv(filepath)

#Create Download destination folder
outdir ="C:\DevStagePred\datasets\Lund\Stack"
if not os.path.exists(outdir):
		os.makedirs(outdir)

#Initialise list of failed download files
failed= []

#Download TIF files from URL to the destination folder  
for i in range(1, len(metadata)):
    
    #Create URL_filename from metadata indices e.g., index = 2, OG_index = 7 to "lund_i000002_oi_000007"
    filename = 'lund_i{0:06d}_oi_{1:06d}.tif'.format(metadata.index[i], metadata.original_index[i])
    
		#Create destination downloading file path
    outpath = os.path.join(outdir, filename)
    
    #Create final URL to download filename
    url = 'https://zenodo.org/record/5837363/files/' + filename
    
    #Download and Save the image file in destination folder with "filename"
    if not os.path.exists(outpath):
        print(i, filename)
        start_time = time.time()
        
        try:
            r = urllib.request.urlretrieve(url, outpath)
        except urllib.error.ContentTooShortError as shortError:
            print("Content too short error...Trying again " + filename)
            time.sleep(30)
            try:
                r = urllib.request.urlretrieve(url, outpath)
            except urllib.error.ContentTooShortError as shortError:
                print("Content too short error 2nd time.. adding filename to failed list " + filename)
                failed.append(filename)
                continue
        except urllib.error.HTTPError as hp:
            print("HTTP 404 Error, trying again")
            time.sleep(30)
            try:
                r = urllib.request.urlretrieve(url, outpath)
            except urllib.error.HTTPError as hp:
                print("HTTP 404 Error again..., check failed list" + filename)
                failed.append(filename)
                continue
            except urllib.error.ContentTooShortError as shortError:
                print("Content too short error...Trying again " + filename)
                time.sleep(30)
                try:
                    r = urllib.request.urlretrieve(url, outpath)
                except urllib.error.ContentTooShortError as shortError:
                    print("Content too short error 2nd time.. adding filename to failed list " + filename)
                    failed.append(filename)
                    continue
        
        end_time = time.time()
        time_elapsed = end_time - start_time
        print('Downloading time: ' , time_elapsed)
        
        #Stall the downloading to avoid HTTP error
        time.sleep(15)
        
