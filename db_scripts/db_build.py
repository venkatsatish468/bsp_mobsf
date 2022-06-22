from fileinput import filename
from pprint import pprint
import random
from urllib import response
import pymongo
import json
import requests
from bson.dbref import DBRef
import os
import time

# Parameters for mongoDB connections
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DB_NAME = 'App_Scan_MobsfDB'
COLLECTION_NAME = "gmail2"


# Mobsf server url at port 8000 and url key for authorization
SERVER = "http://127.0.0.1:8000"
APIKEY = "24e4f20a5dc019a48eff83106410a95a6e024f353e5f90b83fdc9de7ef47c7f7"

hash=dict()

def mongodb_connect():
    try:
        # connect to mongodb
        # client = pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT)
        # print("Connected to MongoDB server at port 27017")
        client = pymongo.MongoClient("mongodb+srv://VenkatSatish:Vsatish1400@cluster0.v6ymz.mongodb.net/App_Scan_MobsfDB?retryWrites=true&w=majority")
        print("Connected to MongoDB Atlas")
        print("\n")
        return client
    except Exception as e:
        print("Error while connecting to database : \n",e)


# connect to mongodb
client = mongodb_connect()

# Connect to database with name DB_NAME
db = client[DB_NAME]

# Create a collection or table
buildCollection = db["build_records"] 
scanCollection = db["apk_report_records"]
chipSetCollection = db["chip_set_records"]

chipSetRecords = [
    {
        "_id": "SDM660",
        "os_list": ["oreo","A10","A11","HoneyComb","SnowCone"],
        "oreo":["11-14-15.00-RG-U38-PRD-SDM-01","11-14-15.00-RG-U38-PRD-SDM-02"],
        "A10": ["11-14-15.00-RG-U38-PRD-SDM-03","11-14-15.00-RG-U38-PRD-SDM-04"],
        "A11": ["11-14-15.00-RG-U38-PRD-SDM-05","11-14-15.00-RG-U38-PRD-SDM-06"],
        "HoneyComb": ["11-14-15.00-RG-U38-PRD-SDM-07","11-14-15.00-RG-U38-PRD-SDM-08"],
        "SnowCone": ["11-14-15.00-RG-U38-PRD-SDM-09","11-14-15.00-RG-U38-PRD-SDM-10"]
    },
    {
        "_id": "8956",
        "os_list": ["oreo","A10","A11","HoneyComb","SnowCone"],
        "oreo":["11-14-15.00-RG-U38-PRD-8956-01","11-14-15.00-RG-U38-PRD-8956-02"],
        "A10": ["11-14-15.00-RG-U38-PRD-8956-03","11-14-15.00-RG-U38-PRD-8956-04"],
        "A11": ["11-14-15.00-RG-U38-PRD-8956-05","11-14-15.00-RG-U38-PRD-8956-06"],
        "HoneyComb": ["11-14-15.00-RG-U38-PRD-8956-07","11-14-15.00-RG-U38-PRD-8956-08"],
        "SnowCone": ["11-14-15.00-RG-U38-PRD-8956-09","11-14-15.00-RG-U38-PRD-8956-10"]        
    },
    {
        "_id": "Helix",
        "os_list": ["oreo","A10","A11","HoneyComb","SnowCone"],
        "oreo":["11-14-15.00-RG-U38-PRD-HEL-01","11-14-15.00-RG-U38-PRD-HEL-02"],
        "A10": ["11-14-15.00-RG-U38-PRD-HEL-03","11-14-15.00-RG-U38-PRD-HEL-04"],
        "A11": ["11-14-15.00-RG-U38-PRD-HEL-05","11-14-15.00-RG-U38-PRD-HEL-06"],
        "HoneyComb": ["11-14-15.00-RG-U38-PRD-HEL-07","11-14-15.00-RG-U38-PRD-HEL-08"],
        "SnowCone": ["11-14-15.00-RG-U38-PRD-HEL-09","11-14-15.00-RG-U38-PRD-HEL-10"]
    },    
]

# Application Build information
build_records = [
    {
        "_id": "11-14-15.00-RG-U38-PRD-HEL-01",
        "platform": "helios",
        "product": "TC26PG",
        "host": "emc-gcp-build-r-ru9221",
        "data": "Wed Sep 22 09:52:56 UTC 2021",
        "display_id": "11-14-15.00-RG-U38-PRD-HEL-04",
        "flavor": "helios-userdebug",
        "os":"oreo",
        "api_list": [] 
    },
    {
        "_id": "11-14-15.00-RG-U38-PRD-HEL-03",
        "platform": "helios",
        "product": "TC26PG",
        "host": "emc-gcp-build-r-ru9221",
        "data": "Wed Sep 22 09:52:56 UTC 2021",
        "display_id": "11-14-15.00-RG-U38-PRD-HEL-04",
        "flavor": "helios-userdebug",
        "os": "A10",
        "api_list": [] 
    },
    {
        "_id": "11-14-15.00-RG-U38-PRD-HEL-05",
        "platform": "EMC",
        "product": "TC26PG",
        "host": "emc-gcp-build-r-ru9221",
        "data": "Fri Sep 24 09:52:56 UTC 2022",
        "display_id": "11-14-15.00-RG-U38-PRD-FTC-04",
        "flavor": "helios-userdebug" ,
        "os" : "A11",
        "api_list": []
    },
    {
        "_id": "11-14-15.00-RG-U38-PRD-HEL-07",
        "platform": "helios",
        "product": "TC26PG",
        "host": "emc-gcp-build-r-ru9221",
        "data": "Wed Sep 22 09:52:56 UTC 2021",
        "display_id": "11-14-15.00-RG-U38-PRD-HEL-04",
        "flavor": "helios-userdebug",
        "os":"HoneyComb",
        "api_list": []  
    },
    {
        "_id": "11-14-15.00-RG-U38-PRD-HEL-09",
        "platform": "helios",
        "product": "TC26PG",
        "host": "emc-gcp-build-r-ru9221",
        "data": "Wed Sep 22 09:52:56 UTC 2021",
        "display_id": "11-14-15.00-RG-U38-PRD-HEL-04",
        "flavor": "helios-userdebug",
        "os": "SnowCone",
        "api_list": []  
    },

    {
        "_id": "11-14-15.00-RG-U38-PRD-SDM-01",
        "platform": "SDM",
        "product": "TC26PG",
        "host": "emc-gcp-build-r-ru9221",
        "data": "Wed Sep 22 09:52:56 UTC 2021",
        "display_id": "11-14-15.00-RG-U38-PRD-HEL-04",
        "flavor": "helios-userdebug",
        "os":"oreo",
        "api_list": []  
    },
    {
        "_id": "11-14-15.00-RG-U38-PRD-SDM-03",
        "platform": "helios",
        "product": "TC26PG",
        "host": "emc-gcp-build-r-ru9221",
        "data": "Wed Sep 22 09:52:56 UTC 2021",
        "display_id": "11-14-15.00-RG-U38-PRD-HEL-04",
        "flavor": "helios-userdebug",
        "os": "A10",
        "api_list": [] 
    },
    {
        "_id": "11-14-15.00-RG-U38-PRD-SDM-05",
        "platform": "EMC",
        "product": "TC26PG",
        "host": "emc-gcp-build-r-ru9221",
        "data": "Fri Sep 24 09:52:56 UTC 2022",
        "display_id": "11-14-15.00-RG-U38-PRD-FTC-04",
        "flavor": "helios-userdebug" ,
        "os" : "A11",
        "api_list": [] 
    },
    {
        "_id": "11-14-15.00-RG-U38-PRD-SDM-07",
        "platform": "helios",
        "product": "TC26PG",
        "host": "emc-gcp-build-r-ru9221",
        "data": "Wed Sep 22 09:52:56 UTC 2021",
        "display_id": "11-14-15.00-RG-U38-PRD-HEL-04",
        "flavor": "helios-userdebug",
        "os":"HoneyComb",
        "api_list": []  
    },
    {
        "_id": "11-14-15.00-RG-U38-PRD-SDM-09",
        "platform": "helios",
        "product": "TC26PG",
        "host": "emc-gcp-build-r-ru9221",
        "data": "Wed Sep 22 09:52:56 UTC 2021",
        "display_id": "11-14-15.00-RG-U38-PRD-HEL-04",
        "flavor": "helios-userdebug",
        "os": "SnowCone",
        "api_list": []  
    },

    {
        "_id": "11-14-15.00-RG-U38-PRD-8956-01",
        "platform": "8956",
        "product": "TC26PG",
        "host": "emc-gcp-build-r-ru9221",
        "data": "Wed Sep 22 09:52:56 UTC 2021",
        "display_id": "11-14-15.00-RG-U38-PRD-HEL-04",
        "flavor": "helios-userdebug",
        "os":"oreo" ,
        "api_list": [] 
    },
    {
        "_id": "11-14-15.00-RG-U38-PRD-8956-03",
        "platform": "helios",
        "product": "TC26PG",
        "host": "emc-gcp-build-r-ru9221",
        "data": "Wed Sep 22 09:52:56 UTC 2021",
        "display_id": "11-14-15.00-RG-U38-PRD-HEL-04",
        "flavor": "helios-userdebug",
        "os": "A10",
        "api_list": []  
    },
    {
        "_id": "11-14-15.00-RG-U38-PRD-8956-05",
        "platform": "EMC",
        "product": "TC26PG",
        "host": "emc-gcp-build-r-ru9221",
        "data": "Fri Sep 24 09:52:56 UTC 2022",
        "display_id": "11-14-15.00-RG-U38-PRD-FTC-04",
        "flavor": "helios-userdebug" ,
        "os" : "A11",
        "api_list": [] 
    },
    {
        "_id": "11-14-15.00-RG-U38-PRD-8956-07",
        "platform": "helios",
        "product": "TC26PG",
        "host": "emc-gcp-build-r-ru9221",
        "data": "Wed Sep 22 09:52:56 UTC 2021",
        "display_id": "11-14-15.00-RG-U38-PRD-HEL-04",
        "flavor": "helios-userdebug",
        "os":"HoneyComb",
        "api_list": [] 
    },
    {
        "_id": "11-14-15.00-RG-U38-PRD-8956-09",
        "platform": "helios",
        "product": "TC26PG",
        "host": "emc-gcp-build-r-ru9221",
        "data": "Wed Sep 22 09:52:56 UTC 2021",
        "display_id": "11-14-15.00-RG-U38-PRD-HEL-04",
        "flavor": "helios-userdebug",
        "os": "SnowCone",
        "api_list": [] 
    },
]

# function to get the paths to all the .apk files
def getFilePaths(root):
    filePathList = list()
    for root,dirs,files in os.walk(root):
        for file in files:
            if file.endswith(".apk"):
                filePathList.append(os.path.join(root,file).replace("\\","/"))
    return filePathList

# function to insert build and chipset data into sample database
def insert_build_records_and_chipset(build_records,chipSetRecords):
    try:
        chipSetCollection.insert_many(chipSetRecords)
        print("Chip set Records Inserted Successfully")
    except Exception as e:
        print("Error while inserting Chip set Records : \n",e)    
    try:
        buildCollection.insert_many(build_records)
        print("build document inserted successfully")
    except Exception as e:
        print("Error while inserting the build records : \n",e)
    
insert_build_records_and_chipset(build_records,chipSetRecords)

def upload_and_scan():
    # Folder path to scan all the apk files
    root = "/Users/VA4991/Documents/A11"
    filePathList = getFilePaths(root)
    for filePath in filePathList:
        # Code to upload file to Mobsf server
        fileObject = open(filePath,"rb")
        file = {"file": (filePath, fileObject, "application/octet-stream")}
        headers = {'Authorization': APIKEY}
        try:
            uploadResponse = requests.post(SERVER + '/api/v1/upload', files=file, headers=headers)
            print("Uploading the file : ",filePath)
        except Exception as e:
            print("Error while uploading the file : ",filePath,"\n",e)
        uploadOutput = json.loads(uploadResponse.text)
        hash[filePath] = uploadOutput

        # code to get scan report from Mobsf server
        try:
            scanResponse = requests.post(SERVER + '/api/v1/scan', data=hash[filePath], headers=headers)
        except Exception as e:
            print("error while getting response from MobSF server : \n")

        scanOutput=json.loads(scanResponse.text)
        randomChipSet = random.choice(chipSetRecords) #get a random chipset
        randomOs = random.choice(randomChipSet["os_list"]) #get a random OS from the random chipset
        buildId = randomChipSet[randomOs][0] #get a build number from the random os
        packageName = scanOutput["package_name"]

        try:
            buildCollection.find_one_and_update({"_id":buildId},{'$push': {"api_list": packageName}}) #update the api_list in the build records
        except Exception as e:
            print("Error while updating build records : \n",e)

        primaryKey = buildId + ":"+packageName
        scanOutput["_id"]=primaryKey
        scanOutput["build_id"] = DBRef("build_records",buildId,"NewApkScanDB")
        try:
            scanCollection.insert_one(scanOutput)
            print("Inserted scaned report : ",packageName)
        except Exception as e:
            print("Error while Inserting the document : \n",e)
        print("\n")
        fileObject.close()
        time.sleep(1)

upload_and_scan()
        